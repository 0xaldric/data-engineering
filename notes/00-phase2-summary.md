# 🏁 Phase 2 — Tổng kết: Databases & Data Modeling

Hoàn thành Phase 2. Trọng tâm: **hiểu database sâu + thiết kế data model chuẩn** (chuẩn hoá cho OLTP, dimensional/star + SCD cho OLAP).

## Đã làm gì (Batch #3)
| # | Chủ đề | Artifact |
|---|--------|----------|
| T020 | Indexing & EXPLAIN | `01_explain_index.sql`, `notes/14-indexing.md` |
| T021 | Constraints/Transactions/ACID, OLTP vs OLAP | `02_constraints_tx.py`, `notes/15-oltp-olap-acid.md` |
| T022 | Normalization 1NF→3NF | `03_normalization.sql`, `notes/16-normalization.md` |
| T023 | Dimensional Modeling (thiết kế) | `notes/17-dimensional-modeling.md`, `star_schema_design.md` |
| T024 | Build Star Schema (DuckDB) | `04_build_star.py` → `warehouse/star.duckdb` |
| T025 | SCD Type 1/2/3 ⭐ | `05_scd.py`, `notes/18-scd.md` |
| T026 | Fact table types | `06_fact_types.sql`, `notes/19-fact-types.md` |
| T027 | NoSQL & khi nào dùng | `07_nosql_modeling.py`, `notes/20-nosql.md` |
| T028 | Review + smoke test | file này, `scripts/run_all.sh` |

**Kiểm chứng:** `bash scripts/run_all.sh` → Phase 0+1+2 = **ALL GREEN ✅** (9 SQL + 11 script Python + pytest + shell).

---

## 📑 Cheat-Sheet Phase 2

### Database engine
- **EXPLAIN** đọc từ dưới lên: scan → filter pushdown → join → aggregate; để ý cardinality estimate.
- **Index**: B-tree (range+equality), hash (equality), composite (left-most prefix), partial, covering. Giúp khi selective + bảng lớn; hại khi ghi nhiều/ít selective. OLAP columnar ít cần index (zonemap/pruning).
- **Constraints**: PK/UNIQUE/NOT NULL/CHECK/FK = phòng thủ chất lượng ở DB.
- **ACID**: Atomicity/Consistency/Isolation/Durability. Isolation levels chặn dirty/non-repeatable/phantom read.

### OLTP vs OLAP
Vận hành (row-store, 3NF, point ops) vs Phân tích (column-store, denormalized, quét lớn). DE chuyển OLTP→OLAP.

### Normalization (OLTP)
- 1NF (nguyên tử) → 2NF (hết phụ thuộc bộ phận) → 3NF (hết phụ thuộc bắc cầu) → BCNF.
- Diệt 3 anomaly (update/insert/delete). Lossless decomposition: join lại đúng gốc.
- OLAP **cố tình denormalize** (star schema) để đọc nhanh.

### Dimensional Modeling (Kimball, OLAP) ⭐
- **Fact** (measures + FK) vs **Dimension** (thuộc tính mô tả).
- **Grain** = quyết định đầu tiên (chọn nguyên tử nhất).
- **Surrogate key** cho dimension (cần cho SCD2).
- **Star** (denormalized, mặc định) vs snowflake.
- 4 bước: process → grain → dimensions → facts. Bus matrix = process × conformed dim.

### SCD ⭐
- Type 1 (overwrite, mất lịch sử) · **Type 2 (versioning: effective_from/to + is_current + surrogate key mới)** · Type 3 (previous value).
- Type 2 cho truy vấn **as-of** (point-in-time) chính xác.

### Fact types & additivity
- Transaction / periodic snapshot / accumulating snapshot (nhiều date role + lag + funnel).
- Measure: **additive** (SUM mọi chiều) / **semi-additive** (không theo thời gian: tồn kho, số dư) / **non-additive** (đơn giá, %). Lưu additive, tính tỉ lệ lúc query.

### NoSQL
4 họ: document/key-value/wide-column/graph. Embedding vs referencing (model theo access pattern). CAP (CP vs AP), BASE vs ACID. NoSQL ở tầng vận hành, không thay OLAP.

---

## ✅ Self-assessment Phase 2
- [ ] Đọc query plan, biết khi nào index giúp/hại
- [ ] Giải thích ACID + isolation anomalies; OLTP vs OLAP
- [ ] Chuẩn hoá 1NF→3NF, biết khi nào denormalize
- [ ] Thiết kế star schema: grain, fact/dim, surrogate key, conformed dim
- [ ] Implement & giải thích SCD Type 2 + as-of query
- [ ] Phân loại fact types & additivity của measure
- [ ] Chọn SQL vs NoSQL theo access pattern; hiểu CAP

> 2 warehouse DuckDB: `de.duckdb` (gold marts) & `star.duckdb` (dimensional). Revenue khớp xuyên SQL/pandas/polars/ETL/star (`Grocery=1,714,225.45`).

## ➡️ Tiếp theo: Phase 3 — Data Warehousing & Analytics Engineering
Warehouse concepts, **dbt** (models/tests/docs/snapshots/incremental) trên dbt-duckdb, medallion staging→marts. Loop sẽ sinh **Batch #4**.
