# 🏁 Phase 3 — Tổng kết: Data Warehousing & Analytics Engineering (dbt)

Hoàn thành Phase 3. Trọng tâm: **dbt** — biến SQL thành pipeline transform có kỹ thuật phần mềm (modular, test, docs, lineage).

## Đã làm gì (Batch #4)
| # | Chủ đề | Artifact |
|---|--------|----------|
| T029 | Warehouse concepts + dbt setup | `projects/04-dbt/` (dbt_project/profiles/sources), `notes/21` |
| T030 | Staging models | `models/staging/stg_*`, `notes/22` |
| T031 | Intermediate + Marts (star schema) | `models/intermediate|marts/*`, `notes/23` |
| T032 | dbt tests | `_marts.yml`, `tests/`, `notes/24` |
| T033 | Macros & Jinja | `macros/price_tier.sql`, `mart_sales_by_status`, `notes/25` |
| T034 | Snapshots (SCD2) | `snapshots/scd_customer.sql`, `notes/26` |
| T035 | Incremental models | `fct_daily_sales_inc.sql`, `notes/27` |
| T036 | Docs, lineage, seeds | `seeds/`, `mart_revenue_by_region`, `notes/28` |
| T037 | Review + smoke test | file này, `scripts/run_all.sh` |

**Kiểm chứng:** `bash scripts/run_all.sh` → Phase 0+1+2+3 = **ALL GREEN** (9 SQL + 11 Python + pytest + **dbt build** + shell). Bug đã fix: glob `*.sql` từng quét nhầm file dbt → loại trừ `*/04-dbt/*` (dbt do `dbt build` lo).

---

## 📑 Cheat-Sheet dbt

### Kiến trúc & lệnh
```
source → staging(view) → intermediate(view) → dim/fct/mart(table)
```
| Lệnh | Việc |
|------|------|
| `dbt deps` | cài packages (dbt_utils) |
| `dbt run` | build models (`-s model+`, `+model`) |
| `dbt test` | chạy tests |
| `dbt snapshot` | SCD2 snapshots |
| `dbt seed` | nạp CSV |
| `dbt build` | run+test+snapshot+seed theo DAG (chặn lan lỗi) |
| `dbt docs generate` | manifest.json (DAG) + catalog.json |

### Khái niệm cốt lõi
- **`ref()`/`source()`** → dbt tự dựng DAG & lineage. Không hardcode tên bảng.
- **Materializations**: view (staging/int) · table (marts) · ephemeral (CTE) · incremental (data lớn).
- **Tests**: generic (`unique/not_null/accepted_values/relationships`) + singular (SQL tuỳ ý). `relationships` = FK fact→dim (OLAP không tự enforce).
- **Jinja**: `{{ }}` biểu thức · `{% %}` lệnh · `{# #}` comment. Macro = hàm sinh SQL (DRY). ⚠️ không để tag Jinja trong comment `--`.
- **dbt_utils**: `generate_surrogate_key`, `star`, `date_spine`, `pivot`...
- **Snapshots** = SCD2 tự động (`dbt_valid_from/to`, strategy `check`/`timestamp`).
- **Incremental**: `is_incremental()` + `{{ this }}` watermark; strategy append/merge/delete+insert/insert_overwrite.
- **Seeds**: CSV nhỏ tĩnh versioned (lookup).
- **Lineage**: impact analysis (`dbt ls -s model+`), exposures (nơi tiêu thụ).

### ELT & warehouse
- dbt lo **"T"** trong ELT (transform trong warehouse bằng SQL). Không lo E/L.
- Layering medallion; tách compute/storage ở cloud DW (BigQuery/Snowflake/Redshift).

---

## ✅ Self-assessment Phase 3
- [ ] Scaffold dbt project, sources, profiles; phân biệt ELT vs ETL
- [ ] Layering staging→intermediate→marts; chọn materialization đúng
- [ ] `ref()`/`source()` dựng DAG; chạy chọn lọc `model+`/`+model`
- [ ] Viết generic + singular tests; hiểu `relationships` quan trọng vì sao
- [ ] Macro + Jinja loop (DRY); dùng dbt_utils
- [ ] Snapshot SCD2 (strategy, cột dbt_valid_*)
- [ ] Incremental (is_incremental, strategies, late data)
- [ ] Seeds, docs/lineage, `dbt build`

> dbt project hoàn chỉnh: 11 models + 17 tests + macro + SCD2 snapshot + incremental + seed + docs. `Grocery=1,714,225.45` khớp với mọi cách triển khai trước.

## ➡️ Tiếp theo: Phase 4 — Batch Processing & Big Data
Apache Spark (PySpark): RDD/DataFrame, partition/shuffle, Catalyst, performance tuning; lakehouse (Delta/Iceberg). Loop sẽ sinh **Batch #5**.
