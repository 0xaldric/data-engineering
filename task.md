# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 23 script).

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

**Batch hiện tại:** #35 — AI-Advanced 12: Deep Techniques & Debugging ⭐
**Nguồn:** đào sâu AI/LLM — kỹ thuật sâu, debug, fusion

---

## BATCH HIỆN TẠI

### [x] AM01 — RAG Failure Modes & Debugging ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/am01-rag-debugging.md` + code `rag_debugger.py`. Catalog cách RAG HỎNG (retrieval miss, sai chunk, lost-in-middle, chunk quá nhỏ/to, embedding lệch, generation bỏ context) + cách DEBUG từng cái. Code: với query fail, chẩn đoán — doc đúng có trong index? chunk tốt nhất điểm bao nhiêu? bị rank dưới k? note nào "cướp" top? Liên hệ [[ab02-rag-eval-harness]], [[ae01-self-correcting-rag]].

### [x] AM02 — Advanced Prompt Patterns
- **Note:** `notes/advanced/am02-prompt-patterns.md`. Mẫu prompt nâng cao: Chain-of-Thought (nghĩ từng bước), ReAct (reason+act+observe [[aa05-agentic-pipelines]]), few-shot (ví dụ trong prompt), structured output (JSON schema [[ai06-llm-output-governance]]), self-consistency (vote nhiều lần), role/persona. Khi nào dùng cái nào. Liên hệ [[aj08-prompt-optimization]], [[aj01-reasoning-models]].

### [x] AM03 — Advanced Chunking Strategies
- **Note:** `notes/advanced/am03-advanced-chunking.md`. Sâu hơn [[ai03-chunking]]: semantic chunking (cắt theo điểm đổi ngữ nghĩa), propositional (mệnh đề), parent-child (chunk nhỏ tìm, trả context cha), late chunking (embed cả doc rồi cắt), sliding window + overlap tuning. Trade-off mỗi cái. Liên hệ [[ad06-doc-parsing]], [[ae08-rag-for-code]].

### [x] AM04 — Hybrid Search Tuning: RRF & Fusion ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/am04-hybrid-fusion.md` + code `rrf_fusion.py`. Sâu về kết hợp vector + keyword: Reciprocal Rank Fusion (RRF — gộp THỨ HẠNG không gộp điểm), weighted fusion, tuning trọng số α. Code: trên capstone, so RRF vs weighted-hybrid vs vector-only, đo recall@k → thấy fusion ảnh hưởng. Sâu hơn [[aa03-rag-production]], [[ae07-reranking-deep]].

### [ ] AM05 — Evaluation Metrics Deep
- **Note:** `notes/advanced/am05-eval-metrics-deep.md`. Sâu về metric: nDCG (công thức + IDCG + graded relevance), MAP (mean average precision), hit-rate@k, precision/recall trade-off, latency percentiles (p50/p95/p99), RAGAS internals (faithfulness/context-precision/recall). Chọn metric theo bài toán. Liên hệ [[ab02-rag-eval-harness]], [[aa06-llm-eval]].

### [ ] AM06 — Case Study: Gaming AI Data
- **Note:** `notes/advanced/am06-case-gaming-ai.md`. AI game: NPC thông minh (LLM dialogue), matchmaking, anti-cheat (anomaly), player analytics, content generation. Nhấn: real-time scale (triệu player [[g04-case-gaming]]), latency thấp, cost (LLM cho NPC đắt), an toàn (chat moderation). Khung 7 bước.

### [ ] AM07 — Case Study: Agriculture/AgriTech AI
- **Note:** `notes/advanced/am07-case-agritech-ai.md`. AI nông nghiệp: phân tích ảnh cây/sâu bệnh (multimodal [[ae04-multimodal-rag]]), dự báo mùa vụ/thời tiết (time-series [[ak08-timeseries-tabular-fm]]), RAG kiến thức canh tác, edge (đồng ruộng mạng yếu [[ae05-edge-ai-data]]). Nhấn: multimodal + edge + đa ngữ nông dân. Liên hệ [[k04-case-agritech]].

### [ ] AM08 — AI-DE Coding Exercises 3 (bài tập + lời giải)
- **Note:** `notes/advanced/am08-coding-exercises-3.md`. 5 bài (retrieval/fusion/eval nâng cao) có đề + lời giải + reasoning: RRF fusion, nDCG đầy đủ, MMR diversity, sliding-window chunk, semantic-cache lookup. Dạng coding-round. Liên hệ [[am04-hybrid-fusion]], [[am05-eval-metrics-deep]].

### [ ] AM09 — AI review 12 + tổng kết kỹ thuật sâu
- **Note:** `notes/advanced/am09-ai-review12.md` + cập nhật `00-INDEX.md`. Tổng kết; bảng "kỹ thuật sâu → khi nào dùng"; debug checklist RAG; tổng kết 12 batch Module AI.

---
*Hết batch → sinh batch AI tiếp (kỹ thuật mới, ngành mới, mock/exercise mới) — vẫn ưu tiên AI/LLM.*
