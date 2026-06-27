# AJ01 — Reasoning Models & Process Supervision Data

> Model "suy luận" (o1-style): nghĩ từng bước (chain-of-thought) trước khi trả lời. Cần data đặc thù — chấm **từng BƯỚC** suy luận, không chỉ đáp án cuối. Liên hệ [[ag03-rlhf-preference-data]], [[ah04-tokenization]], [[ae03-training-data-quality]].

## Reasoning model khác gì model thường
- Model thường: prompt → đáp án (1 phát).
- Reasoning model: prompt → **chuỗi suy luận dài** (nháp, thử, tự sửa) → đáp án.
- Mạnh ở: toán, code, logic nhiều bước (nơi 1-phát hay sai).
- Đổi lại: **token nhiều hơn nhiều** (nghĩ dài) → đắt + chậm ([[ah04-tokenization]], [[ah07-inference-optimization]]).

## ⭐ Test-time compute (ý tưởng cốt lõi)
```
thay vì model TO hơn -> cho model NGHĨ LÂU hơn lúc inference
   "nghĩ" = sinh nhiều bước/nhiều nhánh -> chọn đường tốt
-> đánh đổi: compute lúc CHẠY (không phải lúc train) đổi lấy chất lượng
```
→ Càng cho nghĩ lâu (nhiều token reasoning) → càng đúng (tới giới hạn). Một trục scale mới: **scale test-time**, không chỉ scale model/data.

## ⭐⭐ Process supervision vs Outcome supervision (data cốt lõi)
```
OUTCOME: chỉ chấm ĐÁP ÁN CUỐI đúng/sai
   -> model có thể đúng đáp án bằng lý luận SAI (ăn may) -> học bậy
PROCESS: chấm TỪNG BƯỚC suy luận đúng/sai
   -> thưởng lý luận đúng từng bước -> reasoning chất lượng, ít ăn may
```
→ **Process supervision** (chấm từng bước) cho reasoning tốt hơn nhiều, nhưng **đắt** (phải gán nhãn mỗi bước). Đây là loại data mới DE phải thu/quản.

## ⭐ PRM (Process Reward Model) & verifier
```
PRM: model chấm điểm MỖI BƯỚC reasoning ("bước này hợp lý không?")
   -> dùng để: chọn nhánh tốt (search), train reasoning, lọc trace tốt
verifier: kiểm đáp án cuối (vd chạy code, kiểm toán học) -> reward chắc chắn
```
- DE chuẩn bị data train PRM: (bước reasoning, nhãn đúng/sai) — gán nhãn người hoặc tự động (verifier).
- Reasoning trace tốt → lọc giữ làm training data (self-improvement).

## Vai trò DE (data cho reasoning)
- **Thu reasoning traces**: prompt → chuỗi suy luận → đáp án + nhãn (đúng/sai mỗi bước hoặc cuối).
- **Verifier tự động**: toán (kiểm số), code (chạy test) → gán nhãn rẻ ở scale (không cần người mọi bước).
- **Lọc chất lượng**: trace dài, lặp, sai → lọc ([[ae03-training-data-quality]]); dedup.
- **Cost/token**: reasoning đốt token → ước cost ([[ah04-tokenization]]); lưu trace nặng.

## Cạm bẫy
- **Chỉ outcome supervision** → model học lý luận sai mà đúng đáp án (ăn may) → process supervision khi cần reasoning thật.
- **Gán nhãn từng bước thủ công** không scale → verifier tự động (toán/code) + người spot-check.
- **Trace rác** (lặp, lan man) vào training → lọc chất lượng.
- **Quên cost reasoning** → token gấp nhiều lần → ước + giới hạn độ dài nghĩ.
- **Reward hacking** ([[ag03-rlhf-preference-data]]) → model "giả vờ nghĩ" dài mà rỗng → đo chất lượng bước.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Reasoning model: nghĩ từng bước trước trả lời; mạnh ở toán/code/logic.
- [ ] Test-time compute: nghĩ lâu hơn đổi lấy đúng hơn (trục scale mới).
- [ ] ⭐ Process vs outcome supervision (chấm bước vs đáp án) — vì sao process tốt cho reasoning.
- [ ] PRM/verifier; DE thu trace + verifier tự động.
- [ ] Cạm bẫy: outcome ăn may, trace rác, cost token.
- 🔭 Tự mò: lấy 5 bài toán nhỏ, viết tay 2 "reasoning trace" mỗi bài (1 đúng từng bước, 1 sai 1 bước giữa nhưng đúng đáp án cuối) → gán nhãn process (mỗi bước) vs outcome (cuối) → thấy outcome bỏ lỡ trace "đúng đáp án lý luận sai". Đó là data process supervision.

➡️ Tiếp [[aj02-ai-alignment]] — alignment & safety.
