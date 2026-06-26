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
5. **Khi tất cả `[x]`**: Module F là module **CUỐI** trong ADVANCED.md. Hết Module F → **đào sâu thêm**: sinh batch mới gồm (a) bộ bài tập SQL mới (set 3,4...), (b) case study system design mới (log analytics, gaming telemetry, healthcare, ML platform...), (c) đào sâu bất kỳ chủ đề nào. Đặt tên batch tiếp (G/H...) hoặc "Extra". Giữ PROTOCOL.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #16 — Module F: DataOps, Architecture & Career (module cuối ADVANCED.md)
**Nguồn:** ADVANCED.md

---

## BATCH HIỆN TẠI

### [x] F01 — Data Testing Strategy toàn diện
- **Note:** `notes/advanced/f01-testing-strategy.md`. Kim tự tháp test cho data (unit transform → schema/contract → data quality → integration → e2e); test ở đâu trong pipeline; GE/Soda/dbt phối hợp; test data tổng hợp; CI gate. Tổng hợp [[12-testing-de]], [[24-dbt-tests]], [[60-data-quality]].

### [x] F02 — Pipeline Reliability & Incident Management (SRE cho data)
- **Note:** `notes/advanced/f02-reliability-sre.md`. SLA/SLO/SLI cho data, error budget; on-call cho data; incident lifecycle (detect→triage→mitigate→resolve→postmortem); TTD/TTR; runbook; blameless postmortem; backfill/replay khi recovery.

### [x] F03 — Modern Data Stack & chọn tool
- **Note:** `notes/advanced/f03-modern-data-stack.md`. Bản đồ MDS (ingestion: Fivetran/Airbyte; warehouse/lake; transform: dbt; orchestration; BI; observability; reverse-ETL); build vs buy; tiêu chí chọn tool; lakehouse vs MDS; xu hướng.

### [x] F04 — Cost Optimization Case Studies
- **Note:** `notes/advanced/f04-cost-cases.md`. 3-4 tình huống giảm chi phí thật (số liệu): query Athena/BQ giảm 90% nhờ partition+Parquet; warehouse Snowflake auto-suspend; small files compaction; incremental thay full; storage tiering. Quy trình audit chi phí. Tổng hợp [[59-cost-finops]].

### [ ] F05 — Data Mesh, Data Products & Team Topology
- **Note:** `notes/advanced/f05-data-mesh.md`. 4 nguyên tắc data mesh (domain ownership, data as product, self-serve platform, federated governance); data product là gì; centralized vs embedded vs mesh team; khi nào mesh (và khi nào KHÔNG — over-hype); data contracts vai trò.

### [ ] F06 — DataOps & CI/CD nâng cao
- **Note:** `notes/advanced/f06-dataops.md`. DataOps là gì (DevOps cho data); CI/CD pipeline cho data đầy đủ (lint→test→build→deploy→monitor); môi trường dev/staging/prod cho data; blue-green/zero-downtime data deploy; version data & code; automation. Sâu hơn [[58-cicd]].

### [ ] F07 — Roadmap Senior/Staff DE & Career
- **Note:** `notes/advanced/f07-career-roadmap.md`. Junior→mid→senior→staff DE khác nhau gì (scope, impact, ảnh hưởng); kỹ năng kỹ thuật + system design + leadership + communication; cách phát triển (T-shaped, học gì tiếp); DE vs analytics engineer vs ML engineer vs platform engineer; xu hướng nghề (AI/LLM ảnh hưởng DE).

### [ ] F08 — Module F review + Track 2 milestone
- **Note:** `notes/advanced/00-moduleF-summary.md` + cập nhật `notes/advanced/00-INDEX.md` (index toàn Track 2: Module A–F). Tổng kết + self-assessment. Hết ADVANCED.md → batch sau theo PROTOCOL bước 5 (đào sâu: SQL set 3, case study mới...).

---
*Module F là cuối ADVANCED.md. Hết batch → theo PROTOCOL bước 5: sinh batch "đào sâu" (bài tập/case mới).*
