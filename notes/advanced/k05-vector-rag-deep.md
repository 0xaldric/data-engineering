# K05 — Deep-dive: Vector DB & RAG sâu

> Đào sâu phần data cho LLM/RAG — kỹ năng DE ngày càng cần. Sâu hơn [[g06-case-ml-llm-data]].

## Vector & embedding (nhắc nhanh)
Embedding model biến text/image → **vector** (vd 768/1536 chiều); khoảng cách vector ≈ độ giống nghĩa. RAG = tìm chunk gần câu hỏi nhất → đưa vào prompt LLM.

## ⭐ Vector index: ANN (Approximate Nearest Neighbor)
Tìm vector gần nhất chính xác (brute-force) trên triệu vector = O(n) đắt. → **ANN** đổi chính xác lấy tốc độ (giống probabilistic — [[g08-probabilistic-ds]]):
| Index | Ý tưởng | Đặc điểm |
|-------|---------|----------|
| **HNSW** (graph) | đồ thị nhiều tầng "navigable small world", đi từ thô→mịn | nhanh, recall cao, tốn RAM; phổ biến nhất |
| **IVF** (inverted file) | chia không gian thành cluster, chỉ tìm trong cluster gần | cân RAM/tốc độ, cần train |
| **PQ** (product quantization) | nén vector → giảm RAM | tiết kiệm bộ nhớ, giảm chính xác |
→ Tham số (ef_search/nprobe) cân **recall vs latency**. Vector DB: pgvector, Pinecone, Weaviate, Milvus, Qdrant; cũng có trong DuckDB (VSS), ClickHouse.

## Chunking strategies ⭐
Chia tài liệu thành đoạn để embed — **ảnh hưởng lớn** chất lượng retrieval:
- **Fixed-size** (vd 512 token + overlap 50): đơn giản; có thể cắt giữa ý.
- **Semantic/structure-aware**: chia theo heading/đoạn/câu → giữ ngữ cảnh (tốt hơn).
- **Overlap**: chồng lấn để không mất ngữ cảnh ở ranh giới.
- Trade-off: chunk to → ngữ cảnh đủ nhưng nhiễu + ít chính xác; nhỏ → chính xác nhưng mất ngữ cảnh. Tuỳ tài liệu/use case.

## ⭐ Hybrid search (vector + keyword)
Vector search giỏi nghĩa, kém với từ khoá chính xác (mã, tên riêng, số). **Hybrid**:
```
vector search (semantic) + BM25/keyword (lexical) → kết hợp điểm (RRF: Reciprocal Rank Fusion) → re-rank
```
- **BM25** (full-text) bắt khớp từ khoá; vector bắt nghĩa → kết hợp recall tốt hơn cả hai.
- **Re-ranking**: model cross-encoder chấm lại top-k → sắp chính xác hơn (đắt hơn, chỉ top-k).
- **Metadata filter**: kết hợp similarity + filter (nguồn/ngày/quyền) → đúng + an toàn.

## RAG evaluation
Đo chất lượng RAG (không chỉ "chạy"):
- **Retrieval**: recall@k (chunk đúng có trong top-k?), precision, MRR.
- **Generation**: faithfulness (trả lời bám tài liệu, không bịa), answer relevance, groundedness.
- Công cụ: RAGAS, đánh giá bằng LLM-judge + bộ test có nhãn.

## ⭐ Pipeline DE cho RAG (freshness/incremental)
```
ingest docs → chunk → embed → upsert vector DB (theo doc_id+chunk_id)
   │ doc đổi → re-chunk + re-embed CHỈ doc đó (incremental) → upsert (idempotent)
   │ doc xoá → xoá chunk tương ứng
   monitor: freshness (doc mới bao lâu vào index), coverage, eval drift
```
= ETL quen thuộc (idempotent upsert theo key, incremental — [[27-dbt-incremental]], [[40-pipeline-patterns]]) áp lên dữ liệu vector. **Đừng re-embed toàn bộ mỗi lần** (đắt).

## ⚠️ Cạm bẫy
- Re-embed toàn bộ khi 1 doc đổi (đắt) → incremental theo doc_id.
- Chỉ vector search → trượt từ khoá chính xác → hybrid.
- Chunk sai size → retrieval kém.
- Bỏ qua quyền/PII trong chunk → lộ qua LLM ([[64-governance-pii]]).
- Không eval → không biết RAG tốt hay tệ ("garbage retrieval in").
- Embedding model đổi version → phải re-embed tất cả (vector không tương thích).

## ✅ "Tự mò"
🔭 DuckDB VSS hoặc pgvector: embed các note khoá này → index; query "giải thích shuffle" so kết quả vector-only vs hybrid (thêm keyword "shuffle"); thử incremental khi thêm 1 note mới.

➡️ Tiếp: [[k06-data-contract-impl]].
