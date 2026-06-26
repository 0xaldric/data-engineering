# 40 — Idempotency & Pipeline Design Patterns ⭐

> Nguyên tắc quan trọng nhất của pipeline production: **idempotency**. Nắm cái này thì retry/backfill/replay mới an toàn.

## Idempotency là gì?
Một task **idempotent** = chạy **một lần hay nhiều lần** đều cho **cùng kết quả**, không tạo trùng/sai. `f(f(x)) = f(x)`.

Vì sao sống còn: task **sẽ** chạy lại (retry khi lỗi mạng, backfill, rerun tay, scheduler restart). Nếu không idempotent → dữ liệu nhân đôi, sai số liệu **âm thầm**.

### Không idempotent (xấu) vs idempotent (tốt)
```python
# ❌ XẤU: append -> chạy lại là nhân đôi dữ liệu
INSERT INTO sales SELECT * FROM staging;

# ✅ TỐT: overwrite đúng partition của khoảng đang xử lý
DELETE FROM sales WHERE date = '{{ ds }}';
INSERT INTO sales SELECT * FROM staging WHERE date = '{{ ds }}';
-- hoặc MERGE/upsert theo key, hoặc ghi đè partition date='{{ ds }}'
```

## Các pattern cốt lõi
### 1. Partitioned overwrite (delete-insert by partition)
Xử lý theo **khoảng/partition** (thường theo ngày = logical_date). Mỗi run **xoá rồi ghi lại đúng partition của nó** → chạy lại/backfill bao nhiêu lần cũng đúng. Kết hợp `data_interval` ([[39-airflow-scheduling]]).

### 2. Incremental load + watermark
Chỉ xử lý dữ liệu mới kể từ lần trước (theo timestamp/id lớn nhất). Cẩn thận **late-arriving data** → dùng lookback window + upsert (xem [[27-dbt-incremental]], [[11-api-ingestion]]).

### 3. Upsert / MERGE
Update nếu trùng key, insert nếu mới → tự nhiên idempotent. Nền của SCD2/CDC ([[18-scd]], [[34-delta-lake]]).

### 4. Atomic publish (staging → swap)
Ghi vào bảng/thư mục tạm, **xong xuôi mới** swap/rename sang vị trí thật → consumer không bao giờ thấy dữ liệu nửa vời. (Table format Delta/Iceberg làm sẵn việc này bằng commit nguyên tử.)

### 5. Tách extract / transform / load
Lưu **raw trước** (bronze) rồi transform → lỗi transform thì replay từ raw, không gọi nguồn lại ([[11-api-ingestion]]).

## Cấu trúc phụ thuộc
- **Fan-out**: 1 task → nhiều task song song (vd ingest nhiều nguồn).
- **Fan-in**: nhiều task → 1 task gộp (vd transform chờ mọi ingest xong).
- **Trigger rules**: mặc định `all_success` (chạy khi mọi upstream OK); khác: `all_done` (chạy dù upstream lỗi — hợp task cleanup/notify), `one_success`...

## Data freshness & SLA
- **Freshness**: dữ liệu mới đến đâu (vd "gold cập nhật trong vòng 1h sau nửa đêm").
- **SLA**: cam kết thời gian hoàn thành; Airflow cảnh báo nếu task vượt SLA ([[43-airflow-reliability]]).
- Theo dõi freshness là một phần data observability (Phase 8).

## ⚠️ Cạm bẫy
- Append mù → nhân đôi khi rerun.
- Dùng `now()` thay vì logical_date → không replay được.
- Task "đa việc" khó retry (lỗi giữa chừng để lại trạng thái bẩn) → chia nhỏ, mỗi task một việc nguyên tử.
- Phụ thuộc ngầm (task B giả định B chạy sau A nhưng không khai báo `A >> B`).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Định nghĩa idempotency; cho ví dụ append (xấu) vs partition-overwrite/upsert (tốt).
- [ ] 5 pattern: partitioned overwrite, incremental+watermark, upsert, atomic publish, tách E/T/L.
- [ ] Fan-in/fan-out, trigger rules.
- [ ] Freshness vs SLA.
- 🔭 *Tự mò:* viết lại một bước ETL đã làm (Phase 1) theo kiểu "delete partition date=X rồi insert" và tự hỏi: chạy 3 lần liên tiếp kết quả có đổi không?

➡️ Tiếp: [[41-airflow-taskflow]].
