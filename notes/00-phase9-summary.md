# 🏁 Phase 9 — Tổng kết: Capstone & Career

> Phase cuối. Ghép tất cả thành portfolio + định hướng học tiếp.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| T079 | Portfolio & cách trình bày | [65](65-capstone-portfolio.md) |
| T080 | Capstone A: Batch Analytics | [66](66-capstone-batch.md) |
| T081 | Capstone B: Streaming | [67](67-capstone-streaming.md) |
| T082 | Capstone C: Lakehouse | [68](68-capstone-lakehouse.md) |

## 3 Capstone (chọn ít nhất 1–2 để build thật)
- **A — Batch Analytics**: ingest → lake → dbt → Airflow → dashboard. Dễ nhất, dùng lại Phase 1+3. Nền tảng must-have.
- **B — Streaming**: Kafka → stream processing → sink → live dashboard (+CDC). Nổi bật, chứng minh real-time.
- **C — Lakehouse**: medallion Delta + DQ + orchestration + lineage. "Đỉnh", chạy được local bằng delta-rs.

## 🎯 Career & next steps
- **Kỹ năng cốt lõi (ưu tiên)**: SQL ⭐ → Python → data modeling → 1 orchestrator (Airflow) → Spark → dbt → 1 cloud (AWS) → streaming → IaC/CI → data quality. (Bảng đầy đủ ở [ROADMAP.md](../ROADMAP.md).)
- **Phỏng vấn DE hay hỏi**: SQL window functions, fan-out, SCD2, idempotency, shuffle/partitioning, exactly-once, ELT vs ETL, star schema, CAP. → Mọi cái này có note riêng trong khoá.
- **Học tiếp**: build capstone thật → đọc *Designing Data-Intensive Applications* (Kleppmann) → đóng góp open-source → DE Zoomcamp (free, hands-on) → chứng chỉ cloud (AWS Data Analytics / GCP Data Engineer) nếu cần.
- **Thực hành > lý thuyết**: notes cho nền tảng, nhưng **phải tự build** (the "tự mò") mới vững. Mỗi note có mục 🔭 gợi ý.

## Tự đánh giá toàn khoá
Mở từng `notes/00-phaseN-summary.md`, làm checklist self-assessment. Ô nào chưa chắc → đọc lại note + làm phần "tự mò".

➡️ Xem [00-COURSE-COMPLETE.md](00-COURSE-COMPLETE.md) — index toàn bộ + lời kết.
