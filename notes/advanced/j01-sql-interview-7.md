# J01 — SQL Interview Problems — Set 7 (mixed hard)

> 10 bài tổng hợp khó. Đề + lời giải + tư duy. Tiền đề toàn bộ Module A + [[i01-sql-interview-6]].

## 1. Running max (cao nhất tới hiện tại)
```sql
select day, value,
  max(value) over (order by day rows between unbounded preceding and current row) as running_max
from t;
```

## 2. Islands có điều kiện (chuỗi trạng thái 'active')
**Đề:** Tìm các đoạn liên tiếp status='active' của mỗi user.
```sql
with f as (
  select user_id, day, status,
    case when status='active' and lag(status) over (partition by user_id order by day) is distinct from 'active'
      then 1 else 0 end as new_island
  from t where status='active' or true   -- giữ context
),
g as (select *, sum(new_island) over (partition by user_id order by day) grp from f where status='active')
select user_id, min(day) start, max(day) end, count(*) len from g group by user_id, grp;
```

## 3. Recursive running balance (mỗi giao dịch ra số dư)
```sql
-- window đủ dùng (không cần recursive thật):
select txn_id, amount,
  sum(amount) over (partition by account order by ts
       rows between unbounded preceding and current row) as balance
from txn;
```
Tư duy: running sum = balance; recursive chỉ cần khi phụ thuộc kết quả hàng trước phi tuyến.

## 4. Conditional first/last (giá trị tại sự kiện cụ thể)
**Đề:** Với mỗi đơn, giá tại lần 'view' đầu tiên.
```sql
select order_id,
  min(case when event='view' then price end) as first_view_price  -- min trên CASE-null
from t group by order_id;
```

## 5. Time-weighted average
**Đề:** Giá trung bình **có trọng số theo thời gian** giữ (vd giá cổ phiếu mỗi giá giữ bao lâu).
```sql
with d as (
  select price, ts,
    extract(epoch from lead(ts) over (order by ts) - ts) as duration_sec
  from prices
)
select sum(price * duration_sec) / sum(duration_sec) as twap from d where duration_sec is not null;
```
Tư duy: trọng số = thời lượng giữ (lead - current); không phải avg đơn thuần.

## 6. Khách mua đủ N category khác nhau
```sql
select customer_id from sales
group by customer_id
having count(distinct category) >= 3;
```

## 7. Percentile bucket (chia 100 nhóm)
```sql
select customer_id, total,
  ntile(100) over (order by total) as percentile_bucket  -- 1..100
from spend;
```

## 8. Lead/lag nhiều bước + so sánh
```sql
select month, rev,
  lag(rev,1) over (order by month) prev,
  lag(rev,12) over (order by month) yoy,
  rev - lag(rev,3) over (order by month) as q_change
from monthly;
```

## 9. Dedup giữ bản "đầy đủ nhất" (không phải mới nhất)
**Đề:** Trùng theo id, giữ bản có ít NULL nhất.
```sql
select * from (
  select *, row_number() over (partition by id order by
    (case when col_a is null then 0 else 1 end)+(case when col_b is null then 0 else 1 end) desc) rn
  from t
) where rn = 1;
```
Tư duy: ORDER BY theo "số cột non-null" giảm dần → giữ bản đầy đủ nhất.

## 10. Gap-free ranking (đếm hạng không nhảy)
DENSE_RANK cho hạng liên tục; ROW_NUMBER cho thứ tự duy nhất; RANK cho hạng nhảy. Chọn đúng theo yêu cầu ([[a04-sql-interview-1]]).

## ✅ "Tự mò"
🔭 Bài 5 (time-weighted average) trên giá sản phẩm theo thời gian; bài 2 (islands trạng thái) trên order status sequence; bài 9 (dedup đầy đủ nhất).

➡️ Tiếp: [[j02-case-telecom]].
