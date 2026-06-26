# 21 — Data Warehousing & dbt (setup)

> Project: [`projects/04-dbt/`](../projects/04-dbt/) (dbt-duckdb)
> Chạy: `dbt <cmd> --project-dir projects/04-dbt --profiles-dir projects/04-dbt` (từ thư mục `data-engineering/`)

## Data Warehouse là gì?
Kho dữ liệu tập trung, tối ưu cho **phân tích** (OLAP), gom dữ liệu từ nhiều nguồn vận hành. Khác production DB (OLTP) — xem [[15-oltp-olap-acid]].

### Kiến trúc theo lớp (layering) — medallion
```
Nguồn (OLTP, API, file)
   │  ingest
   ▼
BRONZE / raw / landing   — dữ liệu thô, giữ nguyên gốc (parquet)
   │  staging: clean, rename, cast
   ▼
SILVER / staging+intermediate — 1 model/nguồn, chuẩn hoá, join trung gian
   │  business logic
   ▼
GOLD / marts            — fact + dimension (star schema), sẵn sàng cho BI
```
Mỗi lớp một trách nhiệm → dễ test, dễ debug, tái dùng. Đây chính là cách dbt khuyến nghị (staging → intermediate → marts).

## ETL vs ELT ⭐
- **ETL** (Extract–Transform–Load): transform **trước** khi nạp vào warehouse (thường bằng Spark/Python ngoài). Hợp khi warehouse yếu hoặc cần xử lý nặng trước.
- **ELT** (Extract–Load–Transform): nạp **thô** vào warehouse rồi transform **bằng SQL ngay trong warehouse**. Warehouse cloud (BigQuery/Snowflake) mạnh + rẻ → ELT thành chuẩn hiện đại. **dbt là công cụ chủ lực của chữ "T" trong ELT.**

## Cloud Data Warehouses
| | Đặc điểm | Mô hình tính tiền |
|--|----------|-------------------|
| **BigQuery** (GCP) | serverless, tách compute/storage, SQL | theo lượng dữ liệu quét |
| **Snowflake** | multi-cloud, virtual warehouse co giãn, tách compute/storage | theo thời gian compute |
| **Redshift** (AWS) | cluster, gần hệ AWS | theo node/giờ (hoặc serverless) |
| **DuckDB** (ở đây) | embedded OLAP, chạy local | miễn phí — học không tốn tiền |
Điểm chung hiện đại: **tách compute khỏi storage** → co giãn độc lập.

## dbt (data build tool) là gì?
Công cụ biến **SQL SELECT** thành pipeline transform có kỹ thuật phần mềm:
- **Model** = 1 file `.sql` chứa 1 câu `SELECT`; dbt tự `CREATE TABLE/VIEW AS`.
- **`ref()` / `source()`** = khai báo phụ thuộc → dbt tự dựng **DAG** thứ tự chạy.
- **Materialization** = view / table / incremental / ephemeral.
- **Tests, docs, snapshots, macros, packages** — kèm sẵn (các task sau).
- Đem **version control, test, CI, modularity** vào analytics → "analytics engineering".

dbt **không** ingest/extract; nó chỉ lo phần **transform** trong warehouse (chữ T của ELT).

## Setup đã làm (T029)
- `dbt_project.yml` — cấu hình project, materialization mặc định theo layer.
- `profiles.yml` — kết nối **dbt-duckdb** → `warehouse/dbt.duckdb`.
- `packages.yml` — `dbt_utils` (cài bằng `dbt deps`).
- `models/staging/_sources.yml` — **sources** đọc thẳng `data/raw/*.parquet` qua `external_location` (`{name}` → tên bảng).
- Verify: `dbt debug` (All checks passed) + `dbt run` model nháp đọc 2000 customers ✓.

## Lệnh dbt cốt lõi
| Lệnh | Việc |
|------|------|
| `dbt deps` | cài packages |
| `dbt debug` | kiểm tra kết nối/cấu hình |
| `dbt run` | build models (`-s` chọn model/layer) |
| `dbt test` | chạy tests |
| `dbt snapshot` | chạy SCD2 snapshots |
| `dbt seed` | nạp CSV seed |
| `dbt build` | run + test + snapshot + seed theo đúng DAG |
| `dbt docs generate` | sinh tài liệu + lineage |

## ✅ Tự kiểm tra
- [ ] Vẽ kiến trúc layer bronze→silver→gold (staging→intermediate→marts)
- [ ] Phân biệt ETL vs ELT, vì sao ELT + dbt thành chuẩn
- [ ] Kể đặc điểm BigQuery/Snowflake/Redshift (tách compute/storage)
- [ ] Giải thích dbt làm gì (model, ref/source, DAG, materialization)
- [ ] Biết dbt lo "T", không lo "E/L"

➡️ Tiếp theo: [[22-dbt-staging]] — staging models.
