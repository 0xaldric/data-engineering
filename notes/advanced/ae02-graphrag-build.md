# AE02 — GraphRAG từ Wikilinks ⭐ (có code chạy được)

> Dựng **knowledge graph THẬT** từ `[[links]]` giữa các note → trả lời câu cần đi qua **quan hệ** (A→B→C), thứ vector similarity bỏ sót. Hybrid: vector tìm seed, graph mở rộng. Code: [`graphrag_links.py`](../../projects/06-ai-data-engineering/graphrag_links.py). Sâu hơn [[aa09-graphrag]].

## Vector RAG vs GraphRAG (bổ sung nhau)
| | Vector RAG | GraphRAG |
|--|-----------|----------|
| Tìm theo | **giống nghĩa** (cosine) | **quan hệ** (cạnh nối) |
| Mạnh | "đoạn nào nói về X" | "X liên quan gì → cái đó liên quan gì" (multi-hop) |
| Yếu | câu multi-hop, suy luận quan hệ | cần graph có sẵn/trích được |
| Ví dụ | "chunking là gì" | "công cụ nào ảnh hưởng cost mà cũng đụng governance" |
→ **Kết hợp**: vector tìm điểm vào (seed), graph đi tiếp theo liên kết.

## ⭐ Dựng graph (ở đây: từ [[links]] có sẵn)
```
mỗi note = NODE ; mỗi [[link]] = CẠNH có hướng (note A trỏ B)
parse [[../18-scd.md|dimensional]] -> chuẩn hoá -> '18-scd' (bỏ path/alias/.md)
out[A].add(B) ; inc[B].add(A)   (adjacency dict, không cần thư viện)
```
Thực tế (không có [[links]] sẵn): **LLM trích entity + relation** từ text → graph ([[aa09-graphrag]]); entity resolution gộp trùng. Ở đây ta may mắn có sẵn liên kết do người viết note tạo.

## ⭐ Kết quả thật (code chạy)
```
graph: 216 node, 1044 cạnh
Hub (in-degree cao = khái niệm NỀN TẢNG):
  c01-system-design-framework in=25 | 34-delta-lake in=21
  aa02-guardrails in=19 | ai06-llm-output-governance in=19
```
→ ⭐ **Phát hiện thú vị**: các note bị trỏ tới nhiều nhất chính là **khái niệm nền** (system design, guardrails, governance, delta lake). Graph **tự lộ ra** cái gì quan trọng — thứ vector không nói được. (Đây là **centrality** — như PageRank thu nhỏ.)

## ⭐ Hybrid retrieval: vector seed × graph expand
```
Query 'đánh giá chất lượng RAG'
 -> vector SEED = k05-vector-rag-deep
 -> graph mở rộng 2 hop:
    1-hop: pipeline-patterns, data-contract, governance-pii...
    2-hop: delta-lake, scd, dbt-docs-lineage...
 -> từ 1 seed, graph kéo thêm 32 note liên quan vector top-k BỎ SÓT
```
→ Vector cho **điểm vào đúng nghĩa**; graph cho **vùng lân cận theo quan hệ** → context phong phú hơn cho LLM.

## Khi nào GraphRAG > vector RAG
- Câu **multi-hop**: "công cụ A dùng ở case nào, case đó gặp vấn đề gì".
- Câu cần **tổng hợp toàn cục**: "chủ đề trung tâm của tài liệu là gì" → centrality/community.
- Quan hệ **tường minh quan trọng**: tổ chức (ai báo cáo ai), phụ thuộc (service gọi service), trích dẫn.
- Vector đủ cho: "đoạn nào nói về X" (đa số câu thực tế) → **đừng vẽ graph khi không cần**.

## Snippet (BFS multi-hop)
```python
def bfs(out, start, hops=2):           # neighborhood trong <= hops bước
    seen, frontier = {start}, {start}
    for _ in range(hops):
        nxt = set().union(*(out.get(u, set()) for u in frontier)) - seen
        seen |= nxt; frontier = nxt
    return seen
```

## Cạm bẫy
- **Vẽ graph khi vector đủ** → phức tạp thừa; GraphRAG đắt (trích + lưu + traverse).
- **Trích entity/relation kém** (LLM sai) → graph rác → đi sai; cần entity resolution + validate.
- **Graph phình** (quá nhiều cạnh) → traverse nổ tổ hợp → giới hạn hops + lọc cạnh yếu.
- **Quên cập nhật graph** khi doc đổi ([[ac06-kb-freshness]]) → graph lỗi thời.
- **Chỉ graph, bỏ vector** → mất khả năng "giống nghĩa"; **hybrid** mới mạnh.
- **Hub thống trị** (1 node nối tất cả) → mọi đường đi qua nó, nhiễu → cân nhắc bỏ hub khi traverse.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vector (giống nghĩa) vs Graph (quan hệ) — bổ sung nhau.
- [ ] Dựng graph: node=doc/entity, cạnh=link/relation; thực tế LLM trích.
- [ ] In-degree/centrality lộ khái niệm nền tảng.
- [ ] Hybrid vector-seed × graph-expand multi-hop.
- [ ] Khi nào GraphRAG > vector (multi-hop, tổng hợp toàn cục); đừng over-dùng.
- 🔭 Tự mò: sửa `graphrag_links.py` — tính **PageRank** đơn giản (lặp phân phối điểm theo cạnh) thay in-degree, xem hub đổi không; thêm "graph-answer": ghép text của seed + 1-hop neighbors thành context, đưa cho `llm_output_pipeline` validate → một GraphRAG end-to-end mini.

➡️ Tiếp [[ae03-training-data-quality]] — chấm chất lượng training data.
