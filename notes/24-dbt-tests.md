# 24 — dbt Tests ⭐

> Code: [`models/marts/_marts.yml`](../projects/04-dbt/models/marts/_marts.yml) · [`tests/assert_revenue_non_negative.sql`](../projects/04-dbt/tests/assert_revenue_non_negative.sql)
> Chạy: `dbt test --project-dir projects/04-dbt --profiles-dir projects/04-dbt` → **PASS=17**

dbt test kiểm tra **chất lượng DỮ LIỆU** (khác pytest kiểm tra **logic code** ở [[12-testing-de]]). Đây là "lưới an toàn" của warehouse: bắt dữ liệu bẩn trước khi nó tới dashboard/quyết định.

## Triết lý: test = một query tìm "hàng vi phạm"
dbt test chạy một câu SQL; **PASS nếu trả về 0 hàng**, FAIL nếu có hàng (mỗi hàng = một vi phạm). Đơn giản mà mạnh.

## Generic tests (khai báo trong YAML)
Gắn vào cột trong `schema.yml`, dbt tự sinh SQL:
| Test | Kiểm | Ví dụ |
|------|------|-------|
| **`unique`** | không trùng | surrogate/natural key |
| **`not_null`** | không NULL | khoá, FK |
| **`accepted_values`** | chỉ thuộc tập cho phép | `status ∈ {completed,...}`, `price_tier ∈ {premium,mid,budget}` |
| **`relationships`** | toàn vẹn tham chiếu (FK) | `fct_sales.customer_key` phải tồn tại trong `dim_customer.customer_key` |

```yaml
- name: customer_key
  tests:
    - not_null
    - relationships:
        to: ref('dim_customer')
        field: customer_key
```
→ `relationships` chính là kiểm **FK fact→dim** mà warehouse OLAP thường **không enforce** ở DB ([[15-oltp-olap-acid]]) — dbt bù lại bằng test.

## Singular tests (SQL tuỳ ý trong `tests/`)
Một file `.sql` trả về hàng vi phạm cho logic nghiệp vụ riêng:
```sql
-- PASS nếu 0 hàng: doanh thu không được âm
select category, revenue from {{ ref('mart_revenue_by_category') }}
where revenue < 0
```
Dùng cho rule phức tạp không có generic test sẵn (vd: tổng con phải bằng tổng cha, ngày kết thúc ≥ ngày bắt đầu, không trùng theo tổ hợp nhiều cột).

## Tests từ packages
`dbt_utils`/`dbt_expectations` cung cấp nhiều test mạnh: `expression_is_true`, `accepted_range`, `unique_combination_of_columns`, `not_null_proportion`... (cài qua `dbt deps`).

## Cấu hình mức độ nghiêm
- `severity: warn` (chỉ cảnh báo) vs `error` (chặn, mặc định).
- `where:` lọc tập kiểm; `config: {limit: N}`.
- Ngưỡng: `error_if`, `warn_if` (vd warn nếu >0, error nếu >100 hàng vi phạm).

## Kết quả & ý nghĩa
17 test PASS: 4 `unique`, 5 `not_null`, 2 `accepted_values`, 2 `relationships` (FK), 1 singular. → Đảm bảo khoá duy nhất, không NULL, giá trị hợp lệ, FK toàn vẹn, doanh thu không âm.

## Đưa vào quy trình
- **`dbt build`** = chạy model + test theo DAG: nếu test một model FAIL, dbt **dừng** các model phụ thuộc → dữ liệu bẩn không lan xuống.
- **CI/CD** (Phase 7): chạy `dbt build` mỗi PR. Kết hợp **data contract** & freshness (Phase 8).
- **`dbt test --select <model>`** chạy test cho một phần.

## ✅ Tự kiểm tra
- [ ] Hiểu "test = query tìm hàng vi phạm, PASS nếu 0 hàng"
- [ ] 4 generic test cốt lõi (unique/not_null/accepted_values/relationships)
- [ ] Viết singular test cho rule nghiệp vụ
- [ ] Vì sao `relationships` quan trọng (warehouse không enforce FK)
- [ ] `dbt build` dừng lan dữ liệu bẩn; severity warn vs error

➡️ Tiếp theo: [[25-dbt-macros]] — Jinja & macros.
