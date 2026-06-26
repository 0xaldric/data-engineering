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
