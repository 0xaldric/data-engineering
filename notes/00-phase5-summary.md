# 🏁 Phase 5 — Tổng kết: Workflow Orchestration (Airflow)

> Notes-first. Trọng tâm: điều phối pipeline tin cậy — Airflow + nguyên tắc idempotency/backfill.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| T047 | Orchestration intro (vì sao, DAG) | [37](37-orchestration-intro.md) |
| T048 | Airflow core concepts | [38](38-airflow-core.md) |
| T049 | Scheduling, execution_date, catchup, backfill | [39](39-airflow-scheduling.md) |
| T050 | Idempotency & pipeline patterns | [40](40-pipeline-patterns.md) |
| T051 | XComs, TaskFlow, dynamic mapping | [41](41-airflow-taskflow.md) |
| T052 | Connections, Variables, Pools, Operators | [42](42-airflow-resources.md) |
| T053 | Retries, SLAs, alerting, monitoring | [43](43-airflow-reliability.md) |
| T054 | Dagster & Prefect | [44](44-dagster-prefect.md) |

## 📑 Cheat-Sheet Airflow
- **DAG** = pipeline (Python ở `dags/`); **task** = instance của **operator**; **sensor** chờ điều kiện; **hook** nối hệ ngoài.
- Kiến trúc: **scheduler** (xếp lịch) + **executor/workers** (chạy) + **metadata DB** (trạng thái) + **webserver** (UI).
- **Phụ thuộc**: `a >> b`; fan-out `a >> [b,c]`; fan-in `[b,c] >> d`.
- ⭐ **Thời gian**: nghĩ theo **data interval**; `logical_date` = nhãn khoảng, KHÔNG phải lúc chạy ("run hôm nay = dữ liệu hôm qua"). Dùng `data_interval_start/end`/`{{ ds }}`, **không** `now()`.
- **catchup=False** (thường); **backfill** chạy bù quá khứ — chỉ an toàn nếu **idempotent**.
- ⭐ **Idempotency**: append = xấu; partition-overwrite/upsert/MERGE = tốt. Là điều kiện để retry/backfill an toàn.
- **TaskFlow `@task`** (gọn, hiện đại) > PythonOperator; **XCom** chỉ cho dữ liệu nhỏ (lớn → ghi storage + truyền path); **`.expand()`** tạo task động.
- **Connections/secret** (không hardcode), **Variables** (config, đọc trong task), **Pools** (giới hạn concurrency bảo vệ nguồn).
- **Retries + backoff**, `execution_timeout`, **SLA**, `on_failure_callback` (Slack); trigger rule `all_done` cho cleanup.
- Airflow chỉ **điều phối** — việc nặng đẩy xuống Spark/dbt/warehouse.

## ✅ Self-assessment Phase 5
- [ ] Vì sao cần orchestrator; DAG là gì.
- [ ] Airflow: DAG/task/operator/sensor/hook + kiến trúc.
- [ ] Giải thích logical_date/data_interval, catchup, backfill.
- [ ] Idempotency + 5 pipeline patterns.
- [ ] XCom/TaskFlow/dynamic mapping; connections/variables/pools.
- [ ] Retries/SLA/alerting; đọc Airflow UI.
- [ ] Dagster (assets) vs Prefect vs Airflow — chọn khi nào.

## 🔭 Để "tự mò"
1. `pip install apache-airflow` → `airflow standalone` → UI :8080. Viết DAG `@daily` ETL (TaskFlow) tái dùng pipeline Phase 1.
2. Thử `catchup=True/False`, chạy `airflow dags backfill` cho 1 tuần.
3. Cố tình `raise` để xem retries; thêm `on_failure_callback`.
4. `pip install dagster` → viết vài `@asset` (staging→mart) → `dagster dev` xem asset lineage.

## ➡️ Tiếp theo: Phase 6 — Streaming & Real-time (Kafka)
Kafka (topic/partition/consumer group, delivery semantics), stream processing (Spark Structured Streaming/Flink, windowing/watermark), CDC (Debezium), Lambda vs Kappa. (notes-first)
