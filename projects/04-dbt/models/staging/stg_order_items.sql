-- Staging: order_items — grain dòng hàng, chuẩn hoá kiểu số. Materialized: view.
select
    order_item_id,
    order_id,
    product_id,
    quantity,
    cast(unit_price as double) as unit_price,
    cast(discount   as double) as discount,
    cast(line_total as double) as line_total
from {{ source('raw', 'order_items') }}
