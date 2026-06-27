# AE01 — Self-Correcting / Self-Improving RAG ⭐ (có code chạy được)

> RAG **tự đánh giá** retrieval của chính nó; nếu yếu/không tự tin → **tự viết lại query** rồi thử lại → giữ kết quả tốt hơn. Một dạng agent tự sửa. Code: [`self_correcting_rag.py`](../../projects/06-ai-data-engineering/self_correcting_rag.py). Liên hệ [[aa03-rag-production]], [[aa05-agentic-pipelines]], [[ae06-query-understanding]].

## Vì sao cần
- Retrieval **không phải lúc nào cũng trúng** ngay lần đầu: câu hỏi cộc lốc, mơ hồ, từ viết tắt → kéo về note chung chung/sai.
- RAG "1 phát" không biết mình vừa trượt → đưa context tệ cho LLM → trả lời tệ.
- → Cho RAG **tự nhìn lại**: "retrieval này có đủ tốt không? chưa → thử cách khác." Giống người tìm không ra thì đổi từ khoá.

## ⭐ Vòng self-correction
```
query ─> retrieve ─> ĐO confidence (điểm top / có doc liên quan?)
   ├─ đủ tự tin (≥ ngưỡng) ─> DÙNG
   └─ thấp ─> REFORMULATE query (mở rộng / HyDE / đổi từ) ─> retry
              ─> tốt hơn? giữ bản mới : giữ bản gốc
   (lặp tối đa N lần -> tránh loop vô tận)
```

## ⭐ Các cách reformulate
| Cách | Làm gì |
|------|--------|
| **Query expansion** | thêm đồng nghĩa/từ liên quan ("EOS" → "exactly once semantics kafka") |
| **HyDE** (Hypothetical Doc Embedding) | LLM sinh **giả thuyết câu trả lời** rồi embed *nó* thay câu hỏi → khớp chunk khai báo tốt hơn |
| **Decompose** | câu phức → nhiều câu con, retrieve từng cái ([[ae06-query-understanding]]) |
| **Step-back** | hỏi câu tổng quát hơn để lấy bối cảnh trước |
→ **HyDE** mạnh vì: doc trong corpus là câu **khai báo** ("Shuffle đắt vì..."), còn câu hỏi cộc lốc ("shuffle?") embed lệch; giả thuyết-trả-lời cùng "giọng khai báo" → gần doc hơn.

## ⭐ Kết quả thật (code chạy)
Ngưỡng tự tin 0.75; câu cộc lốc → tự sửa bằng HyDE:
```
'EOS'        0.643 (kafka-internals) -> 0.808 (kafka-qa)        +0.165 ✓
'SCD'        0.704 (b08-explain chung) -> 0.821 (18-scd ĐÚNG)   +0.117 ✓
'RAG đánh giá'0.620 (vector-rag chung) -> 0.812 (ai05-retrieval ĐÚNG) +0.192 ✓
confidence trung bình: 0.656 -> 0.814 (+0.158)
```
→ Câu cộc lốc kéo note **chung chung**; viết lại thành giả-thuyết-trả-lời kéo đúng **note cụ thể** lên top. Tự sửa = thắng thật, đo được.

## ⭐ Tự đánh giá bằng gì (confidence signal)
- **Điểm retrieval top** (đã dùng): top < ngưỡng → nghi ngờ.
- **Khoảng cách top-1 vs top-2**: sát nhau → mơ hồ.
- **LLM tự chấm**: "context này có đủ trả lời câu hỏi không?" (grounding [[aa02-guardrails]]).
- **Không có doc nào ≥ ngưỡng** → thừa nhận "không biết" thay vì bịa (chống hallucinate).

## ⚠️ Điều kiện DỪNG (bắt buộc — chống loop & cost)
- **Max retries** (vd 2–3): không cải thiện sau N lần → dừng, trả tốt nhất có / "không tìm thấy".
- **Chỉ giữ khi THỰC SỰ tốt hơn** (đo, không đoán) — reformulate có thể làm tệ đi.
- Mỗi vòng = thêm LLM/embedding call → **cost & latency tăng** ([[ac08-ai-cost-scale]]) → đừng sửa vô hạn.

## Liên hệ — đây là agentic pattern
Self-correction = **ReAct/reflection** thu nhỏ ([[aa05-agentic-pipelines]]): hành động (retrieve) → quan sát (đo) → suy nghĩ (đủ chưa?) → hành động lại. Cùng cần guardrail: max-steps, budget, đo trước khi tin.

## Cạm bẫy
- **Loop vô tận** (sửa mãi không tốt hơn) → max retries + điều kiện dừng.
- **Giữ bản reformulate mù** (không đo) → có thể tệ hơn bản gốc → luôn so điểm.
- **Reformulate đắt** mỗi câu → chỉ kích hoạt khi confidence thấp, không phải mọi câu.
- **Ngưỡng sai**: cao quá → sửa cả câu đã ổn (tốn); thấp quá → bỏ qua câu yếu → calibrate ([[ac03-eval-driven-dev]]).
- **Không có "tôi không biết"** → ép trả lời từ context tệ → hallucinate; phải cho phép thừa nhận trượt.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vòng self-correction: retrieve → đo → reformulate → retry → giữ tốt hơn.
- [ ] 4 cách reformulate; vì sao HyDE mạnh (giọng khai báo khớp doc).
- [ ] Confidence signal (điểm top, gap top1-top2, LLM tự chấm).
- [ ] Điều kiện dừng: max retries + chỉ giữ khi đo thấy tốt hơn.
- [ ] Liên hệ agentic reflection; cost mỗi vòng.
- 🔭 Tự mò: sửa `self_correcting_rag.py` — thêm **vòng lặp 2 bước** (nếu HyDE vẫn < ngưỡng → thử query expansion), max_retries=2; thêm trường hợp câu đã tốt sẵn (≥0.75) để thấy nó KHÔNG sửa; log số lần sửa + "cost" (số lần retrieve) để thấy đánh đổi.

➡️ Tiếp [[ae02-graphrag-build]] — dựng knowledge graph từ wikilinks.
