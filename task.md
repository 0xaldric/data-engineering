# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.
> ✅ ADVANCED.md (A–F) + Extra G,H,I xong. Tiếp tục **ĐÀO SÂU** (Extra J...).

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–5 note/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt: khái niệm + "tại sao", sơ đồ/bảng, snippet, cạm bẫy, checklist + "tự mò". Bài tập: **đề + lời giải + giải thích**.
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch Extra tiếp theo (K...): case domain chưa làm, SQL set mới, deep-dive. Cập nhật `00-INDEX.md`. Giữ PROTOCOL. Không lặp note đã có.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`.

**Batch hiện tại:** #20 — Extra J: case mới + deep-dive
**Nguồn:** đào sâu

---

## BATCH HIỆN TẠI

### [x] J01 — SQL Interview Problems — Set 7 (mixed hard)
- **Note:** `notes/advanced/j01-sql-interview-7.md`. 10 bài tổng hợp khó: running max/min, islands có điều kiện, pivot + aggregate, recursive running balance, lead/lag nhiều bước, conditional first/last, dedup phức tạp, percentile bucket, time-weighted average, "khách mua đủ N category". Đề + lời giải.

### [x] J02 — Case: Telecom / CDR Platform
- **Note:** `notes/advanced/j02-case-telecom.md`. Call Detail Records (CDR) khối lượng khổng lồ: billing, network usage, dropped call analytics, churn prediction; rating/charging real-time, fraud (SIM box), data usage; high volume + chính xác billing.

### [x] J03 — Case: Energy / Utility / Smart Meter
- **Note:** `notes/advanced/j03-case-energy.md`. Smart meter (đọc điện/nước theo interval), demand forecast, billing, grid monitoring, anomaly (rò rỉ/trộm); time-series khổng lồ, out-of-order, interval data, rollup. Liên hệ [[c04-case-iot]].

### [x] J04 — Case: GovTech / Public Data Platform
- **Note:** `notes/advanced/j04-case-govtech.md`. Dữ liệu công (census, thuế, y tế công, giao thông): tích hợp nhiều nguồn (Data Vault), privacy/anonymization, open data, audit, độ tin cậy; governance + lineage nặng. Liên hệ [[e01-data-vault]], [[64-governance-pii]].

### [ ] J05 — Deep-dive: Streaming Exactly-once thực chiến
- **Note:** `notes/advanced/j05-streaming-eos.md`. Triển khai exactly-once end-to-end thật: Kafka EOS (idempotent producer + transaction) + Spark/Flink checkpoint + **sink idempotent** (upsert/dedup theo key); các điểm có thể trùng/mất; pattern cho sink ngoài (DB/lake). Sâu hơn [[47-kafka-consumers]], [[49-stream-processing]].

### [ ] J06 — Deep-dive: Lakehouse Migration
- **Note:** `notes/advanced/j06-lakehouse-migration.md`. Di chuyển: Hive→Iceberg/Delta, on-prem Hadoop→cloud lakehouse, warehouse→lakehouse; chiến lược (dual-write, backfill, cutover, validation); rủi ro & rollback; chi phí; downtime. Liên hệ [[35-table-formats]], [[i07-backfill-reprocessing]].

### [ ] J07 — Deep-dive: dbt at Scale (large project)
- **Note:** `notes/advanced/j07-dbt-at-scale.md`. dbt project nghìn model: cấu trúc theo domain, naming, tags, exposures, performance (incremental, không full rebuild), CI slim, governance metric, ownership; tránh "spaghetti dbt". Sâu hơn [[d02-dbt-advanced]].

### [ ] J08 — Extra J review + index
- **Note:** `notes/advanced/00-extraJ-summary.md` + cập nhật `00-INDEX.md`. Tổng kết Extra J. Sẵn sàng Extra K.

---
*Hết batch → sinh Extra K (case: insurance, real estate, agritech...; SQL set 8; deep-dive: vector DB/RAG sâu, data contract implementation...).*
