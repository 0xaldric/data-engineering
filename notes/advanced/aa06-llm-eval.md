# AA06 — LLM Evaluation Frameworks (RAGAS sâu)

> Đo chất lượng hệ LLM/RAG **end-to-end** (không chỉ retrieval — [[ai05-retrieval-eval]]). "Không đo được thì không cải thiện được" — càng đúng với LLM non-deterministic.

## Vì sao eval LLM khó
- Output **non-deterministic** (exact-match vô dụng — [[ai07-testing-nondeterministic]]).
- "Đúng" mơ hồ (nhiều câu trả lời đúng, đúng một phần, đúng nhưng bịa nguồn).
- Cần đo cả **retrieval** lẫn **generation**.

## ⭐ RAGAS metrics (cho RAG)
Bộ metric chuẩn, mỗi cái đo một khía cạnh (thường dùng LLM-as-judge để chấm):
| Metric | Đo gì | Câu hỏi |
|--------|-------|---------|
| **Faithfulness** | trả lời có bám context (không bịa) | "câu trả lời có suy ra được từ context không?" |
| **Answer relevance** | trả lời có đúng câu hỏi | "có lạc đề không?" |
| **Context precision** | chunk retrieved có liên quan (đầu danh sách) | "rác trong top-k không?" |
| **Context recall** | retrieved có đủ thông tin cần | "thiếu chunk quan trọng không?" |
→ Phân tách: retrieval kém (context recall thấp) vs generation kém (faithfulness thấp) → biết sửa đâu.

## Eval harness (quy trình)
```
golden dataset (question, ground-truth answer/context)
   │
chạy hệ RAG → (retrieved context, generated answer)
   │
chấm bằng: metric tự động (recall@k, RAGAS) + LLM-judge + human (sample)
   │
báo cáo + so version (prompt/model/chunk) → chọn cấu hình tốt nhất
```

## Golden dataset — xây thế nào
- Thủ công (chuyên gia viết question + answer đúng).
- Sinh bằng LLM (sinh câu hỏi từ tài liệu) + người review.
- Từ **production feedback** (câu hỏi thật + câu trả lời được đánh giá tốt).
- Cần **đa dạng** (dễ/khó, đơn/multi-hop, edge case) + đủ lớn để tin cậy.

## ⭐ LLM-as-judge (+ bias cần biết)
Dùng LLM (mạnh) chấm output LLM khác. Rẻ + scale hơn human. **Nhưng bias**:
- **Position bias** (thiên vị câu đầu/cuối) → đảo thứ tự, lấy trung bình.
- **Verbosity bias** (thích câu dài) → kiểm soát.
- **Self-preference** (thiên vị output cùng model) → dùng judge khác model.
- **Calibrate** judge với human labels (judge có khớp người không?).

## Eval offline vs online
- **Offline**: trên golden set, trước deploy (regression). Nhanh, lặp lại.
- **Online**: production thật — feedback người dùng (thumbs up/down, click, có dùng câu trả lời không), A/B test. Bắt cái offline bỏ sót (offline ≠ phân phối thật).

## Regression suite (như CI cho data)
- Eval chạy **mỗi lần đổi** prompt/model/chunk/index → bắt regression ([[aa07-prompt-management]]).
- Metric tụt → chặn deploy (gate, như dbt test — [[i06-dq-framework]]).
- Track theo thời gian (drift).

## Cấu trúc đo (gắn cả khoá)
LLM eval = **data quality cho output AI**: golden set (test data), metric (DQ dimension), threshold gate (DQ gate), drift monitor (observability). Cùng tư duy [[60-data-quality]], chỉ đối tượng là output LLM.

## ⚠️ Cạm bẫy
- Chỉ eval retrieval, quên generation (chunk đúng nhưng LLM bịa).
- Golden set nhỏ/lệch → metric không tin cậy.
- Tin LLM-judge mù (bias) → calibrate với human.
- Offline tốt nhưng online tệ (phân phối khác) → cần cả hai.
- Không regression khi đổi prompt → tụt chất lượng âm thầm.
- "Vibe check" thủ công thay metric → không scale, không reproduce.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 4 RAGAS metric + chúng tách retrieval vs generation thế nào.
- [ ] Xây golden dataset (nguồn + đa dạng).
- [ ] LLM-judge bias (position/verbosity/self-preference) + calibrate.
- [ ] Offline vs online; regression suite.
- 🔭 Mở rộng golden set của `rag_over_notes.py` thành (question, expected answer); tự chấm faithfulness thủ công vài câu (answer có trong note retrieved không).

➡️ Tiếp: [[aa07-prompt-management]].
