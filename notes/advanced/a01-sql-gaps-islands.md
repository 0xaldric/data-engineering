# A01 — Advanced SQL I: Gaps & Islands, Sessionization

> Track nâng cao. Những pattern SQL "khó" hay gặp trong phân tích & phỏng vấn. Tiền đề: [[04-sql-window]].

## Gaps & Islands ⭐
Bài toán kinh điển: tìm **chuỗi giá trị liên tiếp** (islands) và **khoảng trống** (gaps). VD: ngày hoạt động liên tiếp của user, dãy số liền nhau, streak.

**Mẹo vàng:** `số_thứ_tự − ROW_NUMBER()` là **hằng số trong cùng một đảo**.
```sql
-- Tìm các chuỗi ngày đăng nhập liên tiếp của mỗi user
with logins as (
  select user_id, login_date,
         row_number() over (partition by user_id order by login_date) as rn
  from daily_logins
),
grouped as (
  -- login_date - rn ngày = "neo đảo": cùng đảo thì hiệu này không đổi
  select user_id, login_date,
         login_date - (rn * interval '1 day') as island_key
  from logins
)
select user_id,
       min(login_date) as streak_start,
       max(login_date) as streak_end,
       count(*)        as streak_len
from grouped
group by user_id, island_key
order by user_id, streak_start;
```
- Với số nguyên liên tiếp: `value - row_number()` không đổi trong đảo.
- Tìm **gaps**: dùng `LEAD(date) - date > 1` để phát hiện điểm đứt.

## Sessionization ⭐
Gom event thành **phiên (session)**: một phiên mới bắt đầu khi khoảng cách thời gian giữa 2 event > ngưỡng (vd 30 phút).
```sql
with ev as (
  select user_id, event_ts,
         lag(event_ts) over (partition by user_id order by event_ts) as prev_ts
  from events
),
flagged as (
  select *,
         -- đánh dấu điểm bắt đầu session mới (gap > 30')
         case when prev_ts is null
                or event_ts - prev_ts > interval '30 minutes'
              then 1 else 0 end as is_new_session
  from ev
),
sessioned as (
  select *,
         -- running sum của cờ = session_id tăng dần
         sum(is_new_session) over (partition by user_id order by event_ts) as session_id
  from flagged
)
select user_id, session_id,
       min(event_ts) as session_start,
       max(event_ts) as session_end,
       count(*)      as n_events
from sessioned
group by user_id, session_id;
```
Pattern lõi: **LAG để đo gap → cờ bắt đầu → running sum cờ = session id**. Cực hay dùng cho clickstream/analytics.

## Running & Cumulative nâng cao
- Running total: `sum(x) over (order by t rows between unbounded preceding and current row)`.
- Moving average N kỳ: `avg(x) over (order by t rows between (N-1) preceding and current row)`.
- % của tổng nhóm: `x / sum(x) over (partition by g)`.
- Running distinct count: khó — thường cần self-join hoặc approx; cân nhắc.

## ⭐ Frame: ROWS vs RANGE vs GROUPS (điểm hay sai)
```
ROWS   BETWEEN 2 PRECEDING AND CURRENT ROW   -- đếm theo SỐ HÀNG vật lý
RANGE  BETWEEN ... -- theo GIÁ TRỊ order-by (gộp mọi hàng cùng giá trị)
GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW   -- theo nhóm giá trị bằng nhau
```
- Mặc định khi có ORDER BY mà không ghi frame = `RANGE UNBOUNDED PRECEDING ... CURRENT ROW` → với giá trị trùng, running total **nhảy cục** (gộp hết hàng cùng giá trị). → **Luôn ghi rõ `ROWS`** cho running/moving (xem lại [[04-sql-window]]).

## ⚠️ Cạm bẫy
- Gaps & islands: quên `PARTITION BY` entity → trộn chuỗi của nhiều user.
- Sessionization: ngưỡng gap sai đơn vị (phút vs giây).
- Frame `RANGE` ngầm gây sai running total khi có ties.
- `value - row_number()` chỉ đúng khi value tăng đều bước 1 (ngày/số nguyên liên tục).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Giải thích "neo đảo" `value − row_number()`.
- [ ] Viết sessionization (LAG → cờ → running sum).
- [ ] ROWS vs RANGE vs GROUPS; vì sao ghi rõ ROWS.
- 🔭 *Tự mò:* sinh bảng `events(user_id, event_ts)` từ orders e-commerce (dùng order_ts), chạy sessionization trên DuckDB; thử đổi ngưỡng 30' → 1h xem số session đổi.

➡️ Tiếp: [[a02-sql-pivot-hierarchical]].
