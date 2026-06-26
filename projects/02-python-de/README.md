# Phase 1 — Programming for Data Engineering

Code thực hành Phase 1. Mọi script chạy với venv ở gốc dự án:
```bash
cd data-engineering && source .venv/bin/activate
```

## Các module
| File | Nội dung |
|------|----------|
| `01_pandas_basics.py` | pandas: select/filter, groupby, merge, pivot, vectorization |
| `02_polars_basics.py` | polars: expression API, lazy, benchmark vs pandas |
| `03_formats_benchmark.py` | CSV vs Parquet: size, read speed, pushdown, codecs |
| `04_json_avro.py` | JSON/JSONL flatten + Avro schema evolution |
| `05_api_ingest.py` | Ingest REST API resilient (retry/backoff, fallback) |
| `transforms.py` | Hàm transform **thuần** + pydantic validation (test được) |
| `utils.py` | Logging, config (env/YAML), retry decorator, exceptions |
| `etl_pipeline.py` | ⭐ **Capstone**: ETL end-to-end bronze→silver→gold |
| `tests/` | pytest cho `transforms.py` (14 tests) |

## ⭐ Capstone ETL (`etl_pipeline.py`)
Kiến trúc **medallion**:
```
data/raw/*.parquet          (BRONZE — dữ liệu thô)
        │  extract()
        ▼
silver: clean + enrich       (parse ts, lọc status hợp lệ, join category,
        │  transform_silver()  thêm order_month, quality gate null-check)
        ▼
gold: marts                  (mart_revenue_by_category, mart_monthly_revenue,
        │  build_gold()         mart_customer_ltv)
        ▼
warehouse/de.duckdb          (LOAD — CREATE OR REPLACE, idempotent)
+ data/processed/gold/*.parquet
```
Ghép: **polars** (transform), **transforms.py** (logic thuần test được), **utils.py** (logging + custom exceptions `Extract/Transform/LoadError`). Idempotent — chạy lại ra cùng kết quả.

### Chạy
```bash
python projects/02-python-de/etl_pipeline.py     # chạy pipeline, tạo bảng trong DuckDB
pytest projects/02-python-de -q                  # 14 tests
```

### Truy vấn warehouse sau khi chạy
```bash
python scripts/run_sql.py <(echo "SELECT * FROM mart_revenue_by_category")  # nếu muốn
# hoặc mở warehouse/de.duckdb bằng duckdb CLI / python
```

## Kiểm chứng chéo
Doanh thu theo category cho **cùng một con số** ở SQL (Phase 0), pandas (T011), polars (T012) và ETL gold (T018) — vd `Grocery = 1,714,225.45`. Một logic, nhiều công cụ, kết quả nhất quán = pipeline đúng.
