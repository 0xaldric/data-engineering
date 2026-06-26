# 66 — Capstone A: Batch Analytics Platform

> Dự án "xương sống" của DE: batch pipeline end-to-end từ nguồn tới dashboard. Dùng lại phần lớn những gì đã build (Phase 1 + 3).

## Bài toán
"Phân tích bán hàng e-commerce: doanh thu theo category/tháng/region, top khách hàng, retention — cập nhật hàng ngày, có kiểm thử chất lượng, chạy tự động."

## Kiến trúc
```
   ┌─ API (T015) ─┐
   ├─ Files/CSV ──┤  EXTRACT
   └─ DB (CDC?) ──┘
         │ ingest (Python, idempotent, raw-first)
         ▼
   data lake (Parquet, partitioned)        ← BRONZE
         │ Spark/polars transform
         ▼
   warehouse (DuckDB / BigQuery)           ← SILVER
         │ dbt (staging→intermediate→marts, tests, snapshots)
         ▼
   marts: fct_sales, dim_*, mart_*         ← GOLD
         │
         ▼
   dashboard (Metabase/Superset/Streamlit)
         ▲
   Airflow orchestrate toàn bộ (daily) + alerting + DQ gates
```

## Map sang artifact đã có
| Thành phần | Đã có ở |
|-----------|---------|
| Dataset | `scripts/gen_ecommerce.py` |
| Ingest resilient | `05_api_ingest.py` ([[11-api-ingestion]]) |
| Transform medallion | `etl_pipeline.py` ([[00-phase1-summary]]) |
| dbt models+tests+snapshot+incremental | `projects/04-dbt/` ([[00-phase3-summary]]) |
| Star schema + SCD2 | Phase 2 |
→ Capstone A ≈ **ghép chúng + thêm Airflow + dashboard + DQ gate**.

## Checklist build
1. **Ingest**: script idempotent ghi raw Parquet partitioned theo ngày (bronze). Lưu raw trước ([[40-pipeline-patterns]]).
2. **Transform**: dbt staging→marts (đã có) + incremental cho fact lớn ([[27-dbt-incremental]]).
3. **DQ gates**: `dbt test` + Great Expectations ở ranh giới ingest ([[60-data-quality]]); fail → chặn downstream.
4. **Orchestration**: Airflow DAG `@daily`: ingest → load → `dbt build` → DQ → notify. Idempotent + backfill được ([[39-airflow-scheduling]], [[43-airflow-reliability]]).
5. **Serve**: dashboard (Streamlit đọc DuckDB là nhẹ nhất; hoặc Metabase/Superset).
6. **Ops**: logging/config ([[13-logging-config]]), Docker hoá ([[53-docker]]), CI chạy tests ([[58-cicd]]).

## Mở rộng để "ghi điểm"
- SCD2 cho dim_customer (snapshot dbt — [[26-dbt-snapshots]]).
- Incremental + backfill demo.
- CI/CD (GitHub Actions chạy `dbt build`).
- Data observability mini (freshness/volume check — [[62-observability]]).
- Cost note: Parquet + partition ([[59-cost-finops]]).

## Tiêu chí đạt
- [ ] `docker compose up` / `make run` chạy trọn pipeline.
- [ ] Airflow DAG chạy daily, idempotent, có retry + alert.
- [ ] dbt tests + DQ gate pass; fail thì chặn.
- [ ] Dashboard hiển thị các metric; số khớp (cross-check như Grocery=1.714M).
- [ ] README + sơ đồ + reproduce steps.

## 🔭 "Tự mò"
Bắt đầu nhỏ: Airflow local (`airflow standalone`) + 1 DAG gọi lại `etl_pipeline.py` rồi `dbt build` (DuckDB) + 1 Streamlit đọc `de.duckdb`. Sau đó thêm DQ gate & CI.

➡️ Tiếp: [[67-capstone-streaming]].
