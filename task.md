# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 20 script).

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

**Batch hiện tại:** #32 — AI-Advanced 9: Frontier & Capstone Integration ⭐
**Nguồn:** đào sâu AI/LLM — frontier + tích hợp + vertical case studies

---

## BATCH HIỆN TẠI

### [x] AJ01 — Reasoning Models & Process Supervision Data
- **Note:** `notes/advanced/aj01-reasoning-models.md`. Model suy luận (o1-style, chain-of-thought): data cho reasoning — process supervision (chấm từng BƯỚC suy luận, không chỉ đáp án cuối), CoT dataset, verifier/PRM (process reward model), test-time compute. Vai trò DE: thu/chấm reasoning traces, token nhiều ([[ah04-tokenization]]). Liên hệ [[ag03-rlhf-preference-data]].

### [x] AJ02 — AI Alignment & Safety (sâu)
- **Note:** `notes/advanced/aj02-ai-alignment.md`. Căn chỉnh model theo giá trị con người: RLHF → Constitutional AI (AI tự phê theo "hiến pháp"), refusal/safety training, helpfulness vs harmlessness trade-off, jailbreak resistance, value alignment. Vai trò DE: data alignment + red-team ([[ah03-red-teaming]]). Liên hệ [[ag03-rlhf-preference-data]], [[ad04-llm-security]].

### [x] AJ03 — Capstone Integration: AI Data Product ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/aj03-capstone-integration.md` + code `ai_product.py`. Ghép các script thành 1 LUỒNG hoàn chỉnh: câu hỏi → guardrail ([[aa02-guardrails]]) → semantic cache ([[ad08-semantic-cache]]) → retrieve ([[ai02-rag-capstone-writeup]]) → (mock generate) → validate ([[ai06-llm-output-governance]]) → log trace mỗi tầng. Chạy vài câu, in hành trình mỗi câu (cache hit? chặn? quarantine?). Đây là "AI data product" thu nhỏ — portfolio mạnh nhất ([[ad09-ai-review4]]).

### [x] AJ04 — Next-gen Vector Search: Matryoshka & Binary Quant ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/aj04-nextgen-vector.md` + code `vector_compression.py`. Kỹ thuật mới: Matryoshka embedding (cắt chiều 384→128→64 vẫn dùng được), binary quantization (mỗi chiều→1 bit, Hamming distance). Code: trên capstone, cắt chiều + binary-quantize vector, đo recall@5 vs full → thấy trade-off RAM/recall thật. Sâu hơn [[af04-vector-db-internals]], [[ab07-vector-search-opt]].

### [ ] AJ05 — Case Study: Healthcare AI Data Platform
- **Note:** `notes/advanced/aj05-case-healthcare-ai.md`. RAG/AI cho y tế: privacy cực cao (PHI/HIPAA — [[ad03-privacy-compliance]]), không được bịa (an toàn bệnh nhân — [[ag02-hallucination-detection]]), citation bắt buộc, human-in-loop bác sĩ, audit, self-host. Nhấn: an toàn + privacy + grounding tuyệt đối.

### [ ] AJ06 — Case Study: Financial/Trading AI Data
- **Note:** `notes/advanced/aj06-case-finance-ai.md`. AI cho tài chính: real-time (giá/giao dịch), compliance/audit nghiêm, point-in-time chống leakage ([[ac07-feature-store]]), LLM bổ trợ không tự quyết tiền ([[ad04-llm-security]] excessive agency), explainability (giải trình quyết định). Nhấn: real-time + compliance + explainability.

### [ ] AJ07 — LLM Data Flywheel (vòng cải tiến)
- **Note:** `notes/advanced/aj07-data-flywheel.md`. Vòng tự cải tiến: usage → log (feedback/👍👎) → data mới → eval/fine-tune → model tốt hơn → usage nhiều hơn. DE xây flywheel: thu signal, lọc, đưa vào golden/training ([[ag03-rlhf-preference-data]]), đo cải tiến ([[af07-continuous-eval]]). "Data tốt → model tốt → data tốt hơn".

### [ ] AJ08 — Prompt Optimization (tự động)
- **Note:** `notes/advanced/aj08-prompt-optimization.md`. Tối ưu prompt bằng DATA thay tay: DSPy (compile prompt từ ví dụ + metric), automatic prompt optimization, few-shot example selection (chọn ví dụ tốt nhất từ pool), bootstrap. Vai trò DE: cung cấp ví dụ + metric để tối ưu. Liên hệ [[aa07-prompt-management]], [[ac03-eval-driven-dev]].

### [ ] AJ09 — AI review 9 + grand finale Module AI
- **Note:** `notes/advanced/aj09-ai-review9.md` + cập nhật `00-INDEX.md`. Tổng kết AI-Advanced 9; **grand finale toàn Module AI** (9 batch): bản đồ tổng, 22 script, "ngày 1 đi làm AI-DE" checklist, lời kết hành trình.

---
*Hết batch → sinh batch AI tiếp (vertical case studies mới, AI infra sâu hơn, data engineering cho AGI-era, hoặc đào sâu trục yếu) — vẫn ưu tiên AI/LLM.*
