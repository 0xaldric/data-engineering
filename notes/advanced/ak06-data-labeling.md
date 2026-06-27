# AK06 — Data Labeling & Annotation Infrastructure ⭐ (có code chạy được)

> Nhãn là **nhiên liệu** của AI có giám sát (training/eval/preference). Hạ tầng gán nhãn + QC chất lượng (Cohen's kappa) quyết định data tốt hay rác. Code: [`annotation_agreement.py`](../../projects/06-ai-data-engineering/annotation_agreement.py). Liên hệ [[ag03-rlhf-preference-data]], [[ae03-training-data-quality]].

## Vì sao gán nhãn là hạ tầng quan trọng
- Model học từ nhãn → **nhãn rác = model rác** (garbage in, garbage out).
- Gán nhãn **đắt + chậm + chủ quan** → cần quy trình + QC, không phó mặc.
- DE xây: pipeline gán nhãn, đo chất lượng, kết hợp người + AI.

## ⭐ Đo chất lượng nhãn: Inter-annotator Agreement
Nhiều người gán cùng mẫu → đo **đồng thuận**. Nhưng accuracy thô đánh lừa (đoán bừa cũng "đúng" theo tỉ lệ) → dùng **Cohen's kappa** (trừ may rủi):
```
κ = (po - pe) / (1 - pe)
   po = đồng thuận quan sát ; pe = đồng thuận do MAY RỦI (theo phân phối nhãn)
κ = 1: hoàn hảo ; κ = 0: chỉ bằng may rủi ; κ < 0: tệ hơn ngẫu nhiên
```
Thang Landis-Koch: <0.2 kém · 0.2-0.4 tạm · 0.4-0.6 khá · 0.6-0.8 tốt · >0.8 rất tốt.

## ⭐ Kết quả thật (code chạy) — kappa lộ annotator ẩu
```
A ↔ B: kappa=+0.63 (tốt)        <- 2 người cẩn thận đồng thuận thật
A ↔ C: kappa=+0.00 (kém)        <- C vô dụng
C vs gold: kappa=+0.00 | accuracy THÔ=33%   <- C gán "bil" mọi mẫu (lười/bias)
```
→ ⭐ **Bài học**: C "đúng 33%" theo accuracy thô (nhờ đoán bừa 1 nhãn), nhưng **kappa ~0** vạch trần = không đóng góp gì hơn may rủi. **Accuracy thô giấu annotator ẩu; kappa lộ ra.** Đây là lý do dùng kappa, không phải accuracy.

## ⭐ Kỹ thuật hạ tầng gán nhãn
| Kỹ thuật | Ý tưởng |
|----------|---------|
| **Guideline rõ** | tiêu chí "đúng" cụ thể → giảm chủ quan, tăng kappa |
| **Gold questions** | chèn mẫu biết đáp án → bắt annotator ẩu (như C) |
| **Đa annotator + majority** | nhiều người/mẫu → vote, đo agreement |
| **Active learning** | model chọn mẫu **đáng gán nhất** (mơ hồ nhất) → gán ít mà hiệu quả |
| **Weak supervision** | nhãn tự động từ rule/heuristic (nhiễu) → nhiều nhãn rẻ (Snorkel) |
| **AI pre-label + human verify** | LLM gán trước → người sửa (nhanh hơn gán từ đầu) |

## ⭐ Active learning (gán thông minh)
```
nhãn ít -> train model -> model CHỌN mẫu nó KHÔNG CHẮC nhất (gần ranh giới)
   -> người gán những mẫu đó (đáng giá nhất) -> train lại -> lặp
-> đạt chất lượng với ÍT nhãn hơn nhiều so với gán ngẫu nhiên
```
→ Gán nhãn là tài nguyên đắt → ưu tiên mẫu **giảm bất định nhiều nhất**.

## Cạm bẫy
- **Đo accuracy thô** → annotator bias/ẩu lọt (như C) → Cohen's kappa.
- **Guideline mơ hồ** → kappa thấp → làm rõ tiêu chí + ví dụ.
- **1 annotator/mẫu** → không đo được agreement → đa annotator mẫu kiểm.
- **Không gold question** → không bắt được người ẩu → chèn gold.
- **AI pre-label tin mù** → người không sửa → vẫn phải verify (AI sai).
- **Weak supervision nhiễu vào thẳng** → nhãn rác → khử nhiễu/đo.
- **Bỏ active learning** → gán bừa tốn → ưu tiên mẫu mơ hồ.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao nhãn = nhiên liệu; gán nhãn cần QC.
- [ ] Cohen's kappa = đồng thuận TRỪ may rủi; vì sao hơn accuracy thô.
- [ ] ⭐ Kappa lộ annotator ẩu (C: acc 33% nhưng kappa 0).
- [ ] Kỹ thuật: guideline/gold/majority/active-learning/weak-sup/AI-prelabel.
- [ ] Active learning: gán mẫu mơ hồ nhất (hiệu quả).
- [ ] Cạm bẫy: accuracy thô, guideline mơ hồ, không gold.
- 🔭 Tự mò: sửa `annotation_agreement.py` — thêm annotator D "ngẫu nhiên" (đổi vài nhãn theo index), tính kappa; thêm **Fleiss' kappa** (cho >2 annotator cùng lúc); thử "majority vote" 3 người làm gold mới, đo mỗi người vs majority.

➡️ Tiếp [[ak07-kg-construction]] — dựng knowledge graph bằng LLM.
