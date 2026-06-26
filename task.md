# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, chế độ **MAX OUTPUT**). Nguồn chủ đề: [`ADVANCED.md`](ADVANCED.md). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt trong lượt** (overnight max-output — nhắm 3–5 note/lượt) trong khi vẫn **giữ chất lượng**. Mỗi task = 1 note đầy đủ (tiếng Việt) trong `notes/advanced/`: khái niệm + "tại sao", sơ đồ/bảng, snippet minh hoạ, cạm bẫy, checklist + "tự mò". Task interview/bài tập: **đề + lời giải + giải thích**.
3. Mỗi task xong: đổi `[ ]` → `[x]` + thêm dòng vào `PROGRESS.md`.
4. **Cuối mỗi lượt: commit + push** (KHÔNG kèm Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By" / "Generated with Claude". Push lỗi mạng → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch mới (6–10 task) từ **Module tiếp theo trong `ADVANCED.md`**, ghi đè "BATCH HIỆN TẠI", cập nhật header. Giữ PROTOCOL. Hết module → đào sâu thêm (bài tập/case mới).
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #12 — Module B: DE Interview Prep (conceptual)
**Nguồn:** ADVANCED.md

---

## BATCH HIỆN TẠI

### [ ] B01 — Spark & Big Data Q&A
- **Note:** `notes/advanced/b01-spark-qa.md`. 15+ câu phỏng vấn + đáp án: lazy/action, narrow/wide, shuffle, partition, broadcast vs sort-merge, Catalyst/Tungsten/AQE, cache, skew, OOM, small files, RDD vs DataFrame. Link [[30-spark-model]]..[[33-spark-tuning]].

### [ ] B02 — Streaming & Kafka Q&A
- **Note:** `notes/advanced/b02-kafka-qa.md`. 15+ câu: partition/key/offset, consumer group, delivery semantics, exactly-once, watermark/late data, windowing, retention vs compaction, CDC, Lambda vs Kappa, backpressure. Link [[46-kafka-core]]..[[52-lambda-kappa]].

### [ ] B03 — Warehousing & dbt Q&A
- **Note:** `notes/advanced/b03-dbt-qa.md`. 15+ câu: ELT vs ETL, materializations, ref/source/DAG, tests (relationships vì sao quan trọng), snapshots SCD2, incremental strategies, macros, exposures, slim CI. Link Phase 3 notes.

### [ ] B04 — Orchestration & Reliability Q&A
- **Note:** `notes/advanced/b04-orchestration-qa.md`. 15+ câu: DAG, idempotency (vì sao sống còn), execution_date/data_interval, catchup/backfill, XCom limits, retries/SLA, trigger rules, Airflow vs Dagster vs Prefect. Link Phase 5.

### [ ] B05 — Cloud & Infra Q&A
- **Note:** `notes/advanced/b05-cloud-qa.md`. 15+ câu: S3 không phải filesystem, partition layout, IAM least privilege, Athena bytes-scanned, EMR vs Glue, Terraform state, Docker layer cache, K8s cho data, CI/CD cho dbt. Link Phase 7.

### [ ] B06 — Data Modeling Q&A (sâu)
- **Note:** `notes/advanced/b06-modeling-qa.md`. 15+ câu sâu hơn A07: grain, fan-out, SCD types & khi nào, fact types & additivity, conformed dimension, surrogate vs natural key, normalize vs denormalize, Data Vault sơ lược, slowly changing fact. Link Phase 2.

### [ ] B07 — Behavioral & Scenario (STAR)
- **Note:** `notes/advanced/b07-behavioral-star.md`. Phương pháp **STAR** (Situation/Task/Action/Result); 10 câu behavioral DE hay gặp (pipeline lỗi production, dữ liệu sai, xung đột stakeholder, tối ưu chi phí, deadline...) + khung trả lời mẫu; câu hỏi nên hỏi ngược nhà tuyển dụng.

### [ ] B08 — "Explain like senior" + Module B review
- **Note:** `notes/advanced/b08-explain-senior.md` + `notes/advanced/00-moduleB-summary.md`. Giải thích SÂU 10 khái niệm hay bị đào (idempotency, exactly-once, shuffle, SCD2, partitioning, CAP, ELT, lineage, backfill, watermark) ở mức "senior trả lời". + tổng kết Module B. Sẵn sàng sinh Batch #13 (Module C: System Design).

---
*Hết batch → sinh Batch #13 từ Module C (System Design) trong ADVANCED.md.*
