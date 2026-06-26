# 📋 task.md — Data Engineering (batch hiện tại)

> Hàng đợi cho loop. **Chế độ: NOTES-FIRST**. Phase 9 = phase cuối (capstone hướng dẫn để tự build portfolio).

## 🔁 PROTOCOL (đọc kỹ)
1. Tìm task `[ ]` đầu tiên theo ID. 2. Viết note ĐẦY ĐỦ (tiếng Việt) trong `notes/`. 3. KHÔNG bắt buộc code chạy/verify. 4. Xong: tick `[x]` + log `PROGRESS.md`. 5. Còn token làm tiếp. 6. **Khi hết Phase 9** → curriculum HOÀN TẤT: viết `notes/00-COURSE-COMPLETE.md` (index + lời kết), cập nhật README, KHÔNG sinh batch mới (đã hết ROADMAP). 7. Notes tiếng Việt, liên kết `[[...]]`.

**Batch hiện tại:** #10 — Phase 9: Capstone Projects (CUỐI)
**Phase:** 9/9

---

## BATCH HIỆN TẠI

### [x] T079 — Portfolio & cách trình bày dự án DE
- **Note:** `notes/65-capstone-portfolio.md`. Dự án portfolio tốt là gì; nhà tuyển dụng DE tìm gì; cách trình bày (README + sơ đồ kiến trúc + reproduce steps + tests + trade-off writeup); tránh "tutorial clone"; dùng lại 3 warehouse + pipeline đã build.

### [x] T080 — Capstone A: Batch Analytics Platform
- **Note:** `notes/66-capstone-batch.md`. Kiến trúc end-to-end: ingest (API/file) → lake (Parquet) → transform (Spark/polars) → warehouse (DuckDB/BigQuery) → **dbt** (models+tests) → **Airflow** orchestration → dashboard. Map sang artifact đã có (Phase 1 ETL + Phase 3 dbt). Checklist build + tiêu chí "đạt".

### [x] T081 — Capstone B: Streaming Pipeline
- **Note:** `notes/67-capstone-streaming.md`. Event generator → **Kafka** → Spark Structured Streaming (windowed aggregation + watermark) → sink (Delta/Postgres) → real-time dashboard; bonus **CDC** Postgres→Kafka (Debezium). Kiến trúc + docker-compose stack + checklist.

### [x] T082 — Capstone C: Lakehouse
- **Note:** `notes/68-capstone-lakehouse.md`. Multi-source ingest → **lakehouse** (Delta/Iceberg, medallion bronze/silver/gold) → Spark + dbt → orchestration → **data quality gates** (GE) → lineage. Kiến trúc + checklist; dùng delta-rs để làm được phần lớn local.

### [x] T083 — Course wrap-up: career & next steps
- **Note:** `notes/00-phase9-summary.md` + `notes/00-COURSE-COMPLETE.md` (index toàn bộ 60+ notes theo phase + lời kết). Lộ trình học tiếp, chứng chỉ, cách ôn, cập nhật README "DONE 9/9". Curriculum hoàn tất.

---
*Đây là batch CUỐI (Phase 9). Hết batch → curriculum hoàn tất, không sinh thêm.*
