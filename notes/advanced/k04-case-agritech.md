# K04 — Case: AgriTech / Precision Farming Platform

> Cảm biến nông nghiệp + ảnh vệ tinh/drone → tối ưu canh tác. IoT + geospatial + image. Khung [[c01-system-design-framework]]. Gần [[c04-case-iot]].

## 1. Requirements
- **Functional**: thu cảm biến (độ ẩm đất, nhiệt độ, thời tiết, drone/satellite imagery), yield prediction (dự đoán năng suất), irrigation optimization (tưới tối ưu), pest/disease detection, recommendation canh tác.
- **Scale**: nhiều cánh đồng × nhiều cảm biến × imagery lớn (ảnh nặng).
- **Latency**: alert (sâu bệnh/thiếu nước) ~giờ; analytics/forecast batch theo mùa vụ.
- **Đặc thù**: **đa dạng dữ liệu** (time-series sensor + image + weather + geospatial), kết nối kém (cánh đồng xa), theo mùa vụ.

## 2. Kiến trúc
```
Field sensors (soil/weather) ──► IoT gateway (edge, buffer offline) ──► Kafka/ingest
Drone/Satellite imagery ──► object storage (ảnh raw, lớn)
Weather API (external) ──► ingest
        │
        ▼
   BRONZE: sensor readings (time-series) + imagery (S3) + weather
        │  align theo field/geo + time
        ▼
   SILVER: clean sensor, rollup; imagery processed (NDVI index từ ảnh — vegetation health)
        │
        ▼
   GOLD: field health, yield features, irrigation schedule
        │
        ▼
   ML (yield prediction, disease detection từ ảnh) + dashboard + alert
```

## 3. ⭐ Đa dạng dữ liệu (đặc thù)
- **Time-series sensor** (như IoT — [[c04-case-iot]]): độ ẩm/nhiệt theo interval; out-of-order (kết nối kém), gap-fill, rollup.
- **Imagery** (drone/satellite): ảnh lớn → object storage; xử lý thành **index** (NDVI = chỉ số sức khoẻ cây từ phổ ảnh) → giảm về dạng bảng/feature. DE quản pipeline ảnh→feature (không tự làm CV, nhưng orchestrate).
- **Weather** (external API): tích hợp dự báo + lịch sử → feature.
- **Geospatial**: field boundaries, zone-level (chia cánh đồng thành ô).

## 4. Bài toán phân tích/ML
- **Yield prediction**: features từ sensor + NDVI + weather + lịch sử → model (feature pipeline — [[c09-case-recsys]], point-in-time).
- **Irrigation optimization**: độ ẩm đất + dự báo mưa → lịch tưới.
- **Pest/disease detection**: anomaly trên NDVI/ảnh → alert.
- Mùa vụ: dữ liệu theo crop cycle (so sánh năm/vụ).

## 5. Tech & failure
- Edge buffer (cánh đồng mất mạng → gửi bù, out-of-order).
- Imagery lớn → object storage + xử lý batch (Spark + CV pipeline orchestrate).
- Downsample sensor; tiered retention.

## 6. DQ & observability
- Sensor freshness (cảm biến chết giữa đồng → gap detection).
- Imagery completeness (drone flight đủ coverage?).
- Weather data align đúng field/time.

## Câu hỏi đào sâu
- "Tích hợp sensor + ảnh + weather?" → align theo field+time; ảnh→feature (NDVI); time-series rollup; weather join.
- "Yield prediction data?" → feature pipeline point-in-time (không dùng data sau thời điểm dự đoán).
- "Cánh đồng mất mạng?" → edge buffer + out-of-order + recompute.

## ✅ "Tự mò"
🔭 Thiết kế schema: sensor_readings (field_id, zone, ts, metric, value) + imagery_features (field_id, date, ndvi) + weather; query field health (avg NDVI + soil moisture) theo zone/tuần; alert khi NDVI giảm bất thường.

➡️ Tiếp: [[k05-vector-rag-deep]].
