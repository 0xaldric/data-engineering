# AG04 — AI Observability sâu: Drift Detection ⭐ (có code chạy được)

> Hệ AI **"im lặng hỏng"**: không có exception, chỉ chất lượng tụt dần khi phân phối đổi. Phải **chủ động đo drift**. Code: [`drift_detect.py`](../../projects/06-ai-data-engineering/drift_detect.py). Liên hệ [[ab06-llm-observability]], [[aa10-llmops]], [[af07-continuous-eval]].

## Vì sao drift nguy hiểm (im lặng hỏng)
- Code lỗi → exception → biết ngay. AI drift → **không lỗi**, chỉ tệ dần → biết khi user bỏ đi.
- Phân phối câu hỏi/đdata production **dịch chuyển** theo thời gian (mùa, sản phẩm mới, hành vi đổi) → model/RAG gặp input lạ → kém.
- → Quan sát AI phải đo **drift**, không chỉ uptime/latency.

## ⭐ 4 loại drift trong hệ AI
| Loại | Là gì | Đo bằng |
|------|-------|---------|
| **Input drift** | câu hỏi/đầu vào đổi phân phối | embedding centroid dịch (code này) |
| **Embedding drift** | vector phân phối đổi (đổi model/data) | so phân phối vector |
| **Output drift** | phân phối câu trả lời/nhãn đổi | thống kê output (độ dài, nhãn) |
| **Quality/concept drift** | "đúng" đổi nghĩa (tài liệu cũ, khái niệm mới) | eval định kỳ tụt ([[af07-continuous-eval]]) |

## ⭐ Đo input drift bằng centroid (code chạy)
```
batch tham chiếu (lúc build) ─> centroid_ref (vector trung bình)
batch mới ─> centroid_new
drift = 1 - cosine(centroid_ref, centroid_new)   (cao = phân phối dịch xa)
```
Kết quả thật:
```
ngưỡng drift = 0.15
batch CÙNG chủ đề (DE)        drift=0.076 -> OK (ổn định)
batch LẠ chủ đề (nấu ăn/bóng đá) drift=0.201 -> ⚠️ DRIFT!
```
→ Câu hỏi vẫn về DE → drift thấp; câu hỏi lạ hẳn → drift cao → cảnh báo. Centroid dịch = phân phối input đã đổi.

## ⭐ Calibrate ngưỡng (bài học lặp lại)
- Cùng phân phối **vẫn có drift > 0** (embedding nhiễu, mẫu hữu hạn) → ngưỡng phải **trên mức nhiễu nền**.
- Thử auto-calibrate bằng split-half tham chiếu → **không tin cậy ở N nhỏ** (centroid mẫu nhỏ bất ổn, nhiễu nền bị thổi phồng).
- → Production: calibrate ngưỡng từ **lịch sử batch-to-batch** (đủ mẫu), không hardcode mò. Cùng tinh thần calibrate grounding ([[aa02-guardrails]]) và TOL ([[af07-continuous-eval]]).

## Phương pháp drift khác (ngoài centroid)
- **Population Stability Index (PSI)** / KL divergence: so phân phối feature cũ vs mới (DE cổ điển).
- **KS test**: so phân phối 2 mẫu (số liệu).
- **Outlier rate**: % câu hỏi xa mọi cluster đã biết (out-of-distribution).
- **Eval tụt**: drift gián tiếp lộ qua recall/faithfulness giảm ([[af07-continuous-eval]]).

## ⭐ Khi phát hiện drift → làm gì
```
DRIFT phát hiện ─> 1. re-eval golden (chất lượng có tụt thật?)
                ─> 2. mở rộng KB/golden theo chủ đề mới ([[ac06-kb-freshness]])
                ─> 3. cân nhắc re-index / fine-tune / đổi model
                ─> 4. cảnh báo team (alert [[ab06-llm-observability]])
```
→ Drift là **tín hiệu sớm** để hành động trước khi user phàn nàn.

## Cạm bẫy
- **Không đo drift** → im lặng hỏng → chủ động đo định kỳ.
- **Ngưỡng quá chặt** → false-alarm liên tục (nhiễu nền) → calibrate trên baseline.
- **Centroid mẫu nhỏ** → bất ổn → batch đủ lớn.
- **Chỉ đo input, quên quality** → input ổn nhưng "đúng" đổi (concept drift) → kết hợp eval.
- **Phát hiện mà không hành động** → alert vô dụng → gắn playbook (re-eval/re-index).
- **Centroid che mất multi-modal** → 2 cụm tách ra, centroid không đổi → xét cả phân phối, không chỉ trung bình.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao drift = "im lặng hỏng" (không exception).
- [ ] 4 loại drift (input/embedding/output/concept).
- [ ] Đo input drift bằng centroid cosine; calibrate ngưỡng trên nhiễu nền.
- [ ] PSI/KL/KS/outlier rate; drift lộ qua eval tụt.
- [ ] Hành động khi drift: re-eval, mở rộng KB, re-index, alert.
- 🔭 Tự mò: chạy `drift_detect.py` rồi thêm batch thứ 3 "DE pha trộn" (1 nửa DE + 1 nửa lạ) → xem drift nằm giữa; thử đo **outlier rate** thay centroid: với mỗi câu mới, cosine tới câu tham chiếu gần nhất < ngưỡng = outlier; đếm % outlier như tín hiệu drift bổ sung.

➡️ Tiếp [[ag05-agent-platform]] — nền tảng data cho agent.
