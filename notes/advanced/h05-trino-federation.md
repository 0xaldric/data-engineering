# H05 — Deep-dive: Query Engines (Trino/Presto) & Federation

> Trino (trước là PrestoSQL) — engine SQL phân tán **không có storage riêng**, query thẳng nhiều nguồn. Khác Spark, khác warehouse.

## Trino là gì
Engine **MPP** (massively parallel processing) chạy SQL **interactive** trên dữ liệu ở nơi khác (lake, DB, Kafka...). **Không lưu trữ** — chỉ compute. "SQL query engine cho mọi thứ".
```
        ┌─ COORDINATOR ─┐   (parse, plan, schedule, gom kết quả)
        └───────┬───────┘
        ┌───────┼───────┐
        ▼       ▼       ▼
     WORKER  WORKER  WORKER   (thực thi song song, đọc từ connector)
        │       │       │
        └─── CONNECTORS ───┘  Hive/Iceberg (S3), MySQL, Postgres, Kafka, MongoDB...
```
- **Coordinator**: nhận query, lập plan, chia task cho worker, gom kết quả.
- **Worker**: chạy task song song, đọc data qua **connector**.
- **Connector**: plugin cho mỗi nguồn (Hive/Iceberg trên S3, JDBC DB, Kafka...).
- **In-memory, pipelined**: không ghi shuffle ra đĩa như Spark (mặc định) → **nhanh cho query interactive**, nhưng job cực lớn/dài kém bền hơn Spark.

## ⭐ Query Federation
Join **across nhiều nguồn** trong MỘT query, không cần ETL gộp trước:
```sql
-- join dữ liệu S3 (lake) với MySQL (OLTP) với Kafka — tất cả trong 1 query
select o.order_id, c.name, e.event_type
from iceberg.lake.orders o
join mysql.app.customers c on c.id = o.customer_id
join kafka.events.clicks  e on e.order_id = o.order_id;
```
- Mỗi `catalog.schema.table` trỏ tới một connector/nguồn.
- Lợi: query ad-hoc xuyên nguồn không cần pipeline; data ở đâu cũng query được.
- Trade-off: kéo data qua mạng (không có data locality như đọc lake thuần); nguồn chậm (OLTP) kéo lùi query; nên dùng cho **ad-hoc/federation**, không thay ETL cho workload lặp.

## Trino vs Spark SQL
| | **Trino** | **Spark SQL** |
|--|-----------|---------------|
| Mục đích | **interactive/ad-hoc** SQL, federation | **batch ETL** lớn, ML, pipeline |
| Storage | không (chỉ compute) | không (nhưng hệ Spark rộng) |
| Shuffle | in-memory/pipelined (ít ghi đĩa) | ghi đĩa (bền hơn cho job lớn) |
| Job lớn/dài | kém bền | **bền** (retry stage, spill) |
| Latency | thấp (interactive) | cao hơn (job khởi động) |
| Federation | **mạnh** (nhiều connector) | qua data source API |
→ Dùng **cả hai**: Spark cho ETL nặng/transform; Trino cho analyst query interactive trên lake + federation. (Athena = Trino/Presto managed của AWS — [[56-aws-data-stack]].)

## Tối ưu query Trino trên lake
- **Partition pruning** + **predicate/projection pushdown** (đẩy filter/cột xuống connector — [[31-partitioning-shuffle]], [[a06-sql-optimization]]).
- Parquet/Iceberg (columnar + stats) → đọc ít.
- Broadcast bảng nhỏ; tránh join 2 nguồn chậm khổng lồ.
- Đọc `EXPLAIN` xem connector pushdown được không.

## ⚠️ Cạm bẫy
- Dùng Trino federation thay ETL cho workload **lặp** → chậm/tải nguồn OLTP mỗi lần. ETL gộp 1 lần thay vì federate nghìn lần.
- Join nguồn OLTP lớn → kéo data qua mạng, OLTP bị tải.
- Job ETL khổng lồ trên Trino → kém bền (dùng Spark).

## ✅ "Tự mò"
🔭 DuckDB là "Trino mini" cho một máy — query thẳng parquet + attach Postgres/MySQL (`ATTACH`) rồi join across; cảm nhận federation. Đọc Trino connector docs cho S3+JDBC.

➡️ Tiếp: [[h06-realtime-olap]].
