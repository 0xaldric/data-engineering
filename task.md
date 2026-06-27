# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.
> ✅ ADVANCED.md (A–F) + Extra G,H,I,J xong. Tiếp tục **ĐÀO SÂU** (Extra K...).

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–5 note/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt: khái niệm + "tại sao", sơ đồ/bảng, snippet, cạm bẫy, checklist + "tự mò". Bài tập: **đề + lời giải + giải thích**.
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch Extra tiếp theo (L...): case domain chưa làm, SQL set mới, deep-dive. Cập nhật `00-INDEX.md`. Giữ PROTOCOL. Không lặp note đã có.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`.

**Batch hiện tại:** #21 — Extra K: case mới + deep-dive AI/contract/observability
**Nguồn:** đào sâu

---

## BATCH HIỆN TẠI

### [x] K01 — SQL Interview Problems — Set 8 (mixed)
- **Note:** `notes/advanced/k01-sql-interview-8.md`. 10 bài: overlapping count (max concurrent), running count distinct theo window, conditional pivot, hierarchical aggregate (rollup theo cây), nearest neighbor (asof join), first event after condition, ratio/share, sliding window distinct, deduplicate keeping latest non-null, sequence gap detection. Đề + lời giải.

### [x] K02 — Case: Insurance Data Platform
- **Note:** `notes/advanced/k02-case-insurance.md`. Bảo hiểm: policy lifecycle, claims processing, underwriting/risk pricing, fraud detection, actuarial; bitemporal (policy/claim sửa hồi tố), reserving chính xác, regulatory. Liên hệ [[e04-bitemporal]], [[c07-case-fintech]].

### [x] K03 — Case: Real Estate / PropTech
- **Note:** `notes/advanced/k03-case-realestate.md`. Listing, pricing/valuation (AVM), market analytics, search; ingest đa nguồn (MLS, public records), geospatial, slowly changing listing, price history; estimate model data.

### [x] K04 — Case: AgriTech / Precision Farming
- **Note:** `notes/advanced/k04-case-agritech.md`. Cảm biến nông nghiệp (đất/thời tiết/drone/satellite), yield prediction, irrigation optimization; IoT + geospatial + weather data integration; time-series + image data. Liên hệ [[c04-case-iot]].

### [ ] K05 — Deep-dive: Vector DB & RAG sâu
- **Note:** `notes/advanced/k05-vector-rag-deep.md`. Vector DB nội tại (HNSW/IVF index, ANN search), embedding pipeline, chunking strategies, hybrid search (vector + keyword/BM25), re-ranking, RAG eval (recall@k, faithfulness), freshness/incremental re-embed. Sâu hơn [[g06-case-ml-llm-data]].

### [ ] K06 — Deep-dive: Data Contract Implementation
- **Note:** `notes/advanced/k06-data-contract-impl.md`. Triển khai data contract thật: định nghĩa (YAML/JSON schema + SLA + semantics), enforcement (CI schema diff, runtime validation, Schema Registry), versioning & breaking change workflow, producer/consumer responsibility. Sâu hơn [[61-data-contracts]].

### [ ] K07 — Deep-dive: Data Observability Tooling
- **Note:** `notes/advanced/k07-observability-tooling.md`. Triển khai observability: 5 trụ (freshness/volume/schema/distribution/lineage) đo thế nào; Elementary (dbt-native), Monte Carlo, Soda; anomaly detection (baseline + ML); alerting + incident; SLO data. Sâu hơn [[62-observability]].

### [ ] K08 — Extra K review + index
- **Note:** `notes/advanced/00-extraK-summary.md` + cập nhật `00-INDEX.md`. Tổng kết Extra K. Sẵn sàng Extra L.

---
*Hết batch → sinh Extra L (case: HR/people analytics, manufacturing, retail omnichannel...; SQL set 9; deep-dive: data catalog, FinOps sâu, schema evolution patterns...).*
