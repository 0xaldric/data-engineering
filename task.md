# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.
> ✅ ADVANCED.md (6 module A–F) + Extra G xong. Tiếp tục **ĐÀO SÂU** (Extra H...): case mới, SQL set mới, deep-dive engine.

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–5 note/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt: khái niệm + "tại sao", sơ đồ/bảng, snippet, cạm bẫy, checklist + "tự mò". Bài tập: **đề + lời giải + giải thích**.
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch Extra tiếp theo (I, J...): case domain chưa làm, SQL set mới, deep-dive engine/concept. Cập nhật `00-INDEX.md`. Giữ PROTOCOL. Không lặp note đã có.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`.

**Batch hiện tại:** #18 — Extra H: case mới + engine deep-dive + mock interview
**Nguồn:** đào sâu

---

## BATCH HIỆN TẠI

### [x] H01 — SQL Interview Problems — Set 5 (window edge cases)
- **Note:** `notes/advanced/h01-sql-interview-5.md`. 10 bài mẹo: frame edge (LAST_VALUE sai frame), RANGE vs ROWS với ties, ignore nulls, qualify, lag với default, running distinct (khó), median chính xác, gap-fill forward (carry-forward last value), pivot conditional nâng cao. Đề + lời giải.

### [x] H02 — Case: Marketplace / Two-sided Platform
- **Note:** `notes/advanced/h02-case-marketplace.md`. Như Airbnb/eBay/Etsy: buyer + seller, listing, search ranking, transaction, GMV, take rate, supply-demand matching, review/trust, fraud. Hai phía analytics. Khung [[c01-system-design-framework]].

### [x] H03 — Case: SaaS / Subscription Metrics Platform
- **Note:** `notes/advanced/h03-case-saas-metrics.md`. Metrics SaaS: MRR/ARR, churn (logo vs revenue), expansion/contraction, LTV/CAC, cohort retention; subscription events (CDC từ billing), SCD cho plan changes; báo cáo nhà đầu tư chính xác. Liên hệ [[18-scd]], [[a03-analytics-patterns]].

### [x] H04 — Case: Social Graph / Network Data
- **Note:** `notes/advanced/h04-case-social-graph.md`. Đồ thị xã hội (follow/friend): graph storage, friend-of-friend, feed generation (fan-out write vs read), graph DB vs relational, recursive traversal ở scale, influencer skew. Liên hệ [[a02-sql-pivot-hierarchical]] recursive.

### [ ] H05 — Deep-dive: Query Engines (Trino/Presto) & Federation
- **Note:** `notes/advanced/h05-trino-federation.md`. Trino/Presto kiến trúc (coordinator/worker, MPP, không storage); query federation (join across nguồn: S3+MySQL+Kafka); connector; so với Spark SQL; khi nào dùng. Tối ưu query trên lake.

### [ ] H06 — Deep-dive: Real-time OLAP (ClickHouse/Druid/Pinot)
- **Note:** `notes/advanced/h06-realtime-olap.md`. Vì sao cần OLAP store riêng (dashboard sub-giây trên tỉ row); ClickHouse (columnar, vectorized, MergeTree), Druid (segment, real-time ingest), Pinot; so warehouse; khi nào dùng; pre-aggregation. Liên hệ [[g03-case-log-analytics]].

### [ ] H07 — Mock Interview: full DE interview walkthrough
- **Note:** `notes/advanced/h07-mock-interview.md`. Mô phỏng 1 vòng phỏng vấn DE đầy đủ: SQL coding (2 bài + lời giải nói), system design (1 case đi qua framework live), conceptual (5 câu), behavioral (2 STAR). Như kịch bản thật, kèm "tips người phỏng vấn đánh giá gì".

### [ ] H08 — Extra H review + index
- **Note:** `notes/advanced/00-extraH-summary.md` + cập nhật `00-INDEX.md`. Tổng kết Extra H + self-assessment tổng. Sẵn sàng Extra I.

---
*Hết batch → sinh Extra I (case: tài chính/ngân hàng, logistics/supply-chain, video streaming...; SQL set 6; deep-dive: data quality framework, Spark tuning thực chiến...).*
