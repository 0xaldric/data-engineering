-- Fact: sales ở grain order-item, tham chiếu SURROGATE KEY của dimension.
-- Materialized: table.
with enriched as (
    select * from {{ ref('int_sales_enriched') }}
)
select
    dc.customer_key,                                            -- FK -> dim_customer
    dp.product_key,                                             -- FK -> dim_product
    cast(strftime(e.order_date, '%Y%m%d') as integer) as date_key,  -- smart date key
    e.order_id,                                                 -- degenerate dimension
    e.status,
    e.channel,
    e.quantity,
    e.unit_price,
    e.discount,
    e.line_total,
    e.gross_margin
from enriched e
join {{ ref('dim_customer') }} dc on dc.customer_id = e.customer_id
join {{ ref('dim_product') }}  dp on dp.product_id  = e.product_id
