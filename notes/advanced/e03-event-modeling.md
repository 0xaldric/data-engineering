# E03 — Modeling Event / Clickstream Data

> Event data (click, view, app action) khác data giao dịch: khối lượng lớn, schema linh hoạt, bán cấu trúc. Cách model cho đúng. Liên hệ [[c06-case-clickstream]].

## Đặc điểm event data
- **Append-only, immutable** (event đã xảy ra không sửa).
- **Khối lượng khổng lồ** (tỉ/ngày).
- **Schema bán cấu trúc**: mỗi loại event có property chung + property riêng, đổi liên tục.
- Cần: funnel, retention, sessionization, path analysis.

## Cấu trúc event chuẩn
```
common fields:  event_id, event_name, user_id, session_id, ts (event time),
                device, platform, app_version, source
custom props:   properties (JSON/STRUCT) — riêng từng event_name
```
- **Common + custom** tách rõ: cột common cho query/partition; custom trong **JSON/STRUCT column** (linh hoạt, không đổi schema khi thêm property).

## 3 cách lưu property linh hoạt
| Cách | Mô tả | Ưu / Nhược |
|------|-------|-----------|
| **JSON/STRUCT column** ⭐ | property trong 1 cột semi-structured | linh hoạt, warehouse hiện đại query được (`properties.price`); cần biết key |
| **Wide table (sparse)** | mỗi property 1 cột, nhiều NULL | query nhanh, nhưng nhiều cột thưa, đổi schema thường |
| **EAV** (entity-attribute-value) | mỗi property 1 hàng (key,value) | siêu linh hoạt nhưng query khổ (pivot), tránh nếu được |
→ Hiện đại: **JSON/STRUCT column** trên columnar warehouse (BigQuery STRUCT, Snowflake VARIANT, DuckDB STRUCT) — cân bằng tốt nhất.

## Schema evolution cho event
Event property thêm liên tục → cần chiến lược ([[10-json-avro]], [[61-data-contracts]]):
- Common fields ổn định + contract (Schema Registry nếu qua Kafka — [[48-kafka-ecosystem]]).
- Custom props trong JSON → thêm key thoải mái không phá schema.
- Backward compatible (thêm field optional).

## Sessionization model
Gom event thành session (gap > 30' = session mới — [[a01-sql-gaps-islands]]). Lưu:
- `fct_events` (grain = 1 event) + `dim_session` (grain = 1 session: start/end/n_events/duration/landing/exit page).
- Hoặc gắn `session_id` vào event table.

## Mô hình tổng cho clickstream
```
BRONZE: raw events (JSON, append, partition by dt/event_name)
SILVER: parsed + sessionized (common cols + properties STRUCT, session_id)
GOLD:   - fct_events (event grain, OBT-ish wide)
        - mart funnel / retention / dim_session
        - activity schema (nếu cần customer journey — [[e02-obt-wide]])
```

## Partition & cost
- Partition theo `dt` + (event_name nếu hợp) → pruning ([[31-partitioning-shuffle]]).
- Volume lớn → sampling cho phân tích thăm dò, OLAP store (Druid/ClickHouse) cho dashboard tương tác ([[c06-case-clickstream]]).

## ⚠️ Cạm bẫy
- EAV cho mọi property → query địa ngục (pivot khắp nơi).
- Không partition event table → full scan tỉ row, bill khủng.
- Schema cứng cho custom props → vỡ liên tục khi thêm event.
- Quên dedup (SDK gửi trùng, at-least-once) → đếm sai.
- Trộn event time vs ingest time → phân tích sai.

## ✅ "Tự mò"
🔭 Tạo bảng event từ orders e-commerce (event_name=order_placed, properties=STRUCT{category,amount}); query `properties.category`; sessionize theo user; build funnel.

➡️ Tiếp: [[e04-bitemporal]].
