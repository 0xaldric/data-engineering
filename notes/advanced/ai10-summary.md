# 🏁 Module AI — Tổng kết: AI Data Engineering (trụ cột thứ 4)

> Tiêu chuẩn phỏng vấn DE 2025+ thêm trụ cột **hạ tầng dữ liệu cho AI**, trọng số ngang SQL/pipeline/modeling. "Danh từ đổi, tư duy không đổi."

## Các note + code chạy được
| # | Chủ đề | Note / Code |
|---|--------|-------------|
| AI01 | RAG capstone (chạy được) | `projects/06-ai-data-engineering/rag_over_notes.py` |
| AI02 | RAG writeup & kiến trúc | [ai02](ai02-rag-capstone-writeup.md) |
| AI03 | Chunking strategies | [ai03](ai03-chunking.md) |
| AI04 | Embedding versioning | [ai04](ai04-embedding-versioning.md) |
| AI05 | Retrieval eval (recall/MRR/nDCG, chạy được) | [ai05](ai05-retrieval-eval.md) |
| AI06 | **LLM-output governance** (chạy được) | [ai06](ai06-llm-output-governance.md) + `llm_output_pipeline.py` |
| AI07 | **Test non-deterministic** (chạy được) | [ai07](ai07-testing-nondeterministic.md) + `test_semantic.py` |
| AI08 | Cost & latency | [ai08](ai08-ai-cost-latency.md) |
| AI09 | Streaming AI infra (<1') | [ai09](ai09-streaming-ai.md) |

## ⭐ Map 3 câu hỏi phỏng vấn mới → trả lời ở đâu
| Câu hỏi phỏng vấn (thực tế) | Note + demo chạy được |
|------------------------------|------------------------|
| "Thiết kế pipeline tài liệu phi cấu trúc → tìm kiếm ngữ nghĩa" | [[ai02-rag-capstone-writeup]] + `rag_over_notes.py` |
| "Đánh giá pipeline truy xuất tốt hay không?" | [[ai05-retrieval-eval]] (recall/MRR/nDCG chạy thật) |
| "LLM tạo dữ liệu có cấu trúc đổ vào dashboard — kiểm & version thế nào?" | [[ai06-llm-output-governance]] + [[ai07-testing-nondeterministic]] + 2 demo |
| "Re-index <1' khi tài liệu đổi; vỡ gì khi ×2?" | [[ai09-streaming-ai]] |

## 📑 "Danh từ đổi, tư duy không đổi" — bảng đối chiếu
| DE truyền thống | AI/LLM Data Engineering |
|-----------------|--------------------------|
| nguồn → fact/dimension | tài liệu → chunk → vector |
| transform SQL | chunk + embed |
| warehouse table | vector store (DuckDB/pgvector/Qdrant) |
| SCD2 (dimension đổi) | re-embed (model/tài liệu đổi) |
| data quality (row count, schema) | retrieval quality (recall@k) + semantic test |
| schema contract | data contract cho output LLM + provenance |
| idempotent load | idempotent re-index (theo doc_id) |
| exact-match test | **semantic equivalence test** (cosine) |
| lineage | provenance (model + prompt + input → output) |
| CDC freshness | streaming re-embed < 1' |
| FinOps (bytes scanned) | token cost (embedding + LLM generation) |

→ **Mọi nguyên tắc DE áp y nguyên**: idempotency, incremental, lineage, DQ, contract, cost, streaming. Chỉ **output là vector / dữ liệu LLM** thay vì bảng.

## ✅ Checklist "sẵn sàng trụ cột thứ 4"
- [ ] Build được RAG pipeline (chunk→embed→vector store→search) + giải thích trade-off.
- [ ] Đo retrieval bằng recall@k/MRR/nDCG; biết re-ranking & RAGAS.
- [ ] Chunking strategies + chọn embedding model + **versioning** (đổi model = re-embed).
- [ ] Governance dữ liệu LLM: validate/repair/quarantine + provenance + drift.
- [ ] Test non-deterministic: semantic equivalence + schema + golden set.
- [ ] Cost/latency (token, cache, batch) + streaming re-index <1'.
- [ ] "Vỡ gì khi scale ×2" theo từng tầng.

## 🔭 Để "tự mò"
3 script chạy được trong `projects/06-ai-data-engineering/` là portfolio: chạy, sửa, mở rộng (đổi multilingual model, thêm re-ranking, thêm golden set của bạn). Đó là bằng chứng cho vòng phỏng vấn mới.

## ➡️ Tiếp: Module AI-Advanced
agentic data pipeline · RAG production (semantic cache/citations/guardrails) · PII redaction & prompt injection · training data prep (dedup MinHash) · LLM eval (RAGAS) · prompt versioning · multimodal (OCR/Whisper/CLIP) · GraphRAG · LLMOps · text-to-SQL · vector DB at scale · streaming RAG. (Loop sinh batch tiếp.)
