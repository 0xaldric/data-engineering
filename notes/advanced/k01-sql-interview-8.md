# K01 — SQL Interview Problems — Set 8 (mixed)

> 10 bài thực chiến. Đề + lời giải + tư duy. Tiền đề toàn Module A + [[j01-sql-interview-7]].

## 1. Max concurrent (số sự kiện chồng nhau tối đa) ⭐
**Đề:** Số cuộc gọi/booking đồng thời cao nhất.
```sql
with ev as (
  select start_ts as ts, 1 as delta from calls
  union all
  select end_ts as ts, -1 from calls
)
select max(running) from (
  select sum(delta) over (order by ts, delta desc
         rows between unbounded preceding and current row) as running
  from ev
) t;
```
Tư duy: +1 lúc start, −1 lúc end, sort theo ts, running sum → đỉnh = max concurrent. (Bẫy: end trước start khi cùng ts → `delta desc` để −1 sau.)

## 2. As-of join (nearest neighbor theo thời gian)
**Đề:** Mỗi giao dịch ghép với tỉ giá **hiệu lực tại thời điểm đó**.
```sql
-- DuckDB ASOF JOIN:
select t.*, r.rate
from txn t asof join rates r on r.ts <= t.ts;   -- lấy rate gần nhất <= txn ts
-- chuẩn SQL: correlated lateral lấy max(ts) <= txn ts
```
As-of join = ghép với hàng "gần nhất trước đó" — cực hay trong tài chính/SCD ([[18-scd]] as-of).

## 3. First event after condition
**Đề:** Với mỗi user, event đầu tiên **sau khi** họ 'purchase'.
```sql
with p as (select user_id, min(ts) as buy_ts from events where type='purchase' group by 1)
select e.user_id, min(e.ts) as first_after
from events e join p using(user_id)
where e.ts > p.buy_ts group by 1;
```

## 4. Hierarchical aggregate (rollup theo cây)
**Đề:** Tổng doanh thu mỗi node **gồm cả con cháu** (cây category).
```sql
with recursive sub as (
  select id, id as ancestor from category
  union all
  select c.id, s.ancestor from category c join sub s on c.parent_id = s.id
)
select s.ancestor, sum(sales.amount) total
from sub join sales on sales.category_id = s.id
group by s.ancestor;
```
Tư duy: recursive sinh mọi cặp (node, tổ tiên) → mỗi sale tính cho mọi tổ tiên → rollup cây.

## 5. Running count distinct trong window (xấp xỉ)
Chính xác khó (xem [[h01-sql-interview-5]] #7). Xấp xỉ scale lớn: `approx_count_distinct` ([[g08-probabilistic-ds]]).

## 6. Ratio/share trong nhiều cấp
```sql
select category, product, revenue,
  revenue / sum(revenue) over (partition by category) as share_in_category,
  revenue / sum(revenue) over () as share_total
from t;
```

## 7. Sliding window distinct users (rolling 7-day active)
```sql
-- WAU rolling: distinct user trong 7 ngày tới mỗi ngày
select d, (select count(distinct user_id) from act a
           where a.day between d - interval 6 day and d) as wau
from (select distinct day d from act) days;
```
(Window không làm distinct trực tiếp → correlated/self-join; tối ưu = approx hoặc pre-agg.)

## 8. Dedup keeping latest non-null per column
Xem [[j01-sql-interview-7]] #9 / coalesce qua window: lấy `last_value(col ignore nulls)` mỗi cột.

## 9. Sequence gap (số hoá đơn thiếu)
```sql
select prev_id + 1 as gap_start, id - 1 as gap_end from (
  select id, lag(id) over (order by id) prev_id from invoices
) where id - prev_id > 1;
```

## 10. Percentage change handle divide-by-zero & NULL
```sql
case when prev = 0 or prev is null then null
     else round(100.0*(cur - prev)/prev, 1) end as pct_change
```
Bẫy: chia 0 (prev=0) và prev NULL (kỳ đầu) → xử lý rõ ràng, không để lỗi/NULL ngầm.

## ✅ "Tự mò"
🔭 Bài 1 (max concurrent) trên order overlap; bài 2 (asof join) ghép order với "giá tại thời điểm" — DuckDB hỗ trợ `ASOF JOIN` thật; bài 4 (hierarchical rollup) trên cây category.

➡️ Tiếp: [[k02-case-insurance]].
