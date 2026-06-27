# H06 — Deep-dive: Real-time OLAP (ClickHouse / Druid / Pinot)

> Khi cần dashboard **sub-giây trên tỉ hàng** + ingest real-time → warehouse thường (BigQuery/Snowflake) không đủ nhanh/interactive. Đây là họ "real-time OLAP".

## Vì sao cần OLAP store riêng?
- Warehouse (Snowflake/BQ): tuyệt cho ETL/báo cáo, nhưng latency query ~giây-chục giây, không tối ưu cho **nghìn query đồng thời, sub-giây** (dashboard nhiều user, drill-down tương tác).
- Real-time OLAP: tối ưu cho **query latency cực thấp** + **ingest streaming** + concurrency cao. Dùng cho: user-facing analytics, observability ([[g03-case-log-analytics]]), real-time dashboard.

## Các engine
### ClickHouse ⭐
- Columnar, **vectorized execution**, nén cực tốt, cực nhanh aggregate.
- **MergeTree** engine: dữ liệu sort theo key, ghi thành part immutable → **merge** nền (như LSM — [[g07-dsa-for-de]]); sparse primary index (granule) cho data skipping.
- Mạnh: query analytics thô (group by/filter trên tỉ row) nhanh khủng; SQL đầy đủ.
- Dùng: log/metric analytics, user-facing dashboard.

### Apache Druid
- Lưu theo **segment** (time-partitioned, columnar), **real-time ingest** (Kafka) + batch.
- Pre-aggregation (rollup lúc ingest), bitmap index cho filter nhanh.
- Mạnh: time-series, real-time ingest + query; dashboard.

### Apache Pinot
- Tương tự Druid, tối ưu **user-facing analytics** latency cực thấp (LinkedIn). Nhiều loại index (star-tree pre-agg).

## So với Warehouse
| | Warehouse (Snowflake/BQ) | Real-time OLAP (ClickHouse/Druid) |
|--|--------------------------|-----------------------------------|
| Latency query | giây–chục giây | **sub-giây** |
| Concurrency | vừa (đắt khi cao) | **cao** (nghìn query/s) |
| Ingest | batch (+streaming) | **real-time** (Kafka) tốt |
| Update/transaction | tốt | hạn chế (append-mostly) |
| SQL/ELT/dbt | đầy đủ | hạn chế hơn (ClickHouse khá đủ) |
| Khi nào | ETL, BI nội bộ, ad-hoc | **user-facing**, real-time, observability |

## Kỹ thuật tăng tốc
- **Pre-aggregation / rollup**: tính sẵn aggregate lúc ingest (Druid rollup, ClickHouse materialized view) → query đọc ít.
- **Sort key / primary index**: data skipping theo cột hay lọc (granule/segment).
- **Denormalize** (OBT — [[e02-obt-wide]]): các engine này join yếu hơn → flatten data, ít join.
- **Time partitioning** (segment theo thời gian) cho time-series.

## Vị trí trong kiến trúc
```
Kafka ──► real-time OLAP (ClickHouse/Druid) ──► user-facing dashboard (sub-giây)
   └────► lake/warehouse (lịch sử, ETL, dbt) ──► BI nội bộ
```
Thường **song song** với warehouse: OLAP store cho hot/real-time/user-facing; warehouse cho ETL/lịch sử/BI sâu.

## ⚠️ Cạm bẫy
- Dùng warehouse cho user-facing dashboard nghìn query/s → chậm + đắt → cần OLAP store.
- Mong OLAP store làm mọi thứ (update/join phức tạp/ETL) → nó append-mostly, join yếu; denormalize trước.
- Không pre-aggregate → query vẫn quét nhiều.
- Vận hành thêm một hệ (ClickHouse) → chỉ thêm khi thật cần real-time/user-facing.

## ✅ "Tự mò"
🔭 ClickHouse chạy `docker run clickhouse`: load dataset e-commerce, tạo MergeTree sort theo (category, order_date), so tốc độ group-by với DuckDB; thử materialized view pre-agg.

➡️ Tiếp: [[h07-mock-interview]].
