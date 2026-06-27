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

**Batch hiện tại:** #34 — AI-Advanced 11: Mock Interviews, Exercises & More Verticals ⭐
**Nguồn:** đào sâu AI/LLM — luyện phỏng vấn + bài tập + ngành mới

---

## BATCH HIỆN TẠI

### [ ] AL01 — AI-DE Mock Interview 1 (đề + lời giải đầy đủ)
- **Note:** `notes/advanced/al01-mock-interview-1.md`. Mock phỏng vấn AI Data Engineer hoàn chỉnh: 1 system-design (RAG đa nguồn có phân quyền) + 4 câu khái niệm (RAG eval, hallucination, governance, cost) + 1 behavioral STAR. **Viết đề + lời giải mẫu đầy đủ + thang chấm** (như phỏng vấn thật). Liên hệ [[af09-ai-review6]], [[h07-mock-interview]].

### [ ] AL02 — AI-DE Coding Exercises 1 (bài tập + lời giải)
- **Note:** `notes/advanced/al02-coding-exercises-1.md`. 5 bài tập code AI-DE (RAG/embedding/eval) **có đề + lời giải đầy đủ + reasoning**: vd "tính recall@k/MRR từ kết quả", "chunk text giữ cấu trúc", "đo cosine + ngưỡng", "incremental index theo hash", "dedup gần đúng". Dạng coding-round phỏng vấn. Liên hệ [[ab02-rag-eval-harness]], [[g07-dsa-for-de]].

### [ ] AL03 — Case Study: Logistics/Supply-chain AI
- **Note:** `notes/advanced/al03-case-logistics-ai.md`. AI logistics: tối ưu tuyến (route), dự báo nhu cầu (time-series [[ak08-timeseries-tabular-fm]]), RAG tài liệu vận hành, chatbot tracking đơn, anomaly giao hàng. Nhấn: real-time + tối ưu + dự báo; LLM bổ trợ không tự điều phối. Khung 7 bước ([[af09-ai-review6]]).

### [ ] AL04 — Case Study: Media/Streaming AI
- **Note:** `notes/advanced/al04-case-media-ai.md`. AI media/streaming: content reco ([[ac02-recsys-llm]]), kiểm duyệt nội dung (multimodal [[ag06-multimodal-production]]), tóm tắt/tag tự động, search video. Nhấn: scale nội dung khổng lồ, real-time personalization ([[af08-case-personalization]]), moderation an toàn, cost GPU video.

### [ ] AL05 — Case Study: HR/Recruiting AI (bias-critical)
- **Note:** `notes/advanced/al05-case-hr-ai.md`. AI tuyển dụng: sàng lọc CV, match ứng viên-JD, tóm tắt phỏng vấn. CỰC nhạy bias (phân biệt đối xử = pháp lý + đạo đức — [[af06-ai-data-governance]]), transparency, không tự loại ứng viên. Nhấn: fairness audit nghiêm + human quyết + explainability. Tương tự government về fairness ([[ak04-case-govt-ai]]).

### [ ] AL06 — AI-DE Mock Interview 2 (đề + lời giải đầy đủ)
- **Note:** `notes/advanced/al06-mock-interview-2.md`. Mock 2: 1 system-design (AI agent xử lý email + tool + safety) + 4 câu (drift, RLHF data, vector DB scale, eval-driven) + 1 behavioral. Đề + lời giải mẫu + thang chấm. Liên hệ [[ah03-red-teaming]], [[ag04-drift-detection]].

### [ ] AL07 — AI-DE Coding Exercises 2 (bài tập + lời giải)
- **Note:** `notes/advanced/al07-coding-exercises-2.md`. 5 bài tập (governance/guardrails/DQ) có đề + lời giải + reasoning: vd "validate JSON output theo schema", "redact PII bằng regex", "hard-gate data quality", "Cohen's kappa", "self-consistency check". Dạng coding-round. Liên hệ [[ai06-llm-output-governance]], [[ak06-data-labeling]].

### [ ] AL08 — Case Study: Insurance AI
- **Note:** `notes/advanced/al08-case-insurance-ai.md`. AI bảo hiểm: xử lý claim (trích/validate hồ sơ), phát hiện gian lận, underwriting hỗ trợ, RAG hợp đồng/điều khoản. Nhấn: compliance + explainability (giải trình từ chối) + point-in-time + LLM không tự quyết chi trả. Tương tự finance ([[aj06-case-finance-ai]]). Liên hệ [[k02-case-insurance]].

### [ ] AL09 — AI review 11 + lộ trình luyện phỏng vấn
- **Note:** `notes/advanced/al09-ai-review11.md` + cập nhật `00-INDEX.md`. Tổng kết; **lộ trình luyện phỏng vấn AI-DE** (4 tuần: concept → coding → system-design → mock); tổng hợp mọi mock/exercise; tổng kết 11 batch.

---
*Hết batch → sinh batch AI tiếp (ngành mới, mock/exercise mới, đào sâu kỹ thuật) — vẫn ưu tiên AI/LLM.*
