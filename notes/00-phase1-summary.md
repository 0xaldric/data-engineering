# 🏁 Phase 1 — Tổng kết: Programming for Data Engineering

Hoàn thành Phase 1. Trọng tâm: **Python data stack + file formats + ingestion + code có test + ETL end-to-end**.

## Đã làm gì (Batch #2)
| # | Chủ đề | Artifact |
|---|--------|----------|
| T011 | pandas fundamentals | `01_pandas_basics.py`, `notes/07-pandas.md` |
| T012 | polars + benchmark | `02_polars_basics.py`, `notes/08-polars.md` |
| T013 | File formats CSV vs Parquet | `03_formats_benchmark.py`, `notes/09-file-formats.md` |
| T014 | JSON/JSONL + Avro | `04_json_avro.py`, `notes/10-json-avro.md` |
| T015 | API ingestion resilient | `05_api_ingest.py`, `notes/11-api-ingestion.md` |
| T016 | Clean code + pytest | `transforms.py`, `tests/`, `notes/12-testing-de.md` |
| T017 | Logging/config/errors | `utils.py`, `notes/13-logging-config.md` |
| T018 | ⭐ Capstone ETL | `etl_pipeline.py`, `projects/02-python-de/README.md` |
| T019 | Review + smoke test | file này, `scripts/run_all.sh` mở rộng |

**Kiểm chứng:** `bash scripts/run_all.sh` → Phase 0 (6 SQL + shell) + Phase 1 (7 script Python + pytest 14) = **ALL GREEN ✅**.

---

## 📑 Cheat-Sheet Phase 1

### pandas vs polars
| | pandas | polars |
|--|--------|--------|
| Mô hình | eager, có index | lazy được, không index |
| Tốc độ | baseline | nhanh hơn (Rust, Arrow, đa luồng) |
| Filter | `df[df.x>2]` | `df.filter(pl.col("x")>2)` |
| Cột mới | `df.assign(...)` | `df.with_columns(...)` |
| Lazy | — | `scan_parquet()...collect()` |
| Khi nào | hệ sinh thái rộng, data nhỏ | ETL nặng, data lớn, tốc độ |

⭐ **Luôn vectorize, tránh `apply(axis=1)`** (đo được: chậm ~600×).

### File formats
- **Parquet** (columnar) cho analytics: nhỏ hơn ~5×, đọc nhanh ~10–22×, có **column pruning** + **predicate pushdown** (min/max trên row group).
- Codec: **zstd/snappy**. CSV chỉ để trao đổi đơn giản.
- **Avro** (row, có schema, evolve tốt) cho streaming/Kafka. JSONL cho log/nested.
- Quy tắc: raw=gốc (bronze), analytics=Parquet (silver/gold).

### Ingestion resilient
timeout · retry + **exponential backoff** · pagination có giới hạn · **lưu raw trước** (replay) · idempotent · incremental (watermark) · không gãy im lặng.

### Clean & tested code
- Tách **pure transform** khỏi I/O → test được.
- **pydantic** validate schema; **soft-validation** gom lỗi (quarantine).
- **pytest**: `assert`, `pytest.raises`, `parametrize` (test biên), `fixture` (data nhỏ).
- **utils.py**: logging có cấu trúc (không log secret!), config `defaults<YAML<env`, retry decorator, custom exceptions phân tầng.

### ETL medallion
```
bronze (raw) → silver (clean+enrich) → gold (marts) → warehouse
```
Idempotent (`CREATE OR REPLACE`), có logging + exceptions theo tầng.

---

## ✅ Self-assessment Phase 1
- [ ] Thành thạo pandas & polars; biết khi nào dùng cái nào; luôn vectorize
- [ ] Giải thích vì sao Parquet thắng (columnar, pruning, pushdown); chọn được codec
- [ ] Phân biệt row vs columnar vs Avro; hiểu schema evolution
- [ ] Viết ingestion resilient (retry/backoff/pagination/raw-first/idempotent)
- [ ] Tách pure logic + viết pytest + pydantic validation
- [ ] Logging/config/exception đúng chuẩn production
- [ ] Ghép được ETL end-to-end bronze→silver→gold, idempotent

> Cross-check: doanh thu theo category cho **cùng con số** ở SQL/pandas/polars/ETL (`Grocery=1,714,225.45`) → logic đúng, nhất quán.

## ➡️ Tiếp theo: Phase 2 — Databases & Data Modeling
RDBMS sâu (indexing, EXPLAIN), OLTP vs OLAP, **dimensional modeling (Kimball)**: star schema, fact/dimension, **SCD Type 2**, normalization, NoSQL. Loop sẽ sinh **Batch #3** ngay sau task này.
