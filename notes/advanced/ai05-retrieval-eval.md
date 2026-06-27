# AI05 — Retrieval Eval sâu (đo chất lượng RAG)

> "Làm sao biết pipeline truy xuất trả kết quả tốt?" — câu hỏi phỏng vấn AI-era, thực chất là **data quality mặc áo mới**. Đã triển khai trong [[ai02-rag-capstone-writeup]] (rag_over_notes.py).

## Vì sao phải đo (không "chạy là xong")
RAG có thể "chạy" mà trả chunk rác → LLM trả lời sai. Phải **đo chất lượng retrieval** bằng số, không cảm tính. Đây là precision/recall của DE áp vào embedding.

## Cần một GOLDEN SET (như test data)
Tập `(query, tài liệu/chunk đúng kỳ vọng)` — nhãn thủ công hoặc từ click log. Là "test data" cho retrieval. Capstone dùng 8 cặp (query → mảnh tên note đúng). Càng nhiều/đa dạng càng tin cậy.

## ⭐ Các metric retrieval
| Metric | Đo gì | Công thức (ý) |
|--------|-------|----------------|
| **recall@k** | tài liệu đúng có trong top-k không | hit / tổng query |
| **precision@k** | trong top-k bao nhiêu % đúng | #đúng / k |
| **MRR** (Mean Reciprocal Rank) | tài liệu đúng nằm hạng nào (1/rank) | avg(1/rank của hit đầu) |
| **nDCG@k** | xếp hạng tốt không (đúng ở đầu > cuối) | DCG/IDCG, có giảm log theo rank |
| **Hit rate** | có ít nhất 1 đúng trong top-k | = recall@k (binary) |

Kết quả capstone (đo thật): **recall@5=88%, MRR=0.542, nDCG@5=0.853**.
- recall cao = thường tìm được; MRR 0.54 = tài liệu đúng trung bình ở ~hạng 2; nDCG 0.85 = xếp hạng khá tốt.
- Diễn giải: MRR thấp hơn recall → đôi khi đúng nhưng không ở top → cần **re-ranking**.

## Snippet (đã thêm vào capstone)
```python
rels = [1 if expect in n.lower() else 0 for n in df["note"]]   # relevance theo rank
rr   = next((1/i for i,r in enumerate(rels,1) if r), 0)         # MRR
ndcg = sum(r/math.log2(i+1) for i,r in enumerate(rels,1))       # DCG (IDCG=1 vì 1 doc đúng)
```

## Re-ranking (tăng MRR/nDCG)
Retrieval (bi-encoder, nhanh) lấy top-N rộng → **cross-encoder re-rank** top-N → top-k chính xác hơn (đắt nên chỉ chấm top-N). Đẩy tài liệu đúng lên đầu → MRR/nDCG tăng. Cũng có RRF (Reciprocal Rank Fusion) gộp vector + keyword ([[k05-vector-rag-deep]] hybrid).

## ⭐ Eval phần GENERATION (RAG end-to-end)
Retrieval đúng chưa đủ — LLM có dùng đúng không:
- **Faithfulness/groundedness**: trả lời có **bám tài liệu** retrieved không (không bịa)?
- **Answer relevance**: trả lời có đúng câu hỏi?
- **Context precision/recall**: chunk retrieved có liên quan?
- Công cụ: **RAGAS**, hoặc **LLM-as-judge** (dùng LLM chấm). Đây là test cho output non-deterministic ([[ai07-testing-nondeterministic]]).

## Đưa eval vào pipeline (như CI cho data)
- Chạy eval trên golden set **mỗi lần đổi** (chunk size/model/index) → regression test cho RAG.
- Theo dõi metric theo thời gian (drift): model/tài liệu đổi → recall tụt → alert (observability — [[k07-observability-tooling]]).
- A/B: so chunk size / model / hybrid weight bằng recall@k → chọn bằng SỐ ([[ai03-chunking]]).

## ⚠️ Cạm bẫy
- Không golden set → không đo được, chỉ "cảm thấy ổn".
- Chỉ recall, bỏ MRR/nDCG → đúng nhưng ở hạng 10 (LLM không thấy vì chỉ lấy top-k).
- Golden set quá nhỏ/lệch → metric không tin cậy.
- Eval retrieval mà quên eval generation (LLM bịa dù chunk đúng).
- Không re-run eval khi đổi cấu hình → regression âm thầm.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Phân biệt recall@k / MRR / nDCG; vì sao MRR thấp → cần re-rank.
- [ ] Golden set là "test data cho retrieval".
- [ ] Eval generation (faithfulness) khác eval retrieval.
- 🔭 Chạy `rag_over_notes.py`, thêm 3–5 cặp golden của bạn, xem metric đổi; thử tắt hybrid (`hybrid=False`) so recall.

➡️ Tiếp: [[ai06-llm-output-governance]] (gap quan trọng).
