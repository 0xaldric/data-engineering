# H01 — SQL Interview Problems — Set 5 (window edge cases)

> 10 bài thiên **mẹo window** — chỗ hay sai dù biết window. Đề + lời giải + bẫy. Tiền đề [[04-sql-window]], [[a01-sql-gaps-islands]].

## 1. LAST_VALUE sai frame ⭐
**Đề:** Giá trị cuối cùng của nhóm.
```sql
-- ❌ SAI: mặc định frame = UNBOUNDED PRECEDING..CURRENT ROW -> "last" = chính hàng đó
last_value(x) over (partition by g order by t)
-- ✅ ĐÚNG:
last_value(x) over (partition by g order by t
                    rows between unbounded preceding and unbounded following)
```
Bẫy kinh điển: `LAST_VALUE` cần frame mở tới cuối; nếu không, mỗi hàng trả chính nó.

## 2. RANGE vs ROWS với ties
**Đề:** Running total, dữ liệu có nhiều hàng cùng `order_date`.
```sql
sum(amt) over (order by order_date rows between unbounded preceding and current row)   -- đếm từng hàng
sum(amt) over (order by order_date)  -- ngầm RANGE -> gộp hết hàng cùng ngày (nhảy cục)
```
→ Luôn ghi `ROWS` cho running total nếu muốn từng hàng.

## 3. IGNORE NULLS (carry-forward)
**Đề:** Điền giá trị gần nhất không-null về phía trước (last value carried forward / LOCF).
```sql
-- DB hỗ trợ ignore nulls:
last_value(price ignore nulls) over (partition by id order by ts
       rows between unbounded preceding and current row) as price_filled;
-- DuckDB/Postgres không có ignore nulls trực tiếp -> dùng trick:
-- max(price) over (partition by id, grp) với grp = count(price) over(... đến hiện tại)
```

## 4. Gap-fill forward (LOCF không ignore nulls)
```sql
with g as (
  select *, count(price) over (partition by id order by ts) as grp  -- nhóm theo lần có giá trị
  from t
)
select id, ts, max(price) over (partition by id, grp) as filled from g;
```
Tư duy: `count(non-null) over` tạo nhóm; trong nhóm chỉ 1 giá trị non-null → `max` lấy nó (carry forward).

## 5. QUALIFY (lọc window gọn)
```sql
select * from sales
qualify row_number() over (partition by customer_id order by order_ts desc) = 1;  -- đơn mới nhất
```
QUALIFY (DuckDB/Snowflake/BigQuery) = WHERE cho window, khỏi bọc subquery.

## 6. LAG với default & offset
```sql
lag(revenue, 1, 0) over (order by month)   -- offset 1, default 0 nếu không có (tránh NULL)
```

## 7. Running distinct count (khó)
**Đề:** Số khách **distinct** tích lũy tới mỗi ngày.
```sql
-- không có "distinct" trong window -> trick: đánh dấu lần ĐẦU mỗi khách rồi running sum
with f as (
  select order_date, customer_id,
    row_number() over (partition by customer_id order by order_date) as rn
  from orders
)
select order_date,
  sum(sum(case when rn=1 then 1 else 0 end)) over (order by order_date
       rows between unbounded preceding and current row) as cum_distinct_customers
from f group by order_date order by order_date;
```
Tư duy: distinct count window không có sẵn → đếm "lần đầu xuất hiện" rồi running sum.

## 8. NTH_VALUE
```sql
nth_value(product, 2) over (partition by customer order by order_ts
          rows between unbounded preceding and unbounded following) as second_product;
```

## 9. Phần trăm thay đổi với hàng trước cùng nhóm
```sql
(amt - lag(amt) over (partition by category order by month))
  / nullif(lag(amt) over (partition by category order by month), 0) as pct_change;
```
Bẫy: thiếu `PARTITION BY` → so nhầm xuyên nhóm.

## 10. Rank đổi khi tie-break: ROW_NUMBER không deterministic
**Đề:** Pagination ổn định.
```sql
row_number() over (order by score desc, id asc)  -- THÊM id để tie-break -> deterministic
```
Bẫy: `order by score desc` mà nhiều score bằng → thứ tự ngẫu nhiên giữa các lần chạy → pagination nhảy. Luôn tie-break bằng cột unique.

## ✅ "Tự mò"
🔭 Làm bài 1, 4, 7 trên DuckDB; bài 1 thử cả 2 frame xem khác; bài 4 (gap-fill) cực hay dùng cho time-series thiếu giá trị.

➡️ Tiếp: [[h02-case-marketplace]].
