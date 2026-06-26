# 39 — Scheduling, execution_date, catchup & backfill ⭐

> Phần gây bối rối nhất của Airflow: khái niệm **thời gian**. Hiểu nó là hiểu Airflow.

## schedule (lịch chạy)
Khai báo bằng cron hoặc preset:
- Preset: `@daily`, `@hourly`, `@weekly`, `@monthly`, `None` (chỉ trigger tay), `@once`.
- Cron: `"0 2 * * *"` (2h sáng mỗi ngày).
- `timedelta(hours=6)` (mỗi 6 giờ kể từ start_date).

## ⭐ Data interval & logical date (điểm dễ nhầm nhất)
Airflow nghĩ theo **khoảng thời gian dữ liệu (data interval)**, không phải "thời điểm bấm nút". Một DAG run xử lý dữ liệu **của một khoảng**, và chạy **khi khoảng đó kết thúc**.

Ví dụ `@daily`, run cho ngày **2024-01-01**:
- **data_interval_start** = 2024-01-01 00:00
- **data_interval_end** = 2024-01-02 00:00
- DAG run này thực sự **bắt đầu chạy lúc ~2024-01-02 00:00** (khi đủ dữ liệu của ngày 01).
- **logical_date** (trước đây gọi `execution_date`) = 2024-01-01 — "nhãn" của khoảng, KHÔNG phải lúc chạy thật.

→ Vì thế: "run hôm nay xử lý dữ liệu hôm qua". Đừng dùng `datetime.now()` trong task — dùng **logical_date / data_interval** để task **xác định & lặp lại được** (idempotent). Đây là lý do Airflow có thể backfill.

## catchup
- `catchup=True` (mặc định cũ): nếu `start_date` ở quá khứ, Airflow **chạy bù tất cả** các interval từ start_date đến nay → có thể bùng nổ hàng trăm run.
- `catchup=False` (khuyến nghị cho hầu hết): chỉ chạy từ interval gần nhất trở đi.
→ Luôn cân nhắc `catchup` + đặt `start_date` tĩnh (đừng dùng `now()`).

## backfill
Chạy DAG cho **khoảng quá khứ** một cách có chủ đích (vd: vừa thêm cột, cần tính lại 3 tháng trước):
```bash
airflow dags backfill -s 2024-01-01 -e 2024-03-31 my_dag
```
Backfill **chỉ đúng & an toàn nếu task idempotent** ([[40-pipeline-patterns]]) — vì nó ghi đè lại từng khoảng. Mỗi run dùng logical_date của nó để biết xử lý dữ liệu khoảng nào.

## Dùng ngày trong task (đúng cách)
```python
@task
def load(data_interval_start=None, data_interval_end=None):
    # chỉ xử lý dữ liệu trong [start, end) -> idempotent, backfill-able
    process(where=f"ts >= '{data_interval_start}' AND ts < '{data_interval_end}'")
```
Airflow tự "tiêm" các biến ngữ cảnh (`data_interval_start/end`, `ds`, `logical_date`). Template Jinja: `{{ ds }}` (ngày logical YYYY-MM-DD), `{{ data_interval_start }}`.

## ⚠️ Cạm bẫy
- Nhầm logical_date = lúc chạy → sai dữ liệu.
- `start_date = datetime.now()` → DAG không bao giờ chạy ổn định (luôn dời).
- Quên `catchup=False` → bị bão run khi deploy DAG có start_date xa.
- Dùng `now()` trong task → không backfill/replay được.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Giải thích data_interval_start/end & logical_date; vì sao "run hôm nay = dữ liệu hôm qua".
- [ ] catchup True vs False; khi nào.
- [ ] Backfill làm gì; vì sao cần idempotency.
- [ ] Vì sao không dùng `now()` trong task.
- 🔭 *Tự mò:* tạo DAG `@daily` `start_date` 7 ngày trước, một lần `catchup=True` một lần `False`, xem số DAG run khác nhau trong UI.

➡️ Tiếp: [[40-pipeline-patterns]] — idempotency là chìa khoá.
