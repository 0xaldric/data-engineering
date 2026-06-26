# D06 — Airflow Advanced

> Sâu hơn Phase 5 ([[38-airflow-core]]→[[43-airflow-reliability]]): patterns & tính năng cho production scale.

## Dynamic DAG generation
Sinh DAG/task bằng code thay vì viết tay từng cái:
- **Dynamic task mapping** (`.expand()`) — số task quyết định lúc chạy theo dữ liệu ([[41-airflow-taskflow]]).
- **Sinh nhiều DAG** từ config (vòng lặp Python qua list bảng/nguồn tạo DAG tương tự). Cẩn thận: code chạy lúc **parse** → đừng nặng/gọi DB ở top-level.
```python
for source in CONFIG:          # sinh 1 DAG / nguồn
    with DAG(f"ingest_{source['name']}", ...) as dag:
        ...
    globals()[f"ingest_{source['name']}"] = dag
```

## ⭐ Deferrable operators (async)
Sensor/operator chờ lâu (đợi file, job ngoài) bình thường **giữ một worker slot** suốt thời gian chờ → lãng phí. **Deferrable operator** dùng **triggerer** (async, event loop) → "nhả" worker khi chờ, tỉnh dậy khi điều kiện đến.
- VD `S3KeySensorAsync`, `wait_for_completion=True, deferrable=True`.
- Tiết kiệm tài nguyên khổng lồ khi có nhiều sensor chờ → **nên dùng** thay sensor `mode='reschedule'` ở scale lớn.

## TaskGroups
Gom task liên quan thành nhóm (UI gọn, tái dùng) — thay SubDAG (đã deprecated).
```python
with TaskGroup("ingest") as ingest:
    a = ...; b = ...
ingest >> transform
```

## Datasets / Data-aware scheduling
DAG B chạy khi **dataset** (do DAG A tạo) được cập nhật — không theo lịch cố định mà theo **dữ liệu sẵn sàng** (giống asset của Dagster — [[44-dagster-prefect]]).
```python
ds = Dataset("s3://lake/silver/orders")
# DAG A: outlets=[ds]  ;  DAG B: schedule=[ds]  -> B chạy khi A cập nhật ds
```

## Custom operator / hook
Đóng gói logic tái dùng thành operator riêng (kế thừa `BaseOperator`, implement `execute()`) hoặc hook (kết nối hệ ngoài). Dùng khi pattern lặp nhiều DAG.

## Best practice ở scale
- **DAG parsing nhanh**: không code nặng/gọi DB/import nặng ở top-level (scheduler parse mọi file liên tục). Đọc Variable trong task, không top-level.
- **Executor**: KubernetesExecutor (mỗi task 1 pod, cô lập dependency, scale) hoặc Celery (worker pool) ([[38-airflow-core]]).
- **Pools** giới hạn concurrency bảo vệ nguồn ([[42-airflow-resources]]).
- **Idempotency + data_interval** (không `now()`) để backfill an toàn ([[39-airflow-scheduling]], [[40-pipeline-patterns]]).
- **Đẩy việc nặng xuống** Spark/dbt/warehouse — Airflow chỉ điều phối.

## Testing DAG
- Test **import** (DAG không lỗi cú pháp, không cycle): `airflow dags list` / pytest load DAGbag.
- Unit test logic trong callable (tách hàm thuần — [[12-testing-de]]).
- `airflow tasks test <dag> <task> <date>` chạy 1 task local không cần scheduler.

## ⚠️ Cạm bẫy
- Code nặng top-level → scheduler chậm, parse timeout.
- Sensor đồng bộ nhiều → cạn worker slot (dùng deferrable).
- SubDAG (deprecated) → dùng TaskGroup.
- Dynamic mapping quá nhiều task → quá tải scheduler/metadata DB.

## ✅ "Tự mò"
🔭 Viết DAG sinh động từ list 3 "nguồn"; thêm TaskGroup; đổi 1 sensor sang deferrable; test bằng `airflow tasks test`.

➡️ Tiếp: [[d07-iceberg]].
