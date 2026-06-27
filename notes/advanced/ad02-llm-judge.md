# AD02 — LLM-as-Judge Tự Động ⭐ (có code chạy được)

> Dùng một "judge" chấm điểm câu trả lời **tự động** (thay vì người chấm tay) để eval ở quy mô lớn. Mạnh nhưng **đầy bias** — phải biết và calibrate. Code: [`llm_judge.py`](../../projects/06-ai-data-engineering/llm_judge.py). Sâu hơn [[aa06-llm-eval]], [[ac03-eval-driven-dev]].

## Vì sao cần LLM-judge
- Eval LLM khó: "câu trả lời này tốt không?" không có đáp án nhị phân ([[ai07-testing-nondeterministic]]).
- Người chấm: **chính xác nhưng chậm + đắt + không scale** (nghìn câu mỗi lần đổi prompt).
- → Dùng **LLM mạnh làm giám khảo** chấm theo rubric → tự động, nhanh, rẻ → chạy mỗi lần đổi (CI gate [[ac03-eval-driven-dev]]).

## ⭐ 2 kiểu chấm
| Kiểu | Cách | Khi dùng |
|------|------|----------|
| **Pointwise** | chấm 1 câu theo rubric → điểm/nhãn | đo tuyệt đối, theo dõi theo thời gian |
| **Pairwise** | so A vs B → cái nào tốt hơn | so 2 model/prompt; **ổn định hơn** (so sánh dễ hơn chấm tuyệt đối) |
→ Pairwise thường **đáng tin hơn** vì LLM so sánh tốt hơn cho điểm tuyệt đối.

## ⭐ Rubric — chấm theo tiêu chí rõ
Đừng hỏi "tốt không?" chung chung → cho **rubric**:
```
- Grounding/faithfulness: có bám nguồn/đúng sự thật? (cosine với reference hoặc context)
- Coverage/completeness: trả đủ ý cần?
- Relevance: đúng câu hỏi?
- Conciseness: gọn, không lan man?
```
Code minh hoạ (mock): `score = 0.6*grounding + 0.4*coverage` (grounding = cosine với reference, coverage = từ khoá bắt buộc).

## ⭐ Kết quả thật (code chạy)
```
GOOD    grounding=0.939 coverage=100% -> 0.964 (25 từ)
VERBOSE grounding=0.759 coverage=25%  -> 0.555 (46 từ)   <- dài mà rỗng
Pairwise: Winner = GOOD
```
→ Câu **ngắn-gọn-đúng** thắng câu **dài-lê-thê-rỗng**. Đúng cái ta muốn judge làm.

## ⭐⭐ Bias của LLM-judge (PHẢI biết — đây là phần quan trọng nhất)
| Bias | Là gì | Chống |
|------|-------|-------|
| **Length** | thiên vị câu **dài** (tưởng dài = đầy đủ) | length-control; phạt lan man; chuẩn hoá |
| **Position** | thiên vị câu đặt **trước** (A hơn B chỉ vì đứng đầu) | **test swap** A↔B, lấy trung bình 2 chiều |
| **Self-preference** | thích văn của **chính model mình** | dùng judge khác model bị chấm; calibrate |
| **Verbosity/sycophancy** | thích giọng tự tin/nịnh | rubric chặt, ví dụ neo |
| **Format** | thiên vị markdown/bullet đẹp | chuẩn hoá format trước chấm |
Code có check: VERBOSE dài hơn (46>25 từ) **không** thắng → rubric không length-biased; đổi chỗ A/B điểm bất biến → không position-biased.

## ⭐ Calibrate judge (bắt buộc trước khi tin)
```
1. Lấy ~50 mẫu CÓ NHÃN NGƯỜI (vàng).
2. Cho judge chấm cùng 50 mẫu.
3. Đo tương quan judge vs người (agreement / correlation).
4. Tương quan thấp -> sửa rubric / đổi judge / thêm ví dụ neo -> lặp.
5. Đủ cao mới dùng judge tự động ở scale; vẫn human spot-check định kỳ.
```
→ Judge **chưa calibrate = không tin được**. "Judge cũng cần được eval."

## Trong pipeline (LLMOps)
```
đổi prompt/model ─> chạy golden ─> LLM-judge chấm ─> điểm ≥ ngưỡng? 
   PASS -> merge        FAIL -> chặn        (regression gate [[ac03-eval-driven-dev]])
   + lưu điểm theo thời gian -> phát hiện quality drift ([[aa10-llmops]])
```

## Cạm bẫy
- **Tin judge mù** (không calibrate) → tối ưu theo điểm sai → model tệ đi mà tưởng tốt.
- **Bỏ qua bias** → length/position/self-pref bóp méo kết quả.
- **Judge = model bị chấm** → self-preference → dùng model khác làm judge.
- **Rubric mơ hồ** → điểm nhiễu → rubric cụ thể + ví dụ neo (few-shot).
- **Chỉ judge tự động, bỏ người** → trôi dạt âm thầm → giữ human spot-check.
- **Judge đắt/chậm** (LLM lớn cho mọi mẫu) → sample + cache; judge nhỏ cho sàng lọc.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao cần LLM-judge (người không scale).
- [ ] Pointwise vs pairwise; vì sao pairwise ổn định hơn.
- [ ] Rubric theo tiêu chí (grounding/coverage/relevance/conciseness).
- [ ] 5 bias (length/position/self-pref/verbosity/format) + cách chống.
- [ ] Calibrate judge với nhãn người trước khi tin.
- 🔭 Tự mò: sửa `llm_judge.py` — cố ý làm `score` **thiên vị độ dài** (cộng điểm theo số từ) rồi xem VERBOSE thắng oan thế nào → thấy length bias bằng mắt; thêm chấm **pairwise có swap** (chấm (A,B) và (B,A), cảnh báo nếu kết quả khác nhau = position bias).

➡️ Tiếp [[ad03-privacy-compliance]] — privacy & compliance cho LLM.
