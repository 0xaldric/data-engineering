# A04 — SQL Interview Problems — Set 1

> 10 bài SQL phỏng vấn kinh điển (dễ→khó) + **lời giải + tư duy**. Schema tham chiếu: e-commerce (`orders`, `order_items`, `customers`, `products`) hoặc nêu rõ trong bài. Liên hệ [[04-sql-window]], [[a01-sql-gaps-islands]].

---
## 1. Lương cao thứ N (nth-highest) ⭐
**Đề:** Tìm mức `salary` cao **thứ 2** trong bảng `employees` (không trùng).
```sql
select distinct salary
from employees
order by salary desc
offset 1 limit 1;        -- bỏ 1 cao nhất, lấy cái kế
-- hoặc tổng quát thứ N bằng DENSE_RANK:
select salary from (
  select salary, dense_rank() over (order by salary desc) as rnk
  from employees
) where rnk = 2;
```
**Tư duy:** `DENSE_RANK` để giá trị trùng cùng hạng (cao thứ 2 thật sự). `ROW_NUMBER` sẽ sai khi có ties. Bẫy: phải `DISTINCT`/dense_rank, không `LIMIT 1 OFFSET 1` thô nếu có trùng.

## 2. Top-N mỗi nhóm ⭐
**Đề:** 3 sản phẩm doanh thu cao nhất **mỗi category**.
```sql
select category, product_name, revenue from (
  select category, product_name, sum(line_total) as revenue,
         row_number() over (partition by category order by sum(line_total) desc) as rn
  from sales group by category, product_name
) where rn <= 3;
```
**Tư duy:** `ROW_NUMBER` + `PARTITION BY` nhóm rồi lọc `rn<=N`. DuckDB/Snowflake: dùng `QUALIFY rn<=3` khỏi subquery.

## 3. Running total
**Đề:** Doanh thu lũy kế theo ngày.
```sql
select day, revenue,
       sum(revenue) over (order by day rows between unbounded preceding and current row) as cumulative
from daily_revenue;
```
**Tư duy:** window sum + `ORDER BY` + ghi rõ `ROWS` (tránh RANGE gộp ties — [[a01-sql-gaps-islands]]).

## 4. Phát hiện bản ghi trùng
**Đề:** Tìm `email` xuất hiện > 1 lần.
```sql
select email, count(*) as n
from customers group by email having count(*) > 1;
```
**Tư duy:** `GROUP BY ... HAVING count(*)>1`. Muốn **xoá trùng giữ 1 bản**: `ROW_NUMBER() ... where rn=1` ([[a02-sql-pivot-hierarchical]]).

## 5. Ngày liên tiếp (consecutive)
**Đề:** User đăng nhập **≥3 ngày liên tiếp**.
```sql
with g as (
  select user_id, login_date,
         login_date - (row_number() over (partition by user_id order by login_date) * interval '1 day') as grp
  from logins
)
select user_id, min(login_date) start_date, count(*) streak
from g group by user_id, grp having count(*) >= 3;
```
**Tư duy:** gaps & islands — `date - row_number` là hằng số trong chuỗi liên tiếp ([[a01-sql-gaps-islands]]).

## 6. % của tổng
**Đề:** Tỉ trọng doanh thu mỗi category.
```sql
select category, revenue,
       round(100.0 * revenue / sum(revenue) over (), 1) as pct_total
from category_revenue;
```
**Tư duy:** `sum() over ()` (không partition) = tổng toàn bảng làm mẫu số.

## 7. Self-join: nhân viên lương cao hơn sếp ⭐
**Đề:** Nhân viên có lương > lương người quản lý.
```sql
select e.name
from employees e
join employees m on e.manager_id = m.id
where e.salary > m.salary;
```
**Tư duy:** self-join bảng với chính nó qua `manager_id` → `id` ([[02-sql-joins]]).

## 8. Tăng trưởng tháng-so-tháng (MoM)
```sql
select month, revenue,
       round(100.0*(revenue - lag(revenue) over (order by month))
             / lag(revenue) over (order by month), 1) as mom_pct
from monthly_revenue;
```
**Tư duy:** `LAG` lấy kỳ trước; `nullif` mẫu số nếu lo chia 0.

## 9. Khách không có đơn (anti-join)
```sql
select c.customer_id, c.name
from customers c
left join orders o on o.customer_id = c.customer_id
where o.order_id is null;          -- hoặc NOT EXISTS
```
**Tư duy:** LEFT JOIN + `IS NULL` (an toàn hơn `NOT IN` khi có NULL — [[02-sql-joins]]).

## 10. Median (trung vị) ⭐
**Đề:** Tính median của `amount`.
```sql
-- chuẩn SQL:
select percentile_cont(0.5) within group (order by amount) as median from t;
-- không có percentile? dùng window:
select avg(amount) as median from (
  select amount,
         row_number() over (order by amount) as rn,
         count(*) over () as cnt
  from t
) where rn in (floor((cnt+1)/2.0), ceil((cnt+1)/2.0));
```
**Tư duy:** median không phải aggregate cơ bản; dùng `PERCENTILE_CONT` hoặc trick window lấy 1–2 hàng giữa rồi avg.

---
## ✅ Tự kiểm tra & "tự mò"
- [ ] Giải lại cả 10 không nhìn lời giải.
- [ ] Vì sao nth-highest dùng DENSE_RANK không ROW_NUMBER.
- [ ] Top-N per group, gaps&islands, median — 3 pattern hay quên.
- 🔭 *Tự mò:* chạy bài 2, 5, 10 trên DuckDB với dataset e-commerce thật; tự đặt thêm biến thể (top-5, ≥5 ngày, percentile 90).

➡️ Tiếp: [[a05-sql-interview-2]].
