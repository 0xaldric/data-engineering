# C06 — Case: Clickstream / Social Media Analytics

> Đặc trưng: **khối lượng event khổng lồ**, schema linh hoạt, sessionization, funnel/retention ở scale. Áp [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: track mọi tương tác (page view, click, scroll, like, share); funnel chuyển đổi, retention/cohort, A/B test, real-time active users.
- **Scale**: **tỉ event/ngày** (cao nhất trong các case). Schema event đa dạng & đổi liên tục.
- **Latency**: real-time counters (active users) ~giây; phân tích sâu batch.
- **Đặc thù**: high cardinality, sessionization, schema evolution thường xuyên, cần sampling.

## 2. Kiến trúc
```
Web/App SDK ──► Collector (edge, validate+enrich) ──► Kafka "events" (Avro+Schema Registry)
                                                          │
                          ┌───────────────────────────────┤
                          ▼ real-time                      ▼ batch
                  Stream proc: active users,         Sink → S3 BRONZE (Parquet, partition dt/event_type)
                  rolling counters → Redis/Druid           │ Spark/dbt
                          │                                 ▼
                  real-time dashboard               SILVER: sessionize, dedup, conform
                                                          │
                                                          ▼
                                                  GOLD: funnel, cohort/retention, OBT event table
                                                  + A/B test analysis, ML features
```

## 3. Tech choices & trade-off
- **Schema Registry + Avro** ⭐: event schema đổi liên tục → contract + evolution backward-compatible chặn vỡ consumer ([[48-kafka-ecosystem]], [[61-data-contracts]]).
- **One Big Table (OBT) / wide event table** thay star truyền thống: event bán cấu trúc, query linh hoạt, ít join — phổ biến cho clickstream. (Module E sẽ sâu hơn.)
- **Sessionization** ở batch (LAG → gap → session — [[a01-sql-gaps-islands]]).
- **Sampling**: với tỉ event, một số phân tích chạy trên mẫu (1–10%) để rẻ/nhanh; giữ raw đầy đủ cho cái cần chính xác.
- **OLAP real-time** (Druid/ClickHouse/Pinot) cho dashboard tương tác trên event lớn; lake cho lịch sử/ML.

## 4. Scale & failure
- Partition Kafka theo user_id/session → sessionization đúng + scale.
- Bad/malformed events (SDK lỗi, bot) → validate ở collector, quarantine; lọc bot.
- Late events (mobile offline) → event time + watermark; recompute session.
- Small files (tỉ event → nhiều file) → compaction + partition hợp lý.

## 5. Đặc thù phân tích
- **Funnel** ordered (đúng thứ tự thời gian — [[a03-analytics-patterns]]).
- **Retention triangle** theo cohort.
- **A/B test**: gán variant, đo metric, kiểm ý nghĩa thống kê.
- Dedup event (SDK gửi trùng) — at-least-once → dedup theo event_id.

## 6. DQ & observability
- Volume anomaly (event tụt = SDK/tracking lỗi), schema drift (Schema Registry chặn), bot ratio.
- Freshness real-time counters.

## Câu hỏi đào sâu
- "Tỉ event/ngày lưu sao cho rẻ?" → Parquet + partition + tiered storage + sampling cho phân tích nặng + OLAP store cho hot.
- "Schema event đổi liên tục?" → Schema Registry + Avro evolution + OBT linh hoạt.
- "Dashboard real-time trên tỉ row?" → pre-aggregate + OLAP columnar (Druid/ClickHouse).

## ✅ "Tự mò"
🔭 Lấy orders e-commerce làm "event", sessionize theo user (gap 30') rồi tính funnel view→cart→purchase; nghĩ nếu là tỉ event thì đổi gì (sampling, OLAP store).

➡️ Tiếp: [[c07-case-fintech]].
