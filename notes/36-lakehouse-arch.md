# 36 — Data Lake vs Warehouse vs Lakehouse + Medallion

> Bức tranh kiến trúc tổng: ba mô hình lưu trữ-phân tích và cách lakehouse kết hợp ưu điểm cả hai.

## Ba mô hình
| | **Data Warehouse** | **Data Lake** | **Lakehouse** |
|--|--------------------|---------------|----------------|
| Lưu | bảng có cấu trúc, độc quyền | file thô mọi định dạng trên object store | file mở (Parquet) + **table format** |
| Schema | schema-on-write (chặt) | schema-on-read (lỏng) | schema-on-write có quản lý (table format) |
| Dữ liệu | có cấu trúc | mọi loại (cả ảnh, log, JSON) | mọi loại + bảng ACID |
| ACID/version | có | **không** (chỉ file) | **có** (Delta/Iceberg/Hudi) |
| Chi phí | đắt | rẻ | rẻ (object store) |
| BI/SQL | tốt | yếu/khó | tốt |
| ML/raw | khó | tốt | tốt |
| Ví dụ | Snowflake, Redshift, BigQuery | S3 + parquet | Databricks, S3+Iceberg+Trino |

## Vấn đề của mỗi cái → vì sao có lakehouse
- **Warehouse**: mạnh BI nhưng đắt, khó chứa dữ liệu phi cấu trúc/ML, dữ liệu bị "khoá" trong định dạng độc quyền.
- **Data lake**: rẻ & linh hoạt nhưng **không ACID/transaction** → dễ thành **"data swamp"** (đống file lộn xộn, không tin được, ghi đồng thời hỏng).
- **Lakehouse** = file mở rẻ của lake + ACID/schema/BI của warehouse, nhờ **table format** ([[34-delta-lake]], [[35-table-formats]]). Một bản sao dữ liệu phục vụ **cả BI lẫn ML**.

## ⭐ Kiến trúc Medallion (Bronze → Silver → Gold)
Cách tổ chức dữ liệu trong lakehouse theo tầng chất lượng (đã gặp ở [[21-warehouse-dbt]], [[23-dbt-marts]] — đây là phiên bản "ở quy mô lake"):
```
Nguồn → BRONZE (raw, append-only, y nguyên gốc)
           ↓ clean, dedup, ép kiểu, validate
        SILVER (chuẩn hoá, đáng tin, 1 dòng = 1 thực thể sạch)
           ↓ business logic, join, aggregate
        GOLD (mart/feature, sẵn sàng cho BI/ML)
```
- **Bronze**: nuốt mọi thứ, không sửa → có thể replay. Lưu lịch sử thô.
- **Silver**: lọc rác, dedup (window `[[04-sql-window]]`), conform schema → "single source of truth".
- **Gold**: star schema/aggregate/feature table cho dashboard & model.
Mỗi tầng là **bảng table-format** (Delta/Iceberg) → ACID + time travel ở mọi tầng.

## Tách compute & storage
Tư tưởng cốt lõi của cloud/lakehouse: **storage** (S3 — rẻ, bền, vô hạn) tách khỏi **compute** (Spark/Trino/DuckDB — bật khi cần, co giãn). Nhiều engine cùng đọc một bản dữ liệu. Khác warehouse cũ (compute+storage dính nhau, scale chung).

## Ba lớp ghép thành lakehouse
```
[ Compute/Engine ]  Spark · Trino · Flink · DuckDB        (xử lý)
[ Table format   ]  Delta · Iceberg · Hudi                (ACID, version, schema)
[ File format    ]  Parquet · ORC · Avro                  (lưu cột/dòng)
[ Object storage ]  S3 · GCS · ADLS                       (bền, rẻ)
   + Catalog: Glue/Nessie/Unity/REST  (map tên bảng ↔ metadata, quyền)
```
Hiểu 4 lớp này là hiểu một lakehouse hiện đại được lắp ráp thế nào.

## Khi nào dùng gì?
- BI thuần, dữ liệu có cấu trúc, ngân sách thoải mái, muốn đơn giản → **warehouse cloud** (BigQuery/Snowflake).
- Nhiều dữ liệu thô/ML, cần rẻ & mở, đa engine → **lakehouse** (S3 + Iceberg/Delta).
- Thực tế nhiều nơi **kết hợp**: lakehouse làm nền + warehouse cho lớp phục vụ BI nóng.

## ✅ Tự kiểm tra & "tự mò"
- [ ] So sánh warehouse / lake / lakehouse (ACID, chi phí, schema, BI/ML).
- [ ] Vì sao data lake dễ thành swamp; lakehouse khắc phục bằng gì.
- [ ] Vẽ medallion bronze→silver→gold, trách nhiệm mỗi tầng.
- [ ] 4 lớp: storage / file format / table format / compute (+ catalog).
- 🔭 *Tự mò:* dựng medallion mini bằng `deltalake`: bronze = ghi raw parquet thành Delta; silver = đọc, dedup/clean, ghi Delta; gold = aggregate, ghi Delta. Tất cả **chạy local không cần Java**.

➡️ Tiếp: [[00-phase4-summary]] — chốt Phase 4.
