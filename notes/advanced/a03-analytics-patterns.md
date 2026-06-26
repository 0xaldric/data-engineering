# A03 — Analytics Patterns: Funnel, Cohort, RFM

> Những bài toán phân tích "đắt giá" DE/analytics engineer hay phải build. Mỗi cái là một pattern SQL chuẩn.

## Funnel Analysis ⭐
Đo **tỉ lệ chuyển đổi** qua các bước (view → add_to_cart → checkout → purchase).
```sql
with steps as (
  select user_id,
         max(case when event='view'        then 1 else 0 end) as s1_view,
         max(case when event='add_to_cart' then 1 else 0 end) as s2_cart,
         max(case when event='checkout'    then 1 else 0 end) as s3_checkout,
         max(case when event='purchase'    then 1 else 0 end) as s4_purchase
  from events group by user_id
)
select
  sum(s1_view)     as view,
  sum(s2_cart)     as cart,
  sum(s3_checkout) as checkout,
  sum(s4_purchase) as purchase,
  round(100.0*sum(s2_cart)/nullif(sum(s1_view),0),1)      as view_to_cart_pct,
  round(100.0*sum(s4_purchase)/nullif(sum(s1_view),0),1)  as overall_conv_pct
from steps;
```
- **Ordered funnel** (đúng thứ tự thời gian): cần kiểm `ts(cart) > ts(view)` — dùng window/self-join để đảm bảo bước sau xảy ra **sau** bước trước.
- `nullif(...,0)` tránh chia 0.

## Cohort & Retention ⭐
Nhóm user theo **kỳ tham gia** (cohort, vd tháng signup), đo **tỉ lệ quay lại** theo các kỳ sau.
```sql
with first_month as (
  select user_id, date_trunc('month', min(order_ts)) as cohort_month
  from orders group by user_id
),
activity as (
  select o.user_id, fm.cohort_month,
         date_trunc('month', o.order_ts) as active_month
  from orders o join first_month fm using (user_id)
)
select cohort_month,
       date_diff('month', cohort_month, active_month) as month_offset,  -- 0,1,2...
       count(distinct user_id) as active_users
from activity
group by cohort_month, month_offset
order by cohort_month, month_offset;
```
→ Pivot `month_offset` thành cột = **retention triangle** (ma trận tam giác): mỗi hàng một cohort, mỗi cột "tháng thứ N sau khi tham gia". Retention % = active_users / cohort_size.

## RFM Segmentation ⭐
Phân khúc khách theo **Recency** (mua gần đây), **Frequency** (mua nhiều), **Monetary** (chi nhiều).
```sql
with rfm as (
  select customer_id,
         date_diff('day', max(order_date), current_date) as recency,
         count(distinct order_id)                         as frequency,
         sum(line_total)                                  as monetary
  from sales group by customer_id
),
scored as (
  select *,
         ntile(5) over (order by recency asc)   as r,  -- recency nhỏ = tốt = điểm cao
         ntile(5) over (order by frequency desc) as f,
         ntile(5) over (order by monetary desc)  as m
  from rfm
)
select customer_id, r, f, m,
       case when r>=4 and f>=4 and m>=4 then 'Champions'
            when r>=4 and f<=2          then 'New/Promising'
            when r<=2 and f>=4          then 'At Risk (was loyal)'
            when r<=2 and f<=2          then 'Lost'
            else 'Regular' end as segment
from scored;
```
Dùng `NTILE(5)` ([[04-sql-window]]) chia thang điểm; ghép R/F/M thành segment hành động được (marketing dùng).

## Attribution (cơ bản)
Gán "công" chuyển đổi cho touchpoint nào:
- **First-touch / last-touch**: `FIRST_VALUE`/`LAST_VALUE` theo thời gian trong hành trình user.
- **Linear/time-decay**: chia đều / nặng dần về cuối — cần window + trọng số.

## ⚠️ Cạm bẫy
- Funnel không kiểm thứ tự thời gian → đếm sai (mua trước khi xem).
- Retention quên distinct user / sai mốc cohort.
- RFM: hướng điểm sai (recency nhỏ phải là điểm cao).
- Chia 0 khi cohort/bước rỗng → `nullif`.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Build funnel + tỉ lệ chuyển đổi (ordered vs unordered).
- [ ] Cohort retention (cohort_month + month_offset) → retention triangle.
- [ ] RFM bằng NTILE + ghép segment.
- 🔭 *Tự mò:* trên dataset e-commerce (orders), tính **cohort retention theo tháng signup** và **RFM** cho khách; pivot retention thành ma trận tam giác.

➡️ Tiếp: [[a04-sql-interview-1]].
