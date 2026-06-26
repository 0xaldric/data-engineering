# 34 — Delta Lake (Table Format cho Lakehouse) ⭐

> Vấn đề: data lake (file parquet trên S3) **không có** transaction — ghi đồng thời hỏng dữ liệu, không rollback, không time travel, schema trôi tự do. **Table format** thêm một lớp metadata để có ACID trên file thường.

## Table format là gì?
Một lớp **metadata + transaction log** đặt **trên** các file Parquet, biến "đống file" thành một "bảng" có ACID, version, schema. Ba cái lớn: **Delta Lake** (Databricks), **Apache Iceberg** (Netflix), **Apache Hudi** (Uber) — xem so sánh ở [[35-table-formats]].

## Delta Lake hoạt động thế nào — `_delta_log`
Một Delta table = thư mục gồm:
```
my_table/
├── part-0001.parquet        ← dữ liệu thật (Parquet)
├── part-0002.parquet
└── _delta_log/              ← TRANSACTION LOG (linh hồn của Delta)
    ├── 00000000000000000000.json   ← commit 0: thêm file A, B
    ├── 00000000000000000001.json   ← commit 1: xoá A, thêm C
    └── ...
```
Mỗi **commit** là một file JSON ghi: file nào được **thêm/xoá**, schema, statistics. Đọc bảng = đọc log để biết **tập file hiện hành**. Đây là nền tảng cho mọi tính năng dưới đây.

## ACID trên object storage
- **Atomic**: commit chỉ "tính" khi file log JSON ghi xong → ghi nửa chừng không làm hỏng bảng.
- **Consistent/Isolated**: đọc luôn thấy một **snapshot** nhất quán (đọc không bị ghi làm rối); ghi đồng thời dùng **optimistic concurrency** (kiểm tra version, conflict thì retry).
- **Durable**: nằm trên S3/đĩa bền.

## ⭐ Time travel
Vì log giữ mọi version, đọc lại **trạng thái quá khứ** dễ dàng:
```python
# delta-rs (Python, KHÔNG cần Java) — chạy được ở máy này
from deltalake import DeltaTable, write_deltalake
write_deltalake("t", df_v1)                 # version 0
write_deltalake("t", df_v2, mode="overwrite")  # version 1
DeltaTable("t", version=0).to_pandas()      # đọc lại version cũ!
DeltaTable("t").history()                   # xem lịch sử commit
```
Dùng để: audit, reproduce báo cáo cũ, rollback khi pipeline ghi sai, so sánh thay đổi.

## Schema evolution & enforcement
- **Enforcement**: mặc định Delta **từ chối** ghi sai schema (chặn dữ liệu bẩn).
- **Evolution**: cho phép thêm cột có chủ đích (`mergeSchema=true` / `schema_mode="merge"`).

## MERGE / upsert
`MERGE INTO` thực hiện upsert (update nếu trùng key, insert nếu mới) **nguyên tử** — nền tảng cho SCD2, CDC, incremental ([[27-dbt-incremental]]). Spark SQL:
```sql
MERGE INTO target t USING source s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...
```

## Bảo trì
- **OPTIMIZE / compact**: gộp small files thành file lớn → đọc nhanh ([[33-spark-tuning]]). delta-rs: `DeltaTable("t").optimize.compact()`.
- **Z-ordering**: sắp xếp dữ liệu theo cột hay lọc để data-skipping tốt hơn (gom giá trị gần nhau vào cùng file → bỏ qua nhiều file khi query).
- **VACUUM**: xoá file cũ không còn được tham chiếu (sau khi hết hạn time-travel) để tiết kiệm storage. ⚠️ Vacuum quá sớm sẽ phá time travel.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Vì sao data lake cần table format (ACID, version, schema).
- [ ] `_delta_log` là gì, đọc bảng = đọc log thế nào.
- [ ] Time travel & MERGE dùng để làm gì.
- [ ] OPTIMIZE/Z-order/VACUUM giải quyết gì; bẫy vacuum sớm.
- 🔭 *Tự mò:* máy đã cài `deltalake`. Thử: `write_deltalake` 2 lần, `DeltaTable(..., version=0).to_pandas()` để thấy time travel **chạy thật không cần Java**. Mở thư mục `_delta_log/` xem file JSON commit.

➡️ Tiếp: [[35-table-formats]] — Iceberg, Hudi & so sánh.
