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
5. **Khi tất cả `[x]`**: sinh batch mới (6–10) từ **Module tiếp theo trong `ADVANCED.md`**, ghi đè "BATCH HIỆN TẠI", cập nhật header. Hết module → đào sâu thêm.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #14 — Module D: Advanced Tool Deep-dives
**Nguồn:** ADVANCED.md

---

## BATCH HIỆN TẠI

### [x] D01 — Spark Internals deep ⭐
- **Note:** `notes/advanced/d01-spark-internals.md`. Memory management (execution vs storage, unified memory, spill), Tungsten (codegen, off-heap, columnar), AQE sâu (coalesce shuffle, skew join, dynamic switch), đọc Spark UI debug job chậm (stage/task/SQL/spill). Sâu hơn [[33-spark-tuning]].

### [x] D02 — dbt Advanced (semantic layer, packages, cấu trúc lớn)
- **Note:** `notes/advanced/d02-dbt-advanced.md`. Semantic layer / **metrics** (MetricFlow), packages (dbt_utils/dbt_expectations/audit_helper), custom materialization, cấu trúc project lớn (staging/intermediate/marts + domains), CI/CD nâng cao, contracts. Sâu hơn Phase 3.

### [x] D03 — Kafka Internals deep
- **Note:** `notes/advanced/d03-kafka-internals.md`. Storage (segment, log, page cache, zero-copy), replication protocol (leader epoch, ISR, high watermark), exactly-once sâu (idempotent producer + transactions + read_committed), tuning (batch/linger/compression/partitions). Sâu hơn [[46-kafka-core]].

### [x] D04 — Snowflake deep
- **Note:** `notes/advanced/d04-snowflake.md`. Kiến trúc 3 lớp (storage/compute/services), virtual warehouse (multi-cluster, auto-suspend/resume), **micro-partition** + pruning, clustering keys, time travel/zero-copy clone, tối ưu chi phí (warehouse sizing, query). 

### [ ] D05 — BigQuery deep
- **Note:** `notes/advanced/d05-bigquery.md`. Kiến trúc serverless (Dremel, slot, Colossus), partition + cluster, tối ưu **bytes-scanned** (chi phí), materialized views, BI Engine, streaming inserts, so sánh với Snowflake.

### [ ] D06 — Airflow Advanced
- **Note:** `notes/advanced/d06-airflow-advanced.md`. Dynamic DAG generation, custom operator/hook, **deferrable operators** (async, tiết kiệm worker), TaskGroups, datasets/data-aware scheduling, best practice scale (parsing, pools, executor), testing DAG. Sâu hơn Phase 5.

### [ ] D07 — Iceberg deep
- **Note:** `notes/advanced/d07-iceberg.md`. Metadata layers (metadata file → manifest list → manifest → data file), snapshot/time travel, hidden partitioning + partition evolution, schema evolution by ID, compaction/rewrite, catalog (REST/Glue/Nessie), so Delta vs Iceberg sâu. Sâu hơn [[35-table-formats]].

### [ ] D08 — Module D review + index
- **Note:** `notes/advanced/00-moduleD-summary.md`. Tổng kết Module D + cheat-sheet internals + self-assessment. Sẵn sàng sinh Batch #15 (Module E: Advanced Data Modeling).

---
*Hết batch → sinh Batch #15 từ Module E (ADVANCED.md).*
