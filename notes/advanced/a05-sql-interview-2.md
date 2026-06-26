# A05 — SQL Interview Problems — Set 2 (window-heavy)

> 10 bài nâng cao thiên **window/CTE/analytics** — kiểu hỏi cho vị trí DE/Analytics Engineer. Tiền đề [[a04-sql-interview-1]], [[a03-analytics-patterns]].

---
## 1. Moving average 7 ngày
```sql
select day, revenue,
       round(avg(revenue) over (order by day rows between 6 preceding and current row), 2) as ma7
from daily;
```
Frame `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` = 7 hàng. Bẫy: thiếu data đầu kỳ → MA tính trên < 7 hàng (chấp nhận hoặc lọc).

## 2. Year-over-year (YoY)
```sql
select month, revenue,
       lag(revenue, 12) over (order by month) as same_month_last_year,
       round(100.0*(revenue - lag(revenue,12) over (order by month))
             / lag(revenue,12) over (order by month),1) as yoy_pct
from monthly;
```
`LAG(x, 12)` lùi 12 kỳ. Cần dữ liệu liên tục theo tháng (fill gap nếu thiếu — dùng date spine).

## 3. Khách mua lần đầu vs quay lại
```sql
select order_id, customer_id, order_date,
       case when row_number() over (partition by customer_id order by order_date)=1
            then 'new' else 'returning' end as customer_type
from orders;
```
`ROW_NUMBER=1` theo thời gian = đơn đầu tiên → phân loại new/returning.

## 4. Retention tháng (cohort)
Xem [[a03-analytics-patterns]] — cohort_month + month_offset. Câu hỏi hay: "tính % khách cohort tháng 1 còn hoạt động ở tháng thứ 3".

## 5. Khoảng cách giữa 2 đơn liên tiếp của khách
```sql
select customer_id, order_date,
       order_date - lag(order_date) over (partition by customer_id order by order_date) as days_since_prev
from orders;
```
`LAG` trong partition khách → đo gap (nền của sessionization & churn analysis).

## 6. Sản phẩm thường mua cùng nhau (basket/affinity)
```sql
select a.product_id as p1, b.product_id as p2, count(*) as together
from order_items a
join order_items b on a.order_id=b.order_id and a.product_id < b.product_id
group by 1,2 order by together desc limit 10;
```
Self-join trên cùng `order_id`, `a<b` để khỏi trùng/đảo cặp. Nền của "market basket analysis".

## 7. Rank với tie-break nhiều cột
```sql
select *, row_number() over (order by score desc, created_at asc, id asc) as rnk
from leaderboard;
```
ORDER BY nhiều cột để **xác định** (deterministic) khi điểm bằng nhau — quan trọng cho dedup/pagination ổn định.

## 8. Tỉ lệ tích lũy (running %) đạt mốc
**Đề:** Tìm số khách ít nhất chiếm 80% doanh thu (Pareto).
```sql
with r as (
  select customer_id, sum(line_total) rev from sales group by 1
),
c as (
  select *, sum(rev) over (order by rev desc rows between unbounded preceding and current row)
            / sum(rev) over () as cum_pct,
            row_number() over (order by rev desc) as rn
  from r
)
select min(rn) as customers_for_80pct from c where cum_pct >= 0.8;
```
Running sum / tổng = % tích lũy; tìm điểm chạm 80%.

## 9. Pivot động (số cột không cố định)
SQL thuần **không** pivot động được — cần sinh SQL bằng code/macro (dbt Jinja — [[25-dbt-macros]]) hoặc 2 bước (query distinct values → build query). Câu trả lời phỏng vấn đúng: "nêu giới hạn + cách giải bằng code-gen". (Conditional aggregation chỉ pivot **tĩnh** — [[a02-sql-pivot-hierarchical]].)

## 10. Median theo nhóm
```sql
select category,
       percentile_cont(0.5) within group (order by line_total) as median_line
from sales group by category;
```
Median per group bằng `PERCENTILE_CONT ... WITHIN GROUP` + `GROUP BY`.

---
## Mẹo làm bài window trong phỏng vấn
1. Xác định **grain & partition** (theo entity nào?).
2. Cần **thứ tự** không? (LAG/LEAD/running → có ORDER BY trong OVER).
3. Cần **frame** không? (running/moving → ghi rõ ROWS).
4. Lọc trên kết quả window → **bọc CTE/subquery** hoặc `QUALIFY` (không lọc window trong WHERE).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Phân biệt LAG(x) vs LAG(x,n); frame cho moving average.
- [ ] Pareto/running % tích lũy.
- [ ] Vì sao pivot động cần code-gen.
- 🔭 *Tự mò:* làm bài 6 (affinity) + bài 8 (Pareto 80/20) trên dataset e-commerce; xem 20% khách có chiếm ~80% doanh thu không.

➡️ Tiếp: [[a06-sql-optimization]].
