# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.
> ✅ ADVANCED.md (A–F) + Extra G–K xong. Tiếp tục **ĐÀO SÂU** (Extra L...).

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–5 note/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt: khái niệm + "tại sao", sơ đồ/bảng, snippet, cạm bẫy, checklist + "tự mò". Bài tập: **đề + lời giải + giải thích**.
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch Extra tiếp theo (M...): case domain chưa làm, SQL set mới, deep-dive. Cập nhật `00-INDEX.md`. Giữ PROTOCOL. Không lặp note đã có.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`.

**Batch hiện tại:** #22 — Extra L: case mới + deep-dive
**Nguồn:** đào sâu

---

## BATCH HIỆN TẠI

### [ ] L01 — SQL Interview Problems — Set 9 (mixed)
- **Note:** `notes/advanced/l01-sql-interview-9.md`. 10 bài: pivot rows→cols động (giải thích), conditional cumulative, top-N với filter phức tạp, recursive bill-of-materials, gap-and-island theo nhiều cột, time bucket histogram, year-to-date, rolling correlation, deduplicate by composite key, "khách active liên tục N tuần". Đề + lời giải.

### [ ] L02 — Case: HR / People Analytics Platform
- **Note:** `notes/advanced/l02-case-hr.md`. Dữ liệu nhân sự: headcount, attrition/turnover, hiring funnel, compensation, performance; SCD2 (org/role/salary đổi), bitemporal (sửa hồi tố), PII cực nhạy (lương), org hierarchy (recursive). Liên hệ [[18-scd]], [[64-governance-pii]].

### [ ] L03 — Case: Manufacturing / Industry 4.0
- **Note:** `notes/advanced/l03-case-manufacturing.md`. Sản xuất: machine telemetry (OEE), predictive maintenance, quality control, supply chain integration, production tracking; IoT + time-series + anomaly; downtime analysis. Liên hệ [[c04-case-iot]], [[i02-case-logistics]].

### [ ] L04 — Case: Retail Omnichannel
- **Note:** `notes/advanced/l04-case-retail-omni.md`. Bán lẻ đa kênh: online + store + app hợp nhất; customer 360 (identity resolution across kênh), inventory đồng bộ real-time, basket analysis, loyalty; CDC từ POS + ecommerce. Liên hệ [[c02-case-ecommerce]], [[h02-case-marketplace]].

### [ ] L05 — Deep-dive: Data Catalog Implementation
- **Note:** `notes/advanced/l05-data-catalog-impl.md`. Triển khai catalog: metadata harvesting (auto-scan schema/lineage), discovery/search, glossary, ownership, data classification (PII tagging tự động); DataHub/OpenMetadata; tích hợp dbt/Airflow; adoption (làm sao team dùng). Sâu hơn [[63-lineage-catalog]].

### [ ] L06 — Deep-dive: FinOps sâu (cost allocation)
- **Note:** `notes/advanced/l06-finops-deep.md`. Cost allocation (tag/label theo team/project), showback vs chargeback, unit economics (cost per query/pipeline/GB), budget/forecast, anomaly chi phí, optimization governance; cụ thể warehouse/lake/compute. Sâu hơn [[59-cost-finops]], [[f04-cost-cases]].

### [ ] L07 — Deep-dive: Schema Evolution Patterns
- **Note:** `notes/advanced/l07-schema-evolution.md`. Quản schema đổi an toàn: additive (thêm cột default), backward/forward/full compatibility; Avro/Protobuf/Parquet/Iceberg evolution; handle trong pipeline (nullable, default, versioned); migration cột (rename = add+backfill+drop). Tổng hợp [[10-json-avro]], [[d07-iceberg]], [[k06-data-contract-impl]].

### [ ] L08 — Extra L review + index
- **Note:** `notes/advanced/00-extraL-summary.md` + cập nhật `00-INDEX.md`. Tổng kết Extra L. Sẵn sàng Extra M.

---
*Hết batch → sinh Extra M (case: travel/hospitality, edtech, logistics last-mile...; SQL set 10; deep-dive: Spark structured streaming sâu, data mesh impl...).*
