# 🏁 Phase 4 — Tổng kết: Batch Processing & Big Data (Spark/Lakehouse)

> Chế độ **notes-first**: Phase này học khái niệm vững (môi trường không có Java nên không chạy Spark; code là minh hoạ + "tự mò" bằng polars/DuckDB/delta-rs).

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| T038 | Distributed computing & MapReduce | [29](29-distributed-computing.md) |
| T039 | Spark architecture & execution model | [30](30-spark-model.md) |
| T040 | Partitioning & Shuffle | [31](31-partitioning-shuffle.md) |
| T041 | Joins at scale & Catalyst | [32](32-joins-catalyst.md) |
| T042 | Spark performance tuning | [33](33-spark-tuning.md) |
| T043 | Delta Lake | [34](34-delta-lake.md) |
| T044 | Iceberg, Hudi & table formats | [35](35-table-formats.md) |
| T045 | Lakehouse architecture + Medallion | [36](36-lakehouse-arch.md) |

## 📑 Cheat-Sheet Spark/Lakehouse

### Spark mental model
- **Driver** (lập kế hoạch) + **Executors** (chạy task/partition) + **Cluster Manager**.
- **DataFrame** (mặc định, được Catalyst tối ưu) > RDD (thấp cấp).
- **Lazy**: transformation tích luỹ DAG, **action** mới chạy.
- **Narrow** (map/filter, không shuffle) vs **Wide** (groupBy/join, **shuffle** → cắt stage).

### Tối ưu (đều xoay quanh: đọc ít + ít shuffle + cân bằng)
- Đọc ít: column pruning + predicate pushdown + Parquet + partition pruning.
- Ít shuffle: lọc/bỏ cột trước groupBy/join; **broadcast** bảng nhỏ.
- Cân bằng: partition ~128–256MB; xử lý **skew** (salting/AQE); compact small files.
- Cache khi tái dùng; tránh UDF Python; bật AQE; đọc Spark UI tìm nghẽn.

### Joins
- **Broadcast** (bảng nhỏ, không shuffle) · **Sort-merge** (2 bảng lớn) · **Shuffle-hash**.
- **Catalyst**: logical→optimized→physical (pushdown, pruning, CBO). **Tungsten**: codegen + off-heap. **AQE**: tối ưu lúc chạy.

### Lakehouse
- **Table format** (Delta/Iceberg/Hudi) = ACID + version + schema **trên** Parquet/object store.
- Delta: `_delta_log`, time travel, MERGE, OPTIMIZE/Z-order/VACUUM.
- Iceberg: hidden partitioning, partition evolution, đa engine (xu hướng chuẩn mở).
- Hudi: upsert/CDC, CoW vs MoR.
- **Medallion** bronze→silver→gold; tách compute/storage; 4 lớp: storage→file format→table format→compute (+catalog).

## ✅ Self-assessment Phase 4
- [ ] Giải thích MapReduce & vì sao shuffle đắt.
- [ ] Spark: driver/executor, lazy/action, narrow/wide, DAG→stage.
- [ ] Partitioning, shuffle, skew & cách xử lý.
- [ ] 3 kiểu join + Catalyst/Tungsten/AQE.
- [ ] Checklist tuning (đọc ít, ít shuffle, cân bằng, cache, small files).
- [ ] Table format & ACID trên lake; Delta vs Iceberg vs Hudi.
- [ ] Lakehouse vs lake vs warehouse; medallion; 4 lớp kiến trúc.

## 🔭 Để "tự mò" (hands-on khi rảnh)
1. Cài Java + `pip install pyspark`, chạy local: `spark.read.parquet(...).groupBy(...).agg(...).explain()` — đọc physical plan, tìm join type.
2. `deltalake` (đã cài): write 2 version → time travel `DeltaTable(..., version=0)`; `optimize.compact()`; mở `_delta_log/`.
3. `pyiceberg`: tạo Iceberg table local, xem `metadata/` snapshot/manifest.
4. Dựng medallion mini bằng Delta (bronze/silver/gold) trên dataset e-commerce.

## ➡️ Tiếp theo: Phase 5 — Workflow Orchestration (Airflow)
DAG, operators, scheduling, idempotency, backfill, retries; Dagster/Prefect. (notes-first)
