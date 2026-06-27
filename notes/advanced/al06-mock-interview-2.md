# AL06 — AI-DE Mock Interview 2 (đề + lời giải đầy đủ)

> Mock phỏng vấn 2: system-design **agent + safety** + khái niệm vận hành + behavioral. Kèm lời giải + thang chấm. Liên hệ [[ah03-red-teaming]], [[ag04-drift-detection]], [[al01-mock-interview-1]].

---
## 🎯 Phần 1 — System Design (35 phút)
**Đề:** "Thiết kế AI agent tự động xử lý email khách hàng: đọc → phân loại → soạn trả lời / tạo ticket / chuyển người. Agent có tool (đọc CRM, tạo ticket, gửi mail). Đảm bảo an toàn."

**Lời giải mẫu** (khung 7 bước + nhấn safety):
1. **Clarify**: agent làm gì (đọc/phân loại/trả lời/tạo ticket), quyền hành động, khối lượng, hậu quả sai (gửi mail sai/ticket rác).
2. **Data flow**: email → parse → phân loại intent ([[ae06-query-understanding]]) → RAG context (chính sách + lịch sử khách).
3. **Agent + tool**: tool qua **registry có scope/quyền** ([[ag05-agent-platform]]); đọc CRM (read) vs gửi mail/tạo ticket (write, rủi ro hơn).
4. **⭐ SAFETY (trọng tâm)**:
   - **Indirect injection**: email = nguồn KHÔNG tin → lệnh độc giấu trong email ([[ad04-llm-security]]); quét + tách data/instruction.
   - **Least privilege**: agent chỉ tool tối thiểu; **hành động không hồi phục (gửi mail/hoàn tiền) → human approve**.
   - Validate output trước gửi ([[ai06-llm-output-governance]]); guardrail PII ([[aa02-guardrails]]).
5. **Eval**: task success rate, % escalate đúng, LLM-judge chất lượng trả lời ([[ad02-llm-judge]]); red-team email độc ([[ah03-red-teaming]]).
6. **Scale/state**: checkpoint mỗi bước (resume [[ad07-agent-data]]); run store replay; budget cap chống loop.
7. **Observe**: trace mọi tool-call + audit ([[ab06-llm-observability]]).

**Thang chấm:** ⭐ nhận ra **email = nguồn không tin → indirect injection** + **hành động nguy hiểm cần human approve** = pass. Quên safety/least-privilege = fail (agent có quyền = rủi ro lớn).

---
## 🎯 Phần 2 — Câu hỏi vận hành (20 phút)

**Q1. Hệ AI "im lặng hỏng" — phát hiện sao?**
> Drift detection: input drift (phân phối câu hỏi đổi — centroid embedding [[ag04-drift-detection]]), quality drift (eval tụt [[af07-continuous-eval]]). Im lặng hỏng = không exception, chỉ tệ dần → chủ động đo + alert. Hành động: re-eval, mở rộng KB, re-index.

**Q2. Chuẩn bị data cho RLHF/fine-tune?**
> Preference pairs (chosen/rejected) từ human/RLAIF/implicit; QC: Cohen's kappa ([[ak06-data-labeling]]), gold question, guideline; clean/dedup/**decontaminate** ([[ab08-finetune-pipeline]]); version dataset; coi chừng reward hacking + annotator bias ([[ag03-rlhf-preference-data]]).

**Q3. Vector DB scale lên tỉ vector — đổi gì?**
> ANN (HNSW/IVF) thay brute-force; **quantization** (PQ/binary giảm RAM — binary giữ recall tốt [[aj04-nextgen-vector]]); DiskANN (vector trên SSD vượt RAM [[af04-vector-db-internals]]); sharding + replication; filtered search trong-duyệt; nén-lọc-thô → rerank vector gốc.

**Q4. "Eval-driven development" cho AI là gì?**
> Eval trước, code sau (TDD cho LLM): golden = spec, mọi đổi qua gate, regression CI ([[ac03-eval-driven-dev]], [[af07-continuous-eval]]). Golden lớn dần theo bug. Đo bằng số, không vibe. Continuous gate chặn merge khi recall tụt.

---
## 🎯 Phần 3 — Behavioral (10 phút)
**Đề:** "Kể về lần bạn cân bằng giữa tốc độ giao hàng và chất lượng/an toàn."
> **STAR mẫu**: *S* — agent xử lý email cần ra nhanh. *T* — nhưng rủi ro gửi mail sai. *A* — đặt **human approve cho hành động không hồi phục**, tự động phần đọc/phân loại; đo task success + % escalate. *R* — giao được phần lớn tự động mà 0 sự cố gửi sai. *Bài học*: tự động cái an toàn, người duyệt cái rủi ro — không all-or-nothing.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Giải system-design agent trong 35', nhấn safety sớm.
- [ ] Trả 4 câu vận hành không nhìn đáp án.
- [ ] Kể 1 STAR về cân bằng tốc độ ⇄ an toàn.
- 🔭 Tự mò: với đề agent email, liệt kê mọi tool agent cần + gán scope (read/write/dangerous) + cái nào cần human approve — đó là "threat model" của agent (phần interviewer ấn tượng nhất).

➡️ Tiếp [[al07-coding-exercises-2]] — bài tập governance/guardrails.
