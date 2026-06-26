# 26 — dbt Snapshots (SCD2 tự động) ⭐

> Code: [`snapshots/scd_customer.sql`](../projects/04-dbt/snapshots/scd_customer.sql)
> Chạy: `dbt snapshot ...` (lần 2 thêm `--vars '{move_customer_1: true}'`)

**Snapshot** là cách dbt làm **SCD Type 2 tự động** (xem lý thuyết SCD ở [[18-scd]]). Thay vì tự viết logic expire+insert bằng SQL, chỉ cần khai báo — dbt lo phần versioning.

## Cách hoạt động
Mỗi lần `dbt snapshot`, dbt:
1. So dữ liệu **hiện tại** (kết quả query snapshot) với bản **đã lưu**.
2. Nếu một bản ghi (theo `unique_key`) **đổi** (theo strategy) → **đóng** phiên bản cũ (set `dbt_valid_to = now`) và **chèn** phiên bản mới.
3. Bản ghi mới hoàn toàn → chèn phiên bản đầu.

dbt tự thêm 4 cột metadata:
| Cột | Ý nghĩa |
|-----|---------|
| `dbt_valid_from` | thời điểm phiên bản bắt đầu hiệu lực |
| `dbt_valid_to` | thời điểm hết hiệu lực (**NULL = current**) |
| `dbt_scd_id` | khoá thay thế của phiên bản (hash) |
| `dbt_updated_at` | mốc cập nhật |

## Demo kết quả
Khách #1, sau 2 lần snapshot (lần 2 đổi country US→ZZ):
```
customer_id  country  dbt_valid_from           dbt_valid_to
     1        US       2026-06-26 09:10:00      2026-06-26 09:10:04   <- phiên bản cũ (đóng)
     1        ZZ       2026-06-26 09:10:04      NULL                  <- current
```
→ Giữ **toàn bộ lịch sử** y như SCD2 thủ công ([[18-scd]]) nhưng **không viết logic expire/insert**. Truy vấn as-of: lọc `where '<ngày>' between dbt_valid_from and coalesce(dbt_valid_to, '9999-12-31')`.

## Strategies (cách phát hiện thay đổi)
| Strategy | Cách phát hiện | Khi nào dùng |
|----------|----------------|--------------|
| **`timestamp`** | so cột `updated_at` (mới hơn = đổi) | nguồn **có** cột cập nhật đáng tin (tốt nhất) |
| **`check`** | so giá trị các `check_cols` | nguồn **không** có updated_at; chọn cột cần theo dõi (hoặc `all`) |

Demo dùng `check` với `check_cols=['country','city']` (dữ liệu không có updated_at). Config khác: `invalidate_hard_deletes=true` (đánh dấu bản ghi biến mất khỏi nguồn).

## Khai báo
```sql
{% snapshot scd_customer %}
{{ config(target_schema='snapshots', unique_key='customer_id',
          strategy='check', check_cols=['country','city']) }}
select customer_id, customer_name, country, city from {{ ref('stg_customers') }}
{% endsnapshot %}
```
Đặt trong `snapshots/`, chạy bằng `dbt snapshot` (riêng với `dbt run`; `dbt build` gộp cả hai).

## Lưu ý thực hành
- Snapshot nên đọc dữ liệu **càng gần nguồn càng tốt** (raw/staging) để bắt đúng thời điểm thay đổi; chạy **đều đặn** (mỗi lần load) vì nó chỉ thấy trạng thái tại lúc chạy — bỏ lỡ lần chạy = mất phiên bản trung gian.
- `unique_key` phải là **business key** ổn định.
- Bảng snapshot là nguồn để build `dim_*` SCD2 ở marts (join lấy phiên bản đúng).

## ✅ Tự kiểm tra
- [ ] Snapshot = SCD2 tự động; kể 4 cột dbt_* và ý nghĩa
- [ ] Phân biệt strategy `timestamp` vs `check`
- [ ] Đọc bảng snapshot: phiên bản current là `dbt_valid_to IS NULL`
- [ ] Vì sao phải chạy snapshot đều đặn & gần nguồn
- [ ] Viết truy vấn as-of trên bảng snapshot

➡️ Tiếp theo: [[27-dbt-incremental]] — incremental models.
