# 68 — Capstone C: Lakehouse

> Dự án "đỉnh" gộp gần như mọi thứ: lakehouse medallion + table format + orchestration + data quality + lineage. Phần lớn **chạy được local** bằng delta-rs (không cần Java).

## Bài toán
"Xây lakehouse từ nhiều nguồn: dữ liệu đổ về lake dạng Delta theo medallion (bronze→silver→gold), có ACID + time travel, được orchestrate, có data quality gates và lineage."

## Kiến trúc
```
Nguồn (API, files, CDC) 
   │ ingest (idempotent, raw-first)
   ▼
BRONZE  Delta tables (raw, append, partitioned by ingest_date)
   │ clean/dedup/cast + DQ check
   ▼
SILVER  Delta tables (conformed, 1 dòng = 1 thực thể sạch)
   │ business logic (dbt / Spark) + SCD2
   ▼
GOLD    Delta tables (star schema, marts) ──► BI / ML
   
Xuyên suốt:  Orchestration (Airflow/Dagster) · DQ gates (GE) · Lineage (OpenLineage/dbt) · Catalog
```

## Kiến thức nền
| Phần | Note |
|------|------|
| Lakehouse & medallion | [[36-lakehouse-arch]] |
| Delta Lake (ACID/time travel/MERGE) | [[34-delta-lake]] |
| Iceberg/Hudi & table formats | [[35-table-formats]] |
| Partitioning/tuning | [[31-partitioning-shuffle]], [[33-spark-tuning]] |
| dbt transform | Phase 3 |
| DQ gates | [[60-data-quality]] |
| Lineage | [[63-lineage-catalog]] |

## ⭐ Chạy được local bằng delta-rs (đã cài `deltalake`)
Không cần Java/Spark — `deltalake` (Rust) + polars/pandas làm được phần lớn:
```python
from deltalake import write_deltalake, DeltaTable
import polars as pl

# BRONZE: ghi raw thành Delta, partitioned
df = pl.read_parquet("data/raw/order_items.parquet").to_arrow()
write_deltalake("lake/bronze/order_items", df, mode="overwrite", partition_by=[])

# SILVER: đọc, clean/dedup, ghi Delta
silver = (pl.scan_delta("lake/bronze/order_items")  # hoặc đọc rồi xử lý
            .filter(...).unique(...).collect().to_arrow())
write_deltalake("lake/silver/order_items", silver, mode="overwrite")

# GOLD: aggregate -> Delta; time travel
DeltaTable("lake/gold/revenue").history()
DeltaTable("lake/gold/revenue", version=0).to_pandas()  # time travel
DeltaTable("lake/silver/order_items").optimize.compact()  # compaction
```
→ Demo được **ACID, time travel, schema evolution, compaction, medallion** — toàn bộ trên laptop.

## Checklist build
1. **Bronze**: ingest nhiều nguồn → Delta tables (raw, partitioned), idempotent overwrite theo partition.
2. **Silver**: clean/dedup (window dedup — [[04-sql-window]]), conform schema, SCD2 cho dimension.
3. **Gold**: star schema/marts (dùng dbt hoặc polars) → Delta.
4. **DQ gates** giữa các tầng: GE/Soda check, fail thì dừng ([[60-data-quality]]).
5. **Orchestration**: Airflow/Dagster điều phối bronze→silver→gold + DQ + lineage.
6. **Lineage/catalog**: dbt docs hoặc OpenLineage; tag PII ([[64-governance-pii]]).
7. **Time travel demo**: ghi 2 version, đọc lại version cũ, rollback.

## Mở rộng "ghi điểm"
- Iceberg thay Delta (pyiceberg) để so sánh table format.
- Streaming ingest vào bronze (gộp Capstone B).
- Z-ordering/compaction + đo cải thiện.
- Column-level lineage; data contract cho nguồn.

## Tiêu chí đạt
- [ ] Medallion 3 tầng Delta chạy được (local delta-rs OK).
- [ ] ACID + time travel demo được.
- [ ] DQ gates + orchestration.
- [ ] Lineage/catalog + PII handling.
- [ ] README + sơ đồ + trade-off (Delta vs Iceberg, vì sao medallion).

## 🔭 "Tự mò"
Đã có `deltalake`. Bắt đầu: chuyển `etl_pipeline.py` (Phase 1) sang ghi **Delta** thay parquet thường cho 3 tầng; thêm `DeltaTable(...).history()` + time travel; thêm 1 GE check giữa silver→gold.

➡️ Tiếp: [[00-phase9-summary]] — chốt khoá học.
