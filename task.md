# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.
> ✅ Đã hoàn thành toàn bộ [`ADVANCED.md`](ADVANCED.md) (6 module A–F). Nay sang phần **ĐÀO SÂU** (Extra): bài tập SQL mới, case study system design mới, deep-dive thêm.

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–5 note/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt trong `notes/advanced/`: khái niệm + "tại sao", sơ đồ/bảng, snippet, cạm bẫy, checklist + "tự mò". Bài tập: **đề + lời giải + giải thích**.
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated với Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch "Extra" tiếp theo (đào sâu): SQL set mới, case study mới (chọn domain chưa làm: log analytics, gaming, healthcare, IoT khác, marketplace...), hoặc deep-dive chủ đề. Cập nhật `notes/advanced/00-INDEX.md` phần Extra. Giữ PROTOCOL. Không lặp note đã có.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`.

**Batch hiện tại:** #17 — Extra G: Deepening (SQL set 3-4, case mới, DS&A cho DE)
**Nguồn:** đào sâu (post-ADVANCED.md)

---

## BATCH HIỆN TẠI

### [x] G01 — SQL Interview Problems — Set 3 (advanced)
- **Note:** `notes/advanced/g01-sql-interview-3.md`. 10 bài khó: nth-highest per group, gaps nâng cao, conditional running total, pivot dynamic (giải thích giới hạn), date spine + fill gaps, top-N with ties, recursive (hierarchy/path), self-join inequality. Đề + lời giải + tư duy.

### [x] G02 — SQL Interview Problems — Set 4 (analytics-heavy)
- **Note:** `notes/advanced/g02-sql-interview-4.md`. 10 bài analytics: retention curve, cohort LTV, funnel ordered (time-bound), market basket, churn definition, MAU/DAU stickiness, percentile/median per group, sessionize + metrics. Đề + lời giải.

### [x] G03 — Case: Log Analytics / Observability Platform
- **Note:** `notes/advanced/g03-case-log-analytics.md`. Thu thập log/metric/trace khối lượng khổng lồ (như Datadog/ELK): ingest, parse, index, retention tiered, search, alerting; OLAP store (ClickHouse/Druid); cardinality explosion. Khung [[c01-system-design-framework]].

### [x] G04 — Case: Gaming Telemetry Platform
- **Note:** `notes/advanced/g04-case-gaming.md`. Telemetry game (player events, sessions, matchmaking, economy): real-time leaderboard, A/B test, anti-cheat, player retention; high write, sessionization, real-time + batch.

### [ ] G05 — Case: Healthcare Data Platform (compliance-heavy)
- **Note:** `notes/advanced/g05-case-healthcare.md`. Dữ liệu y tế: HIPAA/PII cực nhạy, audit, lineage, consent, de-identification; HL7/FHIR; bitemporal (lịch sử bệnh án); chính xác + governance là vua. Liên hệ [[64-governance-pii]], [[e04-bitemporal]].

### [ ] G06 — Case: ML Feature Platform & Data for LLM/RAG
- **Note:** `notes/advanced/g06-case-ml-llm-data.md`. Data cho ML/AI: feature store (online/offline, point-in-time — [[c09-case-recsys]]); data cho **LLM/RAG** (chunking, embedding, **vector DB**, retrieval pipeline, freshness); vai trò DE trong AI stack.

### [ ] G07 — Data Structures & Algorithms cho DE
- **Note:** `notes/advanced/g07-dsa-for-de.md`. Cấu trúc/giải thuật DE thực dùng: hashing & hash join, sorting & external sort, partitioning, merge, **B-tree vs LSM-tree** (storage engine), heap cho top-K. Vì sao quan trọng (Spark join, DB index).

### [ ] G08 — Probabilistic Data Structures & Approximate Queries
- **Note:** `notes/advanced/g08-probabilistic-ds.md` + cập nhật `00-INDEX.md` (Extra). **Bloom filter** (membership, dùng trong join/storage skip), **HyperLogLog** (approx count distinct — vì sao COUNT DISTINCT đắt), **t-digest/quantile sketch** (approx percentile), Count-Min sketch. Khi nào chấp nhận approx để scale.

---
*Hết batch → sinh Extra H (case mới: marketplace, fintech khác, social graph...; hoặc SQL set 5, deep-dive khác).*
