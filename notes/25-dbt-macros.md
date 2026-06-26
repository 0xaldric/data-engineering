# 25 — dbt Macros & Jinja

> Code: [`macros/price_tier.sql`](../projects/04-dbt/macros/price_tier.sql) · [`models/marts/mart_sales_by_status.sql`](../projects/04-dbt/models/marts/mart_sales_by_status.sql)
> Chạy: `dbt run ...` → `PASS=10`

dbt model = **Jinja + SQL**. Jinja là template engine cho phép sinh SQL động (biến, vòng lặp, hàm) → code DRY, tái dùng, ít lỗi sao chép.

## Cú pháp Jinja (3 dấu)
| Dấu | Ý nghĩa | Ví dụ |
|-----|---------|-------|
| `{{ ... }}` | **biểu thức** — chèn giá trị | `{{ ref('x') }}`, `{{ var('y') }}` |
| `{% ... %}` | **lệnh** — logic (set/for/if/macro) | `{% for s in statuses %}` |
| `{# ... #}` | **comment** Jinja (không vào SQL) | `{# giải thích #}` |

## ⚠️ Bẫy: Jinja parse cả comment SQL `--`
Jinja xử lý template **trước** khi SQL chạy → nó **không biết** `--` là comment SQL. Đặt tag `{% %}` trong comment `--` sẽ bị parse và **lỗi compile**. → Giải thích về Jinja phải để trong `{# #}`, không để trong `-- ... {% %}`. (Đã gặp đúng lỗi này khi viết bài.)

## Macro — hàm tái dùng sinh SQL
```sql
{% macro price_tier(price_column) %}
    case when {{ price_column }} >= 200 then 'premium'
         when {{ price_column }} >= 50  then 'mid'
         else 'budget' end
{% endmacro %}
```
Dùng: `{{ price_tier('unit_price') }}` trong `dim_product` → sinh ra CASE. Viết **một lần**, dùng nhiều model; sửa ngưỡng chỉ một chỗ. (Kết quả: premium 203 / mid 76 / budget 21.)

## Jinja for-loop — sinh nhiều cột (DRY pivot)
```sql
{% set statuses = ['completed','shipped','cancelled','returned'] %}
select dp.category,
  {% for s in statuses %}
  round(sum(case when f.status='{{ s }}' then f.line_total else 0 end),2) as revenue_{{ s }}{{ "," if not loop.last else "" }}
  {% endfor %}
from ...
```
Compile thành 4 cột `revenue_completed/shipped/cancelled/returned` **thật**. `loop.last` để bỏ dấu phẩy cuối. Sửa danh sách status → tự thêm/bớt cột. Xem SQL đã compile ở `target/compiled/...`.

## Packages — dùng macro của người khác
`dbt deps` cài package (khai báo trong `packages.yml`). **dbt_utils** rất phổ biến:
- `dbt_utils.generate_surrogate_key(['product_id'])` → hash surrogate key (ổn định hơn `row_number`, không phụ thuộc thứ tự/khối lượng dữ liệu). Đã thay vào `dim_customer`/`dim_product`; 17 test vẫn PASS (relationships fact→dim toàn vẹn vì cùng hash).
- Khác: `dbt_utils.star` (chọn mọi cột trừ vài cột), `date_spine`, `pivot`, `union_relations`, nhiều generic test.

## Macro hữu ích nên biết
- **`{{ this }}`** — tham chiếu chính model hiện tại (dùng trong incremental).
- **`{{ var('x', default) }}`** — đọc biến từ `dbt_project.yml`/CLI `--vars`.
- **`{{ env_var('X') }}`** — đọc biến môi trường (secret, path).
- **`{{ config(...) }}`** — cấu hình model (materialized, tags...).
- **`run_query()`** + `{% if execute %}` — chạy SQL lúc compile (metadata-driven).

## Khi nào dùng macro?
- Logic SQL **lặp lại** ở nhiều model (price_tier, chuẩn hoá tiền tệ, mask PII).
- Sinh code theo danh sách (pivot, nhiều cột/bảng tương tự).
- Đừng lạm dụng: macro quá nhiều làm SQL khó đọc/khó debug. Ưu tiên rõ ràng.

## ✅ Tự kiểm tra
- [ ] Phân biệt `{{ }}`, `{% %}`, `{# #}`
- [ ] Vì sao không để tag Jinja trong comment `--`
- [ ] Viết macro nhận tham số và dùng trong model
- [ ] Dùng for-loop + `loop.last` sinh nhiều cột
- [ ] Cài & dùng macro dbt_utils (generate_surrogate_key); đọc SQL compiled

➡️ Tiếp theo: [[26-dbt-snapshots]] — snapshots (SCD2 tự động).
