# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 26 script).

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

**Batch hiện tại:** #37 — AI-Advanced 14: Capstone Build & Production Ops ⭐
**Nguồn:** đào sâu AI/LLM — dựng sản phẩm + vận hành + portfolio

---

## BATCH HIỆN TẠI

### [ ] AO01 — Capstone Build Guide: Thiết kế & Dựng AI Data Product
- **Note:** `notes/advanced/ao01-capstone-build-guide.md`. Hướng dẫn DỰNG 1 AI data product hoàn chỉnh từ con số 0, dùng 26 script như component: requirements → kiến trúc → ingest/index → route → retrieve → generate → guardrail → validate → eval → observe. Map mỗi bước → script đã có. "Từ ý tưởng tới sản phẩm chạy được". Liên hệ [[aj03-capstone-integration]], [[af09-ai-review6]].

### [ ] AO02 — Portfolio Packaging + Smoke Test ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ao02-portfolio-packaging.md` + code `smoke_test.py`. Đóng gói portfolio: smoke-test chạy các script chính báo PASS/FAIL (CI cho portfolio), README template, cách trình bày GitHub, pitch. Code: `smoke_test.py` chạy thử N script không cần mạng, đếm pass/fail, exit code. Liên hệ [[ae09-ai-review5]], [[af07-continuous-eval]].

### [ ] AO03 — AI Evaluation at Scale
- **Note:** `notes/advanced/ao03-eval-at-scale.md`. Eval khi nhiều model/prompt/version: eval dataset management (version golden, mở rộng), LLM-judge fleet (nhiều judge song song), eval CI/CD, human-in-loop eval sampling, cost của eval. Sâu hơn [[ab02-rag-eval-harness]], [[ad02-llm-judge]], [[af07-continuous-eval]].

### [ ] AO04 — Production Incident Response cho AI
- **Note:** `notes/advanced/ao04-incident-response.md`. Khi hệ AI HỎNG ở production: phân loại sự cố (chất lượng tụt/cost spike/rò PII/hallucination lan/model API down), playbook xử lý, rollback (model/prompt/index — [[aa07-prompt-management]]), kill switch, postmortem. SRE cho AI ([[f02-reliability-sre]]). Liên hệ [[ag04-drift-detection]], [[ab06-llm-observability]].

### [ ] AO05 — Case Study: Real Estate/PropTech AI
- **Note:** `notes/advanced/ao05-case-realestate-ai.md`. AI bất động sản: định giá (model + giải thích), search nhà (multimodal ảnh + mô tả [[ae04-multimodal-rag]]), chatbot tư vấn, RAG pháp lý/hợp đồng. Nhấn: định giá explainable, multimodal, đa ngữ, point-in-time (giá thị trường). Liên hệ [[k03-case-realestate]].

### [ ] AO06 — Case Study: Retail (Omnichannel) AI
- **Note:** `notes/advanced/ao06-case-retail-ai.md`. AI bán lẻ đa kênh (online+cửa hàng): dự báo tồn kho ([[ak08-timeseries-tabular-fm]]), reco đa kênh, planogram, chatbot, computer vision cửa hàng (kệ/khách). Nhấn: hợp nhất data online+offline, real-time tồn kho, edge cửa hàng. Liên hệ [[ak01-case-ecommerce-ai]].

### [ ] AO07 — AI-DE Mock Interview 4 (đề + lời giải đầy đủ)
- **Note:** `notes/advanced/ao07-mock-interview-4.md`. Mock cuối tổng hợp: 1 system-design lớn (AI platform đa năng) + 5 câu rải mọi chủ đề + 1 behavioral + câu hỏi NGƯỢC (hỏi interviewer gì). Đề + lời giải + thang chấm. Liên hệ [[al01-mock-interview-1]], [[an07-mock-interview-3]].

### [ ] AO08 — AI-DE Coding Exercises 5 (bài tập + lời giải)
- **Note:** `notes/advanced/ao08-coding-exercises-5.md`. 5 bài tổng hợp khó hơn có đề + lời giải + reasoning: end-to-end mini RAG, eval harness từ đầu, guardrail pipeline, incremental dedup, drift detector. Dạng take-home. Liên hệ [[al02-coding-exercises-1]], [[am08-coding-exercises-3]].

### [ ] AO09 — AI review 14 + Graduation & What Next
- **Note:** `notes/advanced/ao09-ai-review14.md` + cập nhật `00-INDEX.md`. Tổng kết; **"tốt nghiệp" AI-DE**: bạn đã có gì, tự đánh giá năng lực, what-next (chuyên sâu/rộng/thực chiến), duy trì học khi field tiến. Tổng kết 14 batch.

---
*Hết batch → sinh batch AI tiếp (đào sâu/ngành mới/luyện tập) — vẫn ưu tiên AI/LLM.*
