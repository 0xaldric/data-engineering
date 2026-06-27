# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 16 script).

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

**Batch hiện tại:** #29 — AI-Advanced 6: Case Studies AI-DE + Scale/Internals ⭐
**Nguồn:** đào sâu AI/LLM — system design & vận hành thực tế

---

## BATCH HIỆN TẠI

### [x] AF01 — Case Study: Customer Support AI Platform (system design)
- **Note:** `notes/advanced/af01-case-support-ai.md`. Thiết kế hệ AI hỗ trợ khách: ingest tài liệu/ticket → RAG trả lời + trích dẫn → guardrail (PII/injection) → escalation sang người khi không tự tin ([[ae01-self-correcting-rag]]) → feedback loop. Kiến trúc, data flow, freshness, eval (deflection rate), cost. Tổng hợp [[aa03-rag-production]], [[ad02-llm-judge]], [[ac05-voice-audio-pipeline]].

### [x] AF02 — Case Study: Enterprise Knowledge Assistant (multi-source + permissions)
- **Note:** `notes/advanced/af02-case-enterprise-kb.md`. RAG trên nhiều nguồn (Confluence/Drive/Slack/DB) với **phân quyền** (user chỉ thấy doc được phép — row-level security cho RAG), freshness đa nguồn ([[ac06-kb-freshness]]), conflicting info, audit. Thách thức: permission-aware retrieval, multi-tenancy ([[ad03-privacy-compliance]]).

### [x] AF03 — Case Study: AI Coding Assistant Data Platform
- **Note:** `notes/advanced/af03-case-coding-assistant.md`. Nền data cho code assistant ở repo scale: index nghìn repo ([[ae08-rag-for-code]]), incremental theo commit, repo-context (import/call graph), eval (acceptance rate), privacy (code là tài sản), latency thấp. Kiến trúc + trade-off.

### [x] AF04 — Vector DB Internals sâu
- **Note:** `notes/advanced/af04-vector-db-internals.md`. Bên trong vector DB: HNSW build (layer/M/ef), IVF-PQ (cụm + nén), **DiskANN** (ANN trên đĩa khi vector vượt RAM), filtered search internals, sharding/replication, consistency. Vì sao chọn Qdrant/Milvus/pgvector. Sâu hơn [[ab07-vector-search-opt]], [[aa10-llmops]].

### [x] AF05 — LLM Training Data Pipeline ở Scale (petabyte)
- **Note:** `notes/advanced/af05-training-data-scale.md`. Pipeline data train LLM ở scale lớn: thu thập web-scale, dedup ở scale (MinHash/LSH phân tán — [[aa04-training-data-prep]]), tokenization, sharding/streaming tới trainer, data mixing/weighting, quality filter ở scale ([[ae03-training-data-quality]]), decontamination. Spark/Ray, định dạng (WebDataset/Parquet).

### [ ] AF06 — AI Data Governance & Compliance
- **Note:** `notes/advanced/af06-ai-data-governance.md`. Governance cho AI: data catalog + lineage cho AI artifact (dataset→model→prompt→output), **model cards** & **datasheets**, audit trail ([[ad03-privacy-compliance]]), EU AI Act/risk tiers (khái niệm), data provenance & consent, bias/fairness audit. Liên hệ [[k06-data-contract-impl]], [[f06-dataops]].

### [ ] AF07 — Continuous RAG Eval & Regression Gate ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/af07-continuous-eval.md` + code `continuous_eval.py`. Eval liên tục như CI: chạy harness → so với baseline lưu (JSON) → PASS/FAIL theo ngưỡng (exit code) → cảnh báo regression. Code: chạy eval, lưu/đọc baseline, gate recall@k, in delta + exit ≠0 nếu tụt. Sâu hơn [[ab02-rag-eval-harness]], [[ac03-eval-driven-dev]].

### [ ] AF08 — Case Study: Real-time AI Personalization
- **Note:** `notes/advanced/af08-case-personalization.md`. Cá nhân hoá real-time bằng AI: streaming features ([[ac07-feature-store]]) + embedding user/item ([[ac02-recsys-llm]]) + LLM re-rank/giải thích; point-in-time, freshness, cold-start, cost ở scale. Kiến trúc lambda/kappa cho AI personalization.

### [ ] AF09 — AI review 6 + system-design interview drill
- **Note:** `notes/advanced/af09-ai-review6.md` + cập nhật `00-INDEX.md`. Tổng kết case studies; **khung trả lời system-design AI** (clarify→data flow→retrieval→safety→eval→scale→cost) + 3 đề system-design AI có lời giải; tổng kết 6 batch Module AI.

---
*Hết batch → sinh batch AI tiếp (agent platform data, RAG cho analytics/BI, AI observability sâu, data cho fine-tune RLHF, multi-modal production...) — vẫn ưu tiên AI/LLM.*
