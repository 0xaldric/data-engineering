# AI07 — Testing Dữ liệu Non-deterministic ⭐⭐

> **Gap quan trọng**: test hệ thống mà cùng input cho **khác output** mỗi lần. Exact-match (như ETL) vô dụng. Code chạy được: [`test_semantic.py`](../../projects/06-ai-data-engineering/test_semantic.py).

## Vì sao test ETL không áp được
| Test ETL (tất định) | Test output LLM (non-deterministic) |
|---------------------|--------------------------------------|
| `assert output == expected` (exact) | exact-match **luôn FAIL** (khác chữ mỗi lần) |
| row count khớp | số dòng có thể khác |
| schema giữ vững | format có thể trôi |
→ Cùng câu hỏi, LLM trả "Shuffle tốn network I/O" lần này, "Shuffle đắt do truyền dữ liệu qua mạng" lần sau — **cùng nghĩa, khác chữ**. Phải test **ngữ nghĩa**, không phải chữ.

## ⭐ Chiến lược test cho output non-deterministic
### 1. Semantic equivalence (cosine) — cốt lõi
So **tương đương ngữ nghĩa** bằng embedding: cosine(reference, candidate) ≥ ngưỡng → coi là "đúng".
```python
sim = cosine(embed(reference), embed(candidate))
assert sim >= 0.80   # "khác chữ cùng nghĩa" pass; "khác nghĩa" fail
```
Demo chạy thật (5 cặp): "khác chữ cùng nghĩa" cos **0.84/0.87/0.82 → PASS**; "khác nghĩa" cos **0.57/0.56 → FAIL đúng**. Tất cả exact-match=F → ETL test sẽ trượt hết, semantic test đúng 5/5.

### 2. Schema/format validation (phần tất định)
Output có cấu trúc (JSON) → kiểm format/schema **vẫn deterministic** được: parse được không, đủ field, đúng kiểu/range (pydantic — [[ai06-llm-output-governance]]). Demo: 4/4 (valid JSON pass, confidence>1/thiếu field/non-JSON fail).

### 3. Golden set + ngưỡng
Tập `(input, output kỳ vọng/tham chiếu)` do người chuẩn bị. Chạy LLM → so semantic với reference. Là "test data" cho hệ non-deterministic ([[ai05-retrieval-eval]] golden set).

### 4. Statistical / distribution test
Không test từng dòng (non-det) mà test **tổng thể**: phân phối nhãn có hợp lý (vd không phải 90% "other")? % quarantine < ngưỡng? độ dài output trong khoảng? → phát hiện model "lệch" mà không cần exact-match.

### 5. Property-based / invariant
Kiểm **tính chất** thay vì giá trị: "summary luôn ngắn hơn input", "confidence ∈ [0,1]", "extracted entities là tập con của input". Đúng dù output khác nhau.

### 6. LLM-as-judge (cho generation)
Dùng một LLM chấm output LLM khác: "câu trả lời này có bám tài liệu không (faithfulness)?" → điểm. Đắt nhưng bắt được cái cosine bỏ sót (RAGAS — [[ai05-retrieval-eval]]).

### 7. Snapshot + human review
Lưu output, sample cho người duyệt định kỳ (như review label — staff DE ở fintech dành nhiều thời gian cho cái này). Bắt lỗi tinh vi mà tự động bỏ sót.

## Đưa vào CI/pipeline
- Golden set semantic test chạy **mỗi lần đổi** (prompt/model/chunk) → regression test cho hệ AI.
- Ngưỡng cosine + % quarantine làm **gate** (như DQ gate — [[i06-dq-framework]]).
- Theo dõi metric theo thời gian (drift) → alert.

## ⚠️ Cạm bẫy
- Dùng exact-match cho output LLM → fail giả khắp nơi (hoặc tệ hơn: bỏ test luôn).
- Ngưỡng cosine quá cao → reject câu đúng; quá thấp → chấp nhận câu sai. Phải **calibrate** trên golden set.
- Chỉ semantic, bỏ schema validation (JSON hỏng vẫn lọt).
- Test 1 lần, không re-run khi đổi model/prompt (regression âm thầm).
- Tin một metric duy nhất (cosine có thể "đồng nghĩa bề mặt" mà sai chi tiết) → kết hợp nhiều cách.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao exact-match vô dụng cho output LLM.
- [ ] 7 chiến lược: semantic/schema/golden/statistical/property/LLM-judge/snapshot.
- [ ] Calibrate ngưỡng cosine trên golden set.
- 🔭 Chạy `python projects/06-ai-data-engineering/test_semantic.py`; thêm cặp "cùng nghĩa khác chữ" của bạn; chỉnh `THRESHOLD` xem case nào đổi pass/fail → cảm nhận calibration.

➡️ Tiếp: [[ai08-ai-cost-latency]].
