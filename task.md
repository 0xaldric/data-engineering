# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). Module này **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/`.

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–4/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt trong `notes/advanced/` (khái niệm + "tại sao" + sơ đồ + snippet + cạm bẫy + checklist + "tự mò"). **Task có code: viết + CHẠY THỬ verify rồi mới tick.**
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch AI tiếp theo từ Module AI-Advanced trong `ADVANCED.md` (vẫn AI/LLM — user ưu tiên). Cập nhật `00-INDEX.md`. Giữ PROTOCOL.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #24 — AI-Advanced (đẩy mạnh AI/LLM) ⭐
**Nguồn:** ADVANCED.md (Module AI-Advanced)

---

## BATCH HIỆN TẠI

### [x] AA01 — Text-to-SQL / NL2SQL Pipeline ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/aa01-text-to-sql.md` + code `projects/06-ai-data-engineering/text_to_sql.py`. Vai trò DE: schema linking (đưa schema context cho LLM), SQL validation (parse/EXPLAIN trước khi chạy), **guardrail** (chặn DROP/DELETE, chỉ SELECT, giới hạn rows), sandbox execution, eval. Code: mock-LLM sinh SQL từ câu hỏi → validate trên DuckDB e-commerce → chặn lệnh nguy hiểm → chạy an toàn (không cần API). Liên hệ [[e05-semantic-layer]].

### [x] AA02 — Guardrails & Safety cho LLM ⭐⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/aa02-guardrails.md` + code `guardrails_demo.py`. **PII redaction** input/output (regex email/phone/CCCD), prompt injection detection (pattern), output filtering, grounding/hallucination check (output có trong context không). Code: redact PII + phát hiện injection + kiểm output grounded bằng cosine (dùng fastembed). Liên hệ [[64-governance-pii]], [[ai07-testing-nondeterministic]].

### [x] AA03 — RAG Production Patterns
- **Note:** `notes/advanced/aa03-rag-production.md`. Semantic cache (câu hỏi tương tự → cache, dùng cosine), citations (trả nguồn chunk), fallback (retrieval rỗng → "không biết"), multi-tenancy (filter theo tenant), reranking, query rewriting/HyDE, online eval. Sâu hơn [[k05-vector-rag-deep]], [[ai05-retrieval-eval]].

### [x] AA04 — Training / Fine-tuning Data Prep (vai trò DE) ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/aa04-training-data-prep.md` + code `dedup_minhash.py`. DE chuẩn bị dữ liệu train: **near-duplicate detection (MinHash + LSH)**, quality filtering, dedup, instruction/RLHF data format, decontamination (loại test khỏi train), data mixing. Code: MinHash/LSH dedup phát hiện near-dup trên tập văn bản, đo. Liên hệ [[g07-dsa-for-de]].

### [x] AA05 — Agentic Data Pipelines
- **Note:** `notes/advanced/aa05-agentic-pipelines.md`. LLM agent điều phối công việc data: tool use (gọi SQL/API/search), ReAct loop, self-healing pipeline (agent debug lỗi), text-to-pipeline; rủi ro (non-determinism, cost, loop vô hạn, sai lệnh); DE giám sát agent (guardrail, human approval, observability).

### [x] AA06 — LLM Evaluation Frameworks (RAGAS sâu)
- **Note:** `notes/advanced/aa06-llm-eval.md`. Eval harness, RAGAS metrics (faithfulness, answer/context relevance, context precision/recall), golden dataset xây thế nào, human eval, LLM-as-judge bias, online eval (production feedback), regression suite cho prompt/model. Sâu hơn [[ai05-retrieval-eval]].

### [x] AA07 — Prompt Management & Versioning
- **Note:** `notes/advanced/aa07-prompt-management.md`. Prompt as code (git, review), prompt registry, versioning (prompt + model + output lineage), A/B prompt, template + variable, regression khi đổi prompt; vì sao prompt là "config" cần quản lý như code/schema. Liên hệ [[ai06-llm-output-governance]].

### [x] AA08 — Multimodal Data Pipelines
- **Note:** `notes/advanced/aa08-multimodal.md`. Pipeline cho ảnh/audio/video: image embedding (CLIP), OCR (tài liệu scan), transcription (Whisper audio→text), video frame sampling; lưu trữ (object store + vector), multimodal RAG; vai trò DE (orchestrate model inference → feature/vector). Liên hệ [[c04-case-iot]] imagery, [[k05-vector-rag-deep]].

### [ ] AA09 — GraphRAG + Knowledge Graph
- **Note:** `notes/advanced/aa09-graphrag.md`. Trích xuất entity/relation (LLM) → knowledge graph; GraphRAG (retrieval trên graph + vector hybrid); khi nào graph hơn vector (multi-hop/quan hệ); community detection; pipeline build KG. Liên hệ [[h04-case-social-graph]].

### [ ] AA10 — LLMOps + Vector DB at scale + review
- **Note:** `notes/advanced/aa10-llmops.md` + cập nhật `00-INDEX.md`. LLMOps (deploy/monitor model+prompt, cost dashboard, drift, A/B, model registry); vector DB at scale (sharding, quantization PQ, filtered search perf); tổng kết AI-Advanced. Sẵn sàng batch AI tiếp.

---
*Hết batch → sinh batch AI tiếp (synthetic data, context engineering, semantic layer cho LLM, RAG eval nâng cao...) — vẫn ưu tiên AI/LLM theo yêu cầu user.*
