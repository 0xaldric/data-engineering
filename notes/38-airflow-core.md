# 38 — Airflow Core Concepts ⭐

> Airflow: định nghĩa pipeline bằng **Python code** (DAG), scheduler tự chạy theo lịch, UI để theo dõi/retry.

## Các khái niệm
- **DAG**: một pipeline — tập task + phụ thuộc, có lịch chạy. Định nghĩa trong file `.py` đặt ở `dags/`.
- **Task**: một bước trong DAG (một **instance** của operator).
- **Operator**: "khuôn" định nghĩa *làm gì*. Tạo operator → ra task.
  - `PythonOperator` / `@task` — chạy hàm Python.
  - `BashOperator` — chạy lệnh shell.
  - `SQLExecuteQueryOperator` — chạy SQL.
  - Provider operators: `S3*`, `PostgresOperator`, `SparkSubmitOperator`, `DbtCloudRunJobOperator`...
- **Sensor**: operator đặc biệt **chờ một điều kiện** (file xuất hiện, partition sẵn sàng, giờ tới) rồi mới cho downstream chạy. (Dùng `mode='reschedule'` để khỏi giữ slot khi chờ lâu.)
- **Hook**: lớp giao tiếp hệ ngoài (DB, S3, API) — operator dùng hook bên dưới; bạn cũng gọi hook trong task Python.

## Kiến trúc Airflow
```
┌─────────────┐   ┌──────────────┐   ┌──────────────┐
│  Scheduler  │──►│ Metadata DB  │◄──│  Webserver   │ (UI)
│ (đọc DAG,   │   │ (Postgres:   │   │  theo dõi,   │
│  xếp lịch,  │   │  trạng thái  │   │  trigger,    │
│  giao task) │   │  task/DAG)   │   │  retry tay)  │
└──────┬──────┘   └──────────────┘   └──────────────┘
       │ giao task
       ▼
┌──────────────┐
│   Executor   │  Local / Celery / Kubernetes
│  + Workers   │  → nơi task THẬT chạy
└──────────────┘
```
- **Scheduler**: quét DAG, quyết định task nào tới lượt, đẩy vào hàng đợi.
- **Executor**: cơ chế chạy task. `LocalExecutor` (1 máy), `CeleryExecutor` (nhiều worker qua message queue), `KubernetesExecutor` (mỗi task 1 pod).
- **Metadata DB**: lưu trạng thái mọi DAG run/task (nguồn sự thật). Thường Postgres.
- **Webserver**: UI xem DAG, log, trạng thái, trigger/retry tay.

## DAG cơ bản (minh hoạ)
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum

def extract(): ...
def transform(): ...

with DAG(
    dag_id="ecommerce_etl",
    schedule="@daily",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    default_args={"retries": 2},
) as dag:
    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t1 >> t2          # định nghĩa phụ thuộc: t1 trước t2
```
`>>` (và `<<`) khai báo thứ tự. `t1 >> [t2, t3]` = t2,t3 chạy song song sau t1.

## ⚠️ Cạm bẫy
- **DAG file = code định nghĩa, KHÔNG phải nơi xử lý dữ liệu**: scheduler **parse** file này liên tục → đừng để code nặng/đọc DB ở top-level (làm chậm scheduler). Việc nặng để **trong** task.
- **Top-level code chạy mỗi lần parse** → import nặng, gọi API ở top-level = tệ.
- Một task nên **làm một việc** + **idempotent** ([[40-pipeline-patterns]]).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Phân biệt DAG/task/operator/sensor/hook.
- [ ] Vai trò scheduler/executor/metadata DB/webserver.
- [ ] Các loại executor (Local/Celery/Kubernetes).
- [ ] Vì sao không để code nặng ở top-level DAG file.
- 🔭 *Tự mò:* `pip install apache-airflow`, `airflow standalone` (chạy local SQLite+LocalExecutor), mở UI :8080, bỏ một DAG mẫu vào `~/airflow/dags/`, xem nó chạy.

➡️ Tiếp: [[39-airflow-scheduling]].
