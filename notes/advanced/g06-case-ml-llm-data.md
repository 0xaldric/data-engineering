# G06 — Case: ML Feature Platform & Data for LLM/RAG

> Vai trò DE trong AI stack: xây data pipeline cho ML truyền thống (feature store) **và** cho LLM/RAG (embedding/vector). Xu hướng nóng. Liên hệ [[c09-case-recsys]].

## Phần 1 — Feature Platform (ML truyền thống)
### Feature Store (nhắc + sâu)
2 store + 1 định nghĩa chung (tránh train/serve skew — [[c09-case-recsys]]):
```
Định nghĩa feature (1 lần)
   ├─ Offline store (lake/warehouse): training data (lịch sử lớn, batch)
   └─ Online store (Redis/DynamoDB): serving (low-latency lookup ms)
```
- **Point-in-time correctness** ⭐: training data phải dùng feature **tại thời điểm event** (as-of join) → tránh **data leakage** (dùng feature tương lai). Giống as-of của bitemporal/SCD ([[e04-bitemporal]], [[18-scd]]).
- **Batch vs streaming features**: ổn định (popularity) batch; nhanh đổi (session) streaming.
- Công cụ: Feast, Tecton.

## Phần 2 — Data cho LLM / RAG ⭐ (mới, DE ngày càng làm)
**RAG** (Retrieval-Augmented Generation): LLM trả lời dựa trên tài liệu **truy xuất** được, không chỉ kiến thức train. DE xây **pipeline cấp dữ liệu** cho RAG.
```
Tài liệu (docs/PDF/DB/web) 
   │ ingest
   ▼
PARSE & CHUNK (chia tài liệu thành đoạn ~vài trăm token, overlap)
   │
   ▼
EMBED (gọi embedding model → vector mỗi chunk)
   │
   ▼
VECTOR DB (pgvector/Pinecone/Weaviate/Milvus) — lưu vector + metadata
   ▲                                              │ retrieval
   │ (re-embed khi tài liệu đổi — freshness)      ▼
   └──────────────────────────  LLM query: embed câu hỏi → similarity search top-k chunk → đưa vào prompt → trả lời
```

### Khái niệm DE cho RAG
- **Chunking**: chia tài liệu thành đoạn (size + overlap) — ảnh hưởng chất lượng retrieval. Quá to → nhiễu; quá nhỏ → mất ngữ cảnh.
- **Embedding**: model biến text → vector (vd 768/1536 chiều); "gần nhau" = nghĩa giống. Đây là một **transform** trong pipeline.
- **Vector DB / vector index**: lưu + tìm **nearest neighbor** (ANN: HNSW, IVF). Khác index B-tree (similarity, không equality).
- **Metadata filtering**: kết hợp similarity + filter (theo nguồn/ngày/quyền).
- **Freshness/incremental** ⭐: tài liệu đổi → re-chunk + re-embed phần đổi (incremental, không embed lại tất cả — đắt). Pipeline freshness như ETL ([[27-dbt-incremental]]).
- **Quality**: dedup chunk, đánh giá retrieval (recall@k), tránh "garbage in".

### DE pipeline cho RAG = ETL quen thuộc
ingest → chunk (transform) → embed (transform, gọi model) → load vào vector DB → incremental update khi nguồn đổi → monitor freshness/quality. **Cùng nguyên tắc** idempotency/incremental/DQ đã học, áp lên data dạng mới.

## Vai trò DE trong AI stack
- Cấp **data sạch, tươi, có cấu trúc** cho train + RAG.
- Feature/vector pipeline (giống ETL).
- Data quality cho AI ("garbage in, garbage out" càng đúng với LLM).
- Governance (PII trong tài liệu RAG, quyền truy cập chunk).

## ⚠️ Cạm bẫy
- Data leakage trong training (feature tương lai) → point-in-time.
- Train/serve skew → feature store chung định nghĩa.
- RAG: re-embed toàn bộ mỗi lần đổi (đắt) → incremental.
- Chunk sai size → retrieval kém.
- Bỏ qua quyền/PII trong tài liệu RAG (lộ data nhạy cảm qua LLM).

## ✅ "Tự mò"
🔭 Phác pipeline RAG: lấy notes khoá này (md) → chunk theo heading → embed (model bất kỳ) → pgvector/DuckDB VSS → query "giải thích shuffle" tìm top-3 chunk. Nghĩ incremental khi thêm note mới.

➡️ Tiếp: [[g07-dsa-for-de]].
