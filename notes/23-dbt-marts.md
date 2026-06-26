# 23 — dbt Intermediate & Marts

> Code: [`projects/04-dbt/models/`](../projects/04-dbt/models/) (intermediate/, marts/)
> Chạy: `dbt run --project-dir projects/04-dbt --profiles-dir projects/04-dbt` → `PASS=9`

## Ba lớp model (medallion trong dbt)
```
staging (view)      → làm sạch 1-1 với source          (stg_*)
intermediate (view) → join/business logic trung gian   (int_*)
marts (table)       → fact + dimension cho BI           (dim_*, fct_*, mart_*)
```
- **Intermediate** (`int_sales_enriched`): gộp `stg_order_items + stg_orders + stg_products` về grain order-item — nơi đặt logic join phức tạp, tái dùng cho nhiều mart. Thường `view`/`ephemeral`.
- **Marts**: bảng cuối cùng người dùng/BI truy vấn — star schema (`dim_customer`, `dim_product`, `fct_sales`) + bảng tổng hợp (`mart_revenue_by_category`). Materialized **`table`** để đọc nhanh.

## Materializations ⭐ (cấu hình bằng `+materialized`)
| Kiểu | dbt làm gì | Khi nào dùng |
|------|-----------|--------------|
| **view** | `CREATE VIEW` | staging/intermediate — rẻ, luôn tươi, dữ liệu nhỏ |
| **table** | `CREATE TABLE AS` | marts — query nhiều lần, cần nhanh |
| **ephemeral** | chèn dạng CTE vào model dùng nó (không tạo object) | model trung gian nhỏ, chỉ 1 nơi dùng |
| **incremental** | chỉ build phần dữ liệu MỚI (T035) | fact lớn, append theo thời gian |
Đặt mặc định theo thư mục trong `dbt_project.yml`; override từng model bằng `{{ config(materialized='...') }}`.

## ref() & DAG ⭐
Mỗi model gọi `{{ ref('model_khac') }}` thay vì tên bảng cứng → dbt:
1. Biết **thứ tự chạy** (staging trước marts) và tự sắp xếp.
2. Dựng **lineage DAG**: `source → stg → int → dim/fct → mart`.
3. Cho phép `dbt run -s <model>+` (model và mọi thứ phụ thuộc nó), `+model` (model và upstream).

Kết quả `dbt run`: 9 model theo đúng DAG (4 stg view → int view → 2 dim table → fct table → mart table), `PASS=9`.

## Surrogate key trong dbt
`dim_customer`/`dim_product` tạo `*_key` bằng `row_number() over (order by natural_key)`. `fct_sales` join dim theo **natural key** để lấy **surrogate key** rồi chỉ giữ surrogate trong fact (xem [[17-dimensional-modeling]]). (T033 sẽ đổi sang `dbt_utils.generate_surrogate_key` — hash, ổn định hơn.)

## Kiểm chứng nhất quán
`mart_revenue_by_category` cho `Grocery = 1,714,225.45` — **khớp** với SQL (Phase 0), pandas (T011), polars (T012), star schema thủ công (T024). **5 cách, một con số** → logic đúng & nhất quán across công cụ.

## Vì sao kiến trúc này tốt
- **Mô-đun hoá**: mỗi model một việc, dễ đọc/test/sửa.
- **Tái dùng**: `int_sales_enriched` dùng lại cho nhiều mart.
- **Lineage minh bạch**: đổi staging → biết mart nào ảnh hưởng.
- **Đổi materialization không đổi SQL**: dev dùng view, prod đổi sang table/incremental chỉ bằng config.

## ✅ Tự kiểm tra
- [ ] Phân biệt staging / intermediate / marts (vai trò & materialization)
- [ ] 4 materialization và khi nào dùng
- [ ] `ref()` dựng DAG thế nào; cú pháp chọn `model+` / `+model`
- [ ] Surrogate key trong dbt (dim tạo, fct tham chiếu)
- [ ] Vì sao tách lớp giúp mô-đun/tái dùng/lineage

➡️ Tiếp theo: [[24-dbt-tests]] — kiểm thử dữ liệu trong dbt.
