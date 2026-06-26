# 41 — XComs, TaskFlow API & Dynamic Task Mapping

> Cách task **truyền dữ liệu** cho nhau và cách viết DAG gọn hơn (TaskFlow), tạo task động theo dữ liệu.

## XCom (cross-communication)
Cơ chế task **đẩy/kéo giá trị nhỏ** cho nhau qua metadata DB.
```python
# cách cổ điển
def extract(**ctx): ctx['ti'].xcom_push(key='n', value=42)
def load(**ctx):    n = ctx['ti'].xcom_pull(key='n', task_ids='extract')
```
⚠️ **Chỉ cho dữ liệu NHỎ** (id, count, đường dẫn file, ngày) — XCom lưu trong metadata DB. **KHÔNG** đẩy DataFrame/triệu dòng qua XCom. Dữ liệu lớn → ghi ra **storage (S3/parquet)** rồi truyền **đường dẫn** qua XCom (pattern "claim check").

## TaskFlow API (cách hiện đại, gọn)
Dùng decorator `@task`, trả/nhận giá trị như hàm Python bình thường — Airflow tự tạo XCom & phụ thuộc.
```python
from airflow.decorators import dag, task
import pendulum

@dag(schedule="@daily", start_date=pendulum.datetime(2024,1,1), catchup=False)
def etl():
    @task
    def extract() -> list[int]:
        return [1, 2, 3]

    @task
    def transform(rows: list[int]) -> int:
        return sum(rows)

    @task
    def load(total: int):
        print("total =", total)

    load(transform(extract()))     # gọi như hàm -> Airflow tự suy ra DAG & XCom

etl()
```
So với PythonOperator cổ điển: ít boilerplate, phụ thuộc suy ra từ lời gọi hàm, type hint rõ. Nên ưu tiên TaskFlow cho code Python.

## Dynamic Task Mapping (`.expand()`)
Tạo **số task động lúc chạy** dựa trên dữ liệu (vd: mỗi file/đối tác một task) — không biết trước số lượng khi viết DAG.
```python
@task
def list_files() -> list[str]:
    return ["a.csv", "b.csv", "c.csv"]   # quyết định lúc chạy

@task
def process(path: str): ...

process.expand(path=list_files())   # tạo 3 task process song song
```
Giống `map()` ở cấp task. Hợp xử lý N partition/file/đối tác mà N thay đổi.

## Khi nào dùng gì
- Truyền **ID/đường dẫn/giá trị nhỏ** → XCom (qua TaskFlow return).
- Truyền **dữ liệu lớn** → ghi ra storage, truyền đường dẫn.
- Viết task Python → **TaskFlow `@task`**.
- Số việc động theo dữ liệu → **dynamic mapping `.expand()`**.

## ⚠️ Cạm bẫy
- Đẩy dữ liệu lớn qua XCom → phình metadata DB, chậm.
- Lạm dụng XCom thành "biến toàn cục" → DAG khó hiểu; giữ luồng dữ liệu rõ ràng.
- Dynamic mapping quá nhiều task (hàng chục nghìn) → quá tải scheduler.

## ✅ Tự kiểm tra & "tự mò"
- [ ] XCom dùng cho gì, giới hạn (dữ liệu nhỏ); pattern claim-check cho dữ liệu lớn.
- [ ] Viết DAG bằng TaskFlow `@task`; phụ thuộc suy ra thế nào.
- [ ] Dynamic mapping `.expand()` giải quyết bài toán gì.
- 🔭 *Tự mò:* viết lại pipeline extract→transform→load bằng TaskFlow `@task` (chỉ in ra), thêm `.expand()` để xử lý danh sách 3 "nguồn".

➡️ Tiếp: [[42-airflow-resources]].
