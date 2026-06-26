-- Intermediate: gộp order_items + orders + products về grain ORDER-ITEM.
-- Chứa business logic join trung gian; materialized view (theo dbt_project.yml).
with items as (
    select * from {{ ref('stg_order_items') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
),
products as (
    select * from {{ ref('stg_products') }}
)
select
    i.order_item_id,
    i.order_id,
    i.product_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.channel,
    p.category,
    p.unit_cost,
    i.quantity,
    i.unit_price,
    i.discount,
    i.line_total,
    round(i.line_total - p.unit_cost * i.quantity, 2) as gross_margin
from items i
join orders   o on o.order_id   = i.order_id
join products p on p.product_id = i.product_id
