# C01 — Framework thiết kế hệ thống DE ⭐

> System design interview cho DE khác SWE: trọng tâm là **dữ liệu** (volume, velocity, schema, chất lượng, chi phí), không phải API/microservice. Đây là khung trả lời 6 bước.

## ⭐ Khung 6 bước
```
1. Làm rõ REQUIREMENTS  → 2. Ước lượng SCALE  → 3. DATA MODEL
        ↓
4. PIPELINE (ingest→process→store→serve)  → 5. SCALE & FAILURE  → 6. DQ/OBSERVABILITY
```

### 1. Làm rõ requirements (đừng vội vẽ!)
Hỏi để khoanh vùng:
- **Functional**: cần trả lời câu hỏi gì? batch report hay real-time? ai dùng (BI/ML/app)?
- **Volume**: bao nhiêu event/ngày? kích thước/record? lịch sử giữ bao lâu?
- **Velocity**: real-time (ms/giây) hay batch (giờ/ngày)? peak vs trung bình?
- **Latency/freshness SLA**: dashboard tươi trong bao lâu?
- **Consistency**: cần exactly-once/chính xác tuyệt đối (tiền) hay gần đúng chấp nhận được (analytics)?
- **Budget/team**: cloud nào? team mạnh gì?

### 2. Ước lượng scale (back-of-envelope)
VD: 100M event/ngày × 1KB ≈ 100GB/ngày ≈ 36TB/năm → quyết định storage (lake), compute (Spark), partition theo ngày. Tính **QPS peak** cho streaming. Con số định hướng lựa chọn công nghệ.

### 3. Data model
- Nguồn → bronze (raw) → silver (clean) → gold (mart/feature) — medallion ([[36-lakehouse-arch]]).
- Star schema cho analytics ([[17-dimensional-modeling]]); One Big Table/event cho clickstream.
- Chọn **grain** rõ; SCD cho dimension đổi ([[18-scd]]).

### 4. Pipeline (xương sống câu trả lời)
```
INGEST → PROCESS → STORE → SERVE
```
- **Ingest**: batch (file/API/CDC) hay stream (Kafka/Kinesis)? raw-first, idempotent.
- **Process**: Spark batch / Spark-Flink streaming / dbt SQL. Windowing nếu stream.
- **Store**: lake (S3+Parquet+table format) + warehouse (BigQuery/Snowflake) cho serving.
- **Serve**: BI (dashboard), API, feature store (ML), reverse-ETL.
- **Orchestrate**: Airflow/Dagster; idempotency + backfill.

### 5. Scale & failure
- Partition/shuffle, scale ngang ([[31-partitioning-shuffle]]); tách compute/storage.
- Failure: retry idempotent, replay từ Kafka/raw, dead-letter queue cho bad records, backfill.
- Bottleneck: hot partition/skew, small files, late data.

### 6. DQ & observability
- Tests (dbt/GE), data contracts, 5 trụ observability (freshness/volume/schema/distribution/lineage), alerting, SLA ([[60-data-quality]]→[[62-observability]]).

## Batch vs Stream vs Lambda/Kappa — chọn thế nào
| Yêu cầu | Chọn |
|---------|------|
| Báo cáo định kỳ, latency giờ/ngày | **Batch** (đơn giản, rẻ) |
| Phản ứng giây/ms (fraud, alert) | **Streaming** |
| Cần cả real-time lẫn chính xác lịch sử | **Lambda** (hoặc Kappa nếu log đủ) |
Mặc định: bắt đầu batch, thêm streaming khi requirement latency ép. ([[52-lambda-kappa]])

## Các trục đánh đổi (luôn nêu)
- **Latency vs cost vs complexity**: real-time đắt & phức tạp hơn batch.
- **Consistency vs availability** (CAP).
- **Build vs buy** (managed service vs tự vận hành).
- **Normalize vs denormalize** (ghi vs đọc).

## ⚠️ Cạm bẫy interview
- Vẽ kiến trúc trước khi hỏi requirements.
- Không ước lượng scale → chọn công nghệ vu vơ.
- Quên failure handling, DQ, idempotency, backfill (điểm phân biệt DE).
- Over-engineer (Kafka+Flink cho 1GB/ngày).

## ✅ "Tự mò"
🔭 Lấy 1 case bất kỳ (Module C), tự đi qua 6 bước trong 15 phút, vẽ sơ đồ ingest→serve + nêu 3 trade-off.

➡️ Tiếp: [[c02-case-ecommerce]].
