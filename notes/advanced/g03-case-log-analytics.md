# G03 — Case: Log Analytics / Observability Platform

> Như Datadog/Splunk/ELK: thu log/metric/trace khối lượng khổng lồ, search + alert real-time. Khung [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: thu log/metric/trace từ hàng nghìn service; search log near-real-time; dashboard metric; alert theo rule; phân tích lịch sử.
- **Scale**: **TB–PB/ngày**, hàng triệu dòng/giây ở peak. Cao nhất về volume + velocity.
- **Latency**: log searchable trong **giây**; alert vài giây; lịch sử query được.
- **Đặc thù**: high cardinality (tag/label), retention tiered (log nóng vài ngày, lạnh lâu), bursty.

## 2. Kiến trúc
```
Services ──(agent: Fluentd/Vector/OTel)──► Kafka (buffer, backpressure) 
                                              │
                          ┌───────────────────┼────────────────────┐
                          ▼ hot (search/alert) ▼                    ▼ cold (lịch sử)
                  OLAP/search store          Stream proc            S3 (Parquet, partition by hr/service)
                  (ClickHouse/Elasticsearch/  (alert rules,                │ rollup metric
                   Loki/Druid)                aggregation)          batch analytics / cold search
                          │                                                
                  dashboard + search UI + alerting
```

## 3. Tech choices & trade-off
- **Agent + Kafka buffer**: agent gửi vào Kafka làm **shock absorber** (bursty log không sập downstream); backpressure ([[46-kafka-core]]).
- **Search/OLAP store nóng**: ClickHouse/Druid (metric/analytics, columnar, cực nhanh aggregate) hoặc Elasticsearch/Loki (full-text log search). Trade-off: ES tốn (index), Loki rẻ (index ít, label-based), ClickHouse mạnh aggregate.
- **Tiered retention** ⭐: nóng (vài ngày, store đắt) → lạnh (S3 Parquet, rẻ, query chậm hơn). Phần lớn log không bao giờ đọc lại → đẩy lạnh nhanh ([[59-cost-finops]]).
- **Metric rollup**: downsample (1s → 1m → 1h) cho lịch sử dài (giống IoT — [[c04-case-iot]]).

## 4. ⭐ Cardinality explosion (vấn đề đặc thù)
Metric với nhiều **label/tag** (user_id, request_id...) → số time-series bùng nổ → store sập/đắt. Cách trị:
- Giới hạn label cardinality cao (đừng để user_id làm label metric).
- Tách high-cardinality sang log/trace (không phải metric).
- Aggregation/sampling.

## 5. Scale & failure
- Partition Kafka theo service/source; scale ngang triệu/s.
- Sampling trace (giữ 100% error trace, sample success).
- Agent buffer khi mất kết nối; at-least-once → log có thể trùng (chấp nhận hoặc dedup theo id).
- Hot shard (service nói nhiều) → cân bằng.

## 6. DQ & observability (meta!)
- Phát hiện service **ngừng gửi log** (freshness per service — gap detection).
- Volume anomaly (log spike = sự cố hoặc loop lỗi).
- "Observability cho observability platform".

## Câu hỏi đào sâu
- "TB/ngày lưu rẻ sao?" → tiered (nóng ngắn + S3 lạnh), Parquet, sampling, rollup metric.
- "Cardinality explosion?" → giới hạn label, tách metric vs log/trace.
- "Search near-real-time trên volume lớn?" → store chuyên (ClickHouse/ES) + index hợp lý, không full-scan S3.

## ✅ "Tự mò"
🔭 Thiết kế schema log event (ts, service, level, message, trace_id, labels STRUCT) + chính sách retention tiered + nêu metric nào KHÔNG nên gắn high-cardinality label.

➡️ Tiếp: [[g04-case-gaming]].
