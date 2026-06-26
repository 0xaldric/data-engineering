# C05 — Case: Ride-sharing Data Platform (như Uber)

> Đặc trưng: geospatial, real-time pricing, trip lifecycle, nhiều bên (rider/driver). Áp [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: theo dõi trip (request→match→pickup→dropoff→pay), **surge pricing real-time** theo cung-cầu vùng, ETA, analytics (utilization, driver earnings, demand forecast).
- **Scale**: triệu trip/ngày, hàng trăm nghìn driver gửi vị trí mỗi vài giây → location ghi cực lớn.
- **Latency**: surge & matching ~giây; analytics batch.
- **Đặc thù**: **geospatial** (vùng/H3 hexagon), trip là **accumulating snapshot** (nhiều mốc thời gian).

## 2. Kiến trúc
```
Driver/Rider apps ──► Kafka: "locations" (high vol), "trip_events"
   │                       │
   │ hot path              ├──► Stream proc (Flink): demand/supply theo vùng (H3) trong cửa sổ
   │                       │       → surge multiplier (serving store) ──► pricing API
   │                       │       → ETA features
OLTP (trips, Postgres) ──CDC──► Kafka ──► lake
                                   ▼
                         S3 BRONZE → SILVER (trip fact accumulating snapshot) → GOLD
                                   ▼
                         dbt marts: utilization, earnings, demand by region/time
                         ML: demand forecast, ETA model (batch train, online serve)
```

## 3. Tech choices & trade-off
- **Geospatial indexing** (Uber **H3** hexagon / geohash): gom vị trí về vùng để tính cung-cầu & surge. Trade-off: độ phân giải hexagon vs chi phí.
- **Flink** cho surge/matching (stateful, windowed demand-supply per region, latency giây) ([[50-flink]]).
- **Accumulating snapshot** cho trip (request_ts→match_ts→pickup_ts→dropoff_ts + lag measures) ([[19-fact-types]]).
- **CDC** từ OLTP trips → lake (nguồn sự thật cho analytics) ([[51-cdc-debezium]]).
- Location stream: **không** lưu mọi điểm thô lâu dài → downsample/giữ ngắn hạn ([[c04-case-iot]] tương tự IoT).

## 4. Scale & failure
- Partition Kafka theo region/driver → scale ghi location.
- Hot region (sân bay giờ cao điểm) → skew; pre-aggregate theo H3.
- Surge serving store (Redis) — eventual consistency chấp nhận (giá cập nhật mỗi vài giây).
- Out-of-order location (mạng driver chập) → event time + watermark.

## 5. Analytics & ML
- Trip fact (accumulating) → utilization, conversion (request→completed), driver earnings.
- Demand forecast (theo region×time) → reposition driver.
- ETA model: train offline trên trip lịch sử, serve online.

## 6. DQ & observability
- Trip không đóng (thiếu dropoff) → alert (accumulating snapshot có mốc null lâu).
- Location gap per driver (gap detection).
- Reconciliation: tiền trip (fare) khớp payment.

## Câu hỏi đào sâu
- "Surge tính thế nào?" → windowed demand/supply ratio per H3 region trong stream → multiplier.
- "Geospatial query scale?" → index H3/geohash, pre-aggregate theo cell.
- "Trip lifecycle model?" → accumulating snapshot, mỗi mốc update hàng.

## ✅ "Tự mò"
🔭 Thiết kế trip fact accumulating snapshot (các cột ts + lag: wait_time, trip_duration) và 1 query tính demand-supply ratio theo region×giờ.

➡️ Tiếp: [[c06-case-clickstream]].
