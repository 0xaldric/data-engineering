# J03 — Case: Energy / Utility / Smart Meter Platform

> Smart meter đọc điện/nước/gas theo interval → billing + grid analytics. Time-series khổng lồ. Khung [[c01-system-design-framework]], gần [[c04-case-iot]].

## 1. Requirements
- **Functional**: thu đọc đồng hồ (interval 15'/30'/1h), billing theo usage, demand forecast, grid monitoring, anomaly (rò rỉ/trộm điện), demand response.
- **Scale**: triệu meter × đọc mỗi 15' = hàng tỉ điểm/ngày.
- **Latency**: grid monitoring near-real-time; billing batch; forecast batch.
- **Đặc thù**: **interval data** (time-series đều), out-of-order (meter offline gửi bù), billing chính xác, đọc thiếu (gap-fill).

## 2. Kiến trúc
```
Smart meters ──(AMI network)──► meter readings ──► Kafka/ingest
        │
        ▼
   BRONZE: raw readings (partition by dt/region)
        │ validate (VEE: Validation/Estimation/Editing), gap-fill, dedup
        ▼
   SILVER: clean interval data (đọc thiếu → ước lượng)
        │ rollup (15' → hourly → daily → monthly)
        ▼
   GOLD: 
     - billing (usage per meter per kỳ)
     - load profile, demand forecast features
     - anomaly (consumption bất thường = rò rỉ/trộm)
        │
        ▼
   billing run + grid dashboard + ML (forecast, anomaly detection)
```

## 3. ⭐ VEE (Validation, Estimation, Editing) — đặc thù utility
Đọc đồng hồ không hoàn hảo (meter lỗi, mất kết nối) → quy trình chuẩn ngành:
- **Validation**: đọc hợp lệ? (trong range, không âm, không nhảy vọt).
- **Estimation**: đọc **thiếu** → ước lượng (gap-fill: nội suy, dùng cùng kỳ trước, profile) — billing cần giá trị đầy đủ. Carry-forward/interpolation ([[h01-sql-interview-5]] LOCF, [[i01-sql-interview-6]]).
- **Editing**: sửa đọc sai có kiểm soát + audit.
→ Cân bằng chính xác billing vs dữ liệu thực tế thiếu.

## 4. Interval data & rollup
- Time-series đều (interval cố định) → rollup phân cấp (15' → giờ → ngày → tháng) cho billing & lịch sử dài, tiết kiệm storage ([[c04-case-iot]] downsample).
- Out-of-order (meter offline rồi gửi bù) → event time + cho phép recompute partition.
- Semi-additive (consumption cộng được theo thời gian; nhưng "công suất tức thời" thì last/avg) ([[19-fact-types]]).

## 5. Phân tích
- **Load profile** (mẫu tiêu thụ theo giờ/mùa), **peak demand**.
- **Demand forecast** (ML) → cân bằng lưới, mua điện.
- **Anomaly**: consumption giảm đột ngột (meter hỏng) hoặc bất thường (trộm điện, rò rỉ nước) — detection ([[62-observability]]).
- **Demand response**: khuyến khích giảm tải giờ cao điểm.

## 6. DQ & observability
- Meter ngừng gửi (freshness per meter — gap detection ở scale triệu meter).
- Đọc thiếu % (cần VEE), giá trị bất thường.
- Billing reconciliation (tổng usage khớp grid input?).

## Câu hỏi đào sâu
- "Đọc đồng hồ thiếu, billing sao?" → VEE: ước lượng (interpolation/profile) + audit; billing cần giá trị đầy đủ.
- "Tỉ điểm/ngày lưu rẻ?" → rollup phân cấp + partition + tiered storage.
- "Phát hiện trộm điện?" → anomaly consumption (giảm bất thường vs profile lịch sử).

## ✅ "Tự mò"
🔭 Tạo interval readings (meter_id, ts, kwh) có vài đọc thiếu (NULL); gap-fill bằng interpolation/carry-forward; rollup 15'→hourly→daily; anomaly = consumption lệch >X% so trung bình.

➡️ Tiếp: [[j04-case-govtech]].
