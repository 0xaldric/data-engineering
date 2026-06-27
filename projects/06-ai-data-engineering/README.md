# 06 — AI Data Engineering: RAG over your own notes ⭐

> Capstone **hạ tầng dữ liệu cho AI** — đúng thứ vòng phỏng vấn DE 2025+ đang hỏi. Chạy **100% local** (fastembed ONNX + DuckDB), không API key / torch / Java.

## Bài toán (phiên bản mới của "thiết kế pipeline ETL")
> *"Thiết kế pipeline thu thập tài liệu phi cấu trúc, chia nhỏ, tạo embedding, lưu vào vector DB để tìm kiếm theo ngữ nghĩa. Đánh giá pipeline truy xuất tốt hay không? Cái gì vỡ khi scale?"*

Ở đây "tài liệu phi cấu trúc" = chính **kho ~170 notes Markdown** của khoá học này.

## Pipeline (cùng tư duy ETL — output là vector thay vì fact/dim)
```
notes/*.md ──► CHUNK (structure-aware: theo heading + size/overlap)
          ──► EMBED (fastembed bge-small, local, 384-dim)
          ──► VECTOR STORE (DuckDB: FLOAT[384] + HNSW index)
          ──► SEARCH (hybrid: vector cosine + keyword)
          ──► EVAL (recall@k trên golden set)
```

## Skill DE được minh hoạ (= câu hỏi phỏng vấn AI-era)
| Skill | Trong code | Câu hỏi phỏng vấn tương ứng |
|-------|-----------|------------------------------|
| Chunking strategy | `chunk_markdown()` heading + overlap | "chiến lược chia nhỏ tài liệu?" |
| Embedding pipeline | fastembed, query prefix | "mô hình embedding nào, vì sao?" |
| Vector store + ANN | DuckDB `FLOAT[384]` + HNSW (`vss`) | "lưu trữ vector thế nào?" |
| **Incremental/idempotent** ⭐ | re-embed CHỈ file đổi (content hash), xử lý update/delete | "cập nhật khi tài liệu đổi? freshness?" |
| **Eval retrieval** ⭐ | `recall@k` golden set | "đánh giá pipeline truy xuất tốt không?" |
| Hybrid search | vector + keyword bonus | "vector trượt từ khoá chính xác thì sao?" |
| **Provenance** | lưu `model + indexed_at` mỗi chunk | "quản version dữ liệu LLM-era?" |

## Chạy
```bash
cd data-engineering && source .venv/bin/activate
python projects/06-ai-data-engineering/rag_over_notes.py                 # index + demo + eval
python projects/06-ai-data-engineering/rag_over_notes.py search "vì sao shuffle đắt"
```

## Kết quả thực tế (đo được)
- Index **169 notes → 1454 chunks**, embed local ~63s (lần đầu, tải model), HNSW index built.
- **Incremental:** chạy lại → 0 file re-embed (unchanged theo hash), 0.2s. Idempotent.
- **Semantic search** đúng: `"vì sao shuffle đắt"` → `31-partitioning-shuffle.md` (cosine 0.774).
- **recall@5 = 88%** (7/8 golden). Cross-lingual EN↔VI nên 1 miss — cải thiện bằng model multilingual.

## Hướng nâng cấp (để "ghi điểm" hơn)
- Đổi `MODEL_NAME` → `intfloat/multilingual-e5-small` (tốt cho tiếng Việt).
- Thêm **re-ranking** (cross-encoder) top-k; **nDCG/MRR**; faithfulness (RAGAS).
- **Streaming re-index < 1 phút** khi note đổi (watch file → embed → upsert) — xem notes Module AI.
- **Embedding model versioning**: đổi model → re-embed toàn bộ (vector cũ/mới không tương thích).
- Governance dữ liệu LLM-sinh: validate structured output + data contract — xem `notes/advanced/`.

> Đây là pipeline ETL quen thuộc, chỉ **output là vector**. Danh từ đổi, tư duy không đổi.
