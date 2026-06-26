# 42 — Connections, Variables, Pools & Operators ecosystem

> Cách Airflow quản lý **kết nối/secret**, **cấu hình**, **giới hạn tài nguyên**, và hệ sinh thái operator.

## Connections
Lưu thông tin kết nối hệ ngoài (DB, S3, API): host, port, user, password, extra. Quản lý ở UI/CLI/env, **không hardcode trong DAG**. Operator/Hook tham chiếu qua `conn_id`.
```python
PostgresOperator(task_id="load", postgres_conn_id="dwh", sql="...")
```
- Secret thật nên để **secrets backend** (AWS Secrets Manager, Vault, HashiCorp) thay vì metadata DB. Đừng log secret ([[13-logging-config]]).

## Variables
Cặp key-value cấu hình toàn cục (vd `env=prod`, `s3_bucket=...`). Đọc: `Variable.get("s3_bucket")`.
- ⚠️ Đọc Variable ở **top-level DAG** = gọi DB mỗi lần parse → chậm scheduler. Đọc **trong task**, hoặc dùng Jinja `{{ var.value.s3_bucket }}` (lazy).

## Pools — giới hạn concurrency
Pool giới hạn **số task chạy đồng thời** dùng chung một tài nguyên hữu hạn (vd DB chỉ chịu 5 kết nối nặng). Gán `pool="dwh_pool"` (vd 5 slot) → tối đa 5 task pool đó chạy cùng lúc, dù cluster rảnh.
- Tránh "đập chết" nguồn (DB/API) khi nhiều task cùng gọi.
- Liên quan: `max_active_runs` (số DAG run song song), `max_active_tasks` (task/ DAG), `concurrency`.

## Operators ecosystem (Providers)
Airflow có **provider packages** cho hầu hết hệ thống:
| Nhóm | Operator/Hook ví dụ |
|------|---------------------|
| Cloud | `S3*`, `GCSToBigQueryOperator`, `RedshiftSQLOperator` |
| DB | `SQLExecuteQueryOperator`, `PostgresOperator` |
| Compute | `SparkSubmitOperator`, `DatabricksRunNowOperator`, `KubernetesPodOperator` |
| Transform | `DbtCloudRunJobOperator` (gọi dbt) |
| Generic | `PythonOperator`/`@task`, `BashOperator`, `EmailOperator` |
| Sensor | `S3KeySensor`, `ExternalTaskSensor`, `DateTimeSensor` |

**KubernetesPodOperator** rất hay dùng: chạy mỗi task trong một container riêng → cô lập dependency, scale tốt.

## Best practice tổ chức
- Secret → connections/secrets backend, **không** trong code/log.
- Config theo môi trường → Variables/env (dev/staging/prod), giống [[13-logging-config]] (defaults < config < env).
- Giới hạn tải nguồn ngoài bằng **pools**.
- Việc nặng → đẩy xuống Spark/dbt/warehouse qua operator tương ứng, Airflow chỉ điều phối ([[37-orchestration-intro]]).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Connection vs Variable vs Pool — mỗi cái giải quyết gì.
- [ ] Vì sao không đọc Variable ở top-level DAG.
- [ ] Pool giới hạn concurrency để bảo vệ nguồn thế nào.
- [ ] Kể vài operator/sensor theo nhóm; vai trò KubernetesPodOperator.
- 🔭 *Tự mò:* trong Airflow local, tạo 1 Connection (vd sqlite/duckdb), 1 Variable, 1 Pool (2 slot); viết DAG 3 task cùng pool xem chỉ 2 chạy song song.

➡️ Tiếp: [[43-airflow-reliability]].
