# 🛠️ Data Engineering Roadmap — Lộ trình đầy đủ

> Lộ trình thực hành từ zero → job-ready Data Engineer. Mọi thứ chạy được **local** bằng Python + DuckDB + docker-compose, không cần trả tiền cloud. Mỗi phase có lý thuyết (notes) + dự án thực hành (projects).

**Cách dùng:** `task.md` chứa các task cụ thể đang làm. Khi xong hết → sinh batch task mới từ phase tiếp theo của roadmap này. `PROGRESS.md` ghi log những gì đã hoàn thành.

**Triết lý:** Học bằng cách *build*. Mỗi khái niệm phải đi kèm code chạy được + dataset thật + giải thích "tại sao", không chỉ "làm thế nào".

---

## 📍 Tổng quan 10 Phase

| Phase | Chủ đề | Mục tiêu chính | Công cụ |
|-------|--------|----------------|---------|
| 0 | Foundations & Environment | Dev env, shell, Git, SQL nền tảng | Python, DuckDB, Git |
| 1 | Programming for DE | Python data stack, file formats, APIs, testing | pandas, polars, pyarrow, pytest |
| 2 | Databases & Data Modeling | RDBMS, indexing, dimensional modeling, SCD | Postgres, DuckDB |
| 3 | Data Warehousing & Analytics Eng | Columnar storage, dbt, data marts | dbt, DuckDB/BigQuery |
| 4 | Batch Processing & Big Data | Spark, distributed computing, lakehouse | PySpark, Delta/Iceberg |
| 5 | Workflow Orchestration | Airflow/Dagster, idempotency, backfill | Airflow, Dagster |
| 6 | Streaming & Real-time | Kafka, stream processing, CDC | Kafka, Spark Streaming, Debezium |
| 7 | Cloud & Infrastructure | AWS data stack, Docker, Terraform, CI/CD | AWS, Docker, Terraform |
| 8 | Data Quality & Governance | Testing, contracts, lineage, observability | Great Expectations, dbt tests |
| 9 | Capstone Projects | 3 pipeline end-to-end hoàn chỉnh | Tất cả những gì đã học |

---

## Phase 0 — Foundations & Environment

**Mục tiêu:** Có môi trường làm việc vững và đọc/viết SQL thành thạo (kỹ năng #1 của DE).

### 0.1 Dev environment
- Python venv / `uv`, quản lý dependency, `requirements.txt` vs `pyproject.toml`
- Cấu trúc project chuẩn cho data project
- VS Code / Jupyter cho data work

### 0.2 Linux & Shell
- Navigation, pipes, `grep`/`sed`/`awk`, `cron`
- Xử lý file lớn bằng shell (`wc`, `sort`, `uniq`, `cut`, `head/tail`)
- Bash scripting cơ bản cho automation

### 0.3 Git & version control
- Branch, merge, rebase, PR workflow
- `.gitignore` cho data project (không commit data/secrets)

### 0.4 SQL Fundamentals ⭐ (quan trọng nhất)
- DDL: `CREATE`, `ALTER`, `DROP`; kiểu dữ liệu
- DML: `INSERT`, `UPDATE`, `DELETE`, `MERGE`
- `SELECT`: filter, sort, `DISTINCT`, `LIMIT`
- JOINs: inner/left/right/full/cross, self-join
- Aggregation: `GROUP BY`, `HAVING`, aggregate functions
- **Window functions**: `ROW_NUMBER`, `RANK`, `LAG/LEAD`, running totals, `PARTITION BY`
- **CTEs** và recursive CTEs
- Subqueries (scalar, correlated)
- Set operations: `UNION`, `INTERSECT`, `EXCEPT`

**Dự án P0:** Bộ dataset e-commerce synthetic (customers, orders, products, order_items) + 1 file SQL tutorial chạy được trên DuckDB với 30+ truy vấn từ cơ bản → window functions.

---

## Phase 1 — Programming for Data Engineering

**Mục tiêu:** Viết Python sạch, có test, để xử lý dữ liệu ở mọi định dạng.

### 1.1 Python data stack
- `pandas`: Series/DataFrame, indexing, groupby, merge, pivot, apply
- `polars`: lazy evaluation, expressions, tại sao nhanh hơn pandas
- `numpy`: vectorization, broadcasting
- So sánh khi nào dùng cái nào

### 1.2 File formats ⭐
- Row-based: CSV, JSON, JSONL
- Columnar: **Parquet** (deep dive: row groups, encoding, compression, predicate pushdown), ORC
- Serialization: Avro (schema evolution), Protobuf
- Benchmark: kích thước & tốc độ đọc CSV vs Parquet trên cùng dataset

### 1.3 Data ingestion
- Đọc/ghi từ REST API (`requests`, pagination, rate limit, retry/backoff)
- Web scraping cơ bản
- Đọc từ database (`sqlalchemy`)

### 1.4 Clean & tested code
- Type hints, `dataclasses`, `pydantic` cho data validation
- `pytest`: unit test cho transformation logic
- Logging, error handling, config management

**Dự án P1:** ETL script: extract từ public API → transform/clean bằng polars → load ra Parquet + DuckDB, có unit tests và logging.

---

## Phase 2 — Databases & Data Modeling

**Mục tiêu:** Hiểu sâu database và thiết kế data model chuẩn.

### 2.1 Relational deep dive
- Postgres: types, constraints, transactions, ACID, isolation levels
- **Indexing**: B-tree, hash, partial, composite; khi nào index giúp/hại
- Query optimization: `EXPLAIN ANALYZE`, đọc query plan
- Partitioning, materialized views

### 2.2 OLTP vs OLAP
- Khác biệt workload, tại sao tách warehouse khỏi production DB
- Row-store vs column-store

### 2.3 Dimensional Modeling (Kimball) ⭐
- Fact tables (transaction, periodic snapshot, accumulating snapshot)
- Dimension tables, surrogate keys
- **Star schema** vs **snowflake schema**
- **Slowly Changing Dimensions (SCD)** type 0/1/2/3/4/6
- Grain, conformed dimensions, bus matrix

### 2.4 Normalization & NoSQL
- 1NF→3NF, BCNF; khi nào denormalize
- NoSQL: document (MongoDB), key-value (Redis), wide-column (Cassandra), khi nào dùng

**Dự án P2:** Thiết kế star schema cho dataset e-commerce ở P0, build dim/fact tables trong DuckDB, implement SCD Type 2 cho dim_customer.

---

## Phase 3 — Data Warehousing & Analytics Engineering

**Mục tiêu:** Build warehouse và làm chủ dbt — công cụ chuẩn của analytics engineering.

### 3.1 Warehouse concepts
- Kiến trúc: staging → core → marts (medallion: bronze/silver/gold)
- Columnar storage deep dive
- Cloud warehouses: BigQuery, Snowflake, Redshift (kiến trúc, pricing model, khi nào chọn cái nào)

### 3.2 dbt (data build tool) ⭐
- Models, refs, sources, seeds
- Materializations: view, table, incremental, ephemeral
- **Tests**: generic (unique, not_null, relationships, accepted_values) + singular
- Macros & Jinja
- Documentation & DAG lineage
- Snapshots (SCD2 trong dbt)
- Packages (dbt_utils)

### 3.3 Modeling patterns
- Staging/intermediate/marts layering
- Semantic layer, metrics
- Incremental strategies (append, merge, insert_overwrite)

**Dự án P3:** dbt project hoàn chỉnh trên DuckDB (`dbt-duckdb`): staging → marts, có tests, docs, snapshot SCD2, incremental model.

---

## Phase 4 — Batch Processing & Big Data

**Mục tiêu:** Xử lý dữ liệu lớn vượt RAM bằng Spark, hiểu distributed computing.

### 4.1 Distributed computing
- MapReduce paradigm
- Tại sao cần distributed processing; CAP theorem
- HDFS / object storage concepts

### 4.2 Apache Spark ⭐
- Kiến trúc: driver, executors, cluster manager
- RDD vs DataFrame vs Dataset
- Transformations (lazy) vs Actions; DAG
- **Partitioning & shuffles** — nguồn gốc của 90% vấn đề performance
- Spark SQL, Catalyst optimizer, Tungsten
- Joins: broadcast vs sort-merge; xử lý data skew
- Caching/persistence
- Performance tuning: partition sizing, AQE, spill

### 4.3 Lakehouse
- Data lake vs warehouse vs **lakehouse**
- **Delta Lake** / **Apache Iceberg**: ACID trên object store, time travel, schema evolution, compaction, Z-ordering
- Table formats so sánh

**Dự án P4:** PySpark job xử lý dataset lớn (sinh ~10M rows): join, aggregate, window; ghi ra Delta/Iceberg table với partitioning; demo time travel.

---

## Phase 5 — Workflow Orchestration

**Mục tiêu:** Lập lịch và quản lý pipeline production-grade.

### 5.1 Apache Airflow ⭐
- DAGs, tasks, operators, sensors, hooks
- Scheduling, `execution_date`, catchup, backfill
- **Idempotency** — task chạy lại nhiều lần vẫn đúng
- XComs, TaskFlow API, dynamic task mapping
- Connections, variables, pools
- Retries, SLAs, alerting

### 5.2 Modern orchestrators
- **Dagster**: software-defined assets, asset lineage, khác Airflow thế nào
- Prefect: flows, tasks, dynamic workflows
- Khi nào chọn cái nào

### 5.3 Pipeline design patterns
- Idempotent + incremental loads
- Backfill strategies
- Dependency management, fan-in/fan-out
- Data freshness & SLA

**Dự án P5:** Airflow DAG (chạy bằng docker-compose) orchestrate pipeline P1→P3: ingest → load → dbt run → test, có retry và backfill được.

---

## Phase 6 — Streaming & Real-time Data

**Mục tiêu:** Xử lý dữ liệu real-time, event-driven architecture.

### 6.1 Apache Kafka ⭐
- Topics, partitions, offsets, replication
- Producers, consumers, **consumer groups**, rebalancing
- Delivery semantics: at-most-once / at-least-once / **exactly-once**
- Kafka Connect, Schema Registry (Avro)
- Retention, compaction

### 6.2 Stream processing
- **Spark Structured Streaming**: micro-batch, watermarking, windowing (tumbling/sliding/session)
- Apache Flink: true streaming, stateful processing
- Stateful vs stateless; late data handling

### 6.3 Event-driven & CDC
- **Change Data Capture** với Debezium (Postgres → Kafka)
- Event sourcing, outbox pattern
- Lambda vs Kappa architecture

**Dự án P6:** docker-compose stack Kafka + producer (sinh events) + Spark Structured Streaming consumer → aggregate theo windowing → ghi ra sink. Bonus: CDC Postgres→Kafka bằng Debezium.

---

## Phase 7 — Cloud & Infrastructure

**Mục tiêu:** Deploy pipeline lên cloud, IaC, containerization, CI/CD.

### 7.1 Containers ⭐
- Docker: images, layers, volumes, networks
- docker-compose cho multi-service local stacks
- Kubernetes basics: pods, deployments, services

### 7.2 AWS data stack
- **S3** (storage, lifecycle, partitioning), IAM
- **Glue** (catalog + ETL), **Athena** (serverless SQL on S3)
- **EMR** (managed Spark), **Kinesis** (streaming), **Redshift**
- **Lambda** cho event-driven ETL
- (Map tương đương sang GCP: GCS/Dataflow/BigQuery, và Azure)

### 7.3 Infrastructure as Code
- **Terraform**: providers, resources, state, modules
- CI/CD: GitHub Actions cho data pipeline (lint, test, deploy dbt/Airflow)

**Dự án P7:** Dockerize pipeline; viết Terraform tạo S3 bucket + Glue catalog (dùng LocalStack để chạy local miễn phí); GitHub Actions chạy dbt tests.

---

## Phase 8 — Data Quality, Governance & Observability

**Mục tiêu:** Đảm bảo dữ liệu đáng tin, có thể quan sát và quản trị.

### 8.1 Data quality ⭐
- **Great Expectations** / **Soda**: expectation suites, validation
- dbt tests nâng cao
- Anomaly detection trên data

### 8.2 Data contracts & governance
- Data contracts (schema + SLA giữa producer/consumer)
- PII, masking, GDPR/compliance
- Access control

### 8.3 Lineage & observability
- Data lineage: OpenLineage, DataHub, OpenMetadata
- Pipeline monitoring, alerting, freshness checks
- Cost monitoring

**Dự án P8:** Thêm Great Expectations vào pipeline P3/P5; định nghĩa expectation suite; data contract dạng YAML; sinh data quality report tự động.

---

## Phase 9 — Capstone Projects

**Mục tiêu:** Ghép tất cả thành 3 pipeline end-to-end để bỏ vào portfolio.

### Capstone A — Batch Analytics Platform
`API/files → ingest (Python) → S3/local lake (Parquet) → Spark transform → DuckDB/warehouse → dbt models + tests → Airflow orchestration → dashboard`

### Capstone B — Streaming Pipeline
`Event generator → Kafka → Spark Structured Streaming (windowed aggregation) → sink (DuckDB/Postgres) → real-time dashboard`. CDC từ Postgres bằng Debezium.

### Capstone C — Lakehouse
`Multi-source ingest → Iceberg/Delta lakehouse (bronze/silver/gold) → Spark + dbt → orchestration → data quality gates → lineage`

Mỗi capstone cần: README kiến trúc + diagram, code chạy được, tests, hướng dẫn reproduce.

---

## 📚 Tài nguyên tham khảo
- *Fundamentals of Data Engineering* — Reis & Housley
- *The Data Warehouse Toolkit* — Kimball (dimensional modeling)
- *Designing Data-Intensive Applications* — Kleppmann (kinh điển)
- *Spark: The Definitive Guide* — Chambers & Zaharia
- dbt docs, Airflow docs, Kafka docs (official)
- DataTalksClub Data Engineering Zoomcamp (free)

## 🎯 Kỹ năng cốt lõi (theo độ ưu tiên)
1. **SQL** (thành thạo, kể cả window functions) — không thể thiếu
2. **Python** (clean, tested)
3. **Data modeling** (dimensional/Kimball)
4. **Một orchestrator** (Airflow)
5. **Spark** (batch big data)
6. **dbt** (analytics engineering)
7. **Cloud** (một platform sâu, AWS)
8. **Streaming** (Kafka)
9. **IaC + CI/CD** (Docker, Terraform)
10. **Data quality & governance**
