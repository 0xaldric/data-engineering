# AA09 — GraphRAG + Knowledge Graph

> RAG vector giỏi "tìm đoạn liên quan" nhưng kém câu hỏi **multi-hop / quan hệ / tổng hợp toàn cục**. GraphRAG kết hợp **knowledge graph** + vector. Liên hệ [[h04-case-social-graph]], [[k05-vector-rag-deep]].

## Vì sao vector RAG chưa đủ
Vector retrieval lấy top-k chunk **giống** câu hỏi → tốt cho "tìm fact". Nhưng yếu khi:
- **Multi-hop**: "Đồng nghiệp của sếp của An làm dự án nào?" → cần đi qua nhiều quan hệ (chunk rời rạc không nối được).
- **Tổng hợp toàn cục**: "Chủ đề chính của toàn bộ tài liệu?" → top-k chunk không bao quát.
- **Quan hệ**: câu hỏi về liên kết giữa thực thể.

## Knowledge Graph (KG) — nền tảng
Trích xuất **thực thể (node)** + **quan hệ (edge)** từ tài liệu → đồ thị:
```
(An) ──[làm việc tại]──► (Công ty X)
(An) ──[báo cáo cho]──► (Bình) ──[quản lý]──► (Dự án Y)
```
Query bằng graph traversal (multi-hop — recursive/graph algorithm, [[a02-sql-pivot-hierarchical]], [[h04-case-social-graph]]).

## ⭐ Pipeline build KG (vai trò DE)
```
Tài liệu ──► LLM trích xuất (entity + relation) ──► (subject, predicate, object) triples
        └─► chunk + embed (vector, như RAG thường)
                                    │
                          KNOWLEDGE GRAPH (Neo4j / graph DB) + vector store
                                    │ (entity có embedding để link)
                          community detection (gom cụm node liên quan)
                          + tóm tắt mỗi community (LLM)
```
- LLM trích **triples** (chủ-vị-tân) từ text → DE chuẩn hoá, dedup entity (cùng "An" ở nhiều tài liệu → 1 node, MDM — [[j04-case-govtech]]), build graph.
- **Entity resolution** (giống MDM): "An", "Nguyễn An", "anh An" → một entity.

## GraphRAG retrieval (hybrid)
```
Câu hỏi → tìm entity liên quan (vector/keyword) → traverse graph quanh entity đó (multi-hop)
        → lấy subgraph + chunk liên quan → đưa vào LLM → trả lời
```
Microsoft GraphRAG: thêm **community summaries** — câu hỏi toàn cục dùng tóm tắt community thay vì chunk lẻ.

## Khi nào GraphRAG > vector RAG
| Câu hỏi | Vector RAG | GraphRAG |
|---------|-----------|----------|
| "Fact X là gì?" | ✅ tốt | overkill |
| "Quan hệ giữa A và B?" | ✗ yếu | ✅ |
| Multi-hop (A→B→C) | ✗ | ✅ |
| Tổng hợp toàn cục | ✗ | ✅ (community) |
→ GraphRAG **đắt + phức tạp hơn** (build KG, LLM trích xuất tốn). Chỉ dùng khi câu hỏi cần quan hệ/multi-hop. Đa số RAG vector vẫn đủ.

## Đặc thù DE
- **Trích xuất entity/relation** = transform LLM (non-deterministic → validate triples, [[ai06-llm-output-governance]]).
- **Entity resolution / dedup** (MDM) — node trùng.
- **Incremental**: tài liệu đổi → cập nhật graph + vector (idempotent).
- **Cost**: LLM trích xuất toàn corpus đắt ([[ai08-ai-cost-latency]]).
- Lưu: graph DB (quan hệ) + vector (similarity) — hybrid store.

## ⚠️ Cạm bẫy
- Dùng GraphRAG khi vector RAG đủ (over-engineer, đắt).
- LLM trích triples sai/bịa quan hệ → graph rác (validate + confidence).
- Không entity resolution → node trùng → graph vỡ (cùng người thành nhiều node).
- Build KG toàn corpus tốn LLM call khổng lồ (cân cost).
- Quên incremental → rebuild graph mỗi lần.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao vector RAG yếu với multi-hop/quan hệ/toàn cục.
- [ ] Pipeline build KG (LLM trích triple → entity resolution → graph + vector).
- [ ] GraphRAG retrieval hybrid; community summary.
- [ ] Khi nào GraphRAG > vector RAG (đắt → chỉ khi cần).
- 🔭 Trên vài note, tự trích thủ công 5 triple (note → [[liên kết]] → note) thành graph nhỏ; nghĩ câu hỏi multi-hop nào vector RAG sẽ trượt.

➡️ Tiếp: [[aa10-llmops]].
