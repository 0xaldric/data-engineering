# D07 — Apache Iceberg deep

> Sâu hơn [[35-table-formats]]: bên trong Iceberg — table format mở đang thành chuẩn ngành (Snowflake, BigQuery, AWS, Databricks đều hỗ trợ).

## ⭐ Metadata layers (cấu trúc nhiều tầng)
Khác Delta (transaction log JSON tuyến tính), Iceberg dùng **cây metadata**:
```
catalog → current metadata pointer
   │
metadata.json        (schema, partition spec, snapshots list, properties)
   │
manifest list        (1 file / snapshot: trỏ tới các manifest + partition stats)
   │
manifest files       (liệt kê data files + column stats: min/max/null/count)
   │
data files           (Parquet/ORC/Avro)
```
- Đọc bảng = đọc current metadata.json → manifest list (snapshot) → manifest → biết **chính xác file nào** cần đọc + stats để prune.
- **Snapshot**: mỗi commit tạo snapshot mới (trỏ manifest list mới) → ACID + time travel.

## Hidden partitioning ⭐ (điểm ăn tiền)
Iceberg lưu **partition transform** trong metadata; người dùng query cột gốc, Iceberg tự suy partition:
```sql
-- định nghĩa: PARTITIONED BY days(event_ts)
-- query bình thường -> Iceberg TỰ prune theo ngày, không cần điều kiện trên cột dẫn xuất
select * from events where event_ts >= '2024-01-01';
```
- Khác Hive/Spark truyền thống (phải biết & lọc theo cột partition dẫn xuất `dt`, quên là full scan). Iceberg **giấu** chi tiết partition → ít lỗi "quên partition filter".
- Transform: `days/hours/months/bucket(N)/truncate(N)/identity`.

## Partition evolution ⭐
Đổi cách partition (vd `days` → `hours` khi dữ liệu tăng) **không cần ghi lại dữ liệu cũ**. Dữ liệu cũ giữ partition spec cũ, mới theo spec mới; Iceberg xử lý query xuyên cả hai. Delta không làm được điều này dễ dàng.

## Schema evolution (an toàn theo ID)
Mỗi cột có **field ID** (không theo tên/vị trí) → add/drop/rename/reorder cột **an toàn**, không vỡ dữ liệu cũ, không cần rewrite.

## Bảo trì
- **Compaction / rewrite_data_files**: gộp small files ([[33-spark-tuning]]).
- **Expire snapshots**: xoá snapshot cũ + data file mồ côi (giải phóng storage; cẩn thận phá time travel — như VACUUM Delta).
- **Rewrite manifests**: tối ưu metadata khi nhiều snapshot.

## Catalog (quan trọng cho Iceberg)
Iceberg cần **catalog** map tên bảng → metadata location:
- **REST catalog** (chuẩn mở, đang phổ biến), **AWS Glue**, **Hive Metastore**, **Nessie** (git-like: branch/merge/tag cho data — môi trường dev/test trên data).
- Catalog quản atomic commit (đổi current metadata pointer nguyên tử).

## Delta vs Iceberg (sâu)
| | Delta | Iceberg |
|--|-------|---------|
| Metadata | transaction log JSON (tuyến tính) | cây metadata + manifest |
| Hidden partition | không | **có** |
| Partition evolution | hạn chế | **có** |
| Schema evolution | tên/vị trí | **field ID** (an toàn hơn) |
| Engine | mạnh Spark/Databricks | **đa engine nhất** (mở) |
| Hệ sinh thái | Databricks | Netflix/Apache, nhiều vendor |
→ Xu hướng nhiều tổ chức chuẩn hoá **Iceberg** vì tính mở + partition/schema evolution. Delta có UniForm để đọc như Iceberg.

## ⚠️ Cạm bẫy
- Không compaction → nhiều small files + nhiều snapshot → metadata phình, đọc chậm.
- Expire snapshot quá sớm → mất time travel.
- Catalog không atomic/đúng → commit conflict.

## ✅ "Tự mò"
🔭 `pip install pyiceberg`: tạo Iceberg table (SQLite/REST catalog) ghi/đọc, xem thư mục `metadata/` (metadata.json → manifest list → manifest); thử schema evolution (add column) + time travel snapshot.

➡️ Tiếp: [[00-moduleD-summary]].
