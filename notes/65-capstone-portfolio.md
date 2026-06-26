# 65 — Portfolio & Cách trình bày dự án DE

> Học xong cần **chứng minh**. Một portfolio tốt quan trọng hơn chứng chỉ. Phase 9 hướng dẫn build 3 capstone — note này là cách làm chúng "đáng tiền".

## Nhà tuyển dụng DE tìm gì ở dự án?
- **End-to-end**: ingest → transform → serve, không chỉ một notebook lẻ.
- **Production thinking**: idempotency, tests, error handling, orchestration, không phải "chạy 1 lần".
- **Đánh đổi có lý do**: giải thích *vì sao* chọn công cụ/kiến trúc này (không phải "vì tutorial bảo thế").
- **Sạch & reproduce được**: người khác clone về chạy được theo README.
- **Hiểu sâu**: nói được về shuffle, SCD, partitioning, exactly-once... khi phỏng vấn.

## Cấu trúc một repo portfolio tốt
```
project/
├── README.md          ← QUAN TRỌNG NHẤT: vấn đề, kiến trúc (sơ đồ), cách chạy, kết quả
├── docs/architecture.md  ← sơ đồ + giải thích lựa chọn & trade-off
├── ingestion/  transform/  orchestration/  tests/
├── docker-compose.yml ← một lệnh dựng được stack
└── Makefile / scripts ← `make run`, `make test`
```
README phải có: **bài toán** (business question), **sơ đồ kiến trúc**, **stack & vì sao**, **cách reproduce** (steps rõ), **kết quả/screenshot**, **điều học được & sẽ cải thiện**.

## Tránh "tutorial clone"
Đừng nộp đúng tutorial ai cũng làm (NYC taxi y hệt). Tạo khác biệt:
- Dataset/đề bài riêng (vd chính dataset e-commerce đã sinh ở project này).
- Thêm chiều sâu: SCD2 thật, data quality gates, CI/CD, observability.
- Viết **trade-off writeup**: "tôi chọn Delta vì..., nếu scale lớn hơn sẽ chuyển Iceberg vì...".

## ⭐ Tận dụng những gì đã build trong khoá này
Bạn đã có sẵn nền cho capstone:
- **Dataset**: `scripts/gen_ecommerce.py` (42k rows, có thể nhân lên triệu).
- **ETL medallion**: `etl_pipeline.py` (bronze→silver→gold) → `de.duckdb` ([[00-phase1-summary]]).
- **Dimensional + SCD2**: `04_build_star.py`, `05_scd.py` ([[00-phase2-summary]]).
- **dbt project đầy đủ**: models/tests/snapshots/incremental ([[00-phase3-summary]]).
- **Kiến thức** Spark/Kafka/cloud/DQ (Phase 4–8) để mở rộng & giải thích.
→ Ghép lại + thêm orchestration/streaming/DQ = 3 capstone.

## Tiêu chí "đạt" cho mỗi capstone
- [ ] Chạy được end-to-end bằng 1–2 lệnh (docker-compose/Makefile).
- [ ] Có **tests** (dbt tests + pytest) và **DQ checks**.
- [ ] **Idempotent** + có orchestration (Airflow/Dagster) hoặc ít nhất script điều phối.
- [ ] README + **sơ đồ kiến trúc** + trade-off.
- [ ] Reproduce được trên máy người khác.

## Cách trình bày khi phỏng vấn
Kể theo cấu trúc: **vấn đề → kiến trúc & vì sao → thách thức gặp & cách giải → kết quả → điều sẽ làm khác**. Nhấn các quyết định kỹ thuật (grain, idempotency, partition, exactly-once) để lộ chiều sâu.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Nêu 5 thứ nhà tuyển dụng tìm.
- [ ] Cấu trúc README/repo portfolio.
- [ ] Vì sao tránh tutorial clone; viết trade-off.
- [ ] Map artifact đã có → capstone.
- 🔭 *Tự mò:* viết README cho một capstone (chọn A/B/C ở các note sau) trước khi code — "README-driven development" giúp rõ phạm vi.

➡️ Tiếp: [[66-capstone-batch]].
