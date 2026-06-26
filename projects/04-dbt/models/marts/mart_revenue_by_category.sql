-- Mart: doanh thu theo category (đơn completed). Materialized: table.
select
    dp.category,
    round(sum(f.line_total), 2)   as revenue,
    sum(f.quantity)               as units,
    count(distinct f.order_id)    as orders
from {{ ref('fct_sales') }} f
join {{ ref('dim_product') }} dp on dp.product_key = f.product_key
where f.status = 'completed'
group by dp.category
order by revenue desc
