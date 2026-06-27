# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 8 script).

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

**Batch hiện tại:** #26 — AI-Advanced 3 (RAG đa ngữ, recsys+LLM, eval-driven, agentic sâu) ⭐
**Nguồn:** đào sâu AI/LLM (tiếp)

---

## BATCH HIỆN TẠI

### [ ] AC01 — RAG đa ngôn ngữ / Cross-lingual ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ac01-multilingual-rag.md` + code `cross_lingual_eval.py`. Vì sao embedding EN-centric (bge-small) yếu cross-lingual; cách: model đa ngữ (multilingual-e5/bge-m3) vs dịch-rồi-embed; eval cross-lingual. Code: bắn golden query bản tiếng Anh vào index note tiếng Việt (rag.duckdb), đo recall **rớt** bao nhiêu so với query tiếng Việt → định lượng "khoảng cách đa ngữ", động lực dùng model đa ngữ. Liên hệ [[ai04-embedding-versioning]], [[ab02-rag-eval-harness]].

### [ ] AC02 — Recommendation + LLM (semantic recsys) ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ac02-recsys-llm.md` + code `semantic_recsys.py`. Embedding-based reco (content/two-tower ý tưởng), cold-start nhờ content embedding, LLM re-rank/giải thích; vai trò DE: item/user embedding pipeline, point-in-time. Code: embed "item" (title note) + user profile = trung bình item đã thích → recommend item gần nhất chưa xem (cosine), in gợi ý + lý do. Liên hệ [[c09-case-recsys]], [[ab07-vector-search-opt]].

### [ ] AC03 — Evaluation-Driven Development cho AI
- **Note:** `notes/advanced/ac03-eval-driven-dev.md`. "Eval trước, code sau" (như TDD cho LLM): golden set = spec, viết eval trước khi build pipeline, mọi thay đổi qua eval gate, regression CI; vòng lặp eval→cải tiến. Vì sao AI không eval-first = bay mù. Liên hệ [[ab02-rag-eval-harness]], [[aa06-llm-eval]], [[ai07-testing-nondeterministic]].

### [ ] AC04 — Agentic sâu: Multi-agent & Tool Design
- **Note:** `notes/advanced/ac04-multi-agent.md`. Planner/executor/critic, orchestration nhiều agent, thiết kế tool schema tốt (rõ input/output/lỗi), error recovery, khi nào multi-agent vs single (đa số single + tool là đủ); chi phí/độ trễ nhân lên. Vai trò DE: tool = truy cập data có kiểm soát. Sâu hơn [[aa05-agentic-pipelines]], [[ab03-context-engineering]].

### [ ] AC05 — Voice/Audio AI Data Pipeline
- **Note:** `notes/advanced/ac05-voice-audio-pipeline.md`. STT (Whisper), diarization (ai nói), alignment timestamp, chunk audio/transcript cho RAG, transcript = dữ liệu (search/analytics), PII trong audio (giọng + nội dung), cost xử lý audio lớn. Liên hệ [[aa08-multimodal]], [[ab06-llm-observability]].

### [ ] AC06 — Knowledge Base Freshness & Maintenance
- **Note:** `notes/advanced/ac06-kb-freshness.md`. Vòng đời corpus RAG: phát hiện doc cũ/lỗi thời, re-ingest, xử lý thông tin **mâu thuẫn** (versions), freshness SLA, xoá/cập nhật (right-to-be-forgotten), incremental re-index. "RAG không phải build 1 lần". Liên hệ [[ai09-streaming-ai]], [[ai04-embedding-versioning]].

### [ ] AC07 — Feature Store cho ML/LLM
- **Note:** `notes/advanced/ac07-feature-store.md`. Online/offline parity, **point-in-time correctness** (chống leakage), embedding như feature, serving low-latency, reuse feature; quan hệ với vector store. Vai trò DE kinh điển gặp ML. Liên hệ [[ab05-embedding-finetune]], [[e04-bitemporal]].

### [ ] AC08 — Cost Optimization sâu cho AI ở scale
- **Note:** `notes/advanced/ac08-ai-cost-scale.md`. Model routing (nhỏ↔lớn theo độ khó), cascade, semantic cache nhiều tầng, batch, prompt compression, distillation; unit economics ($/query), khi nào tự host. Sâu hơn [[ai08-ai-cost-latency]], [[aa10-llmops]].

### [ ] AC09 — AI review 3 + ngân hàng câu hỏi phỏng vấn
- **Note:** `notes/advanced/ac09-ai-review3.md` + cập nhật `00-INDEX.md`. Tổng kết AI-Advanced 3; **ngân hàng câu hỏi phỏng vấn AI-DE** (40+ Q&A ngắn theo chủ đề) + final portfolio pitch.

---
*Hết batch → sinh batch AI tiếp (GraphRAG nâng cao, real-time RAG, data cho AI agents, eval tự động bằng LLM-judge, privacy/compliance cho LLM...) — vẫn ưu tiên AI/LLM.*
