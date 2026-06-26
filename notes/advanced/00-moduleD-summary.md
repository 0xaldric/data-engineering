# 🏁 Module D — Tổng kết: Advanced Tool Deep-dives

> Đào sâu "bên trong" các công cụ chính — để tối ưu & trả lời "vì sao" ở mức senior.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| D01 | Spark internals | [d01](d01-spark-internals.md) |
| D02 | dbt advanced | [d02](d02-dbt-advanced.md) |
| D03 | Kafka internals | [d03](d03-kafka-internals.md) |
| D04 | Snowflake deep | [d04](d04-snowflake.md) |
| D05 | BigQuery deep | [d05](d05-bigquery.md) |
| D06 | Airflow advanced | [d06](d06-airflow-advanced.md) |
| D07 | Iceberg deep | [d07](d07-iceberg.md) |

## 📑 Cheat-Sheet internals
- **Spark**: unified memory (execution⇄storage, spill ra đĩa khi thiếu); Tungsten (codegen + off-heap); AQE (coalesce shuffle, skew join, switch broadcast); debug bằng Spark UI (skew/spill/shuffle).
- **dbt**: semantic layer (metric 1 lần, nhất quán); packages (dbt_utils/expectations/audit_helper); project lớn theo domain; contracts; slim CI (`state:modified+`).
- **Kafka**: log segment + page cache + zero-copy = nhanh; ISR + high-watermark + leader epoch = bền; EOS = idempotent producer + transactions + read_committed (Kafka→Kafka; sink ngoài vẫn cần idempotent).
- **Snowflake**: tách 3 lớp; virtual warehouse (auto-suspend, sizing → **chi phí theo compute-time**); micro-partition + pruning; clustering; zero-copy clone; result cache.
- **BigQuery**: serverless (Dremel/slot/Colossus); **chi phí theo bytes-scanned** → partition + cluster + chọn cột; materialized view; `--dry-run`.
- **Airflow**: dynamic DAG, **deferrable** (async, nhả worker khi chờ), TaskGroup, datasets (data-aware), parse nhanh, KubernetesExecutor.
- **Iceberg**: cây metadata (metadata→manifest list→manifest→data); **hidden partitioning** + **partition evolution** + schema evolution by ID; catalog (REST/Glue/Nessie).

## So sánh nhanh warehouse
| | Snowflake | BigQuery |
|--|-----------|----------|
| Compute | virtual warehouse (bạn quản) | serverless slot |
| Chi phí | compute-time (auto-suspend!) | bytes-scanned (quét ít!) |

## So sánh table format
Delta (log tuyến tính, hệ Spark) vs **Iceberg** (cây metadata, hidden+partition evolution, đa engine — xu hướng mở) vs Hudi (upsert/CDC).

## ✅ Self-assessment Module D
- [ ] Giải thích spill/AQE/Tungsten; debug Spark job qua UI.
- [ ] Semantic layer & slim CI trong dbt.
- [ ] Kafka EOS gồm 3 mảnh; vì sao Kafka nhanh (zero-copy/page cache).
- [ ] Snowflake (compute-time) vs BigQuery (bytes-scanned) — tối ưu chi phí mỗi cái.
- [ ] Iceberg hidden/partition evolution vs Delta.

## 🔭 Để "tự mò"
pyiceberg (xem metadata layers), Snowflake/BigQuery free trial (tối ưu chi phí), Airflow deferrable + datasets, Spark UI debug (nếu có Java).

## ➡️ Tiếp theo: Module E — Advanced Data Modeling
Data Vault 2.0, One Big Table/wide tables, event/clickstream modeling, bitemporal, semantic layer. (Loop sinh Batch #15.)
