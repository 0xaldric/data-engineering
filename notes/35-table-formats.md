# 35 — Iceberg, Hudi & So sánh Table Formats

> Ba table format mở lớn: **Delta Lake, Apache Iceberg, Apache Hudi**. Đều thêm ACID/version/schema lên file trên object store, nhưng khác về thiết kế & thế mạnh.

## Apache Iceberg
Thiết kế bởi Netflix, chuẩn "mở" đang thắng thế ở nhiều nơi (Snowflake, BigQuery, AWS hỗ trợ native).
- **Hidden partitioning** ⭐: người dùng query `where event_date = '...'`, Iceberg tự biết file nào liên quan — **không** phải biết bảng partition theo cột dẫn xuất nào. Tránh lỗi "quên thêm điều kiện partition". 
- **Partition evolution**: đổi cách partition (vd ngày→giờ) **không** cần ghi lại dữ liệu cũ.
- **Schema evolution** an toàn (theo column ID, không theo vị trí → rename/reorder không vỡ).
- **Snapshot** & time travel; **manifest files** liệt kê data file + statistics để skip nhanh.
- Engine-agnostic: Spark, Flink, Trino, Dremio... cùng đọc/ghi.

## Apache Hudi
Thiết kế bởi Uber, mạnh về **upsert/streaming & CDC**.
- **Copy-on-Write (CoW)**: ghi lại file khi update → đọc nhanh, ghi chậm. Hợp đọc nhiều.
- **Merge-on-Read (MoR)**: ghi delta log, gộp lúc đọc → ghi nhanh, đọc chậm hơn (cần compaction). Hợp ghi/upsert nhiều, near-real-time.
- Có **record-level index** để upsert nhanh; tích hợp tốt với ingestion streaming.

## ⭐ So sánh nhanh
| | **Delta Lake** | **Iceberg** | **Hudi** |
|--|---------------|-------------|----------|
| Gốc | Databricks | Netflix | Uber |
| Metadata | transaction log (`_delta_log`) | metadata + manifest + snapshot | timeline + index |
| Điểm mạnh | hệ Databricks/Spark, dễ dùng, MERGE tốt | mở nhất, hidden + partition evolution | upsert/streaming/CDC, MoR |
| Hidden partitioning | không | **có** | một phần |
| Partition evolution | hạn chế | **có** | hạn chế |
| Đa engine | tốt (đang mở rộng) | **tốt nhất** | khá |
| Hợp cho | lakehouse trên Databricks/Spark | lakehouse mở, đa engine, bảng lớn lâu dài | sink streaming/CDC, near-real-time |

## Catalog (cách engine "tìm" bảng)
Table format cần **catalog** để map tên bảng → vị trí metadata:
- **Hive Metastore** (cũ, phổ biến), **AWS Glue Catalog**, **Unity Catalog** (Databricks), **Nessie** (git-like, branch/merge cho data), **REST catalog** (Iceberg, chuẩn mở).
Catalog quản lý schema, version, quyền — quan trọng để nhiều engine/team dùng chung an toàn.

## Chọn cái nào?
- Đang ở **Databricks/Spark-centric** → **Delta** (mượt nhất ở đó).
- Muốn **mở, đa engine, bảng lớn dài hạn, partition evolution** → **Iceberg** (xu hướng chuẩn ngành).
- Trọng tâm **upsert/CDC/near-real-time** → **Hudi**.
- Thực tế: cả ba đang hội tụ tính năng; nhiều tổ chức chuẩn hoá về **Iceberg** vì tính mở. Delta cũng có "Delta UniForm" đọc được như Iceberg.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Hidden partitioning của Iceberg giải quyết vấn đề gì.
- [ ] CoW vs MoR của Hudi; khi nào dùng cái nào.
- [ ] So sánh Delta/Iceberg/Hudi theo điểm mạnh.
- [ ] Vai trò catalog (Glue/Nessie/REST).
- 🔭 *Tự mò:* `pip install pyiceberg`, tạo một Iceberg table local (SQLite catalog) ghi/đọc, xem thư mục `metadata/` (snapshot + manifest). So với `_delta_log/` của Delta ([[34-delta-lake]]).

➡️ Tiếp: [[36-lakehouse-arch]].
