# I07 — Deep-dive: Backfill & Reprocessing Strategies

> Tính lại dữ liệu quá khứ an toàn — kỹ năng phân biệt DE thật. Sâu hơn [[39-airflow-scheduling]], [[40-pipeline-patterns]].

## Khi nào cần backfill/reprocess?
- **Logic đổi**: sửa công thức metric/transform → tính lại lịch sử cho nhất quán.
- **Bug**: pipeline ghi sai một khoảng → sửa + tính lại.
- **Nguồn bổ sung**: dữ liệu cũ tới muộn / nguồn mới được nối.
- **Schema/model đổi**: thêm cột cần tính ngược.
- **Recovery**: sau sự cố, tính lại khoảng ảnh hưởng.

## ⭐ Điều kiện tiên quyết: IDEMPOTENCY
Backfill = chạy lại pipeline cho khoảng quá khứ. **Chỉ an toàn nếu idempotent** ([[40-pipeline-patterns]], [[b08-explain-senior]]): mỗi run xử lý đúng partition của logical_date, ghi đè không nhân đôi. Không idempotent → backfill = thảm hoạ (data trùng/sai).

## Chiến lược backfill (batch)
| Chiến lược | Cách | Khi nào |
|-----------|------|---------|
| **Partition overwrite** ⭐ | xoá+ghi lại từng partition (ngày) trong khoảng | mặc định; idempotent theo ngày |
| **Blue-green / shadow table** | build bảng mới song song → verify → swap | đổi logic lớn, không downtime; rollback dễ |
| **Incremental rebuild** | dbt `--full-refresh` rồi incremental tiếp | model incremental đổi logic ([[27-dbt-incremental]]) |
| **MERGE/upsert** | upsert theo key | dữ liệu đến lẻ, không theo partition |

### Partition overwrite (an toàn nhất)
```sql
-- backfill ngày X: xoá rồi ghi lại đúng partition đó
DELETE FROM fct WHERE dt = '{{ ds }}';
INSERT INTO fct SELECT ... WHERE dt = '{{ ds }}';
-- Airflow backfill -s start -e end -> mỗi ngày một run idempotent
```

### Blue-green (đổi logic lớn, zero-downtime)
```
1. Build fct__new với logic mới (toàn bộ lịch sử) — không đụng fct live
2. Verify fct__new (DQ, so số với fct, sample)
3. SWAP: rename fct → fct__old, fct__new → fct (atomic)
4. Giữ fct__old vài ngày để rollback
```
Consumer không thấy data nửa vời (atomic publish — [[40-pipeline-patterns]], [[f06-dataops]]).

## Kiểm soát tải khi backfill ⭐
Backfill 2 năm = chạy nhiều run đồng thời → **đập chết** nguồn/warehouse + tốn compute.
- Giới hạn concurrency (Airflow `max_active_runs`, **pools** — [[42-airflow-resources]]).
- Chạy backfill ngoài giờ cao điểm; chia nhỏ khoảng.
- Ưu tiên partition gần đây trước (giá trị cao hơn).

## Reprocessing stream (Kappa)
Tính lại dữ liệu streaming = **replay** từ Kafka ([[52-lambda-kappa]]):
```
1. Job streaming MỚI đọc topic từ offset 0 (Kafka retention đủ)
2. Ghi sang bảng/topic MỚI (không đụng live)
3. Verify → swap
```
Điều kiện: Kafka **retention đủ dài** để replay; sink idempotent. Đây là sức mạnh Kappa (một code path cho cả real-time lẫn tính lại).

## Verify sau backfill
- So tổng/sample giữa cũ và mới (audit_helper dbt — [[d02-dbt-advanced]]).
- DQ checks trên data backfill ([[i06-dq-framework]]).
- Reconciliation nếu là số tiền ([[i04-case-banking]]).

## ⚠️ Cạm bẫy
- Backfill pipeline **không idempotent** → nhân đôi/sai.
- Backfill đè trực tiếp bảng live không verify → consumer thấy data sai giữa chừng (dùng blue-green).
- Không giới hạn concurrency → đập chết nguồn/warehouse + bill sốc.
- Dùng `now()` thay logical_date → không backfill được ([[39-airflow-scheduling]]).
- Kafka retention quá ngắn → không replay được (Kappa).

## ✅ "Tự mò"
🔭 Viết pipeline "partition overwrite theo ngày" (delete+insert dt) cho 1 mart e-commerce; chạy lại 1 ngày 3 lần xem kết quả có đổi không (idempotent?). Phác kế hoạch blue-green để đổi công thức revenue.

➡️ Tiếp: [[00-extraI-summary]].
