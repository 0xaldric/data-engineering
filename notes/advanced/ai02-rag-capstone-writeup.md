# AI02 — RAG Capstone: Kiến trúc & Writeup

> Giải thích capstone [`rag_over_notes.py`](../../projects/06-ai-data-engineering/rag_over_notes.py) — đúng bài "thiết kế pipeline tài liệu phi cấu trúc → tìm kiếm ngữ nghĩa" của vòng phỏng vấn DE mới. Liên hệ [[g06-case-ml-llm-data]], [[k05-vector-rag-deep]].

## Bài toán = "ETL batch" phiên bản 2025
> Thiết kế pipeline thu thập tài liệu phi cấu trúc, chia nhỏ, embedding, lưu vector DB, tìm kiếm theo ngữ nghĩa; đánh giá retrieval; cái gì vỡ khi scale?

"Tài liệu phi cấu trúc" ở đây = chính kho ~170 notes Markdown.

## Kiến trúc (cùng tư duy ETL, output là vector)
```
notes/*.md
   │ EXTRACT
   ▼
CHUNK (structure-aware: cắt theo heading ## / ###, section dài → size 1200 + overlap 150)
   │ TRANSFORM 1
   ▼
EMBED (fastembed bge-small, local, 384-dim; query thêm prefix "Represent this sentence...")
   │ TRANSFORM 2 (output = vector thay vì fact/dim)
   ▼
VECTOR STORE (DuckDB: chunk_id, note, heading, text, embedding FLOAT[384], model, indexed_at)
   │  + HNSW index (vss) cho ANN
   ▼
SEARCH (hybrid: array_cosine_similarity + keyword bonus) ──► top-k
   │
   ▼
EVAL (recall@k trên golden set)
```

## Từng quyết định & trade-off (kể khi phỏng vấn)
| Quyết định | Lựa chọn | Vì sao / trade-off |
|-----------|----------|---------------------|
| Chunking | structure-aware (heading) + size cap + overlap | giữ ngữ cảnh đoạn; overlap tránh mất ý ở ranh giới (xem [[ai03-chunking]]) |
| Embedding | fastembed bge-small (local, ONNX) | không API key/cost/torch; trade-off: EN model → cross-lingual VI yếu hơn (đổi multilingual ở [[ai04-embedding-versioning]]) |
| Vector store | DuckDB FLOAT[384] + HNSW | đã có sẵn, query nhanh; brute-force cosine cũng đủ ở 1454 chunks (ANN cần khi triệu chunk) |
| **Incremental** | re-embed CHỈ file đổi (content hash) | embedding tốn thời gian/tiền → không re-embed toàn bộ; idempotent (chạy lại an toàn) |
| Update/delete | xoá chunk cũ của file trước khi ghi; dọn file đã xoá | giữ index nhất quán với nguồn |
| Search | hybrid vector + keyword | vector trượt từ khoá chính xác (mã/tên riêng) → keyword bù |
| Provenance | lưu model + indexed_at | governance dữ liệu LLM-era (biết chunk từ model nào, lúc nào) |

## Kết quả đo được
- 169 notes → **1454 chunks**, embed local ~63s (lần đầu), HNSW built.
- **Incremental**: lần 2 → 0 re-embed (unchanged theo hash), **0.2s** → idempotent.
- recall@5 = **88%** (7/8 golden); 1 miss do cross-lingual EN↔VI.

## "Cái gì vỡ khi scale ×N?" (câu hỏi cốt lõi)
- **Embedding throughput**: triệu tài liệu → embed thành bottleneck → batch + GPU/multiple workers + queue.
- **Vector DB**: brute-force cosine O(n) sập ở triệu vector → cần ANN (HNSW/IVF) + sharding; DuckDB local đổi sang vector DB chuyên (Qdrant/pgvector/Milvus).
- **Re-index khi model đổi**: re-embed toàn bộ = đắt + downtime → blue-green index ([[ai04-embedding-versioning]]).
- **Freshness real-time**: tài liệu đổi cần vào index <1' → streaming ([[ai09-streaming-ai]]).
- **Cost**: token cost embedding/LLM tăng tuyến tính → cache + batch ([[ai08-ai-cost-latency]]).

## "Danh từ đổi, tư duy không đổi"
| ETL truyền thống | RAG pipeline |
|------------------|--------------|
| nguồn → fact/dim | tài liệu → chunk/vector |
| transform SQL | chunk + embed |
| warehouse table | vector store |
| SCD2 (đổi dimension) | re-embed (đổi model/tài liệu) |
| data quality (row/schema) | retrieval quality (recall@k) |
| idempotent load | idempotent re-index |
→ Mọi nguyên tắc DE (idempotency, incremental, lineage, DQ, cost) áp y nguyên, chỉ output khác.

## ✅ "Tự mò"
🔭 Chạy `python projects/06-ai-data-engineering/rag_over_notes.py`; thử `search "..."` vài câu; sửa 1 note rồi chạy lại xem chỉ file đó re-embed (incremental).

➡️ Tiếp: [[ai03-chunking]].
