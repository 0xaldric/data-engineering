# 28 — dbt Docs, Lineage & Seeds

> Code: [`seeds/country_region.csv`](../projects/04-dbt/seeds/country_region.csv) · [`models/marts/mart_revenue_by_region.sql`](../projects/04-dbt/models/marts/mart_revenue_by_region.sql)
> Chạy: `dbt seed`, `dbt run -s mart_revenue_by_region`, `dbt docs generate`

## Seeds — bảng tra cứu nhỏ versioned trong repo
**Seed** = file CSV trong `seeds/`, dbt nạp thành bảng bằng `dbt seed`. Dùng cho **dữ liệu tĩnh, nhỏ, ít đổi** mà nên nằm trong version control:
- mapping/lookup: `country → region`, mã trạng thái → mô tả, tỉ giá, danh mục.
- KHÔNG dùng seed cho dữ liệu lớn/động (đó là việc của ingestion).

Dùng như model: `{{ ref('country_region') }}` (tên seed = tên file bỏ `.csv`). Demo: `mart_revenue_by_region` join `fct_sales → dim_customer → country_region` → doanh thu theo region (APAC 7.73M / EMEA 3.76M / Americas 1.27M). Seed nằm trong repo → đổi mapping là một commit, có review/lịch sử.

## Documentation
Thêm `description:` cho model & column trong `schema.yml` ([[22-dbt-staging]], [[24-dbt-tests]]). Mô tả này:
- Hiển thị trong **dbt docs site** (web tài liệu tự sinh).
- Là **data dictionary** sống cạnh code (không lệch như wiki rời).
- Hỗ trợ: `{{ doc('ten_block') }}` cho mô tả dài (file `.md`), `persist_docs` để đẩy comment xuống DB.

## `dbt docs generate` — manifest & catalog ⭐
Sinh 2 file trong `target/`:
- **`manifest.json`** — "bộ não" của dbt: mọi node (model/test/seed/snapshot/source), cấu hình, **phụ thuộc (DAG)**, SQL compiled. Demo: 31 nodes. Đây cũng là input cho công cụ ngoài (lineage, CI, metadata).
- **`catalog.json`** — thông tin cột/kiểu/thống kê đọc từ warehouse.
`dbt docs serve` mở web có **biểu đồ lineage** click được.

## Lineage (DAG)
dbt suy ra lineage từ `ref()`/`source()`:
```
source(raw.*) → stg_* → int_sales_enriched → dim_*/fct_sales → mart_*
                                                   seed country_region ↗
```
Lợi ích:
- **Impact analysis**: đổi `stg_orders` → biết ngay mart nào ảnh hưởng (`dbt ls -s stg_orders+`).
- **Debug ngược**: mart sai → lần ngược upstream.
- **Chọn lọc chạy**: `dbt build -s +mart_revenue_by_region` (mart và mọi upstream).

## Exposures
Khai báo **nơi tiêu thụ** dữ liệu (dashboard, app, ML) trong `.yml` → lineage kéo dài tới sản phẩm cuối, biết "đổi model này ảnh hưởng dashboard nào". Là cầu nối tới **data observability/lineage** toàn hệ thống (Phase 8: OpenLineage/DataHub).

## `dbt build` — chạy mọi thứ đúng thứ tự ⭐
`dbt build` = `run` + `test` + `snapshot` + `seed` theo **một DAG thống nhất**: seed/snapshot/model build theo thứ tự phụ thuộc, **test chạy ngay sau** node của nó; node FAIL test → **chặn** downstream. Đây là lệnh dùng trong production/CI (thay vì gọi rời từng lệnh).

## ✅ Tự kiểm tra
- [ ] Khi nào dùng seed (tĩnh, nhỏ, versioned) vs ingestion
- [ ] `dbt docs generate` tạo manifest.json (DAG) & catalog.json (cột)
- [ ] Lineage để impact analysis & debug; cú pháp `+model` / `model+`
- [ ] Exposure là gì
- [ ] `dbt build` = run+test+snapshot+seed theo DAG, chặn lan lỗi

➡️ Tiếp theo: [[00-phase3-summary]] — chốt Phase 3.
