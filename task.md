# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 6 script).

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–4/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt trong `notes/advanced/` (khái niệm + "tại sao" + sơ đồ + snippet + cạm bẫy + checklist + "tự mò"). **Task có code: viết + CHẠY THỬ verify rồi mới tick.**
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch AI tiếp (vẫn AI/LLM — user ưu tiên). Cập nhật `00-INDEX.md`. Giữ PROTOCOL.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #25 — AI-Advanced 2 (đẩy mạnh AI/LLM) ⭐
**Nguồn:** đào sâu AI/LLM

---

## BATCH HIỆN TẠI

### [x] AB01 — Synthetic Data Generation với LLM ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ab01-synthetic-data.md` + code `projects/06-ai-data-engineering/synthetic_data.py`. Sinh dữ liệu giả bằng LLM (cho train/test khi thiếu data): đa dạng (diversity), quality filter, dedup (MinHash — [[aa04-training-data-prep]]), tránh mode collapse, label balance; rủi ro (bias khuếch đại, distribution drift vs data thật). Code: mock-LLM sinh N synthetic ticket đa dạng → dedup + balance + quality filter, đo.

### [x] AB02 — RAG Eval Harness (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ab02-rag-eval-harness.md` + code `rag_eval_harness.py`. Eval harness hoàn chỉnh: golden set → chạy retrieval → metric (recall@k/precision@k/MRR/nDCG) → report + so cấu hình (chunk size / hybrid on-off). Code: harness chạy nhiều cấu hình trên capstone, in bảng so sánh. Sâu hơn [[ai05-retrieval-eval]], [[aa06-llm-eval]].

### [x] AB03 — Context Engineering & Memory cho Agent
- **Note:** `notes/advanced/ab03-context-engineering.md`. Quản context window (token budget): chọn/cắt/nén context, memory (short-term conversation + long-term vector), tool-result caching, context compression, "lost in the middle"; DE cung cấp memory store + retrieval cho agent. Liên hệ [[aa05-agentic-pipelines]].

### [x] AB04 — Semantic Layer cho LLM (NL→metrics)
- **Note:** `notes/advanced/ab04-semantic-layer-llm.md`. Vì sao text-to-SQL thô nguy hiểm → LLM sinh **metric query qua semantic layer** ([[e05-semantic-layer]]) thay SQL thô: an toàn (metric định nghĩa sẵn), nhất quán, ít hallucination schema; NL → metric/dimension đã governed. Liên hệ [[aa01-text-to-sql]].

### [ ] AB05 — Embedding Fine-tuning & Domain Adaptation
- **Note:** `notes/advanced/ab05-embedding-finetune.md`. Khi embedding general kém với domain (y tế/legal/tiếng Việt) → fine-tune; contrastive learning (positive/negative pairs), hard negatives; vai trò DE: chuẩn bị training pairs (từ click log/feedback), eval cải thiện; khi nào fine-tune vs đổi model. Liên hệ [[ai04-embedding-versioning]].

### [ ] AB06 — LLM Observability & Tracing Pipeline
- **Note:** `notes/advanced/ab06-llm-observability.md`. Trace mỗi request (input→retrieval→prompt→LLM→output) như distributed tracing; token/cost tracking per request; log để debug/eval/audit; công cụ (Langfuse/LangSmith/Phoenix); data pipeline cho LLM logs (volume lớn như clickstream [[c06-case-clickstream]]). Liên hệ [[k07-observability-tooling]], [[aa10-llmops]].

### [ ] AB07 — Vector Search Optimization (sâu)
- **Note:** `notes/advanced/ab07-vector-search-opt.md`. Tuning ANN: HNSW (ef_construction/ef_search/M) vs recall/latency; IVF nprobe; **quantization** (PQ/SQ/binary) giảm RAM; pre-filter vs post-filter; hybrid weight tuning; trade-off recall-latency-RAM-cost. Sâu hơn [[k05-vector-rag-deep]], [[aa10-llmops]].

### [ ] AB08 — Data Pipeline cho Fine-tuning Workflow
- **Note:** `notes/advanced/ab08-finetune-pipeline.md`. Pipeline end-to-end cho fine-tune: thu thập (instruction/preference) → clean/dedup/decontaminate ([[aa04-training-data-prep]]) → format (chat template) → split → version dataset → train → eval → deploy; vai trò DE (data, không train); reproducibility.

### [ ] AB09 — AI Data Engineering review 2 + checklist phỏng vấn
- **Note:** `notes/advanced/ab09-ai-review2.md` + cập nhật `00-INDEX.md`. Tổng kết AI-Advanced 2; checklist "AI Data Engineer sẵn sàng" đầy đủ; map mọi note/script AI → kỹ năng phỏng vấn; portfolio talking points.

---
*Hết batch → sinh batch AI tiếp (RAG đa ngôn ngữ, agentic sâu, data cho voice AI, recommendation+LLM, evaluation-driven dev...) — vẫn ưu tiên AI/LLM.*
