# G02 — SQL Interview Problems — Set 4 (analytics-heavy)

> 10 bài analytics thực chiến (cohort, retention, churn, stickiness...). Đề + lời giải. Tiền đề [[a03-analytics-patterns]].

## 1. Retention curve (N-day retention)
**Đề:** % user quay lại ở ngày thứ N sau ngày đăng ký.
```sql
with first_day as (select user_id, min(activity_date) d0 from act group by user_id),
joined as (
  select f.user_id, date_diff('day', f.d0, a.activity_date) as day_n
  from first_day f join act a using(user_id)
)
select day_n, count(distinct user_id) as retained,
       round(100.0*count(distinct user_id)/(select count(*) from first_day),1) as pct
from joined where day_n between 0 and 30 group by day_n order by day_n;
```

## 2. Cohort LTV (lifetime value tích lũy theo cohort)
```sql
with c as (select customer_id, date_trunc('month', min(order_ts)) cohort from orders group by 1)
select c.cohort,
       date_diff('month', c.cohort, date_trunc('month', o.order_ts)) as month_n,
       round(sum(oi.line_total),2) as revenue
from c join orders o using(customer_id) join order_items oi using(order_id)
group by 1,2 order by 1,2;
```
Tư duy: cohort + month_n + running sum revenue = LTV cumulative theo cohort.

## 3. Funnel ordered & time-bound
**Đề:** view→cart→purchase, mỗi bước phải xảy ra **sau** bước trước, trong 7 ngày.
```sql
select count(*) filter (where v) as viewed,
       count(*) filter (where c) as carted,
       count(*) filter (where p) as purchased
from (
  select user_id,
    max(event='view') as v,
    max(event='cart' and ts > view_ts) as c,        -- giả định đã tính view_ts
    max(event='purchase' and ts > cart_ts and ts <= view_ts + interval 7 day) as p
  from ... group by user_id
) t;
```
Tư duy: ordered funnel cần kiểm thứ tự thời gian (self-join hoặc window lấy ts mỗi bước) — không chỉ "có xảy ra".

## 4. Churn definition
**Đề:** User "churned" = không hoạt động 30 ngày kể từ lần cuối.
```sql
select count(*) filter (where date_diff('day', last_act, current_date) > 30) as churned,
       count(*) as total
from (select user_id, max(activity_date) last_act from act group by user_id) t;
```
Tư duy: định nghĩa churn rõ ràng (ngưỡng) → đo. Phỏng vấn hay hỏi "định nghĩa churn thế nào".

## 5. DAU/MAU stickiness
```sql
select round(avg(dau)*1.0 / mau, 3) as stickiness from (
  select count(distinct user_id) filter (where activity_date = current_date) as dau,
         count(distinct user_id) as mau
  from act where activity_date >= current_date - interval 30 day
) t;
```
Stickiness = DAU/MAU (cao = dùng thường xuyên).

## 6. Market basket (sản phẩm mua cùng)
```sql
select a.product_id p1, b.product_id p2, count(*) n
from order_items a join order_items b on a.order_id=b.order_id and a.product_id<b.product_id
group by 1,2 order by n desc limit 10;
```

## 7. Week-over-week growth
```sql
with w as (select date_trunc('week', order_ts) wk, sum(line_total) rev from ... group by 1)
select wk, rev, round(100.0*(rev-lag(rev) over(order by wk))/lag(rev) over(order by wk),1) wow
from w order by wk;
```

## 8. % new vs returning revenue mỗi tháng
```sql
with fo as (select customer_id, min(order_ts) first_ts from orders group by 1)
select date_trunc('month', o.order_ts) m,
  round(sum(oi.line_total) filter (where date_trunc('month',o.order_ts)=date_trunc('month',fo.first_ts)),2) new_rev,
  round(sum(oi.line_total) filter (where date_trunc('month',o.order_ts)>date_trunc('month',fo.first_ts)),2) ret_rev
from orders o join fo using(customer_id) join order_items oi using(order_id)
group by 1 order by 1;
```

## 9. Sessionize + metric phiên
LAG gap → session_id (running sum cờ — [[a01-sql-gaps-islands]]) → group by session tính duration, n_events, bounce (1 event).

## 10. Percentile rank của khách (so toàn bộ)
```sql
select customer_id, total_spend,
  round(percent_rank() over (order by total_spend), 3) as pctile
from (select customer_id, sum(line_total) total_spend from ... group by 1) t;
```
`PERCENT_RANK()` cho vị trí tương đối (0–1) — phân khúc top X%.

## ✅ "Tự mò"
🔭 Chạy retention curve (#1) + cohort LTV (#2) + stickiness (#5) trên e-commerce; pivot retention thành ma trận tam giác.

➡️ Tiếp: [[g03-case-log-analytics]].
