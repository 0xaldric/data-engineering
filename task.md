# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 25 script).

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

**Batch hiện tại:** #36 — AI-Advanced 13: Advanced Patterns & More Verticals ⭐
**Nguồn:** đào sâu AI/LLM — RAG/agentic patterns + ngành mới

---

## BATCH HIỆN TẠI

### [ ] AN01 — RAG Advanced Patterns + Query Router ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/an01-rag-advanced-patterns.md` + code `query_router.py`. Mẫu RAG nâng cao: query routing (RAG/SQL/cache/từ chối), multi-vector (1 doc nhiều embedding: summary+chi tiết), hypothetical questions (index câu hỏi giả thay đoạn), RAPTOR (cây tóm tắt phân cấp). Code: router phân loại câu hỏi (định lượng/kiến thức/chitchat/hành động) bằng heuristic + embedding → route đúng đường, in quyết định. Liên hệ [[ae06-query-understanding]], [[ad05-structured-rag]].

### [ ] AN02 — Agentic Patterns Deep
- **Note:** `notes/advanced/an02-agentic-patterns.md`. Sâu hơn [[aa05-agentic-pipelines]], [[ac04-multi-agent]]: planner-executor, reflection (tự phê + sửa), tool-use patterns (chọn/gọi/lỗi), multi-agent debate (nhiều agent tranh luận → đồng thuận), ReAct vs plan-first, khi nào pattern nào. Vai trò DE: tool + state + trace. Liên hệ [[ag05-agent-platform]].

### [ ] AN03 — Case Study: Telecom AI
- **Note:** `notes/advanced/an03-case-telecom-ai.md`. AI viễn thông: tối ưu mạng (anomaly/dự báo tải), churn prediction, chăm sóc khách (RAG + chatbot), phát hiện gian lận cước. Nhấn: scale data khổng lồ (CDR [[j02-case-telecom]]), real-time mạng, time-series. Khung 7 bước.

### [ ] AN04 — Case Study: Energy/Utilities AI
- **Note:** `notes/advanced/an04-case-energy-ai.md`. AI năng lượng: dự báo nhu cầu điện (time-series [[ak08-timeseries-tabular-fm]]), tối ưu lưới (grid), predictive maintenance thiết bị, anomaly tiêu thụ. Nhấn: time-series + real-time grid + an toàn vật lý (không tự điều khiển lưới [[ak05-case-manufacturing-ai]]). Liên hệ [[j03-case-energy]].

### [ ] AN05 — Case Study: Travel/Hospitality AI
- **Note:** `notes/advanced/an05-case-travel-ai.md`. AI du lịch: trợ lý đặt phòng/vé, reco điểm đến ([[ac02-recsys-llm]]), dynamic pricing, tóm tắt review, chatbot đa ngữ. Nhấn: đa ngữ (khách quốc tế [[ac01-multilingual-rag]]), real-time giá/tồn phòng ([[ak01-case-ecommerce-ai]]), personalization. Khung 7 bước.

### [ ] AN06 — Case Study: Social Media AI (Trust & Safety)
- **Note:** `notes/advanced/an06-case-social-ai.md`. AI mạng xã hội: feed ranking ([[af08-case-personalization]]), moderation ở scale khổng lồ (trust & safety), phát hiện misinformation/spam/bot, đề xuất kết nối. Nhấn: moderation scale tỉ post + an toàn + chống lan truyền độc hại + fairness ([[al04-case-media-ai]]). Liên hệ [[h04-case-social-graph]].

### [ ] AN07 — AI-DE Mock Interview 3 (đề + lời giải đầy đủ)
- **Note:** `notes/advanced/an07-mock-interview-3.md`. Mock 3: 1 system-design (multimodal search/moderation ở scale) + 4 câu (chunking, fusion, drift, cost) + 1 behavioral. Đề + lời giải mẫu + thang chấm. Liên hệ [[am03-advanced-chunking]], [[am04-hybrid-fusion]].

### [ ] AN08 — AI-DE Coding Exercises 4 (bài tập + lời giải)
- **Note:** `notes/advanced/an08-coding-exercises-4.md`. 5 bài (router/agent/data) có đề + lời giải + reasoning: query router heuristic, ReAct loop mini, provenance log, budget cap counter, point-in-time as-of join. Dạng coding-round. Liên hệ [[an01-rag-advanced-patterns]], [[an02-agentic-patterns]].

### [ ] AN09 — AI review 13 + tổng kết
- **Note:** `notes/advanced/an09-ai-review13.md` + cập nhật `00-INDEX.md`. Tổng kết; bảng "RAG pattern → vấn đề giải"; tổng kết 13 batch Module AI; trạng thái curriculum.

---
*Hết batch → sinh batch AI tiếp (ngành mới, pattern mới, mock/exercise mới) — vẫn ưu tiên AI/LLM.*
