# G01 — SQL Interview Problems — Set 3 (advanced)

> 10 bài khó hơn [[a04-sql-interview-1]]/[[a05-sql-interview-2]]. Đề + lời giải + tư duy.

## 1. Nth-highest **per group**
**Đề:** Lương cao thứ 2 trong **mỗi phòng ban**.
```sql
select dept, salary from (
  select dept, salary, dense_rank() over (partition by dept order by salary desc) rnk
  from emp
) where rnk = 2;
```
Tư duy: DENSE_RANK + PARTITION BY dept; dense (không nhảy) cho "thứ 2 thật".

## 2. Conditional running total (reset theo điều kiện)
**Đề:** Running sum, **reset về 0** mỗi khi gặp giao dịch 'refund'.
```sql
with f as (
  select *, sum(case when type='refund' then 1 else 0 end)
            over (partition by acct order by ts) as grp   -- nhóm giữa các refund
  from txn
)
select *, sum(amount) over (partition by acct, grp order by ts
                            rows between unbounded preceding and current row) as running
from f;
```
Tư duy: tạo "nhóm" bằng running count của điều kiện reset (giống gaps&islands — [[a01-sql-gaps-islands]]), rồi running sum trong nhóm.

## 3. Date spine + fill gaps
**Đề:** Doanh thu mỗi ngày, **kể cả ngày không bán** (=0).
```sql
with days as (   -- date spine
  select unnest(generate_series(date '2024-01-01', date '2024-01-31', interval 1 day))::date as d
)
select d, coalesce(sum(line_total),0) as revenue
from days left join sales on sales.order_date = days.d
group by d order by d;
```
Tư duy: sinh spine ngày rồi LEFT JOIN → ngày trống ra 0 (không bị "mất ngày").

## 4. Top-N with ties (giữ cả hàng bằng điểm)
**Đề:** Top 3 điểm, nhưng nếu hạng 3 có nhiều người bằng điểm thì giữ hết.
```sql
select * from (select *, rank() over (order by score desc) rnk from t) where rnk <= 3;
```
Tư duy: **RANK** (không ROW_NUMBER) để ties cùng hạng → `<=3` giữ mọi người ở hạng ≤3.

## 5. Median per group (không percentile_cont)
```sql
select grp, avg(val) median from (
  select grp, val,
         row_number() over (partition by grp order by val) rn,
         count(*) over (partition by grp) cnt
  from t
) where rn in (floor((cnt+1)/2.0), ceil((cnt+1)/2.0)) group by grp;
```

## 6. Khoảng trống lớn nhất giữa 2 lần mua (per customer)
```sql
select customer_id, max(gap) max_gap_days from (
  select customer_id,
         order_date - lag(order_date) over (partition by customer_id order by order_date) as gap
  from orders
) group by customer_id;
```
Tư duy: LAG đo gap, MAX gap → churn risk.

## 7. First/last trong nhóm (không subquery)
**Đề:** Với mỗi khách: sản phẩm đơn **đầu tiên** và **cuối cùng**.
```sql
select distinct customer_id,
  first_value(product_id) over (partition by customer_id order by order_ts) as first_prod,
  last_value(product_id)  over (partition by customer_id order by order_ts
     rows between unbounded preceding and unbounded following) as last_prod
from orders;
```
Bẫy: `LAST_VALUE` cần frame `UNBOUNDED FOLLOWING` (mặc định chỉ tới current row → ra sai).

## 8. Recursive: đường đi trong hierarchy
**Đề:** Đường dẫn từ gốc tới mỗi node trong cây category.
```sql
with recursive p as (
  select id, name, parent_id, name as path from category where parent_id is null
  union all
  select c.id, c.name, c.parent_id, p.path || ' > ' || c.name
  from category c join p on c.parent_id = p.id
)
select id, path from p;
```

## 9. Self-join inequality: chạy đua tích lũy
**Đề:** Với mỗi đơn, đếm số đơn trước đó của cùng khách (không dùng window).
```sql
select a.order_id, count(b.order_id) as prior_orders
from orders a left join orders b
  on a.customer_id = b.customer_id and b.order_ts < a.order_ts
group by a.order_id;
```
Tư duy: self-join với `<` (inequality join) — window `count() over` nhanh hơn nhưng đề kiểm hiểu self-join.

## 10. Pivot động — câu trả lời đúng
**Đề:** Pivot doanh thu theo status (status không cố định).
**Trả lời:** SQL thuần không pivot động được. Cách: (1) conditional aggregation nếu biết status; (2) sinh SQL bằng code/macro (dbt Jinja loop — [[25-dbt-macros]]); (3) trả long format, để BI pivot. Nêu giới hạn = ăn điểm.

## ✅ "Tự mò"
🔭 Làm bài 2, 6, 7 trên DuckDB với e-commerce; bài 7 thử bỏ frame của LAST_VALUE xem sai thế nào.

➡️ Tiếp: [[g02-sql-interview-4]].
