# AL01 — AI-DE Mock Interview 1 (đề + lời giải đầy đủ)

> Mock phỏng vấn AI Data Engineer hoàn chỉnh: system-design + khái niệm + behavioral, **kèm lời giải mẫu + thang chấm**. Tự che đáp án, trả lời, rồi đối chiếu. Liên hệ [[af09-ai-review6]], [[ac09-ai-review3]], [[h07-mock-interview]].

---
## 🎯 Phần 1 — System Design (35 phút)
**Đề:** "Thiết kế hệ RAG hỏi-đáp tài liệu nội bộ cho công ty 5000 nhân viên: nhiều nguồn (Confluence, Drive, Slack), **có phân quyền** (mỗi người chỉ thấy tài liệu được phép), tài liệu cập nhật hàng ngày. Vẽ kiến trúc, nêu quyết định then chốt."

**Lời giải mẫu** (theo khung 7 bước [[af09-ai-review6]]):
1. **Clarify**: ai dùng (nhân viên), quyền theo phòng/dự án, freshness cần (giờ), có PII không (có — lương/HR), quy mô (triệu doc). Thước đo: recall, % rò quyền = 0, deflection.
2. **Data flow**: connector mỗi nguồn (giữ **ACL gốc** + updated_at) → parse → chunk structure-aware → embed → vector store (chunk + ACL + source + version).
3. **Retrieve**: ⭐ **permission-aware** — pre-filter ACL theo `user.groups` ([[af02-case-enterprise-kb]]) → hybrid (vector+keyword) → rerank.
4. **Safety**: chỉ đưa doc được phép VÀO context (không lọc ở output); citation; PII redact trước log ([[ad03-privacy-compliance]]).
5. **Eval**: golden có test quyền (user X KHÔNG thấy doc Y) + recall + faithfulness; continuous gate ([[af07-continuous-eval]]).
6. **Scale**: vector DB filtered search (Qdrant [[af04-vector-db-internals]]); incremental theo hash/CDC ([[ad01-streaming-rag]]); freshness mỗi nguồn 1 nhịp.
7. **Cost**: semantic cache (theo user!) + model routing ([[ac08-ai-cost-scale]]).

**Thang chấm:** ⭐ nhận ra **permission-aware retrieval** là cốt lõi (pre-filter ACL, an toàn > tiện) = pass. Nhắc freshness đa nguồn + incremental = tốt. Quên quyền/rò chéo = fail (đây là điểm sống còn).

---
## 🎯 Phần 2 — Câu hỏi khái niệm (20 phút)

**Q1. RAG eval thế nào? Đo gì?**
> Golden set (query, doc đúng) → recall@k (doc lọt context?), MRR/nDCG (thứ hạng). nDCG chia IDCG ∈[0,1]. RAG cho LLM đọc → ưu tiên **recall@k**. Đo bằng harness, sweep config ([[ab02-rag-eval-harness]]). Bonus: faithfulness (RAGAS) cho generation.

**Q2. Output LLM thỉnh thoảng sai format/độc. Đưa vào downstream sao cho an toàn?**
> Coi output = **dữ liệu không tin được** → data contract: schema validate (pydantic) → repair → quarantine → provenance ([[ai06-llm-output-governance]]). + guardrail input/output ([[aa02-guardrails]]). Hành động nguy hiểm → sandbox + human approve.

**Q3. Phát hiện hallucination kiểu gì?**
> Grounding (bám context? cosine/NLI), self-consistency (hỏi N lần lệch nhau = bịa — nhưng so FACT không so cosine [[ag02-hallucination-detection]]), citation check (nguồn có thật?). Mitigate: RAG, "không chắc → từ chối", citation bắt buộc.

**Q4. Cost LLM tăng gấp 5. Điều tra + giảm?**
> Observability dashboard token/cost theo feature/model ([[ab06-llm-observability]]) → tìm chỗ đốt. Giảm: semantic cache ([[ad08-semantic-cache]]), routing/cascade (model nhỏ trước), nén prompt, batch embedding, giới hạn output token, budget cap ([[ac08-ai-cost-scale]]).

---
## 🎯 Phần 3 — Behavioral (STAR, 10 phút)
**Đề:** "Kể về lần bạn phát hiện một giả định/mặc định sai trong hệ thống."
> **Lời giải mẫu (STAR)**: *Situation* — RAG dùng query-prefix theo khuyến nghị model. *Task* — recall thấp hơn kỳ vọng. *Action* — viết benchmark ablation prefix on/off ([[ah02-embedding-benchmark]]). *Result* — phát hiện prefix-OFF tốt hơn 13% (88% vs 75%) vì corpus tiếng Việt; sửa lại. *Bài học*: **đo trên data thật, không tin mặc định**. → kể được "đo bằng số + sửa dựa bằng chứng" = mạnh.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Tự giải system-design trong 35' (vẽ + nói), đối chiếu thang chấm.
- [ ] Trả 4 câu khái niệm không nhìn đáp án.
- [ ] Kể 1 STAR thật của mình theo mẫu.
- 🔭 Tự mò: ghi âm mình trả lời phần 1 trong 35 phút, nghe lại — có nói rõ "permission-aware là cốt lõi" trong 5 phút đầu không? (interviewer cần nghe insight chính SỚM).

➡️ Tiếp [[al02-coding-exercises-1]] — bài tập code AI-DE.
