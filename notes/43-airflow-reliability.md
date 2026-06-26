# 43 — Retries, SLAs, Alerting & Monitoring

> Pipeline production phải **tự phục hồi** khi lỗi tạm thời và **báo động** khi lỗi thật. Đây là phần "độ tin cậy".

## Retries
Lỗi tạm thời (mạng chập, DB busy) rất phổ biến → cấu hình retry tự động:
```python
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,   # 5, 10, 20 phút...
    "max_retry_delay": timedelta(hours=1),
}
```
- Đặt ở `default_args` (cả DAG) hoặc từng task.
- **Chỉ retry mới an toàn nếu task idempotent** ([[40-pipeline-patterns]]) — nếu không, retry nhân đôi dữ liệu.
- Phân biệt lỗi **nên retry** (timeout, 5xx) vs **không** (lỗi logic, 4xx) — giống [[11-api-ingestion]].

## Timeouts
- `execution_timeout`: giết task nếu chạy quá lâu (tránh task treo giữ slot mãi).
- Sensor dùng `timeout` + `mode='reschedule'` để không giữ worker khi chờ lâu.

## SLA (Service Level Agreement)
Cam kết "task/DAG phải xong trong X". Airflow ghi nhận **SLA miss** và có thể gọi callback/alert nếu vượt.
```python
PythonOperator(task_id="load", sla=timedelta(hours=1), ...)
```
→ Theo dõi freshness ([[40-pipeline-patterns]]): nếu gold trễ quá SLA, đội data biết ngay.

## Alerting & callbacks
- `email_on_failure`, `email_on_retry`.
- `on_failure_callback` / `on_success_callback` / `sla_miss_callback`: hàm tuỳ ý → gửi **Slack/PagerDuty/webhook**.
```python
def slack_alert(context):
    send_slack(f"Task {context['task_instance'].task_id} FAILED")
PythonOperator(..., on_failure_callback=slack_alert)
```
- Nguyên tắc: **alert phải hành động được** (ai đó cần làm gì), tránh "alert fatigue" (báo quá nhiều → bị phớt lờ).

## Trigger rules (xử lý lỗi luồng)
Mặc định `all_success`. Hữu ích khác:
- `all_done`: chạy dù upstream lỗi — cho task **cleanup/notify** luôn chạy.
- `one_failed`: kích hoạt nhánh xử lý lỗi.
- `none_failed_min_one_success`: cho nhánh điều kiện.

## Monitoring & observability
- **Airflow UI**: Grid/Graph view (trạng thái mỗi task run), Gantt (thời lượng, nghẽn), Logs từng task.
- **Metrics**: Airflow xuất StatsD/Prometheus (số task fail, thời lượng, lag scheduler) → Grafana dashboard.
- Theo dõi: tỉ lệ fail, thời gian chạy tăng dần (drift), SLA miss, scheduler lag.
- Mức cao hơn: **data observability** (freshness, volume, schema, chất lượng) — Phase 8.

## ⚠️ Cạm bẫy
- Retry task **không** idempotent → nhân đôi dữ liệu.
- Không có timeout → task treo giữ slot, nghẽn cả DAG.
- Alert quá nhiều/không hành động được → bị bỏ qua → bỏ lỡ sự cố thật.
- Chỉ alert on failure mà quên SLA → pipeline "chạy nhưng trễ" không ai biết.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Cấu hình retries + backoff; vì sao cần idempotency.
- [ ] execution_timeout & sensor reschedule.
- [ ] SLA vs retry vs alert — mỗi cái cho gì.
- [ ] on_failure_callback gửi Slack; tránh alert fatigue.
- [ ] Trigger rules (all_done cho cleanup).
- 🔭 *Tự mò:* trong DAG local, set `retries=2` + một task cố tình `raise` → xem nó retry trong UI; thêm `on_failure_callback` in ra log.

➡️ Tiếp: [[44-dagster-prefect]].
