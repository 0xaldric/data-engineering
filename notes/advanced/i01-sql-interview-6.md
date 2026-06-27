# I01 — SQL Interview Problems — Set 6 (tricky/edge)

> 10 bài hóc nhất — bẫy NULL, interval, rewrite. Đề + lời giải + bẫy. Tiền đề [[a06-sql-optimization]], [[h01-sql-interview-5]].

## 1. Merge overlapping intervals ⭐
**Đề:** Gộp các khoảng thời gian chồng nhau (vd booking) thành khoảng liên tục.
```sql
with f as (
  select start_ts, end_ts,
    case when start_ts <= max(end_ts) over (order by start_ts
         rows between unbounded preceding and 1 preceding)
      then 0 else 1 end as new_grp
  from intervals
),
g as (select *, sum(new_grp) over (order by start_ts) as grp from f)
select min(start_ts) start, max(end_ts) end from g group by grp;
```
Tư duy: khoảng mới bắt đầu khi `start > max(end) của các khoảng trước` → đánh nhóm → gộp.

## 2. NOT IN + NULL bẫy ⭐
**Đề:** Khách chưa mua sản phẩm nào trong danh sách cấm.
```sql
-- ❌ nếu subquery có NULL -> rỗng toàn bộ
where product_id not in (select banned_id from banned)
-- ✅
where not exists (select 1 from banned b where b.banned_id = t.product_id)
```
Luôn `NOT EXISTS` thay `NOT IN` khi subquery có thể NULL ([[02-sql-joins]]).

## 3. Correlated subquery → window (rewrite tối ưu)
```sql
-- chậm: correlated chạy mỗi hàng
select *, (select avg(salary) from emp e2 where e2.dept=e1.dept) avg_dept from emp e1;
-- nhanh: window
select *, avg(salary) over (partition by dept) avg_dept from emp;
```

## 4. Second purchase date (per customer)
```sql
select customer_id, order_date as second_purchase from (
  select customer_id, order_date,
    row_number() over (partition by customer_id order by order_date) rn
  from (select distinct customer_id, cast(order_ts as date) order_date from orders)
) where rn = 2;
```
Bẫy: distinct ngày trước (mua 2 lần cùng ngày = 1 "purchase date"?) — làm rõ định nghĩa.

## 5. Conditional aggregate với NULL
**Đề:** AVG chỉ tính giá trị > 0.
```sql
avg(case when amount > 0 then amount end)  -- CASE không else -> NULL -> AVG bỏ qua
-- KHÁC avg(case when amount>0 then amount else 0 end) (gồm 0 làm lệch)
```
Bẫy: `else 0` làm AVG sai (0 được tính); bỏ else → NULL → AVG bỏ qua ([[a07-sql-qa]]).

## 6. Gaps in sequence (số thiếu)
**Đề:** Tìm id bị thiếu trong dãy 1..N.
```sql
select t.id + 1 as missing_start
from t
where not exists (select 1 from t t2 where t2.id = t.id + 1)
  and t.id < (select max(id) from t);
```
Hoặc generate_series LEFT JOIN tìm NULL.

## 7. Pivot 2 chiều (year × quarter)
Conditional aggregation 2 biến: `sum(case when year=2024 and quarter=1 then rev end)`. Nhiều cột → code-gen ([[a02-sql-pivot-hierarchical]]).

## 8. Cumulative distinct (running unique)
Xem [[h01-sql-interview-5]] #7: đếm "lần đầu xuất hiện" rồi running sum.

## 9. Khách mua liên tục N tháng (consecutive months)
gaps & islands trên tháng: `month - row_number()*interval '1 month'` hằng số → group có ≥N ([[a01-sql-gaps-islands]]).

## 10. EXISTS vs IN vs JOIN — chọn đúng
- **EXISTS**: kiểm tồn tại, dừng sớm, an toàn NULL → "có đơn nào không".
- **IN**: tập nhỏ, đơn giản.
- **JOIN**: cần cột từ bảng kia (không chỉ kiểm tồn tại). Bẫy: JOIN để "lọc tồn tại" → **fan-out** nếu nhiều khớp (dùng EXISTS/distinct).

## ✅ "Tự mò"
🔭 Bài 1 (merge intervals) trên booking giả; bài 2 (NOT IN+NULL) tự tạo bảng có NULL xem rỗng thế nào; bài 3 đo correlated vs window.

➡️ Tiếp: [[i02-case-logistics]].
