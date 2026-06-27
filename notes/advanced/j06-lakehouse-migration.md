# J06 — Deep-dive: Lakehouse Migration

> Di chuyển hệ dữ liệu cũ → lakehouse hiện đại. Dự án thực tế hay gặp ở vai trò senior. Liên hệ [[35-table-formats]], [[36-lakehouse-arch]], [[i07-backfill-reprocessing]].

## Các loại migration thường gặp
| Từ | Tới | Lý do |
|----|-----|-------|
| Hive tables (S3) | **Iceberg/Delta** | ACID, time travel, partition evolution, hidden partition |
| On-prem Hadoop/HDFS | cloud lakehouse (S3+Iceberg) | tách compute/storage, rẻ, managed |
| Warehouse cũ (Teradata/Oracle) | Snowflake/BigQuery/lakehouse | chi phí, scale, cloud |
| Legacy ETL (script/Informatica) | dbt + Spark | maintainability, version, test |

## ⭐ Chiến lược chung: dual-run + validate + cutover
```
1. ASSESS: inventory bảng/pipeline/dependency, ưu tiên (giá trị × độ khó)
2. BUILD song song: dựng pipeline mới (lakehouse) BÊN CẠNH cũ, không đụng live
3. BACKFILL: chuyển dữ liệu lịch sử sang format mới ([[i07-backfill-reprocessing]])
4. DUAL-RUN: chạy CẢ HAI một thời gian, ghi cả 2
5. VALIDATE: so sánh output cũ vs mới (row count, checksum, sample, reconciliation)
6. CUTOVER: chuyển consumer sang mới (atomic/blue-green), giữ cũ để rollback
7. DECOMMISSION: tắt cũ sau khi tin tưởng
```

## In-place vs migrate
- **Hive → Iceberg in-place**: Iceberg có thể "add_files"/migrate procedure trỏ tới Parquet sẵn có → không copy data, chỉ tạo metadata. Nhanh, rẻ. Nếu format file tương thích.
- **Full migrate**: đọc cũ → ghi mới (đổi format/partition/schema). Tốn compute nhưng làm sạch/tối ưu được.

## Validation (sống còn) ⭐
Không cutover mù — **chứng minh mới = cũ**:
- **Row count** mỗi partition khớp.
- **Checksum/hash** tổng các cột số (sum, count distinct).
- **Sample diff** (audit_helper dbt — [[d02-dbt-advanced]]): so từng hàng trên mẫu.
- **Reconciliation** (số tiền/metric quan trọng) khớp tuyệt đối ([[c07-case-fintech]]).
- Chạy dual + so output dashboard cũ vs mới.

## Rủi ro & giảm thiểu
- **Đứt gãy consumer**: blue-green cutover, giữ cũ rollback ([[i07-backfill-reprocessing]]).
- **Schema/semantic khác**: data type mapping (Hive→Iceberg), null handling, timezone — dễ lệch âm thầm → validate kỹ.
- **Downtime**: migrate từng phần (theo bảng/domain), không big-bang.
- **Chi phí backfill**: lịch sử lớn → tốn compute; ưu tiên data còn dùng, archive phần cũ.
- **Quên consumer ẩn** (job/dashboard cũ trỏ bảng cũ) → lineage/catalog để tìm hết ([[63-lineage-catalog]]).

## Migrate ETL legacy → dbt
- Reverse-engineer logic cũ → dbt models (staging→marts).
- **audit_helper** so kết quả dbt vs pipeline cũ → đảm bảo logic giữ nguyên trước khi thay.
- Thêm tests/contracts mà cũ không có (cơ hội nâng chất lượng).

## ⚠️ Cạm bẫy
- Big-bang cutover không dual-run → vỡ production, không rollback.
- Không validate → số liệu lệch âm thầm (type/null/timezone).
- Bỏ sót consumer cũ → họ vẫn dùng bảng cũ đã tắt.
- Migrate hết một lần (kể cả data chết) → tốn vô ích; archive thay vì migrate.
- Quên ai đó phụ thuộc semantic cũ (vd "revenue" định nghĩa khác).

## ✅ "Tự mò"
🔭 Lập kế hoạch migrate `de.duckdb` gold marts (Phase 1) sang **Delta lakehouse** (delta-rs đã cài): build song song, validate (row count + sum revenue khớp `Grocery=1,714,225.45`), blue-green cutover. Viết checklist 7 bước.

➡️ Tiếp: [[j07-dbt-at-scale]].
