# 📈 PROGRESS LOG

Nhật ký các task đã hoàn thành. Mỗi dòng: `[ngày giờ] Txxx — mô tả — artifact`.

## Batch #1 — Phase 0: Foundations & SQL

<!-- Loop sẽ thêm dòng vào đây sau mỗi task hoàn thành -->
- [2026-06-26 00:50] T001 — Project README & cấu trúc dự án — `README.md`
- [2026-06-26 00:50] T002 — Synthetic e-commerce dataset (42,435 rows, 4 bảng CSV+Parquet) — `scripts/gen_ecommerce.py`, `scripts/run_sql.py`, `data/raw/*`
- [2026-06-26 00:52] T003 — SQL Fundamentals (DDL/DML/SELECT/filter), 14 stmts chạy OK; fix bug splitter trong run_sql.py (bỏ comment trước khi split `;`) — `projects/01-sql-fundamentals/01_basics.sql`, `notes/01-sql-basics.md`
- [2026-06-26 01:00] T004 — SQL JOINs (inner/left/right/full/cross/self + anti-join), 8 stmts OK; demo fan-out 10k đơn→30k hàng + cạm bẫy NULL/ON-vs-WHERE — `projects/01-sql-fundamentals/02_joins.sql`, `notes/02-sql-joins.md`
- [2026-06-26 01:02] T005 — Aggregation/GROUP BY (COUNT/SUM/AVG, HAVING, FILTER, ROLLUP/GROUPING SETS, % of total), 8 stmts OK — `projects/01-sql-fundamentals/03_aggregation.sql`, `notes/03-sql-aggregation.md`
- [2026-06-26 01:30] T006 — Window Functions ⭐ (ROW_NUMBER/RANK/DENSE_RANK, LAG/LEAD MoM, running total, moving avg, NTILE, dedup); fix lỗi GROUP BY-trên-window; 6 stmts OK — `projects/01-sql-fundamentals/04_window.sql`, `notes/04-sql-window.md`
- [2026-06-26 01:33] T007 — CTEs/Recursive CTE (calendar + org tree)/Subqueries (scalar/correlated/EXISTS)/Set ops (UNION/INTERSECT/EXCEPT), 7 stmts OK — `projects/01-sql-fundamentals/05_cte_subquery.sql`, `notes/05-sql-cte.md`
- [2026-06-26 02:00] T008 — Shell/Linux cho DE (cut/sort/uniq/grep/awk pipeline, awk group-by, cron, bẫy parse CSV); `explore.sh` chạy OK, cross-check khớp SQL (5102 completed) — `scripts/explore.sh`, `notes/06-shell-for-de.md`
- [2026-06-26 02:03] T009 — 15 bài tập SQL dễ→khó (join/aggregate/window/CTE) + lời giải; cả 15 stmts chạy đúng — `projects/01-sql-fundamentals/exercises.sql`, `solutions.sql`
- [2026-06-26 02:30] T010 — Phase 0 review: summary + SQL cheat-sheet + self-assessment; smoke test tái dùng `run_all.sh` = ALL GREEN (58 SQL stmts + shell). **HOÀN THÀNH PHASE 0 (10/10).** — `notes/00-phase0-summary.md`, `scripts/run_all.sh`

## Batch #2 — Phase 1: Programming for Data Engineering
<!-- Loop thêm dòng vào đây khi hoàn thành task Phase 1 -->
- [2026-06-26 03:00] T011 — pandas fundamentals (select/filter, groupby/agg, merge, pivot_table, resample, NULL); revenue/category KHỚP số SQL; vectorization nhanh hơn apply ~628x — `projects/02-python-de/01_pandas_basics.py`, `notes/07-pandas.md`
- [2026-06-26 03:03] T012 — polars (expression API, lazy scan + explain với projection pushdown 3/7 cột); benchmark join+groupby: polars lazy nhanh hơn pandas 3.4x; revenue khớp — `projects/02-python-de/02_polars_basics.py`, `notes/08-polars.md`
- [2026-06-26 03:30] T013 — File formats benchmark (1.2M hàng): Parquet+zstd nhỏ hơn CSV 6.5x, đọc full nhanh 9.6x, đọc 1 cột nhanh 22x, predicate pushdown 3.9ms; row groups/encoding/codecs — `projects/02-python-de/03_formats_benchmark.py`, `notes/09-file-formats.md`
- [2026-06-26 03:33] T014 — JSON/JSONL + flatten nested (json_normalize), Avro write/read (fastavro) + schema evolution demo (đọc data v1 bằng reader v2 → default); +fastavro vào requirements — `projects/02-python-de/04_json_avro.py`, `notes/10-json-avro.md`
- [2026-06-26 04:07] T015 — Resilient REST API ingestion (pagination 5 pages, retry+exponential backoff, timeout, raw→bronze, normalize→Parquet, lineage _source); verify cả API thật (100 recs) lẫn offline fallback (mock) — `projects/02-python-de/05_api_ingest.py`, `notes/11-api-ingestion.md`
- [2026-06-26 04:10] T016 — Clean & tested code: pure transforms + pydantic validation + soft-validation; pytest 14/14 PASS (+pytest,pydantic,conftest) — `projects/02-python-de/transforms.py`, `tests/test_transforms.py`, `notes/12-testing-de.md`
- [2026-06-26 04:37] T017 — Logging/config/error handling: get_logger idempotent, Config (defaults<YAML<env), retry decorator, custom exceptions, redact secrets; refactor 05_api_ingest dùng utils (vẫn chạy + 14/14 test pass) — `projects/02-python-de/utils.py`, `notes/13-logging-config.md`
- [2026-06-26 04:40] T018 — ⭐ Capstone ETL medallion (bronze→silver→gold): extract 4 bảng → fct 30135 → 3 marts (category/monthly/LTV) → DuckDB warehouse/de.duckdb + Parquet; logging+custom exceptions, idempotent (chạy 2 lần khớp), revenue khớp xuyên SQL/pandas/polars — `projects/02-python-de/etl_pipeline.py`, `projects/02-python-de/README.md`
- [2026-06-26 05:00] T019 — Phase 1 review: summary + cheat-sheet pandas/polars/parquet + self-assessment; mở rộng run_all.sh (7 script Python + pytest) = ALL GREEN. **HOÀN THÀNH PHASE 1 (9/9).** — `notes/00-phase1-summary.md`, `scripts/run_all.sh`

## Batch #3 — Phase 2: Databases & Data Modeling
<!-- Loop thêm dòng vào đây khi hoàn thành task Phase 2 -->
- [2026-06-26 05:30] T020 — Indexing & EXPLAIN: query plan thật (SEQ_SCAN+filter pushdown, hash join, cardinality), CREATE INDEX (single/composite), B-tree/hash/partial/covering, OLTP index vs OLAP zonemap; 8 stmts OK — `projects/03-data-modeling/01_explain_index.sql`, `notes/14-indexing.md`
- [2026-06-26 05:33] T021 — Constraints (PK/UNIQUE/NOT NULL/CHECK/FK đều chặn đúng) + transactions (ROLLBACK hoàn tác/COMMIT giữ); notes ACID, isolation levels/anomalies, OLTP vs OLAP, row vs column store — `projects/03-data-modeling/02_constraints_tx.py`, `notes/15-oltp-olap-acid.md`
- [2026-06-26 06:00] T022 — Normalization 1NF→2NF→3NF (FD, 3 anomaly, phân rã 5 bảng), lossless check diff_rows=0, hết dư thừa (An 3→1 dòng); khi nào denormalize cho OLAP; 10 stmts OK — `projects/03-data-modeling/03_normalization.sql`, `notes/16-normalization.md`
- [2026-06-26 06:03] T023 — Dimensional Modeling (Kimball) thiết kế ⭐: grain/fact/dim, surrogate key, star vs snowflake, fact types, conformed dim + bus matrix, sơ đồ ASCII star schema cho e-commerce — `notes/17-dimensional-modeling.md`, `projects/03-data-modeling/star_schema_design.md`
- [2026-06-26 06:30] T024 — Build star schema → warehouse/star.duckdb: dim_date(730, generate_series)/dim_customer(2000)/dim_product(300, surrogate key)/fct_sales(30135); verify revenue khớp gold mart (Grocery 1714225.45, assertion pass) + drill quý×country — `projects/03-data-modeling/04_build_star.py`
- [2026-06-26 06:33] T025 — SCD Type 1/2/3 ⭐ trên cùng thay đổi (khách #1 Hanoi→Tokyo): Type1 ghi đè mất lịch sử; Type2 versioning 2 phiên bản + truy vấn as-of đúng; Type3 previous value — `projects/03-data-modeling/05_scd.py`, `notes/18-scd.md`
- [2026-06-26 07:00] T026 — Fact types: periodic snapshot (fct_daily_sales) + accumulating snapshot (fct_order_lifecycle, funnel placed 10k→shipped 8343→delivered 6688→returned 1586, avg 5 ngày giao); additivity additive/semi-additive/non-additive; fix DATE+int; 8 stmts OK — `projects/03-data-modeling/06_fact_types.sql`, `notes/19-fact-types.md`
- [2026-06-26 07:03] T027 — NoSQL modeling: document model (200 JSON lồng embed customer+items), embedding vs referencing, query không-JOIN + DuckDB read_json_auto; notes 4 họ NoSQL, CAP, SQL vs NoSQL — `projects/03-data-modeling/07_nosql_modeling.py`, `notes/20-nosql.md`
- [2026-06-26 07:30] T028 — Phase 2 review: summary + cheat-sheet modeling/SCD/fact-types + self-assessment; mở rộng run_all.sh (4 script Phase 2) = ALL GREEN (9 SQL + 11 Python + pytest). **HOÀN THÀNH PHASE 2 (9/9).** — `notes/00-phase2-summary.md`, `scripts/run_all.sh`

## Batch #4 — Phase 3: Data Warehousing & Analytics Engineering (dbt)
<!-- Loop thêm dòng vào đây khi hoàn thành task Phase 3 -->
- [2026-06-26 08:00] T029 — dbt-duckdb setup: scaffold projects/04-dbt (dbt_project/profiles/packages), sources đọc parquet qua external_location; dbt deps (dbt_utils 1.4.0)+debug(all passed)+run smoke (2000 customers) OK; notes warehouse/ELT/cloud DW/dbt — `projects/04-dbt/*`, `notes/21-warehouse-dbt.md`
- [2026-06-26 08:03] T030 — 4 staging models (stg_customers/products/orders/order_items) view, rename/cast, source() vs ref(), 1-1 với source; dbt run -s staging PASS=4 — `projects/04-dbt/models/staging/*`, `notes/22-dbt-staging.md`
- [2026-06-26 08:30] T031 — Intermediate (int_sales_enriched) + marts (dim_customer/dim_product/fct_sales 30135/mart_revenue_by_category); dbt run PASS=9 theo DAG; Grocery 1.714M khớp (5 cách triển khai đều khớp) — `projects/04-dbt/models/intermediate|marts/*`, `notes/23-dbt-marts.md`
- [2026-06-26 08:33] T032 — dbt tests ⭐: schema.yml generic (unique/not_null/accepted_values/relationships FK) + 1 singular (revenue≥0); dbt test PASS=17 — `projects/04-dbt/models/marts/_marts.yml`, `tests/assert_revenue_non_negative.sql`, `notes/24-dbt-tests.md`
- [2026-06-26 09:00] T033 — Macros & Jinja: macro price_tier + dbt_utils.generate_surrogate_key (hash key) trong dims, Jinja for-loop pivot status→4 cột; fix bug Jinja parse trong comment SQL; dbt run PASS=10, test vẫn 17 PASS — `projects/04-dbt/macros/price_tier.sql`, `models/marts/mart_sales_by_status.sql`, `notes/25-dbt-macros.md`
- [2026-06-26 09:10] T034 — Snapshots SCD2 ⭐ (strategy check, check_cols country/city); chạy 2 lần (mô phỏng đổi country qua var) → khách #1 có 2 phiên bản US→ZZ với dbt_valid_from/to (current = valid_to NULL) — `projects/04-dbt/snapshots/scd_customer.sql`, `notes/26-dbt-snapshots.md`
- [2026-06-26 09:37] T035 — Incremental model fct_daily_sales_inc (is_incremental, {{this}} watermark, delete+insert/unique_key); RUN1 full cutoff=547 rows → RUN2 incremental append=730 rows (chỉ ngày mới); notes 4 strategies — `projects/04-dbt/models/marts/fct_daily_sales_inc.sql`, `notes/27-dbt-incremental.md`
- [2026-06-26 09:40] T036 — Seeds (country_region.csv→mart_revenue_by_region: APAC 7.73M/EMEA 3.76M/Americas 1.27M) + dbt docs generate (manifest.json 31 nodes + catalog.json); notes docs/lineage/exposures/dbt build — `projects/04-dbt/seeds/`, `models/marts/mart_revenue_by_region.sql`, `notes/28-dbt-docs-lineage.md`
- [2026-06-26 10:00] T037 — Phase 3 review: summary + dbt cheat-sheet + self-assessment; thêm `dbt build` vào run_all.sh + FIX bug glob *.sql quét nhầm file dbt (loại trừ */04-dbt/*) → ALL GREEN. **HOÀN THÀNH PHASE 3 (9/9).** — `notes/00-phase3-summary.md`, `scripts/run_all.sh`

## Batch #5 — Phase 4: Batch Processing & Big Data (Spark) — NOTES-FIRST
<!-- Chuyển sang notes-first (yêu cầu user): chỉ viết notes, không code/verify -->
- [2026-06-26 10:30] T038 — Distributed computing & MapReduce (scale-up/out, map→shuffle→reduce, data locality, HDFS/object storage, CAP) — `notes/29-distributed-computing.md`
- [2026-06-26 10:30] T039 — Spark architecture & execution model (driver/executor, RDD/DataFrame/Dataset, lazy vs action, DAG, narrow/wide) — `notes/30-spark-model.md`
- [2026-06-26 10:30] T040 — Partitioning & Shuffle (partition sizing, shuffle đắt, repartition/coalesce, data skew + salting/AQE) — `notes/31-partitioning-shuffle.md`
- [2026-06-26 10:30] T041 — Joins & Catalyst (broadcast/sort-merge/shuffle-hash, Catalyst/Tungsten/AQE, pushdown) — `notes/32-joins-catalyst.md`
- [2026-06-26 10:30] T042 — Spark performance tuning (small-files, spill, cache, shuffle partitions, tránh UDF Python, Spark UI) — `notes/33-spark-tuning.md`
- [2026-06-26 10:30] T043 — Delta Lake (_delta_log, ACID, time travel, schema evolution, MERGE, OPTIMIZE/Z-order/VACUUM) — `notes/34-delta-lake.md`
- [2026-06-26 10:30] T044 — Iceberg/Hudi & so sánh table formats (hidden partitioning, CoW/MoR, catalog) — `notes/35-table-formats.md`
- [2026-06-26 10:30] T045 — Lakehouse architecture + Medallion (lake/warehouse/lakehouse, 4 lớp, bronze/silver/gold) — `notes/36-lakehouse-arch.md`
- [2026-06-26 10:30] T046 — Phase 4 review + cheat-sheet. **HOÀN THÀNH PHASE 4 (9/9, notes-first).** — `notes/00-phase4-summary.md`

## Batch #6 — Phase 5: Workflow Orchestration (Airflow) — NOTES-FIRST
- [2026-06-26 10:45] T047 — Orchestration intro (cron limits, DAG, Airflow/Dagster/Prefect) — `notes/37-orchestration-intro.md`
- [2026-06-26 10:45] T048 — Airflow core (DAG/task/operator/sensor/hook, scheduler/executor/metadata/webserver) — `notes/38-airflow-core.md`
- [2026-06-26 10:45] T049 — Scheduling/execution_date/catchup/backfill (data interval, logical_date) — `notes/39-airflow-scheduling.md`
- [2026-06-26 10:45] T050 — Idempotency & pipeline patterns (partition overwrite, upsert, atomic publish, fan-in/out) — `notes/40-pipeline-patterns.md`
- [2026-06-26 10:45] T051 — XCom/TaskFlow/dynamic mapping — `notes/41-airflow-taskflow.md`
- [2026-06-26 10:45] T052 — Connections/Variables/Pools/Operators — `notes/42-airflow-resources.md`
- [2026-06-26 10:45] T053 — Retries/SLA/alerting/monitoring — `notes/43-airflow-reliability.md`
- [2026-06-26 10:45] T054 — Dagster (assets) & Prefect vs Airflow — `notes/44-dagster-prefect.md`
- [2026-06-26 10:45] T055 — Phase 5 review + cheat-sheet. **HOÀN THÀNH PHASE 5 (9/9).** — `notes/00-phase5-summary.md`

## Batch #7 — Phase 6: Streaming & Real-time (Kafka) — NOTES-FIRST
- [2026-06-26 11:00] T056 — Streaming vs batch & event-driven — `notes/45-streaming-intro.md`
- [2026-06-26 11:00] T057 — Kafka core (topic/partition/offset/replication/ISR/acks) — `notes/46-kafka-core.md`
- [2026-06-26 11:00] T058 — Consumer groups & delivery semantics (at-most/least/exactly-once) — `notes/47-kafka-consumers.md`
- [2026-06-26 11:00] T059 — Kafka ecosystem (Connect, Schema Registry, retention vs compaction) — `notes/48-kafka-ecosystem.md`
- [2026-06-26 11:00] T060 — Stream processing (windowing/watermark/state/output modes) — `notes/49-stream-processing.md`
- [2026-06-26 11:00] T061 — Flink & engines so sánh — `notes/50-flink.md`
- [2026-06-26 11:00] T062 — CDC & Debezium (log-based, outbox) — `notes/51-cdc-debezium.md`
- [2026-06-26 11:00] T063 — Lambda vs Kappa — `notes/52-lambda-kappa.md`
- [2026-06-26 11:00] T064 — Phase 6 review + cheat-sheet. **HOÀN THÀNH PHASE 6 (9/9).** — `notes/00-phase6-summary.md`

## Batch #8 — Phase 7: Cloud & Infrastructure — NOTES-FIRST
- [2026-06-26 11:15] T065 — Docker & containers — `notes/53-docker.md`
- [2026-06-26 11:15] T066 — docker-compose & Kubernetes — `notes/54-compose-k8s.md`
- [2026-06-26 11:15] T067 — Cloud fundamentals + S3 + IAM — `notes/55-cloud-fundamentals.md`
- [2026-06-26 11:15] T068 — AWS data stack (+GCP/Azure map) — `notes/56-aws-data-stack.md`
- [2026-06-26 11:15] T069 — Terraform (IaC) — `notes/57-terraform.md`
- [2026-06-26 11:15] T070 — CI/CD cho data — `notes/58-cicd.md`
- [2026-06-26 11:15] T071 — Cost & FinOps — `notes/59-cost-finops.md`
- [2026-06-26 11:15] T072 — Phase 7 review. **HOÀN THÀNH PHASE 7 (8/8).** — `notes/00-phase7-summary.md`

## Batch #9 — Phase 8: Data Quality, Governance & Observability — NOTES-FIRST
- [2026-06-26 11:30] T073 — Data quality dimensions & testing (GE/Soda/dbt) — `notes/60-data-quality.md`
- [2026-06-26 11:30] T074 — Data contracts — `notes/61-data-contracts.md`
- [2026-06-26 11:30] T075 — Data observability (5 trụ cột) — `notes/62-observability.md`
- [2026-06-26 11:30] T076 — Lineage & catalog — `notes/63-lineage-catalog.md`
- [2026-06-26 11:30] T077 — Governance, PII, GDPR, security — `notes/64-governance-pii.md`
- [2026-06-26 11:30] T078 — Phase 8 review. **HOÀN THÀNH PHASE 8 (6/6).** — `notes/00-phase8-summary.md`

## Batch #10 — Phase 9: Capstone Projects — NOTES-FIRST
- [2026-06-26 11:45] T079 — Portfolio & cách trình bày dự án DE — `notes/65-capstone-portfolio.md`
- [2026-06-26 11:45] T080 — Capstone A: Batch Analytics Platform — `notes/66-capstone-batch.md`
- [2026-06-26 11:45] T081 — Capstone B: Streaming Pipeline — `notes/67-capstone-streaming.md`
- [2026-06-26 11:45] T082 — Capstone C: Lakehouse — `notes/68-capstone-lakehouse.md`
- [2026-06-26 11:45] T083 — Course wrap-up (career + index toàn khoá). **HOÀN THÀNH PHASE 9 (5/5).** — `notes/00-phase9-summary.md`, `notes/00-COURSE-COMPLETE.md`

## 🎓 CURRICULUM HOÀN TẤT — 9/9 PHASE (toàn bộ ROADMAP)
Phase 0–3: code chạy được + verified (run_all.sh ALL GREEN). Phase 4–9: notes-first (theo yêu cầu user). Tổng 68 note chủ đề + 10 note tổng kết. Index: `notes/00-COURSE-COMPLETE.md`.

## Track 2 (Advanced) — Batch #11: Module A SQL Mastery — NOTES-FIRST (overnight loop)
- [2026-06-26 12:00] A01 — Advanced SQL: gaps & islands, sessionization, frame ROWS/RANGE/GROUPS — `notes/advanced/a01-sql-gaps-islands.md`
- [2026-06-26 12:00] A02 — Advanced SQL: pivot/unpivot, recursive hierarchical, dedup strategies — `notes/advanced/a02-sql-pivot-hierarchical.md`
- [2026-06-26 12:00] A03 — Analytics patterns: funnel, cohort/retention, RFM — `notes/advanced/a03-analytics-patterns.md`
- [2026-06-26 12:30] A04 — SQL interview problems set 1 (10 bài + lời giải: nth-highest, top-N, consecutive, median...) — `notes/advanced/a04-sql-interview-1.md`
- [2026-06-26 12:30] A05 — SQL interview problems set 2 (window-heavy: MoM/YoY, cohort, affinity, Pareto, median/group) — `notes/advanced/a05-sql-interview-2.md`
- [2026-06-26 12:30] A06 — SQL performance & optimization (sargable, anti-patterns, EXPLAIN, OLAP pruning) — `notes/advanced/a06-sql-optimization.md`
- [2026-06-26 12:30] A07 — SQL conceptual Q&A (20+ câu phỏng vấn + đáp án) — `notes/advanced/a07-sql-qa.md`
- [2026-06-26 12:30] A08 — Module A review + cheat-sheet. **HOÀN THÀNH MODULE A (8/8).** — `notes/advanced/00-moduleA-summary.md`

## Track 2 — Batch #12: Module B Interview Q&A — NOTES-FIRST (overnight)
- [2026-06-26 13:00] B01 — Spark & Big Data Q&A (15+ câu) — `notes/advanced/b01-spark-qa.md`
- [2026-06-26 13:00] B02 — Streaming & Kafka Q&A — `notes/advanced/b02-kafka-qa.md`
- [2026-06-26 13:00] B03 — Warehousing & dbt Q&A — `notes/advanced/b03-dbt-qa.md`
- [2026-06-26 13:00] B04 — Orchestration & Reliability Q&A — `notes/advanced/b04-orchestration-qa.md`
- [2026-06-26 13:00] B05 — Cloud & Infra Q&A — `notes/advanced/b05-cloud-qa.md`
- [2026-06-26 13:30] B06 — Data modeling Q&A sâu (grain/fan-out/SCD/additivity/conformed/Data Vault/late-arriving/bridge) — `notes/advanced/b06-modeling-qa.md`
- [2026-06-26 13:30] B07 — Behavioral & scenario (STAR + 10 câu + hỏi ngược) — `notes/advanced/b07-behavioral-star.md`
- [2026-06-26 13:30] B08 — "Explain like senior" 10 khái niệm sâu (idempotency/exactly-once/shuffle/SCD2/CAP/...) — `notes/advanced/b08-explain-senior.md`
- [2026-06-26 13:30] B08b — Module B review. **HOÀN THÀNH MODULE B (8/8).** — `notes/advanced/00-moduleB-summary.md`

## Track 2 — Batch #13: Module C System Design — NOTES-FIRST (overnight)
- [2026-06-26 14:00] C01 — System design framework (6 bước, batch/stream/lambda, trade-off) — `notes/advanced/c01-system-design-framework.md`
- [2026-06-26 14:00] C02 — Case: E-commerce analytics platform (CDC+lakehouse+dbt+real-time inventory) — `notes/advanced/c02-case-ecommerce.md`
- [2026-06-26 14:00] C03 — Case: Real-time fraud detection (Flink, feature store, exactly-once) — `notes/advanced/c03-case-fraud.md`
- [2026-06-26 14:00] C04 — Case: IoT/sensor platform (edge, time-series, rollup, out-of-order) — `notes/advanced/c04-case-iot.md`
- [2026-06-26 14:30] C05 — Case ride-sharing (geospatial H3, surge, accumulating snapshot trip) — `notes/advanced/c05-case-ridesharing.md`
- [2026-06-26 14:30] C06 — Case clickstream (tỉ event, Schema Registry, OBT, sessionization, sampling) — `notes/advanced/c06-case-clickstream.md`
- [2026-06-26 14:30] C07 — Case fintech ledger (double-entry, idempotency, immutable, reconciliation) — `notes/advanced/c07-case-fintech.md`
- [2026-06-26 14:30] C08 — Case ad-tech RTB (lambda, <100ms bidder, attribution window) — `notes/advanced/c08-case-adtech.md`
- [2026-06-26 14:30] C09 — Case recommendation (feature store, train/serve consistency, point-in-time) — `notes/advanced/c09-case-recsys.md`
- [2026-06-26 14:30] C09b — Module C review. **HOÀN THÀNH MODULE C (10/10).** — `notes/advanced/00-moduleC-summary.md`

## Track 2 — Batch #14: Module D Tool Deep-dives — NOTES-FIRST (overnight)
- [2026-06-26 15:00] D01 — Spark internals (unified memory/spill, Tungsten codegen, AQE sâu, debug Spark UI) — `notes/advanced/d01-spark-internals.md`
- [2026-06-26 15:00] D02 — dbt advanced (semantic layer/metrics, packages, project lớn, slim CI, contracts) — `notes/advanced/d02-dbt-advanced.md`
- [2026-06-26 15:00] D03 — Kafka internals (log segments, page cache/zero-copy, replication/ISR/HW, EOS sâu, tuning) — `notes/advanced/d03-kafka-internals.md`
- [2026-06-26 15:00] D04 — Snowflake deep (3 lớp, virtual warehouse, micro-partition/pruning, clustering, zero-copy clone, tối ưu chi phí) — `notes/advanced/d04-snowflake.md`
- [2026-06-26 15:30] D05 — BigQuery deep (Dremel/slot/Colossus, bytes-scanned, partition+cluster, MV) — `notes/advanced/d05-bigquery.md`
- [2026-06-26 15:30] D06 — Airflow advanced (dynamic DAG, deferrable, TaskGroup, datasets, scale) — `notes/advanced/d06-airflow-advanced.md`
- [2026-06-26 15:30] D07 — Iceberg deep (metadata layers, hidden+partition evolution, catalog, vs Delta) — `notes/advanced/d07-iceberg.md`
- [2026-06-26 15:30] D08 — Module D review. **HOÀN THÀNH MODULE D (8/8).** — `notes/advanced/00-moduleD-summary.md`

## Track 2 — Batch #15: Module E Advanced Modeling — NOTES-FIRST (overnight)
- [2026-06-26 16:00] E01 — Data Vault 2.0 (hub/link/satellite, audit/parallel load, raw vs business vault) — `notes/advanced/e01-data-vault.md`
- [2026-06-26 16:00] E02 — OBT/Wide/Activity schema (denormalize hoàn toàn, columnar, vs star) — `notes/advanced/e02-obt-wide.md`
- [2026-06-26 16:00] E03 — Event/clickstream modeling (JSON/STRUCT property, schema evolution, sessionization) — `notes/advanced/e03-event-modeling.md`
- [2026-06-26 16:00] E04 — Bitemporal (valid vs transaction time, backdated correction) — `notes/advanced/e04-bitemporal.md`
- [2026-06-26 16:00] E05 — Semantic layer & metrics (metric drift, headless BI, MetricFlow/Cube) — `notes/advanced/e05-semantic-layer.md`
- [2026-06-26 16:00] E06 — Module E review (so sánh Kimball/Inmon/DV/OBT). **HOÀN THÀNH MODULE E (6/6).** — `notes/advanced/00-moduleE-summary.md`

## Track 2 — Batch #16: Module F DataOps/Architecture/Career — NOTES-FIRST (overnight)
- [2026-06-26 16:30] F01 — Data testing strategy (kim tự tháp test, code vs data, shift-left) — `notes/advanced/f01-testing-strategy.md`
- [2026-06-26 16:30] F02 — Reliability & incident mgmt SRE (SLI/SLO/error budget, incident lifecycle, runbook, blameless postmortem) — `notes/advanced/f02-reliability-sre.md`
- [2026-06-26 16:30] F03 — Modern data stack & chọn tool (bản đồ MDS, build vs buy, tiêu chí) — `notes/advanced/f03-modern-data-stack.md`
- [2026-06-26 16:30] F04 — Cost optimization case studies (4 case số liệu thật, quy trình FinOps audit) — `notes/advanced/f04-cost-cases.md`
- [2026-06-26 17:00] F05 — Data mesh & team topology (4 nguyên tắc, data product, khi nào KHÔNG mesh) — `notes/advanced/f05-data-mesh.md`
- [2026-06-26 17:00] F06 — DataOps & CI/CD nâng cao (automation, version everything, blue-green data deploy) — `notes/advanced/f06-dataops.md`
- [2026-06-26 17:00] F07 — Career roadmap (junior→staff, T-shaped, nhánh nghề, AI/LLM tác động) — `notes/advanced/f07-career-roadmap.md`
- [2026-06-26 17:00] F08 — Module F review + Track 2 INDEX (A–F). **HOÀN THÀNH MODULE F + TOÀN BỘ ADVANCED.md (6 module).** — `notes/advanced/00-moduleF-summary.md`, `notes/advanced/00-INDEX.md`

## Track 2 — Batch #17: Extra G (đào sâu) — NOTES-FIRST (overnight)
- [2026-06-26 17:30] G01 — SQL interview set 3 (nth/group, conditional running total, date spine, ties, recursive path, self-join inequality) — `notes/advanced/g01-sql-interview-3.md`
- [2026-06-26 17:30] G02 — SQL interview set 4 analytics (retention curve, cohort LTV, churn, DAU/MAU, percent_rank) — `notes/advanced/g02-sql-interview-4.md`
- [2026-06-26 17:30] G03 — Case log analytics/observability (Kafka buffer, ClickHouse/ES, tiered retention, cardinality explosion) — `notes/advanced/g03-case-log-analytics.md`
- [2026-06-26 17:30] G04 — Case gaming telemetry (Redis leaderboard, anti-cheat stateful, economy ledger, retention) — `notes/advanced/g04-case-gaming.md`
- [2026-06-26 18:00] G05 — Case healthcare (HIPAA/PHI, de-identify, audit, FHIR, bitemporal bệnh án) — `notes/advanced/g05-case-healthcare.md`
- [2026-06-26 18:00] G06 — Case ML feature platform & data cho LLM/RAG (feature store point-in-time, chunk/embed/vector DB, incremental) — `notes/advanced/g06-case-ml-llm-data.md`
- [2026-06-26 18:00] G07 — DS&A cho DE (hash join, external sort, B-tree vs LSM-tree, heap top-K) — `notes/advanced/g07-dsa-for-de.md`
- [2026-06-26 18:00] G08 — Probabilistic DS (HyperLogLog, bloom filter, t-digest, count-min; approx query) — `notes/advanced/g08-probabilistic-ds.md`. **HOÀN THÀNH EXTRA G (8/8).**

## Track 2 — Batch #18: Extra H — NOTES-FIRST (overnight)
- [2026-06-26 18:30] H01 — SQL set 5 window edge cases (LAST_VALUE frame, RANGE/ROWS ties, carry-forward LOCF, QUALIFY, running distinct, deterministic tie-break) — `notes/advanced/h01-sql-interview-5.md`
- [2026-06-26 18:30] H02 — Case marketplace two-sided (GMV, take rate, supply-demand, 2 cohort, search ranking) — `notes/advanced/h02-case-marketplace.md`
- [2026-06-26 18:30] H03 — Case SaaS metrics (MRR movement new/expansion/churn, logo vs revenue churn, SCD2 subscription, LTV/CAC) — `notes/advanced/h03-case-saas-metrics.md`
- [2026-06-26 18:30] H04 — Case social graph (graph vs edge table, fan-out write/read/hybrid feed, FoF, supernode skew) — `notes/advanced/h04-case-social-graph.md`
- [2026-06-26 19:00] H05 — Trino/Presto & federation (MPP no-storage, query across nguồn, vs Spark SQL) — `notes/advanced/h05-trino-federation.md`
- [2026-06-26 19:00] H06 — Real-time OLAP (ClickHouse/Druid/Pinot, sub-giây user-facing, MergeTree, pre-agg) — `notes/advanced/h06-realtime-olap.md`
- [2026-06-26 19:00] H07 — Mock interview đầy đủ (SQL+system design+conceptual+behavioral, tips đánh giá) — `notes/advanced/h07-mock-interview.md`
- [2026-06-26 19:00] H08 — Extra H review + self-assessment tổng. **HOÀN THÀNH EXTRA H (7+1).** — `notes/advanced/00-extraH-summary.md`

## Track 2 — Batch #19: Extra I — NOTES-FIRST (overnight)
- [2026-06-26 19:30] I01 — SQL set 6 tricky (merge intervals, NOT IN+NULL, correlated→window, gaps, EXISTS vs IN vs JOIN) — `notes/advanced/i01-sql-interview-6.md`
- [2026-06-26 19:30] I02 — Case logistics/supply-chain (shipment accumulating snapshot, inventory semi-additive, geospatial) — `notes/advanced/i02-case-logistics.md`
- [2026-06-26 19:30] I03 — Case video streaming (QoE real-time, watch-time, audience retention, Druid OLAP) — `notes/advanced/i03-case-video-streaming.md`
- [2026-06-26 19:30] I04 — Case banking core/payments (double-entry, exactly-once, reconciliation, AML, bitemporal reporting) — `notes/advanced/i04-case-banking.md`
- [2026-06-26 20:00] I05 — Spark tuning scenarios (OOM/skew/small-files/shuffle/spill/UDF: triệu chứng→fix) — `notes/advanced/i05-spark-tuning-scenarios.md`
- [2026-06-26 20:00] I06 — DQ framework chi tiết (GE/Soda/dbt mỗi tầng, DQ score, quarantine/circuit-breaker) — `notes/advanced/i06-dq-framework.md`
- [2026-06-26 20:00] I07 — Backfill & reprocessing (idempotent, partition overwrite/blue-green/Kappa replay, kiểm soát tải) — `notes/advanced/i07-backfill-reprocessing.md`
- [2026-06-26 20:00] I08 — Extra I review. **HOÀN THÀNH EXTRA I (7+1).** — `notes/advanced/00-extraI-summary.md`

## Track 2 — Batch #20: Extra J — NOTES-FIRST (overnight)
- [2026-06-26 20:30] J01 — SQL set 7 mixed hard (running max, conditional islands, time-weighted avg, dedup đầy đủ nhất) — `notes/advanced/j01-sql-interview-7.md`
- [2026-06-26 20:30] J02 — Case telecom/CDR (mediation, rating, charging real-time, fraud SIM box, billing chính xác) — `notes/advanced/j02-case-telecom.md`
- [2026-06-26 20:30] J03 — Case energy/smart meter (VEE, interval data, gap-fill, rollup, anomaly trộm điện) — `notes/advanced/j03-case-energy.md`
- [2026-06-26 20:30] J04 — Case govtech (Data Vault tích hợp, MDM, de-identify/k-anonymity, open data, privacy) — `notes/advanced/j04-case-govtech.md`
- [2026-06-26 21:00] J05 — Streaming exactly-once thực chiến (3 điểm trùng/mất, idempotent producer+transaction+sink upsert) — `notes/advanced/j05-streaming-eos.md`
- [2026-06-26 21:00] J06 — Lakehouse migration (dual-run+validate+blue-green cutover, Hive→Iceberg in-place, audit_helper) — `notes/advanced/j06-lakehouse-migration.md`
- [2026-06-26 21:00] J07 — dbt at scale (domain+layer, contracts/exposures, slim CI, semantic layer, tránh spaghetti) — `notes/advanced/j07-dbt-at-scale.md`
- [2026-06-26 21:00] J08 — Extra J review. **HOÀN THÀNH EXTRA J (7+1).** — `notes/advanced/00-extraJ-summary.md`

## Track 2 — Batch #21: Extra K — NOTES-FIRST (overnight)
- [2026-06-26 21:30] K01 — SQL set 8 (max concurrent, asof join, hierarchical rollup, sequence gap, divide-by-zero) — `notes/advanced/k01-sql-interview-8.md`
- [2026-06-26 21:30] K02 — Case insurance (bitemporal policy/claim, accumulating snapshot claims, loss ratio, reserving/IBNR) — `notes/advanced/k02-case-insurance.md`
- [2026-06-26 21:30] K03 — Case real estate/PropTech (MDM address, SCD2 listing/price history, AVM as-of comparables) — `notes/advanced/k03-case-realestate.md`
- [2026-06-26 21:30] K04 — Case agritech (sensor+imagery NDVI+weather, yield prediction, edge buffer) — `notes/advanced/k04-case-agritech.md`
- [2026-06-26 22:00] K05 — Vector DB & RAG sâu (HNSW/IVF ANN, chunking, hybrid search BM25+vector+rerank, RAG eval, incremental re-embed) — `notes/advanced/k05-vector-rag-deep.md`
- [2026-06-26 22:00] K06 — Data contract implementation (YAML schema+SLA+semantics, enforce 4 điểm, SemVer dual-publish) — `notes/advanced/k06-data-contract-impl.md`
- [2026-06-26 22:00] K07 — Observability tooling (5 trụ đo cụ thể, rule vs anomaly, Elementary/Soda/Monte Carlo, SLO) — `notes/advanced/k07-observability-tooling.md`
- [2026-06-26 22:00] K08 — Extra K review. **HOÀN THÀNH EXTRA K (7+1).** — `notes/advanced/00-extraK-summary.md`

## Track 2 — Batch #23: Module AI Data Engineering ⭐ (tiêu chuẩn phỏng vấn mới) — overnight
- [2026-06-26 22:30] AI01 — ⭐ RAG capstone CHẠY ĐƯỢC: chunk 169 notes→1454 chunks, fastembed bge-small (local, no API/Java), DuckDB vector store + HNSW, hybrid search, incremental idempotent (re-embed chỉ file đổi, lần 2: 0.2s), recall@5=88% — `projects/06-ai-data-engineering/rag_over_notes.py` + README; +fastembed
- [2026-06-26 23:00] AI02 — RAG capstone writeup + kiến trúc (sơ đồ, trade-off, "cái gì vỡ khi scale", bảng ETL cũ↔RAG mới) — `notes/advanced/ai02-rag-capstone-writeup.md`
- [2026-06-26 23:00] AI03 — Chunking strategies sâu (fixed/semantic/structure-aware/parent-child, overlap, đo size bằng recall) — `notes/advanced/ai03-chunking.md`
- [2026-06-26 23:00] AI04 — Embedding models & versioning ⭐ (chọn model, đổi model=re-embed toàn bộ, blue-green index, cache/batch) — `notes/advanced/ai04-embedding-versioning.md`
- [2026-06-26 23:00] AI05 — Retrieval eval sâu + MỞ RỘNG capstone (recall@k/MRR/nDCG chạy được: recall=88%/MRR=0.542/nDCG=0.853; re-ranking, RAGAS/faithfulness) — `notes/advanced/ai05-retrieval-eval.md`, `rag_over_notes.py`
- [2026-06-27 11:00] AI06 — ⭐⭐ LLM-output governance (CODE CHẠY): parse→validate(pydantic contract)→repair→quarantine + provenance(model+prompt+input+status); demo 8 input→6 production/2 quarantine — `projects/06-ai-data-engineering/llm_output_pipeline.py`, `notes/advanced/ai06-llm-output-governance.md`
- [2026-06-27 11:00] AI07 — ⭐⭐ Test non-deterministic (CODE CHẠY): semantic equivalence bằng cosine (khác chữ cùng nghĩa pass, khác nghĩa fail, 9/9) + schema validation; 7 chiến lược test output LLM — `projects/06-ai-data-engineering/test_semantic.py`, `notes/advanced/ai07-testing-nondeterministic.md`
- [2026-06-27 11:30] AI08 — Cost & latency AI pipeline (token cost, cache/batch embedding, LLM generation đắt nhất, unit economics, latency budget) — `notes/advanced/ai08-ai-cost-latency.md`
- [2026-06-27 11:30] AI09 — Streaming AI infra (event-driven re-index <1', "vỡ gì khi ×2" theo tầng, đừng over-stream) — `notes/advanced/ai09-streaming-ai.md`
- [2026-06-27 11:30] AI10 — Module AI review + map 3 câu phỏng vấn mới + bảng "ETL cũ↔AI mới". **HOÀN THÀNH MODULE AI (10 task + 3 script chạy được).** — `notes/advanced/ai10-summary.md`, `00-INDEX.md`

## Track 2 — Batch #24: AI-Advanced (đẩy mạnh AI/LLM) ⭐ — overnight
- [2026-06-27 12:00] AA01 — ⭐ Text-to-SQL CHẠY ĐƯỢC (schema linking + guardrail chặn DROP/UPDATE + EXPLAIN validate + sandbox read-only); revenue khớp — `projects/06-ai-data-engineering/text_to_sql.py`, `notes/advanced/aa01-text-to-sql.md`
- [2026-06-27 12:00] AA02 — ⭐⭐ Guardrails CHẠY ĐƯỢC (PII redaction email/phone/CCCD + prompt injection EN/VN + grounding cosine calibrate 0.75) — `projects/06-ai-data-engineering/guardrails_demo.py`, `notes/advanced/aa02-guardrails.md`
- [2026-06-27 12:00] AA03 — RAG production patterns (semantic cache, citations, fallback, query rewrite/HyDE, rerank, multi-tenancy, online eval) — `notes/advanced/aa03-rag-production.md`
- [2026-06-27 12:00] AA04 — ⭐ Training data prep CHẠY ĐƯỢC (MinHash+LSH near-dup: 3 candidate vs 21 brute-force, bắt exact+reword; decontamination, quality filter) — `projects/06-ai-data-engineering/dedup_minhash.py`, `notes/advanced/aa04-training-data-prep.md`
- [2026-06-27 12:30] AA05 — Agentic data pipelines (ReAct loop, tool use, self-healing, rủi ro loop/cost/hành-động-nguy-hiểm + DE giám sát: guardrail/human-approval/budget cap/trace) — `notes/advanced/aa05-agentic-pipelines.md`
- [2026-06-27 12:30] AA06 — LLM eval frameworks (RAGAS: faithfulness/relevance/context precision-recall, golden dataset, LLM-judge bias, offline vs online, regression) — `notes/advanced/aa06-llm-eval.md`
- [2026-06-27 12:30] AA07 — Prompt management & versioning (prompt as code, registry, SemVer, regression eval, A/B, lineage prompt→output) — `notes/advanced/aa07-prompt-management.md`
- [2026-06-27 12:30] AA08 — Multimodal pipelines (CLIP/OCR/Whisper, cross-modal search, multimodal RAG, object store + cost/incremental) — `notes/advanced/aa08-multimodal.md`
- [2026-06-27 13:00] AA09 — GraphRAG + knowledge graph (LLM trích entity/relation, entity resolution, graph+vector hybrid, multi-hop, khi nào > vector RAG) — `notes/advanced/aa09-graphrag.md`
- [2026-06-27 13:00] AA10 — LLMOps + vector DB at scale (version/deploy/monitor/cost/safety, quality drift, ANN/PQ/sharding, API vs self-host) + tổng kết AI-Advanced. **HOÀN THÀNH AI-ADVANCED (AA01–AA10 + 3 script mới).** — `notes/advanced/aa10-llmops.md`, `00-INDEX.md`

## Track 2 — Batch #25: AI-Advanced 2 (đẩy mạnh AI/LLM) ⭐ — overnight
- [2026-06-27 13:30] AB01 — ⭐ Synthetic Data Generation CHẠY ĐƯỢC (mock-LLM + 4 cổng chất lượng: quality/dedup/diversity/balance; 144 thô→42 sạch, diversity 0.09→0.34; mode collapse, bias amplify, drift, model collapse) — `projects/06-ai-data-engineering/synthetic_data.py`, `notes/advanced/ab01-synthetic-data.md`
- [2026-06-27 13:30] AB02 — ⭐ RAG Eval Harness CHẠY ĐƯỢC (sweep config trên capstone: hybrid k=5 88% > vector-only 75%, k↑→recall↑ MRR phẳng; nDCG sửa chia IDCG ∈[0,1]; harness→CI gate) — `projects/06-ai-data-engineering/rag_eval_harness.py`, `notes/advanced/ab02-rag-eval-harness.md`
- [2026-06-27 13:30] AB03 — Context Engineering & Memory (token budget, lost-in-the-middle, short-term vs long-term=RAG, truncate/summarize/retrieve/compress/cache/structured) — `notes/advanced/ab03-context-engineering.md`
- [2026-06-27 13:30] AB04 — Semantic Layer cho LLM (NL→{metric,dim,filter} thay SQL thô: nhất quán/an toàn/ít hallucinate, function-calling có kỷ luật, 80/20 vs text-to-SQL) — `notes/advanced/ab04-semantic-layer-llm.md`
- [2026-06-27 14:00] AB05 — Embedding Fine-tuning & Domain Adaptation (vì sao general kém domain, thứ tự thử rẻ→đắt, contrastive + hard negative, DE=training pairs từ click/feedback + decontaminate + eval, đổi model⇒re-embed) — `notes/advanced/ab05-embedding-finetune.md`
- [2026-06-27 14:00] AB06 — LLM Observability & Tracing (trace/span pipeline, provenance log đầy đủ, LLM logs=clickstream/fact table, Langfuse/LangSmith/Phoenix/OTel, 5 trụ obs áp LLM) — `notes/advanced/ab06-llm-observability.md`
- [2026-06-27 14:00] AB07 — Vector Search Optimization sâu (HNSW M/ef_construction/ef_search, IVF nlist/nprobe, quantization SQ/PQ/binary giảm RAM, pre/post filter, tune bằng SLA+harness vặn 1 nút/lần) — `notes/advanced/ab07-vector-search-opt.md`
- [2026-06-27 14:30] AB08 — Fine-tuning Data Pipeline (4 loại fine-tune, 7 bước thu→clean→decontaminate→format→split→version→eval, DE sở hữu phần data, "data>model", khi nào KHÔNG fine-tune) — `notes/advanced/ab08-finetune-pipeline.md`
- [2026-06-27 14:30] AB09 — AI review 2 + checklist phỏng vấn đầy đủ (8 script→câu phỏng vấn, checklist "AI-DE sẵn sàng", 5 thông điệp lớn, portfolio pitch 60s). **HOÀN THÀNH AI-ADVANCED 2 (AB01–AB09, +2 script: synthetic_data, rag_eval_harness = 8 script AI).** — `notes/advanced/ab09-ai-review2.md`, `00-INDEX.md`

## Track 2 — Batch #26: AI-Advanced 3 (đẩy mạnh AI/LLM) ⭐ — overnight
- [2026-06-27 15:00] AC01 — ⭐ Cross-lingual RAG CHẠY ĐƯỢC (query EN vs VI trên index note VI: recall VI=83% EN=67% chênh +17% = "thuế đa ngữ"; 3 cách khắc phục: model đa ngữ/dịch/per-lang index) — `projects/06-ai-data-engineering/cross_lingual_eval.py`, `notes/advanced/ac01-multilingual-rag.md`
- [2026-06-27 15:00] AC02 — ⭐ Semantic Recsys CHẠY ĐƯỢC (two-tower thu nhỏ: item-tower + user-tower=mean liked, cosine recommend, cold-start nhờ content embedding, "why"=item gần nhất; LLM re-rank/giải thích; point-in-time) — `projects/06-ai-data-engineering/semantic_recsys.py`, `notes/advanced/ac02-recsys-llm.md`
- [2026-06-27 15:30] AC03 — Evaluation-Driven Development (eval-first/TDD cho LLM, golden=spec sống lớn dần theo bug, metric theo tầng retrieval/generation/output/system, EDD→CI gate, vibe-based vs eval-driven) — `notes/advanced/ac03-eval-driven-dev.md`
- [2026-06-27 15:30] AC04 — Multi-agent & Tool Design (1 agent vs multi, 5 mẫu orchestration planner/supervisor/pipeline/parallel/critic, 6 nguyên tắc tool tốt=data access layer, error recovery max-steps/budget/human-approve, trace) — `notes/advanced/ac04-multi-agent.md`
- [2026-06-27 16:00] AC05 — Voice/Audio AI Data Pipeline (STT Whisper→diarization→align→chunk→embed, transcript=fact_utterance, PII kép nội dung+giọng/sinh trắc học, cost batch/incremental/cache/tiering) — `notes/advanced/ac05-voice-audio-pipeline.md`
- [2026-06-27 16:00] AC06 — Knowledge Base Freshness (RAG không build-1-lần, CRUD+reconcile nguồn↔index, phát hiện đổi hash/CDC, mâu thuẫn version/authority/supersede, freshness SLA, right-to-be-forgotten) — `notes/advanced/ac06-kb-freshness.md`
- [2026-06-27 16:00] AC07 — Feature Store cho ML/LLM (online/offline parity, point-in-time correctness + as-of join chống leakage, embedding=feature, Feast/Tecton) — `notes/advanced/ac07-feature-store.md`
- [2026-06-27 16:00] AC08 — Cost Optimization ở scale (routing/cascade model nhỏ↔lớn, cache nhiều tầng exact/semantic/embedding + invalidation, prompt compression, distill, $/query unit economics, budget cap) — `notes/advanced/ac08-ai-cost-scale.md`
- [2026-06-27 16:00] AC09 — AI review 3 + **ngân hàng 45 câu hỏi phỏng vấn AI-DE** (6 nhóm RAG/output/data-cho-AI/eval-LLMOps/kiến-trúc/ML-cost) + portfolio pitch 90s. **HOÀN THÀNH AI-ADVANCED 3 (AC01–AC09, +2 script: cross_lingual_eval, semantic_recsys = 10 script AI).** — `notes/advanced/ac09-ai-review3.md`, `00-INDEX.md`

## Track 2 — Batch #27: AI-Advanced 4 (đẩy mạnh AI/LLM) ⭐ — overnight
- [2026-06-27 16:30] AD01 — ⭐ Streaming/Real-time RAG CHẠY ĐƯỢC (doc mới stream vào → searchable 191ms, incremental embed 1/207 doc, reconcile chống ghost; incremental-embed≠incremental-index HNSW rebuild nghẽn; streaming vs batch đừng over-stream) — `projects/06-ai-data-engineering/streaming_rag.py`, `notes/advanced/ad01-streaming-rag.md`
- [2026-06-27 16:30] AD02 — ⭐ LLM-as-Judge CHẠY ĐƯỢC (rubric grounding+coverage, pointwise/pairwise, GOOD 0.964>VERBOSE 0.555, soi length/position bias; 5 bias + calibrate với nhãn người) — `projects/06-ai-data-engineering/llm_judge.py`, `notes/advanced/ad02-llm-judge.md`
- [2026-06-27 17:00] AD03 — Privacy & Compliance cho LLM (5 rủi ro đặc thù: gửi-ra-API/memorization/log/vector-store/rò-chéo; residency self-host vs API; GDPR/NĐ13 consent/RTBF khó với model fine-tuned; differential privacy; privacy-by-design + audit) — `notes/advanced/ad03-privacy-compliance.md`
- [2026-06-27 17:00] AD04 — LLM Security: Indirect Prompt Injection (lệnh độc giấu trong doc RAG kéo vào; RAG poisoning/exfiltration/tool-abuse/jailbreak; 7 tầng defense-in-depth; LLM=không-đáng-tin; OWASP LLM Top 10; excessive agency) — `notes/advanced/ad04-llm-security.md`
- [2026-06-27 17:30] AD05 — RAG trên dữ liệu CÓ CẤU TRÚC (router định lượng/định tính/hybrid, schema/table retrieval chống nhồi cả DB, semantic layer/guardrail thay SQL thô, citation nguồn số) — `notes/advanced/ad05-structured-rag.md`
- [2026-06-27 17:30] AD06 — Document Parsing & Extraction (rác-vào-rác-ra, thử thách PDF text/scan-OCR/bảng/HTML/code, giữ cấu trúc cho chunk, ETL tài liệu parse→clean→normalize→enrich, đo parse) — `notes/advanced/ad06-doc-parsing.md`
- [2026-06-27 17:30] AD07 — Data cho AI Agents Production (4 trụ: memory/tool-data-layer-governance/state-checkpoint-resume/audit-trace; tool idempotent; demo→prod=infra) — `notes/advanced/ad07-agent-data.md`
- [2026-06-27 17:30] AD08 — ⭐ Semantic Cache CHẠY ĐƯỢC (cosine≠ngữ nghĩa: NGHỊCH LÝ reword cùng nghĩa 0.821 < negation ngược nghĩa 0.976; embedding bất biến thứ tự từ; false-hit>false-miss→ngưỡng cao; cache nhiều tầng + invalidation) — `projects/06-ai-data-engineering/semantic_cache.py`, `notes/advanced/ad08-semantic-cache.md`
- [2026-06-27 17:30] AD09 — AI review 4 + **capstone integration 7 tầng** (guardrail→cache→retrieve→generate→validate→judge→observe) + 5 câu drill phỏng vấn whiteboard + tổng kết toàn Module AI (4 batch, 13 script). **HOÀN THÀNH AI-ADVANCED 4 (AD01–AD09).** — `notes/advanced/ad09-ai-review4.md`, `00-INDEX.md`

## Track 2 — Batch #28: AI-Advanced 5 (đẩy mạnh AI/LLM) ⭐ — overnight
- [2026-06-27 18:00] AE01 — ⭐ Self-Correcting RAG CHẠY ĐƯỢC (retrieve→đo confidence→reformulate HyDE→retry→giữ tốt hơn; conf TB 0.656→0.814 +0.158, top đổi sang note đúng; điều kiện dừng max-retries) — `projects/06-ai-data-engineering/self_correcting_rag.py`, `notes/advanced/ae01-self-correcting-rag.md`
- [2026-06-27 18:00] AE02 — ⭐ GraphRAG từ wikilinks CHẠY ĐƯỢC (graph thật 216 node/1044 cạnh từ [[links]]; hub in-degree=khái niệm nền tảng; hybrid vector-seed×graph-expand multi-hop kéo 32 note vector bỏ sót) — `projects/06-ai-data-engineering/graphrag_links.py`, `notes/advanced/ae02-graphrag-build.md`
- [2026-06-27 18:00] AE03 — ⭐ Data Quality Score CHẠY ĐƯỢC (chấm đa chiều; bài học HARD gate toxic/dup/rỗng loại ngay vs trung bình để rác lọt; giữ 3/8; pipeline DQ + log lý do bỏ) — `projects/06-ai-data-engineering/data_quality_score.py`, `notes/advanced/ae03-training-data-quality.md`
- [2026-06-27 18:30] AE04 — Multimodal RAG sâu (shared embedding space CLIP, 4 hướng cross-modal text↔ảnh, OCR vs visual embedding, caption + object store + ref, pipeline data ảnh cost/incremental) — `notes/advanced/ae04-multimodal-rag.md`
- [2026-06-27 18:30] AE05 — On-device/Edge AI Data (4 động lực privacy/latency/offline/cost, quantize/distill/prune/ONNX, thách thức data phân tán OTA/eval-mù/sync/drift, federated learning + DP, fastembed=edge-friendly) — `notes/advanced/ae05-edge-ai-data.md`
- [2026-06-27 19:00] AE06 — Query Understanding & Routing (4 việc: intent/rewrite/decompose/route; intent→đường đi RAG/SQL/tool/từ-chối; coreference + HyDE; routing là ngã ba quyết định) — `notes/advanced/ae06-query-understanding.md`
- [2026-06-27 19:00] AE07 — Reranking sâu (2 tầng retrieve-rộng×rerank-tinh, bi-encoder vs cross-encoder, ColBERT/LLM-rerank/MMR chống trùng, tăng-k không sửa hạng nên cần rerank) — `notes/advanced/ae07-reranking-deep.md`
- [2026-06-27 19:00] AE08 — RAG cho Code (chunk theo AST/hàm không cắt giữa, embedding code chuyên + hybrid cho định danh, repo-context=GraphRAG import/call graph, incremental theo file) — `notes/advanced/ae08-rag-for-code.md`
- [2026-06-27 19:00] AE09 — AI review 5 + **portfolio 16 script** map kỹ năng→phỏng vấn + định vị career "AI Data Engineer" (trụ cột thứ 4) + 5 thông điệp + tổng kết 5 batch (~55 note + 16 script). **HOÀN THÀNH AI-ADVANCED 5 (AE01–AE09).** — `notes/advanced/ae09-ai-review5.md`, `00-INDEX.md`

## Track 2 — Batch #29: AI-Advanced 6 — Case Studies AI-DE + Scale ⭐ — overnight
- [2026-06-28 08:00] AF01 — Case Study: Customer Support AI (kiến trúc ingest+serve, chống bịa=trích dẫn, escalation "biết khi nào không trả lời", deflection/CSAT eval, feedback loop) — `notes/advanced/af01-case-support-ai.md`
- [2026-06-28 08:00] AF02 — Case Study: Enterprise KB (⭐ permission-aware retrieval pre-filter ACL an-toàn>tiện, connector đa nguồn giữ ACL gốc, freshness mỗi nguồn 1 nhịp, authority rank mâu thuẫn) — `notes/advanced/af02-case-enterprise-kb.md`
- [2026-06-28 08:00] AF03 — Case Study: Coding Assistant (incremental theo commit diff, repo-context=vector+graph import/call, cách ly tenant code=tài sản, latency pre-compute+model nhỏ) — `notes/advanced/af03-case-coding-assistant.md`
- [2026-06-28 08:00] AF04 — Vector DB Internals (HNSW tầng/M/ef, IVF-PQ cụm+nén, DiskANN vector trên SSD vượt RAM, filtered search trong-duyệt, sharding/consistency, chọn DB) — `notes/advanced/af04-vector-db-internals.md`
- [2026-06-28 08:00] AF05 — Training Data Pipeline ở Scale (8 bước web-scale, dedup phân tán MinHash+LSH O(n), tokenize+shard+stream shuffle-buffer, data mixing/weighting quyết định model, idempotent/resumable) — `notes/advanced/af05-training-data-scale.md`
- [2026-06-28 08:30] AF06 — AI Data Governance (lineage AI data→model→prompt→output, model card/datasheet/prompt card, data catalog AI artifact, EU AI Act risk tiers, bias/fairness audit, provenance/consent) — `notes/advanced/af06-ai-data-governance.md`
- [2026-06-28 08:30] AF07 — ⭐ Continuous Eval & Regression Gate CHẠY ĐƯỢC (baseline JSON + gate exit-code: 3 kịch bản tạo/PASS/FAIL, exit 1 chặn CI khi recall tụt >TOL; baseline management đừng-cập-nhật-mù trôi xuống) — `projects/06-ai-data-engineering/continuous_eval.py`, `notes/advanced/af07-continuous-eval.md`
- [2026-06-28 08:30] AF08 — Case Study: Real-time Personalization (2 nhịp offline/online, streaming features+profile rolling kappa/lambda, point-in-time as-of chống leakage, LLM bổ trợ ranking, cold-start content embedding) — `notes/advanced/af08-case-personalization.md`
- [2026-06-28 08:30] AF09 — AI review 6 + **khung 7 bước system-design AI** (clarify→flow→retrieve→safety→eval→scale→cost) + 3 đề có lời giải (enterprise RAG/fraud LLM/email agent) + tổng kết 6 batch (~64 note, 17 script). **HOÀN THÀNH AI-ADVANCED 6 (AF01–AF09).** — `notes/advanced/af09-ai-review6.md`, `00-INDEX.md`

## Track 2 — Batch #30: AI-Advanced 7 — Production AI Systems ⭐ — overnight
- [2026-06-28 09:00] AG01 — RAG cho BI/Analytics (chat-với-data: RAG metadata + semantic layer + engine, LLM không tự tính số, conversational follow-up/coreference, số+giải thích+viz+citation) — `notes/advanced/ag01-rag-bi-analytics.md`
- [2026-06-28 09:00] AG02 — ⭐ Hallucination Detection CHẠY ĐƯỢC (self-consistency cosine bị lừa: bịa cùng-khuôn 0.838>đúng 0.767 NGHỊCH LÝ; phải so FACT-năm mâu thuẫn 2015/2019/2021; grounding 0.870 vs 0.681; cosine≠sự-thật) — `projects/06-ai-data-engineering/hallucination_detect.py`, `notes/advanced/ag02-hallucination-detection.md`
- [2026-06-28 09:00] AG03 — RLHF & Preference Data (chosen/rejected pairs, nguồn human/RLAIF/implicit, chất lượng annotation kappa/gold/guideline, reward hacking bias dài/tự-tin, version) — `notes/advanced/ag03-rlhf-preference-data.md`
- [2026-06-28 09:00] AG04 — ⭐ Drift Detection CHẠY ĐƯỢC (im-lặng-hỏng, 4 loại drift, centroid cosine: cùng-chủ-đề 0.076 vs lạ 0.201 ngưỡng 0.15; calibrate trên nhiễu nền/lịch sử không hardcode mò; PSI/KL/outlier) — `projects/06-ai-data-engineering/drift_detect.py`, `notes/advanced/ag04-drift-detection.md`
- [2026-06-28 09:30] AG05 — Agent Platform Data Infra (5 thành phần: tool registry version/scope/quota, state machine+checkpoint, coordination message/blackboard, run store replay/audit, human-in-loop queue) — `notes/advanced/ag05-agent-platform.md`
- [2026-06-28 09:30] AG06 — Multimodal Production (video/ảnh scale: transcode→frame sampling-dedup-thời-gian→scene→trích đa tầng visual/STT/OCR; cost tiering/batch-GPU/CDN; kiểm duyệt/search) — `notes/advanced/ag06-multimodal-production.md`
- [2026-06-28 09:30] AG07 — Conversational Memory (working/episodic/semantic, long-context vs RAG-memory, tóm tắt phân cấp, entity memory cho fact chính xác, forgetting/TTL/decay) — `notes/advanced/ag07-conversational-memory.md`
- [2026-06-28 09:30] AG08 — Data Contracts AI I/O (schema output=hợp đồng validate ở biên, version prompt+schema cùng nhau, breaking vs non-breaking như Avro, contract test CI, embedding contract) — `notes/advanced/ag08-ai-data-contracts.md`
- [2026-06-28 09:30] AG09 — AI review 7 + **bản đồ 7 trục năng lực AI-DE** + 19 script portfolio + 7 thông điệp cốt lõi + reflection "học-bằng-chạy". **HOÀN THÀNH AI-ADVANCED 7 (AG01–AG09). Tổng 7 batch: ~73 note AI + 19 script.** — `notes/advanced/ag09-ai-review7.md`, `00-INDEX.md`

## Track 2 — Batch #31: AI-Advanced 8 — AI Infrastructure & Frontier ⭐ — overnight
- [2026-06-28 10:00] AH01 — LLM Serving & Inference Infra (KV cache stateful tốn RAM, continuous batching > static, prefill-compute vs decode-memory, TTFT/TPOT, tensor/pipeline parallel, quantize serve) — `notes/advanced/ah01-llm-serving.md`
- [2026-06-28 10:00] AH02 — ⭐ Embedding Benchmark CHẠY ĐƯỢC (PHÁT HIỆN BẤT NGỜ: prefix-OFF 88% > prefix-ON 75% trên corpus Việt vì doc no-prefix + prefix tiếng Anh kéo lệch -> "đo đừng tin mặc định", gợi ý sửa capstone; sweep k; tốc độ 4ms/câu; MTEB) — `projects/06-ai-data-engineering/embedding_benchmark.py`, `notes/advanced/ah02-embedding-benchmark.md`
- [2026-06-28 10:00] AH03 — AI Red-Teaming (taxonomy jailbreak/injection/exfiltration/harm/bias, manual vs automated, red-team=test suite an toàn + gate + regression, adversarial dataset) — `notes/advanced/ah03-red-teaming.md`
- [2026-06-28 10:00] AH04 — Tokenization Deep-dive (BPE/WordPiece/SentencePiece, ⭐ token tax tiếng Việt 2-4× tiếng Anh = đắt + context ngắn, special token/chat template, ước cost/context bằng token thật) — `notes/advanced/ah04-tokenization.md`
- [2026-06-28 10:30] AH05 — Data cho Multimodal LLM Training (image-text pairs LAION-scale, ⭐ CLIP-score filter ảnh-text khớp = tăng chất lượng lớn nhất, captioning/re-caption, dedup ảnh perceptual hash, decontaminate) — `notes/advanced/ah05-multimodal-training-data.md`
- [2026-06-28 10:30] AH06 — RAG Benchmarks công khai (MTEB/BEIR/MS-MARCO/RAGAS, metric nDCG@10/recall, ⭐ leaderboard caveat domain-gap/overfit/contamination → benchmark=shortlist golden-riêng=chọn) — `notes/advanced/ah06-rag-benchmarks.md`
- [2026-06-28 10:30] AH07 — LLM Inference Optimization (speculative decoding draft+verify song song, PagedAttention KV-cache như virtual-memory, flash attention tối ưu memory-I/O, continuous batching, prompt caching) — `notes/advanced/ah07-inference-optimization.md`
- [2026-06-28 10:30] AH08 — AI Agents cho DE meta (text-to-pipeline/self-healing/DQ-tự-động/copilot theo mức rủi ro, DE→người giám sát+gác cổng không biến mất, guardrail review/sandbox/least-privilege/human-in-loop) — `notes/advanced/ah08-ai-agents-for-de.md`
- [2026-06-28 10:30] AH09 — AI review 8 + **bản đồ hạ tầng AI** (data→train→serve→optimize→operate) + 6 xu hướng frontier + bài học "đo đừng tin mặc định" (4 ví dụ code). **HOÀN THÀNH AI-ADVANCED 8 (AH01–AH09). Tổng 8 batch: ~82 note AI + 20 script.** — `notes/advanced/ah09-ai-review8.md`, `00-INDEX.md`
