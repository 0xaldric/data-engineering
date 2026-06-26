# 44 — Modern Orchestrators: Dagster & Prefect

> Airflow là chuẩn de-facto, nhưng thế hệ mới (Dagster, Prefect) sửa vài điểm đau của Airflow. Biết để chọn đúng.

## Điểm đau của Airflow (vì sao có thế hệ mới)
- Tư duy **task-centric** (việc), không phải **data-centric** (dữ liệu/asset) → khó biết "bảng này do task nào tạo, có tươi không".
- Khái niệm thời gian (execution_date) gây bối rối ([[39-airflow-scheduling]]).
- Test/local-dev hơi cồng kềnh; truyền dữ liệu giữa task qua XCom hạn chế.

## Dagster — software-defined **assets** ⭐
Xoay quanh **data asset** (bảng/file/model) thay vì task. Bạn khai báo "asset này được tạo từ assets kia".
```python
from dagster import asset

@asset
def stg_orders(): ...            # asset

@asset
def fct_sales(stg_orders):       # phụ thuộc suy ra từ tham số
    return transform(stg_orders)
```
Ưu điểm:
- **Asset lineage** tích hợp sẵn (biết bảng nào sinh ra bảng nào, "tài sản dữ liệu" của tổ chức).
- **Data-aware scheduling**: chạy khi upstream asset đổi (không chỉ theo giờ).
- **Testability** & local dev tốt; **typing**, **IO managers** (tách logic khỏi nơi lưu).
- Tích hợp dbt mạnh (mỗi dbt model thành một asset).
→ Hợp khi muốn quản lý "tài sản dữ liệu" + lineage rõ, đội thiên về software engineering.

## Prefect — Pythonic & động
Biến hàm Python thành flow/task bằng decorator; rất tự nhiên cho luồng động, ít boilerplate.
```python
from prefect import flow, task

@task
def extract(): ...
@task
def transform(x): ...

@flow
def etl():
    transform(extract())

etl()
```
Ưu điểm: viết như Python thuần, **dynamic** (if/loop/đệ quy tự nhiên), lai giữa "chạy tay" và "có lịch", hybrid execution (chạy ở đâu cũng được). Hợp pipeline động/linh hoạt, team muốn nhẹ nhàng.

## So sánh nhanh
| | **Airflow** | **Dagster** | **Prefect** |
|--|-------------|-------------|-------------|
| Tư duy | task-centric | **asset/data-centric** | function/flow-centric |
| Lineage | hạn chế (cần exposure) | **built-in (assets)** | hạn chế |
| Local dev/test | cồng kềnh | **tốt** | **tốt** |
| Dynamic workflow | mapping (hạn chế) | có | **rất linh hoạt** |
| Hệ sinh thái/operator | **lớn nhất** | đang lớn | vừa |
| Độ phổ biến/việc làm | **cao nhất** | tăng nhanh | tăng |
| Hợp cho | chuẩn ngành, nhiều tích hợp | data platform + lineage | pipeline động, nhẹ |

## Chọn cái nào?
- **Airflow**: an toàn, phổ biến nhất (kỹ năng dễ xin việc), nhiều operator sẵn, có managed (MWAA/Composer/Astronomer). Mặc định nếu phân vân.
- **Dagster**: muốn data-asset + lineage + dev experience tốt, tích hợp dbt sâu, xây "data platform".
- **Prefect**: pipeline Python động, team nhỏ, ưu tiên đơn giản/linh hoạt.
→ Học **kỹ Airflow trước** (nền tảng + thị trường), hiểu khái niệm chung (DAG, idempotency, backfill) → chuyển công cụ rất nhanh vì ý tưởng giống nhau.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Điểm đau Airflow mà thế hệ mới giải quyết.
- [ ] Dagster "asset-centric" nghĩa là gì; lợi ích lineage.
- [ ] Prefect mạnh ở đâu (dynamic/Pythonic).
- [ ] Chọn orchestrator theo bối cảnh.
- 🔭 *Tự mò:* `pip install dagster`, viết 2-3 `@asset` (giống staging→mart), chạy `dagster dev`, xem **asset graph** (lineage) trong UI — so với DAG Airflow.

➡️ Tiếp: [[00-phase5-summary]].
