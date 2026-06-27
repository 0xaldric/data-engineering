# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 17 script).

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

**Batch hiện tại:** #30 — AI-Advanced 7: Production AI Systems (hallucination, drift, RLHF, agent platform) ⭐
**Nguồn:** đào sâu AI/LLM — vận hành & data sâu hơn

---

## BATCH HIỆN TẠI

### [x] AG01 — RAG cho BI/Analytics & Conversational Data
- **Note:** `notes/advanced/ag01-rag-bi-analytics.md`. "Chat với dữ liệu": NL → insight, kết hợp semantic layer ([[ab04-semantic-layer-llm]]) + text-to-SQL ([[aa01-text-to-sql]]) + RAG metadata (hiểu bảng/cột). Conversational analytics (follow-up, ngữ cảnh), trả số chính xác + giải thích, viz gợi ý. Khác RAG text ([[ad05-structured-rag]]). Cạm bẫy số sai = mất niềm tin.

### [x] AG02 — Hallucination Detection & Mitigation ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ag02-hallucination-detection.md` + code `hallucination_detect.py`. Phát hiện bịa: grounding (bám context?), **self-consistency** (hỏi N lần, lệch nhau nhiều = bịa), NLI/entailment, citation check. Code: mock-LLM trả N lần cho 2 câu (1 chắc chắn, 1 bịa) → đo độ nhất quán bằng cosine giữa các lần → cờ "có thể bịa". Liên hệ [[aa02-guardrails]], [[ad02-llm-judge]].

### [x] AG03 — RLHF & Preference Data Pipeline
- **Note:** `notes/advanced/ag03-rlhf-preference-data.md`. Data cho RLHF/DPO: thu preference pair (chosen/rejected), nguồn (human annotation, AI feedback - RLAIF), chất lượng annotation (agreement, guideline), reward model data, cạm bẫy (annotator bias, reward hacking). Vai trò DE: pipeline thu/validate/version preference data. Liên hệ [[ab08-finetune-pipeline]], [[ae03-training-data-quality]].

### [x] AG04 — AI Observability sâu: Drift Detection ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ag04-drift-detection.md` + code `drift_detect.py`. Phát hiện drift trong hệ AI: input drift (phân phối câu hỏi đổi), embedding drift (centroid dịch), output drift, quality drift. Code: so 2 batch embedding (cũ vs mới) bằng khoảng cách centroid + avg pairwise → cờ drift khi vượt ngưỡng. Liên hệ [[ab06-llm-observability]], [[aa10-llmops]].

### [ ] AG05 — Agent Platform Data Infrastructure (sâu)
- **Note:** `notes/advanced/ag05-agent-platform.md`. Sâu hơn [[ad07-agent-data]]: tool registry (đăng ký/version/scope tool), orchestration state machine, multi-agent coordination (shared blackboard/message), agent run store (mỗi run = 1 trace có thể replay), human-in-loop queue. Nền tảng vận hành agent ở scale. Liên hệ [[ac04-multi-agent]].

### [ ] AG06 — Multimodal AI in Production (video/ảnh scale)
- **Note:** `notes/advanced/ag06-multimodal-production.md`. Sâu hơn [[ae04-multimodal-rag]]: pipeline video/ảnh ở scale (frame sampling, scene detection, transcode), object store + CDN, cost cực lớn (GPU encode/embed), incremental, eval cross-modal. Case: search video, kiểm duyệt nội dung. Liên hệ [[ac05-voice-audio-pipeline]], [[af05-training-data-scale]].

### [ ] AG07 — Conversational Memory & Long Context
- **Note:** `notes/advanced/ag07-conversational-memory.md`. Sâu hơn [[ab03-context-engineering]]: kiến trúc memory hội thoại dài (episodic/semantic/working), tóm tắt phân cấp, long-context vs RAG-memory (khi nào nhồi cả vs retrieve), entity memory (fact bền), forgetting/TTL. Cạm bẫy chi phí token + lost-in-middle. Liên hệ [[ad07-agent-data]].

### [ ] AG08 — Data Contracts cho AI I/O & Schema Evolution
- **Note:** `notes/advanced/ag08-ai-data-contracts.md`. Hợp đồng dữ liệu cho I/O của AI: schema cho output LLM ([[ai06-llm-output-governance]]), versioning prompt+schema ([[aa07-prompt-management]]), breaking change (đổi schema output phá downstream), backward compat, contract test. Mở rộng [[k06-data-contract-impl]] cho AI.

### [ ] AG09 — AI review 7 + tổng kết toàn Module AI
- **Note:** `notes/advanced/ag09-ai-review7.md` + cập nhật `00-INDEX.md`. Tổng kết AI-Advanced 7; **bản đồ năng lực AI-DE hoàn chỉnh** (7 batch → mọi chủ đề), 19 script, reflection cuối hành trình, định hướng tiếp tục.

---
*Hết batch → sinh batch AI tiếp (RAG benchmark public, LLM serving infra, data cho multimodal LLM, AI red-teaming, case study mới...) — vẫn ưu tiên AI/LLM.*
