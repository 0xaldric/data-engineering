# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Nguồn: [`ADVANCED.md`](ADVANCED.md). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–5 note/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt trong `notes/advanced/`: khái niệm + "tại sao", sơ đồ/bảng, snippet minh hoạ, cạm bẫy, checklist + "tự mò".
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch mới (6–10) từ **Module tiếp theo trong `ADVANCED.md`**, ghi đè "BATCH HIỆN TẠI", cập nhật header. **Hết Module F → đào sâu thêm** (bài tập SQL mới, case study system design mới) bất kỳ chủ đề nào.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #15 — Module E: Advanced Data Modeling
**Nguồn:** ADVANCED.md

---

## BATCH HIỆN TẠI

### [ ] E01 — Data Vault 2.0 ⭐
- **Note:** `notes/advanced/e01-data-vault.md`. Hub (business key) / Link (quan hệ) / Satellite (thuộc tính + lịch sử); vì sao DV (auditability, parallel load, schema linh hoạt, nguồn đổi); raw vault vs business vault; DV → star ở mart; so với Kimball/Inmon. Sơ đồ.

### [ ] E02 — One Big Table, Wide Tables & Activity Schema
- **Note:** `notes/advanced/e02-obt-wide.md`. OBT (denormalize tất cả vào 1 bảng) vs star; khi nào OBT thắng (columnar warehouse, ít join, BI tool); wide tables; **activity schema** (1 bảng stream of events); trade-off storage vs đơn giản/tốc độ.

### [ ] E03 — Modeling Event / Clickstream Data
- **Note:** `notes/advanced/e03-event-modeling.md`. Schema event (common + custom properties), semi-structured (JSON/struct), schema evolution, sessionization model, sparse columns, EAV vs wide vs JSON column; liên hệ [[c06-case-clickstream]].

### [ ] E04 — Bitemporal Modeling
- **Note:** `notes/advanced/e04-bitemporal.md`. **Valid time** (sự thật đúng trong khoảng nào ngoài đời) vs **transaction time** (hệ thống biết khi nào); bi-temporal table; vì sao cần (audit, "as-of" + "as-known"); so với SCD2 ([[18-scd]]); ví dụ bảo hiểm/tài chính.

### [ ] E05 — Semantic Layer & Metrics Layer
- **Note:** `notes/advanced/e05-semantic-layer.md`. Vì sao cần (metric nhất quán, tránh "mỗi dashboard một số"); semantic model (entity/dimension/measure/metric); headless BI; công cụ (dbt MetricFlow, Cube, LookML); governance metric; liên hệ [[d02-dbt-advanced]].

### [ ] E06 — Module E review + index
- **Note:** `notes/advanced/00-moduleE-summary.md`. Tổng kết Module E + so sánh các paradigm modeling (Kimball/Inmon/Data Vault/OBT) + self-assessment. Sẵn sàng sinh Batch #16 (Module F: DataOps, Architecture & Career).

---
*Hết batch → sinh Batch #16 từ Module F (ADVANCED.md).*
