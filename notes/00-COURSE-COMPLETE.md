# 🎓 Data Engineering — Khoá học HOÀN TẤT (9/9 phase)

> Toàn bộ lộ trình DE đã viết thành ghi chú để tự học. Đây là **mục lục tổng** — bắt đầu từ Phase 0 và đi xuống, hoặc nhảy tới chủ đề cần.

## 📚 Cách dùng
- Mỗi **phase** có 1 note tổng kết `00-phaseN-summary.md` (cheat-sheet + self-assessment) — đọc cái này trước để nắm khung, rồi vào note chi tiết.
- Mỗi note có mục **🔭 "tự mò"** — phần thực hành để tự làm (đây là cách học vững nhất).
- Notes liên kết nhau bằng `[[...]]`.

## 🗺️ Toàn bộ note theo phase

### Phase 0 — Foundations & SQL → [tổng kết](00-phase0-summary.md)
01 [SQL basics](01-sql-basics.md) · 02 [JOINs](02-sql-joins.md) · 03 [Aggregation](03-sql-aggregation.md) · 04 [Window functions](04-sql-window.md) · 05 [CTE/Subquery](05-sql-cte.md) · 06 [Shell cho DE](06-shell-for-de.md)

### Phase 1 — Programming for DE → [tổng kết](00-phase1-summary.md)
07 [pandas](07-pandas.md) · 08 [polars](08-polars.md) · 09 [File formats](09-file-formats.md) · 10 [JSON/Avro](10-json-avro.md) · 11 [API ingestion](11-api-ingestion.md) · 12 [Testing](12-testing-de.md) · 13 [Logging/Config](13-logging-config.md)

### Phase 2 — Databases & Data Modeling → [tổng kết](00-phase2-summary.md)
14 [Indexing](14-indexing.md) · 15 [OLTP/OLAP/ACID](15-oltp-olap-acid.md) · 16 [Normalization](16-normalization.md) · 17 [Dimensional modeling](17-dimensional-modeling.md) · 18 [SCD](18-scd.md) · 19 [Fact types](19-fact-types.md) · 20 [NoSQL](20-nosql.md)

### Phase 3 — Warehousing & dbt → [tổng kết](00-phase3-summary.md)
21 [Warehouse/dbt](21-warehouse-dbt.md) · 22 [Staging](22-dbt-staging.md) · 23 [Marts](23-dbt-marts.md) · 24 [Tests](24-dbt-tests.md) · 25 [Macros/Jinja](25-dbt-macros.md) · 26 [Snapshots](26-dbt-snapshots.md) · 27 [Incremental](27-dbt-incremental.md) · 28 [Docs/Lineage](28-dbt-docs-lineage.md)

### Phase 4 — Spark & Big Data → [tổng kết](00-phase4-summary.md)
29 [Distributed/MapReduce](29-distributed-computing.md) · 30 [Spark model](30-spark-model.md) · 31 [Partitioning/Shuffle](31-partitioning-shuffle.md) · 32 [Joins/Catalyst](32-joins-catalyst.md) · 33 [Tuning](33-spark-tuning.md) · 34 [Delta Lake](34-delta-lake.md) · 35 [Table formats](35-table-formats.md) · 36 [Lakehouse](36-lakehouse-arch.md)

### Phase 5 — Orchestration (Airflow) → [tổng kết](00-phase5-summary.md)
37 [Orchestration intro](37-orchestration-intro.md) · 38 [Airflow core](38-airflow-core.md) · 39 [Scheduling/backfill](39-airflow-scheduling.md) · 40 [Idempotency/patterns](40-pipeline-patterns.md) · 41 [TaskFlow/XCom](41-airflow-taskflow.md) · 42 [Resources](42-airflow-resources.md) · 43 [Reliability](43-airflow-reliability.md) · 44 [Dagster/Prefect](44-dagster-prefect.md)

### Phase 6 — Streaming (Kafka) → [tổng kết](00-phase6-summary.md)
45 [Streaming intro](45-streaming-intro.md) · 46 [Kafka core](46-kafka-core.md) · 47 [Consumers/semantics](47-kafka-consumers.md) · 48 [Ecosystem](48-kafka-ecosystem.md) · 49 [Stream processing](49-stream-processing.md) · 50 [Flink](50-flink.md) · 51 [CDC/Debezium](51-cdc-debezium.md) · 52 [Lambda/Kappa](52-lambda-kappa.md)

### Phase 7 — Cloud & Infra → [tổng kết](00-phase7-summary.md)
53 [Docker](53-docker.md) · 54 [Compose/K8s](54-compose-k8s.md) · 55 [Cloud/S3/IAM](55-cloud-fundamentals.md) · 56 [AWS stack](56-aws-data-stack.md) · 57 [Terraform](57-terraform.md) · 58 [CI/CD](58-cicd.md) · 59 [Cost/FinOps](59-cost-finops.md)

### Phase 8 — Data Quality & Governance → [tổng kết](00-phase8-summary.md)
60 [Data quality](60-data-quality.md) · 61 [Data contracts](61-data-contracts.md) · 62 [Observability](62-observability.md) · 63 [Lineage/Catalog](63-lineage-catalog.md) · 64 [Governance/PII](64-governance-pii.md)

### Phase 9 — Capstone & Career → [tổng kết](00-phase9-summary.md)
65 [Portfolio](65-capstone-portfolio.md) · 66 [Capstone Batch](66-capstone-batch.md) · 67 [Capstone Streaming](67-capstone-streaming.md) · 68 [Capstone Lakehouse](68-capstone-lakehouse.md)

## 🛠️ Code chạy được kèm theo (Phase 0–3, đã verify)
Ngoài notes, Phase 0–3 có code thật trong `projects/` + 3 warehouse DuckDB (`de.duckdb`, `star.duckdb`, `dbt.duckdb`). Chạy `bash scripts/run_all.sh` để verify. Phase 4–9 là notes-first (theo yêu cầu) — code minh hoạ trong note + phần "tự mò".

## 💡 Lời kết
- **SQL + data modeling + idempotency** là nền tảng bất biến — nắm chắc.
- Công cụ thay đổi, **khái niệm** thì không (lazy/DAG, partition/shuffle, exactly-once, medallion, ACID...). Học khái niệm → đổi công cụ dễ.
- Học bằng cách **build**: chọn 1–2 capstone, làm thật, viết README, giải thích trade-off.
- Chúc bạn "tự mò" vui & thành DE vững. 🚀
