# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN: Module AI Data Engineering** (tiêu chuẩn phỏng vấn DE mới 2025+). Module này **ĐƯỢC viết code chạy được** (ngoại lệ notes-first) vì là portfolio piece — chạy local bằng fastembed + DuckDB, KHÔNG cần API key. Capstone đã có: `projects/06-ai-data-engineering/rag_over_notes.py`.

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–4/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt trong `notes/advanced/` (khái niệm + "tại sao" + sơ đồ + snippet + cạm bẫy + checklist + "tự mò"). **Nếu task yêu cầu code**: viết + CHẠY THỬ (local fastembed/DuckDB/pydantic, đã cài), verify không lỗi, rồi mới tick.
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: quay lại đào sâu Extra (L: HR/manufacturing/retail; M...) hoặc thêm bài AI. Cập nhật `00-INDEX.md`. Giữ PROTOCOL.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #23 — Module AI Data Engineering ⭐
**Nguồn:** ADVANCED.md (Module AI)

---

## BATCH HIỆN TẠI

### [x] AI01 — RAG Capstone over own notes (CHẠY ĐƯỢC) ⭐
- **Đã build & verify:** `projects/06-ai-data-engineering/rag_over_notes.py` + README. Chunk 169 notes→1454 chunks, embed local (fastembed bge-small), DuckDB vector store + HNSW, hybrid search, **incremental idempotent** (re-embed chỉ file đổi), **recall@5=88%**. Chạy: `python projects/06-ai-data-engineering/rag_over_notes.py`.

### [ ] AI02 — RAG capstone writeup + kiến trúc
- **Note:** `notes/advanced/ai02-rag-capstone-writeup.md`. Giải thích kiến trúc capstone AI01 (sơ đồ chunk→embed→store→search→eval), từng quyết định & trade-off, map sang câu hỏi phỏng vấn AI-era; cách trình bày trong portfolio/interview. Link [[g06-case-ml-llm-data]], [[k05-vector-rag-deep]].

### [ ] AI03 — Chunking strategies sâu
- **Note:** `notes/advanced/ai03-chunking.md`. fixed-size vs semantic vs structure-aware vs parent-child/late-chunking; overlap; chunk size ảnh hưởng recall thế nào; chunk metadata; code: thử 2 chiến lược chunk trên notes, đo recall@k khác nhau (mở rộng rag_over_notes hoặc script nhỏ).

### [ ] AI04 — Embedding models & versioning ⭐
- **Note:** `notes/advanced/ai04-embedding-versioning.md`. Chọn model (dimension/chất lượng/cost/latency/multilingual); **vì sao đổi model = re-embed TOÀN BỘ** (vector không tương thích) → chiến lược migration (blue-green index, dual-index); cache embedding; batch để rẻ. Code: thêm cột model_version + demo "đổi model phải rebuild".

### [ ] AI05 — Retrieval eval sâu (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ai05-retrieval-eval.md` + mở rộng capstone. recall@k, precision@k, MRR, nDCG; re-ranking; RAG faithfulness/groundedness (RAGAS/LLM-judge khái niệm); golden set xây thế nào. Code: thêm hàm tính MRR/nDCG vào rag_over_notes, in bảng metric.

### [ ] AI06 — LLM-as-data-producer Governance ⭐⭐ (GAP quan trọng)
- **Note:** `notes/advanced/ai06-llm-output-governance.md` + code demo. Dữ liệu LLM sinh (nhãn/JSON/tóm tắt) đổ vào bảng production: validate structured output (pydantic + retry/repair), **data contract cho output LLM** (schema+confidence+provenance), version `model+prompt+input→output` (lineage/reproducibility), human-in-loop sampling, drift khi model nâng cấp. Code: `llm_output_pipeline.py` mô phỏng LLM trả JSON (đôi khi lỗi) → validate/repair/quarantine + log provenance (chạy được, không cần API thật).

### [ ] AI07 — Testing dữ liệu Non-deterministic ⭐⭐ (GAP quan trọng)
- **Note:** `notes/advanced/ai07-testing-nondeterministic.md` + code. Vì sao không exact-match (cùng input khác output); golden set; **semantic equivalence test** (cosine > ngưỡng, dùng embedding đã có); schema/format validation; statistical/distribution test; snapshot + review; CI cho output LLM. Code: `test_semantic.py` so 2 câu trả lời "khác chữ cùng nghĩa" pass, "khác nghĩa" fail (dùng fastembed).

### [ ] AI08 — Cost & Latency cho AI pipeline
- **Note:** `notes/advanced/ai08-ai-cost-latency.md`. Token cost embedding/LLM; cache + batch embedding (đo: embed 1454 chunks tốn gì); latency budget real-time serving; rate-limit/backpressure API; chọn model theo cost/latency/chất lượng; FinOps cho AI (khác [[59-cost-finops]]).

### [ ] AI09 — Streaming cho AI infra (re-index <1 phút)
- **Note:** `notes/advanced/ai09-streaming-ai.md`. "Streaming cuối cùng có lý do": event-driven re-embed khi tài liệu đổi (watch→chunk→embed→upsert <1'), feature serving real-time cho inference, kiểm dữ liệu LLM trước khi vào production; cái gì vỡ khi traffic ×2 (embedding model throughput, vector DB write, rate limit). Liên hệ [[45-streaming-intro]], [[c03-case-fraud]].

### [ ] AI10 — Module AI review + tiêu chuẩn phỏng vấn mới
- **Note:** `notes/advanced/ai10-summary.md` + cập nhật `00-INDEX.md`. Tổng kết Module AI; map 3 câu hỏi phỏng vấn mới (RAG pipeline / eval retrieval / version dữ liệu LLM) → note nào trả lời; checklist "sẵn sàng trụ cột thứ 4"; "danh từ đổi tư duy không đổi" — bảng đối chiếu ETL cũ ↔ RAG mới.

---
*Hết Module AI → quay lại Extra L (HR/manufacturing/retail) hoặc thêm bài AI nâng cao (agentic data pipeline, RAG production patterns...).*
