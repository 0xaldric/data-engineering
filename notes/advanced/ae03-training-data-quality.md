# AE03 — Data Quality cho LLM Training Data ⭐ (có code chạy được)

> Train tốt = data sạch. Chấm CHẤT LƯỢNG từng mẫu theo **nhiều chiều**, lọc rác trước khi train. "Garbage in, garbage out" áp tuyệt đối cho LLM. Code: [`data_quality_score.py`](../../projects/06-ai-data-engineering/data_quality_score.py). Liên hệ [[aa04-training-data-prep]], [[ab01-synthetic-data]], [[ab08-finetune-pipeline]].

## Vì sao DQ quyết định kết quả train
- Model học **đúng những gì bạn cho** → data trùng/độc/rác → model trùng/độc/rác.
- 1000 mẫu sạch > 100000 mẫu bẩn: **chất > lượng** với training data.
- DQ là chỗ **DE tạo giá trị** trong vòng đời AI (model có sẵn, data là biến quyết định).

## ⭐ Các chiều chất lượng
| Chiều | Đo gì | Loại |
|-------|-------|------|
| **Format** | không rỗng, đúng schema (chat template) | 🔴 hard |
| **Duplicate** | không trùng/near-dup (MinHash/Jaccard [[aa04-training-data-prep]]) | 🔴 hard |
| **Toxic/safety** | không nội dung độc hại | 🔴 hard |
| **Decontamination** | không trùng test/benchmark ([[ab08-finetune-pipeline]]) | 🔴 hard |
| **PII** | không lộ thông tin cá nhân ([[ad03-privacy-compliance]]) | 🔴 hard |
| **Length** | độ dài hợp lý (không quá ngắn/dài) | 🟡 soft |
| **Diversity** | từ vựng phong phú (không lặp khuôn — mode collapse [[ab01-synthetic-data]]) | 🟡 soft |
| **Language** | đúng ngôn ngữ mục tiêu | 🟡 soft |

## ⭐⭐ Bài học code: HARD GATE vs trung bình (đừng để trung bình "cứu" rác)
Lần đầu mình tính **trung bình mọi chiều** → ngưỡng 0.8 → mẫu **toxic/trùng vẫn lọt** (chỉ rớt 1/5 chiều = 0.8). **SAI!** Mẫu độc/trùng phải bị **loại tuyệt đối**, không trung bình:
```
HARD gate (rỗng/trùng/toxic/PII/decontaminate): rớt 1 -> LOẠI NGAY
SOFT score (length/diversity/language): tính điểm, phải ≥ ngưỡng
keep = pass ALL hard gates AND soft_score ≥ ngưỡng
```
Kết quả thật sau khi sửa:
```
#1,#2,#7 GIỮ ✓        #3 'ok' BỎ (soft 0.50 ngắn)
#4 BỎ (TRÙNG)         #5 'data data...' BỎ (soft 0.54 lặp)
#6 BỎ (TOXIC)         #8 '' BỎ (rỗng)
-> giữ 3/8, bỏ 5
```
→ **Nguyên tắc**: chiều nghiêm trọng = gate nhị phân; chiều mức độ = điểm. Trộn lẫn = lỗ hổng cho rác/độc lọt.

## Pipeline DQ trong fine-tune workflow
```
raw data ─> [score mỗi mẫu: hard gates + soft] ─> lọc dưới ngưỡng
   ─> [dedup toàn tập] ([[aa04-training-data-prep]]) ─> [decontaminate vs test]
   ─> [balance nhãn] ([[ab01-synthetic-data]]) ─> [version dataset] ([[ab08-finetune-pipeline]])
   ─> data sạch sẵn sàng train
   (log: bao nhiêu bỏ vì lý do gì -> minh bạch, không cắt thầm lặng)
```

## Đo & báo cáo (đừng cắt thầm lặng)
- **Tỉ lệ giữ/bỏ + lý do** (bao nhiêu vì toxic, trùng, ngắn...) → minh bạch.
- **Phân phối trước/sau** (độ dài, nhãn, ngôn ngữ) → lọc có làm lệch không?
- **Spot-check** mẫu bị bỏ → ngưỡng có quá tay (bỏ nhầm mẫu tốt)?
- DQ cho training = **data observability** ([[ab06-llm-observability]]) áp cho dataset.

## Cạm bẫy
- **Trung bình mọi chiều** → toxic/trùng lọt → dùng hard gate cho chiều nghiêm trọng.
- **Quên decontamination** → test rò vào train → eval ảo ([[ab08-finetune-pipeline]]).
- **Ngưỡng quá tay** → bỏ nhầm mẫu tốt → spot-check + đo phân phối.
- **Lọc làm lệch phân phối** (bỏ hết lớp hiếm) → model thiên lệch.
- **Cắt thầm lặng** (không log lý do) → không ai biết data bị xén gì.
- **Chỉ đo bề mặt** (length) bỏ qua ngữ nghĩa (đúng/sai, độc) → cần nhiều chiều.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao DQ quyết định train (chất > lượng).
- [ ] Các chiều: hard (format/dup/toxic/decontam/PII) vs soft (length/diversity/language).
- [ ] ⭐ Hard gate vs trung bình — vì sao trung bình để rác/độc lọt.
- [ ] Pipeline DQ trong fine-tune; log lý do bỏ (minh bạch).
- [ ] Cạm bẫy: quên decontaminate, lọc làm lệch phân phối, cắt thầm.
- 🔭 Tự mò: thêm vào `data_quality_score.py` chiều **language** (heuristic: tỉ lệ ký tự tiếng Việt có dấu) để bắt mẫu #7 (tiếng Anh); thêm **decontamination** (so với 1 "test set" bịa); in báo cáo "bỏ vì lý do gì" dạng bảng đếm.

➡️ Tiếp [[ae04-multimodal-rag]] — multimodal RAG sâu.
