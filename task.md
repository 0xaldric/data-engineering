# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Nguồn: [`ADVANCED.md`](ADVANCED.md). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–5 note/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt trong `notes/advanced/`: khái niệm + "tại sao", sơ đồ/bảng, snippet minh hoạ, cạm bẫy, checklist + "tự mò". Case study: nêu requirements → kiến trúc (sơ đồ) → lựa chọn & trade-off → scale.
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch mới (6–10) từ **Module tiếp theo trong `ADVANCED.md`**, ghi đè "BATCH HIỆN TẠI", cập nhật header. Hết module → đào sâu thêm.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #13 — Module C: System Design for Data Engineering
**Nguồn:** ADVANCED.md

> Mỗi case theo khung: **Requirements** (functional + scale/latency) → **Data model** → **Pipeline** (ingest→process→store→serve, batch/stream) → **Tech choices + trade-off** → **Scale & failure** → **DQ/observability**.

---

## BATCH HIỆN TẠI

### [x] C01 — Framework thiết kế hệ thống DE ⭐
- **Note:** `notes/advanced/c01-system-design-framework.md`. Khung 6 bước trả lời system design interview cho DE; câu hỏi làm rõ requirements (volume/velocity/latency/SLA/consistency); batch vs stream vs lambda/kappa; cách trình bày & các trục đánh đổi (cost/latency/complexity).

### [x] C02 — Case: E-commerce Analytics Platform
- **Note:** `notes/advanced/c02-case-ecommerce.md`. Thiết kế nền tảng phân tích bán hàng (như project đã build nhưng quy mô lớn): ingest đa nguồn → lakehouse medallion → dbt → BI; near-real-time inventory; scale tới hàng tỉ event.

### [x] C03 — Case: Real-time Fraud Detection ⭐
- **Note:** `notes/advanced/c03-case-fraud.md`. Phát hiện gian lận giao dịch real-time: Kafka → stream processing (Flink, stateful + windowed features) → model scoring → block/alert ms; exactly-once, late data, feature store.

### [x] C04 — Case: IoT / Sensor Data Platform
- **Note:** `notes/advanced/c04-case-iot.md`. Hàng triệu sensor gửi telemetry: ingest tải cao (Kafka/Kinesis), time-series storage, downsampling/rollup, edge vs cloud, out-of-order data, retention.

### [ ] C05 — Case: Ride-sharing Data Platform
- **Note:** `notes/advanced/c05-case-ridesharing.md`. Như Uber: trip events, geospatial, surge pricing real-time, ETA, driver-rider matching analytics; lambda/kappa, CDC từ OLTP, lakehouse.

### [ ] C06 — Case: Clickstream / Social Media Analytics
- **Note:** `notes/advanced/c06-case-clickstream.md`. Tracking event web/app khối lượng khổng lồ: SDK→collector→Kafka→stream+batch; sessionization, funnel/retention ở scale; schema evolution; sampling; One Big Table vs star.

### [ ] C07 — Case: Fintech Ledger + Reconciliation ⭐
- **Note:** `notes/advanced/c07-case-fintech.md`. Sổ cái giao dịch tài chính: **chính xác tuyệt đối** (không mất/trùng tiền), idempotency, exactly-once, audit/immutability, reconciliation đối soát, double-entry, compliance.

### [ ] C08 — Case: Ad-tech / Real-time Bidding
- **Note:** `notes/advanced/c08-case-adtech.md`. RTB: latency cực thấp (<100ms), khối lượng cực lớn, impression/click/conversion join (attribution), budget pacing, fraud, lambda architecture.

### [ ] C09 — Case: Recommendation Pipeline + Module C review
- **Note:** `notes/advanced/c09-case-recsys.md` + `notes/advanced/00-moduleC-summary.md`. Data pipeline cho hệ gợi ý: feature engineering, **feature store** (online/offline), training data, batch vs real-time features, feedback loop. + tổng kết Module C. Sẵn sàng sinh Batch #14 (Module D: Tool deep-dives).

---
*Hết batch → sinh Batch #14 từ Module D (ADVANCED.md).*
