# F07 — Roadmap Senior/Staff DE & Career

> Phát triển sự nghiệp Data Engineer: cấp bậc khác nhau gì, học gì tiếp, các nhánh nghề, xu hướng.

## Các cấp & khác biệt (scope of impact)
| Cấp | Scope | Đặc trưng |
|-----|-------|-----------|
| **Junior** | một task/pipeline có hướng dẫn | viết SQL/Python, sửa bug, học stack |
| **Mid** | sở hữu pipeline end-to-end | tự build pipeline đáng tin (test, idempotency, orchestration) |
| **Senior** | sở hữu một mảng/hệ thống | thiết kế hệ thống, đánh đổi, mentor, chuẩn mực kỹ thuật |
| **Staff/Principal** | nhiều team / tổ chức | kiến trúc cross-team, định hướng kỹ thuật, ảnh hưởng qua người khác |
→ Lên cấp = **mở rộng phạm vi tác động** (từ task → hệ thống → tổ chức), không chỉ "biết nhiều tool hơn".

## Kỹ năng theo cấp (T-shaped)
- **Sâu (vertical)**: SQL ⭐, data modeling, một orchestrator, Spark, một cloud, streaming — thành thạo thật.
- **Rộng (horizontal, lên senior+)**:
  - **System design**: thiết kế hệ thống dữ liệu, đánh đổi (Module C).
  - **Reliability/ops**: SRE, incident, cost ([[f02-reliability-sre]], [[f04-cost-cases]]).
  - **Communication**: giải thích cho non-tech, viết design doc, thuyết phục.
  - **Leadership**: mentor, review, định chuẩn, dẫn dắt dự án.
  - **Business sense**: hiểu data phục vụ quyết định gì.

## Cách phát triển
1. **Build thật** (capstone, side project, open-source) — chứng minh > chứng chỉ ([[65-capstone-portfolio]]).
2. **Đọc sâu**: *Designing Data-Intensive Applications* (Kleppmann), Kimball, docs official.
3. **Học khái niệm > tool**: tool đổi, concept (idempotency, shuffle, exactly-once, modeling) bền — đổi tool dễ ([[b08-explain-senior]]).
4. **Viết & chia sẻ**: blog, talk → củng cố hiểu + tăng visibility.
5. **Lấy scope lớn dần**: xung phong việc khó/mơ hồ, sở hữu hệ thống.

## Các nhánh nghề (so sánh)
| Vai trò | Trọng tâm |
|---------|-----------|
| **Data Engineer** | pipeline, hạ tầng data, độ tin cậy |
| **Analytics Engineer** | transform/dbt, modeling, semantic layer (giữa DE & analyst) |
| **ML Engineer** | model training/serving, feature pipeline (chồng DE ở feature) |
| **Platform/Infra DE** | nền tảng self-serve, tooling cho data team |
| **Data Architect** | thiết kế tổng thể, chuẩn, governance |
→ Ranh giới mờ; nhiều người dịch chuyển. Analytics engineer (dbt-centric) là điểm vào phổ biến từ analyst.

## Chứng chỉ (bổ trợ, không thay portfolio)
AWS/GCP Data Engineer, Databricks, Snowflake, Astronomer (Airflow). Hữu ích để lọc CV / học có hệ thống, nhưng **portfolio + phỏng vấn** quyết định.

## Xu hướng nghề (bối cảnh)
- **Lakehouse + table format mở** (Iceberg) thành nền chung.
- **Data quality/contracts/observability** trưởng thành → DQ là kỹ năng cốt lõi.
- **AI/LLM tác động DE**: text-to-SQL, copilot sinh pipeline/test/docs, tự debug → DE dịch lên **thiết kế, giám sát, đảm bảo đúng đắn** (việc lặp lại bị tự động hoá). Hiểu **khái niệm & trade-off** càng quan trọng (cái LLM chưa thay được). DE cũng xây hạ tầng cho AI (RAG, feature/vector store, data cho LLM).
- **Streaming-first & real-time** tăng dần.

## ⚠️ Cạm bẫy nghề
- Chạy theo tool mới mà không vững nền tảng.
- Chỉ code, không phát triển communication/system design (kẹt ở mid).
- Học lý thuyết không build (không có portfolio).
- Bỏ qua business context (build pipeline không ai dùng).

## ✅ "Tự mò"
🔭 Tự đánh giá: bạn đang ở cấp nào? Liệt kê 3 kỹ năng cần phát triển để lên cấp tiếp (vd: system design, một cloud sâu, mentor). Lên kế hoạch build 1 capstone + viết 1 blog post từ notes khoá này.

➡️ Tiếp: [[00-moduleF-summary]].
