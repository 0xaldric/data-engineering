# AK07 — Knowledge Graph Construction với LLM

> **Xây** knowledge graph từ text bằng LLM (trích entity + relation), khác [[ae02-graphrag-build]] (dùng `[[links]]` có sẵn). Đây là pipeline trích → resolve → store → query. Sâu hơn [[aa09-graphrag]]. Liên hệ [[ad06-doc-parsing]], [[ag08-ai-data-contracts]].

## Vì sao dựng KG (không có [[links]] sẵn)
- Đa số text **không có liên kết tường minh** → phải **trích quan hệ** từ nội dung.
- KG = entity (nút) + relation (cạnh có nghĩa) → trả lời multi-hop, suy luận quan hệ ([[ae02-graphrag-build]]).
- LLM giỏi đọc text → trích (entity, relation, entity) = **triple**.

## ⭐ Pipeline dựng KG
```
text ─> [1 TRÍCH triple] LLM: "Spark dùng shuffle" -> (Spark, dùng, Shuffle)
     ─> [2 ENTITY RESOLUTION] gộp "Spark"="Apache Spark"="spark" -> 1 entity
     ─> [3 VALIDATE triple] đúng schema/ontology? quan hệ hợp lệ? ([[ai06-llm-output-governance]])
     ─> [4 STORE] graph DB (Neo4j) hoặc bảng (node, edge) + embedding entity
     ─> [5 QUERY] graph traversal + vector hybrid ([[ae02-graphrag-build]])
```

## ⭐ 1. Trích triple (LLM làm)
```
prompt: "Trích (chủ thể, quan hệ, đối tượng) từ đoạn sau..."
   "DuckDB là CSDL cột, hỗ trợ SQL" -> (DuckDB, là, CSDL cột), (DuckDB, hỗ trợ, SQL)
-> output JSON có schema (validate [[ag08-ai-data-contracts]]); LLM có thể bịa quan hệ -> kiểm
```
→ Đây là "structured extraction" — LLM biến text thành **dữ liệu có cấu trúc**.

## ⭐⭐ 2. Entity Resolution (khó nhất — như dedup)
```
"Spark", "Apache Spark", "spark engine" -> CÙNG 1 entity?
   -> chuẩn hoá tên + so embedding (cosine cao = trùng [[aa04-training-data-prep]])
   -> + ngữ cảnh (Spark engine vs Spark điện?) -> disambiguation
gộp sai -> KG nhập nhằng ; không gộp -> KG phân mảnh (cùng thứ thành nhiều nút)
```
→ Cùng bài toán **dedup/record-linkage** kinh điển của DE ([[aa04-training-data-prep]], [[18-scd|dimensional]] surrogate key), áp cho entity.

## ⭐ 3. Ontology/Schema (KG cần "data contract")
- **Ontology**: định nghĩa loại entity (Tool/Concept/Person) + loại quan hệ (uses/is-a/part-of) hợp lệ.
- LLM trích **theo ontology** → KG nhất quán (không "dùng"/"sử dụng"/"xài" = 3 quan hệ khác nhau).
- Validate triple theo ontology ([[ag08-ai-data-contracts]]): quan hệ có trong schema? kiểu entity đúng?

## Lưu trữ & query
- **Graph DB** (Neo4j/Neptune): native graph, Cypher query, traversal nhanh.
- **Bảng quan hệ** (node, edge) trong DB thường: đơn giản, đủ cho quy mô vừa ([[ae02-graphrag-build]] dùng dict).
- **+ embedding entity** → hybrid: vector tìm entity vào → graph đi tiếp ([[aa09-graphrag]]).

## Cạm bẫy
- **LLM bịa quan hệ** → KG sai → validate triple + nguồn (provenance mỗi triple).
- **Entity resolution kém** → cùng thứ thành nhiều nút (phân mảnh) / gộp sai (nhập nhằng) → chuẩn hoá + embedding + ngữ cảnh.
- **Không ontology** → quan hệ lung tung (đồng nghĩa) → định nghĩa schema, trích theo.
- **KG không cập nhật** → lỗi thời ([[ac06-kb-freshness]]) → re-trích khi text đổi.
- **Dựng KG khi vector đủ** → phức tạp thừa → chỉ khi cần multi-hop/quan hệ ([[ae02-graphrag-build]]).
- **Quên provenance** → triple sai không truy được nguồn → lưu (triple, doc nguồn).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Pipeline: trích triple → entity resolution → validate → store → query.
- [ ] Trích triple = structured extraction (LLM → dữ liệu có cấu trúc).
- [ ] ⭐ Entity resolution = dedup/record-linkage cho entity (gộp trùng).
- [ ] Ontology = data contract cho KG (quan hệ hợp lệ).
- [ ] Cạm bẫy: bịa quan hệ, resolution kém, không ontology, over-dùng KG.
- 🔭 Tự mò: trích triple thủ công từ 3 note (đọc, viết (chủ thể, quan hệ, đối tượng)); chuẩn hoá tên entity (lowercase, bỏ "Apache"); embed tên entity bằng `rag_over_notes.embed`, gộp cặp cosine > 0.9 (entity resolution); dựng graph dict + query 1 entity ra hàng xóm. So với `graphrag_links.py` (dùng links sẵn) — đây là TỰ trích.

➡️ Tiếp [[ak08-timeseries-tabular-fm]] — foundation model cho time-series/tabular.
