-- Mart: doanh thu theo REGION — join fact -> dim_customer -> seed country_region.
-- Minh hoạ seed (bảng tra cứu nhỏ versioned trong repo) dùng như một ref().
select
    cr.region,
    round(sum(f.line_total), 2) as revenue,
    count(distinct f.order_id)  as orders
from {{ ref('fct_sales') }} f
join {{ ref('dim_customer') }}   dc on dc.customer_key = f.customer_key
join {{ ref('country_region') }} cr on cr.country = dc.country
where f.status = 'completed'
group by cr.region
order by revenue desc
