# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.
> ✅ ADVANCED.md (A–F) + Extra G,H xong. Tiếp tục **ĐÀO SÂU** (Extra I...): case mới, SQL set mới, deep-dive.

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–5 note/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt: khái niệm + "tại sao", sơ đồ/bảng, snippet, cạm bẫy, checklist + "tự mò". Bài tập: **đề + lời giải + giải thích**.
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch Extra tiếp theo (J, K...): case domain chưa làm, SQL set mới, deep-dive. Cập nhật `00-INDEX.md`. Giữ PROTOCOL. Không lặp note đã có.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`.

**Batch hiện tại:** #19 — Extra I: case mới + deep-dive thực chiến
**Nguồn:** đào sâu

---

## BATCH HIỆN TẠI

### [ ] I01 — SQL Interview Problems — Set 6 (tricky/edge)
- **Note:** `notes/advanced/i01-sql-interview-6.md`. 10 bài hóc: overlapping intervals (merge khoảng), gaps in sequence, conditional join, anti-pattern rewrite, correlated → window, exists vs in vs join, NULL trong aggregate/join bẫy, pivot nhiều chiều, cumulative distinct, "second purchase date". Đề + lời giải.

### [ ] I02 — Case: Logistics / Supply Chain Platform
- **Note:** `notes/advanced/i02-case-logistics.md`. Theo dõi hàng (shipment lifecycle, warehouse, route, inventory), IoT tracking, ETA, demand forecast, inventory optimization; accumulating snapshot, geospatial, CDC từ WMS/ERP. Khung [[c01-system-design-framework]].

### [ ] I03 — Case: Video Streaming Platform (Netflix/YouTube)
- **Note:** `notes/advanced/i03-case-video-streaming.md`. Playback events (start/pause/buffer/quality), QoE (quality of experience), recommendation data, A/B test encoding, CDN analytics, watch-time; khối lượng cực lớn, real-time QoE + batch.

### [ ] I04 — Case: Banking Core / Payments
- **Note:** `notes/advanced/i04-case-banking.md`. Hệ ngân hàng lõi: account/transaction, double-entry ledger, reconciliation, fraud, regulatory reporting (immutable, audit), real-time balance; chính xác + compliance tuyệt đối. Sâu hơn [[c07-case-fintech]].

### [ ] I05 — Deep-dive: Spark Tuning thực chiến (scenarios)
- **Note:** `notes/advanced/i05-spark-tuning-scenarios.md`. 5-6 tình huống tuning thật + cách chẩn đoán & sửa: OOM executor, skew join chậm, small files, shuffle khổng lồ, spill, UDF chậm. Triệu chứng Spark UI → nguyên nhân → fix. Sâu hơn [[d01-spark-internals]].

### [ ] I06 — Deep-dive: Data Quality Framework chi tiết
- **Note:** `notes/advanced/i06-dq-framework.md`. Triển khai DQ end-to-end: expectation suite (GE), Soda checks, dbt tests phối hợp; DQ ở mỗi tầng medallion; data quality score; quarantine + circuit breaker; report & alert. Sâu hơn [[60-data-quality]], [[f01-testing-strategy]].

### [ ] I07 — Deep-dive: Backfill & Reprocessing Strategies
- **Note:** `notes/advanced/i07-backfill-reprocessing.md`. Khi nào cần backfill (logic đổi, bug, nguồn bổ sung); chiến lược (partition overwrite, blue-green, shadow table); backfill an toàn (idempotent, không ảnh hưởng live); reprocessing stream (Kappa replay); kiểm soát tải. Sâu hơn [[40-pipeline-patterns]].

### [ ] I08 — Extra I review + index
- **Note:** `notes/advanced/00-extraI-summary.md` + cập nhật `00-INDEX.md`. Tổng kết Extra I. Sẵn sàng Extra J.

---
*Hết batch → sinh Extra J (case: telecom, energy/utility, govtech...; SQL set 7; deep-dive: streaming exactly-once thực chiến, lakehouse migration...).*
