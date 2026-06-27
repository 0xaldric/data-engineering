# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 10 script).

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

**Batch hiện tại:** #27 — AI-Advanced 4 (real-time RAG, LLM-judge, privacy/security, agent data) ⭐
**Nguồn:** đào sâu AI/LLM (tiếp)

---

## BATCH HIỆN TẠI

### [x] AD01 — Real-time / Streaming RAG ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ad01-streaming-rag.md` + code `streaming_rag.py`. RAG tươi gần real-time: doc mới → index trong vài giây (incremental theo hash/CDC), freshness SLA, khi nào cần streaming vs batch. Code: mô phỏng "stream" — thêm 1 note MỚI vào corpus, query TRƯỚC (không thấy) → incremental re-index → query SAU (thấy ngay), đo độ trễ freshness. Sâu hơn [[ai09-streaming-ai]], [[ac06-kb-freshness]].

### [x] AD02 — LLM-as-Judge tự động ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ad02-llm-judge.md` + code `llm_judge.py`. Eval tự động bằng "judge" (rubric chấm điểm): pointwise/pairwise, rubric, bias (vị trí/độ dài/tự khen), calibrate vs human. Code: mock-judge chấm câu trả lời theo rubric (grounding bằng cosine với reference + heuristic độ dài/từ khoá), so 2 câu (pairwise), in điểm + cảnh báo bias. Sâu hơn [[aa06-llm-eval]], [[ac03-eval-driven-dev]].

### [ ] AD03 — Privacy & Compliance cho LLM
- **Note:** `notes/advanced/ad03-privacy-compliance.md`. PII governance khi data đi qua LLM: data residency, gửi-ra-API vs self-host, consent, retention, right-to-be-forgotten ở vector store ([[ac06-kb-freshness]]), audit log, differential privacy (khái niệm), redaction trước khi gửi. GDPR/luật VN. Liên hệ [[aa02-guardrails]], [[k06-data-contract-impl]].

### [ ] AD04 — LLM Security sâu: Indirect Prompt Injection
- **Note:** `notes/advanced/ad04-llm-security.md`. Sâu hơn [[aa02-guardrails]]: indirect injection (lệnh độc giấu trong DOC mà RAG kéo vào), data exfiltration, jailbreak, tool abuse; defense-in-depth: least-privilege tool, tách data/instruction, output filter, human approve hành động nguy hiểm, sandbox. Liên hệ [[ac04-multi-agent]], [[aa01-text-to-sql]].

### [ ] AD05 — RAG trên dữ liệu CÓ CẤU TRÚC (tables/SQL)
- **Note:** `notes/advanced/ad05-structured-rag.md`. RAG không chỉ text: hỏi tự nhiên trên BẢNG/DB. Table retrieval (chọn bảng/cột liên quan), kết hợp text-to-SQL ([[aa01-text-to-sql]]) + semantic layer ([[ab04-semantic-layer-llm]]), hybrid structured+unstructured, schema linking. Khi câu hỏi cần SỐ chính xác (không hallucinate). Liên hệ [[ai02-rag-capstone-writeup]].

### [ ] AD06 — Document Parsing & Extraction sâu
- **Note:** `notes/advanced/ad06-doc-parsing.md`. "Rác vào rác ra": chất lượng RAG bắt đầu từ PARSE. PDF/HTML/DOCX, layout-aware, trích bảng, OCR scan, code/markdown, giữ cấu trúc (heading/list) cho chunking ([[ai03-chunking]]); pipeline parse → clean → normalize. Cạm bẫy parse hỏng âm thầm phá retrieval. Liên hệ [[aa08-multimodal]].

### [ ] AD07 — Data cho AI Agents Production
- **Note:** `notes/advanced/ad07-agent-data.md`. Hạ tầng DATA cho agent chạy thật: memory store (short/long [[ab03-context-engineering]]), tool data-access layer có governance, state/checkpoint (resume khi fail), action audit log (agent làm gì — [[ab06-llm-observability]]), idempotent tool. Vai trò DE dựng nền cho agent. Liên hệ [[ac04-multi-agent]], [[aa05-agentic-pipelines]].

### [ ] AD08 — Semantic Caching & Serving Infra ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ad08-semantic-cache.md` + code `semantic_cache.py`. Cache theo NGỮ NGHĨA (không chỉ exact match): câu hỏi gần nghĩa → trả cache, tiết kiệm LLM call ([[ac08-ai-cost-scale]]). Code: semantic cache bằng embedding (cosine ≥ ngưỡng → hit), đo hit rate + cảnh báo false-hit (gần nghĩa nhưng khác ý), invalidation. Liên hệ [[ai08-ai-cost-latency]], [[ab07-vector-search-opt]].

### [ ] AD09 — AI review 4 + capstone integration + drill cuối
- **Note:** `notes/advanced/ad09-ai-review4.md` + cập nhật `00-INDEX.md`. Tổng kết AI-Advanced 4; **mini-product tích hợp** (guardrail→retrieve→judge→cache) bằng các script đã có; drill phỏng vấn cuối (5 câu khó, trả lời whiteboard). Tổng kết toàn Module AI (4 batch, 13 script).

---
*Hết batch → sinh batch AI tiếp (RAG agent tự cải thiện, multimodal sâu, GraphRAG production, data quality cho LLM training, on-device AI...) — vẫn ưu tiên AI/LLM.*
