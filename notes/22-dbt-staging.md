# 22 — dbt Staging Models

> Code: [`projects/04-dbt/models/staging/`](../projects/04-dbt/models/staging/)
> Chạy: `dbt run -s staging --project-dir projects/04-dbt --profiles-dir projects/04-dbt`

**Staging** là lớp đầu tiên trong dbt — "cửa ngõ" chuẩn hoá dữ liệu thô trước khi làm business logic.

## Nguyên tắc lớp staging
1. **Một staging model ↔ một source** (1-1). `stg_customers` ↔ `raw.customers`. Không join nhiều nguồn ở đây.
2. Chỉ **làm nhẹ**: `rename`, `cast`/ép kiểu, đổi tên cột nhất quán, ép chuẩn (lowercase, trim), tính cột đơn giản. **KHÔNG** join, **KHÔNG** aggregate, **KHÔNG** business logic (để dành intermediate/marts).
3. Materialized **`view`** — rẻ, luôn tươi (staging mỏng, query xuyên qua nhanh).
4. Là **giao diện ổn định**: phần còn lại của project chỉ `ref()` staging, không chạm source trực tiếp → đổi nguồn chỉ sửa staging.

## `source()` vs `ref()` ⭐
- **`source('raw', 'customers')`** — trỏ tới dữ liệu **bên ngoài dbt** (bảng/file thô đã khai báo trong `_sources.yml`). Chỉ staging dùng `source()`.
- **`ref('stg_customers')`** — trỏ tới **model khác trong dbt**. Mọi model phía sau dùng `ref()`.
- dbt dựa vào `source()`/`ref()` để **tự xây DAG** thứ tự chạy & lineage. → **Không bao giờ hardcode tên bảng**; luôn qua `ref()`/`source()` để dbt biết phụ thuộc.

## Cấu trúc thư mục
```
models/staging/
├── _sources.yml     # khai báo sources (parquet trong data/raw)
├── _staging.yml     # tài liệu + (sau này) tests cho staging models
├── stg_customers.sql
├── stg_products.sql
├── stg_orders.sql
└── stg_order_items.sql
```
Quy ước tên: `stg_<nguồn>__<thực thể>` (hoặc `stg_<thực thể>`). File `_` ở đầu (yml) gom cấu hình.

## Ví dụ (stg_orders)
```sql
select
    order_id,
    customer_id,
    cast(order_ts as timestamp) as order_ts,
    cast(order_ts as date)      as order_date,  -- tách sẵn date cho tiện join dim_date
    status,
    channel
from {{ source('raw', 'orders') }}
```
Kết quả: `dbt run -s staging` → 4 view (`PASS=4`). Mỗi view là một "bảng sạch" để lớp sau dùng.

## Vì sao tách staging riêng?
- **Tái dùng**: nhiều mart cùng dùng `stg_orders` đã sạch, khỏi lặp logic cast.
- **Một chỗ sửa**: nguồn đổi tên cột → chỉ sửa staging model tương ứng.
- **Dễ test**: kiểm tra chất lượng ngay tại cửa ngõ (T032).
- **DAG rõ ràng**: source → staging → intermediate → marts.

## ✅ Tự kiểm tra
- [ ] Giải thích quy ước staging (1-1 với source, chỉ làm nhẹ, view)
- [ ] Phân biệt `source()` vs `ref()` và vai trò dựng DAG
- [ ] Vì sao không join/business logic ở staging
- [ ] Lợi ích của lớp staging như "giao diện ổn định"

➡️ Tiếp theo: [[23-dbt-marts]] — intermediate + marts (star schema bằng dbt).
