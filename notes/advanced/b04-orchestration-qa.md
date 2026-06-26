# B04 — Orchestration & Reliability Q&A

> Câu hỏi phỏng vấn Airflow/orchestration + đáp án. Chi tiết: [[37-orchestration-intro]]→[[44-dagster-prefect]].

**Q: Vì sao cần orchestrator thay cron?**
A: Cron chỉ "chạy lệnh lúc X". Orchestrator quản **phụ thuộc** (DAG), retry, backfill, monitoring/alert, truyền dữ liệu, chạy lại 1 bước, giới hạn tài nguyên.

**Q: DAG?**
A: Directed Acyclic Graph — node = task, cạnh = phụ thuộc; có hướng (A→B: B sau A), không chu trình. `a >> b`.

**Q: ⭐ Idempotency — là gì & vì sao sống còn?**
A: Chạy 1 hay nhiều lần đều ra cùng kết quả. Task **sẽ** chạy lại (retry/backfill/rerun) → không idempotent thì nhân đôi/sai dữ liệu âm thầm. Cách: partition overwrite / upsert / MERGE, không append mù.

**Q: execution_date / logical_date / data_interval?**
A: Airflow nghĩ theo **khoảng dữ liệu**. Run cho ngày X xử lý dữ liệu của X, chạy **khi X kết thúc**. `logical_date` = nhãn khoảng, KHÔNG phải lúc chạy → "run hôm nay = dữ liệu hôm qua". Dùng `data_interval_start/end`, **không** `now()`.

**Q: catchup?**
A: `catchup=True` chạy bù mọi interval từ start_date (dễ bão run); `catchup=False` (khuyến nghị) chỉ từ interval gần nhất.

**Q: Backfill?**
A: Chạy DAG cho khoảng quá khứ có chủ đích (tính lại). Chỉ an toàn nếu task idempotent; mỗi run dùng logical_date của nó.

**Q: Operator vs Sensor vs Hook?**
A: Operator = làm gì (Python/Bash/SQL...). Sensor = chờ điều kiện (file/partition/giờ), dùng `mode='reschedule'` để khỏi giữ slot. Hook = lớp nối hệ ngoài.

**Q: XCom — dùng & giới hạn?**
A: Truyền **dữ liệu nhỏ** (id/path/count) giữa task qua metadata DB. KHÔNG đẩy DataFrame lớn → ghi storage + truyền path (claim-check).

**Q: TaskFlow API?**
A: `@task` decorator — viết task như hàm Python, phụ thuộc & XCom suy ra tự động. Gọn hơn PythonOperator.

**Q: Retries & SLA?**
A: `retries` + `retry_delay` + exponential backoff cho lỗi tạm thời (cần idempotency). SLA = cam kết thời gian; vượt → alert. `execution_timeout` giết task treo.

**Q: Trigger rules?**
A: Mặc định `all_success`. `all_done` (chạy dù upstream lỗi — cho cleanup/notify); `one_failed` (nhánh xử lý lỗi).

**Q: Executor types?**
A: LocalExecutor (1 máy), CeleryExecutor (nhiều worker qua queue), KubernetesExecutor (mỗi task 1 pod — cô lập, scale).

**Q: Anti-pattern hay gặp trong DAG?**
A: Code nặng/đọc DB ở **top-level** (scheduler parse liên tục → chậm); task đa-việc khó retry; dùng `now()`; phụ thuộc ngầm không khai báo.

**Q: Airflow vs Dagster vs Prefect?**
A: Airflow task-centric, phổ biến nhất, nhiều operator. Dagster asset-centric (lineage built-in, dev tốt, hợp data platform). Prefect Pythonic/động, nhẹ. Học Airflow trước (thị trường + nền tảng).

**Q: Pipeline lỗi lúc 3h sáng, xử lý thế nào?**
A: Alert (on_failure_callback) → xem log/Spark UI tìm task lỗi → vì idempotent nên **rerun** task đó (hoặc backfill khoảng ảnh hưởng) → root cause + thêm test/contract ngăn tái diễn.

## ✅ "Tự mò"
🔭 Lấy pipeline e-commerce, phác DAG Airflow (ingest→load→dbt build→DQ→notify) + chỉ ra mỗi task idempotent thế nào.

➡️ Tiếp: [[b05-cloud-qa]].
