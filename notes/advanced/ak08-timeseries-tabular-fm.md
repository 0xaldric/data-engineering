# AK08 — Time-series & Tabular Foundation Models

> Foundation model không chỉ cho text/ảnh — đang lan sang dữ liệu **CÓ CẤU TRÚC**: time-series (forecast zero-shot) và tabular. Sân nhà của DE gặp "FM hoá". Liên hệ [[ac07-feature-store]], [[ak05-case-manufacturing-ai]], [[c04-case-iot]].

## Vì sao FM cho dữ liệu có cấu trúc
- LLM bùng nổ với text → ý tưởng "pre-train lớn rồi zero-shot" lan sang chuỗi/bảng.
- Hứa hẹn: **forecast/predict không cần train riêng mỗi dataset** (zero-shot/few-shot).
- DE quan tâm: time-series (sensor/giao dịch/metric) và tabular (bảng) là **data chủ đạo** của DE.

## ⭐ Time-series Foundation Models
| Model | Ý tưởng |
|-------|---------|
| **TimeGPT, Chronos, Moirai, TimesFM** | pre-train trên KHỐI LỚN chuỗi đa lĩnh vực → forecast chuỗi MỚI zero-shot |
```
truyền thống: mỗi chuỗi -> train model riêng (ARIMA/Prophet/LSTM)
TS-FM: 1 model pre-trained -> đưa chuỗi mới -> forecast NGAY (không train)
   (Chronos: "token hoá" giá trị chuỗi -> như LLM cho số)
```
- **Khi nào dùng**: nhiều chuỗi, cần forecast nhanh không train từng cái (cold-start chuỗi mới).
- **Đổi lại**: chuỗi đặc thù mạnh (mùa vụ riêng) → model train riêng vẫn có thể hơn.

## ⭐ Tabular Foundation Models
| Model | Ý tưởng |
|-------|---------|
| **TabPFN** | pre-train trên data tabular tổng hợp → predict bảng nhỏ zero-shot (in-context) |
| **LLM cho tabular** | serialize hàng → text ("tuổi=30, thu nhập=…") → LLM predict/giải thích |
```
LLM cho tabular: bảng -> text -> LLM
   + zero/few-shot, giải thích được, xử lý cột text/thiếu linh hoạt
   - đắt (token [[ah04-tokenization]]), kém model cây (XGBoost) trên data lớn dạng số
```
→ Tabular truyền thống **XGBoost/cây vẫn vua** trên data lớn dạng số. FM/LLM mạnh ở: data nhỏ, cột hỗn hợp (text+số), cần giải thích, few-shot.

## ⭐ Khi nào FM vs truyền thống (quyết định)
```
data LỚN, thuần số, ổn định    -> model truyền thống (XGBoost/ARIMA) — mạnh, rẻ
data NHỎ / chuỗi mới / few-shot -> FM (zero-shot, không cần train)
cần GIẢI THÍCH / cột text       -> LLM cho tabular
nhiều chuỗi forecast nhanh      -> TS-FM (không train từng cái)
```
→ Đừng "FM mọi thứ" — truyền thống thường thắng trên data có cấu trúc lớn. FM cho cold-start/few-shot/giải thích.

## Vai trò DE
- **Chuẩn bị data**: time-series (resample/align), tabular (clean/encode) — vẫn DE cổ điển ([[ac07-feature-store]]).
- **Serialize cho LLM**: bảng → text đúng format (point-in-time! [[ac07-feature-store]]).
- **Eval FM vs baseline**: đo FM có hơn XGBoost/ARIMA không (đừng tin hype — [[ah02-embedding-benchmark]] "đo đừng tin mặc định").
- **Cost**: FM/LLM đắt hơn cây ([[ah04-tokenization]]) → cân chất lượng vs cost.

## Cạm bẫy
- **FM mọi thứ** → truyền thống thắng trên data số lớn → đo, chọn đúng công cụ.
- **Tin zero-shot mù** → chuỗi đặc thù FM kém → so baseline.
- **LLM cho tabular data lớn** → đắt + kém cây → dùng cho nhỏ/giải thích.
- **Serialize quên point-in-time** → leakage ([[ac07-feature-store]]).
- **Bỏ qua cost token** tabular/chuỗi dài → đắt → ước trước.
- **Không eval vs baseline** → không biết FM có đáng → luôn so XGBoost/ARIMA.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao FM lan sang time-series/tabular (zero-shot, không train từng cái).
- [ ] TS-FM (Chronos/TimeGPT): forecast chuỗi mới zero-shot.
- [ ] Tabular: TabPFN + LLM-serialize; cây (XGBoost) vẫn vua data số lớn.
- [ ] Khi nào FM (nhỏ/cold-start/giải thích) vs truyền thống (lớn/số/ổn định).
- [ ] DE: chuẩn bị data + serialize + eval vs baseline + cost.
- 🔭 Tự mò: lấy 1 chuỗi số nhỏ, forecast bằng "naive" (lặp giá trị cuối) + "trung bình trượt" làm baseline; serialize chuỗi thành text ("1,2,3,...") đưa vào LLM (nếu có) xin dự đoán tiếp → so với baseline; nhận ra với data đơn giản, baseline thường đủ — FM cho ca khó.

➡️ Tiếp [[ak09-ai-review10]] — review 10 + tổng kết vertical.
