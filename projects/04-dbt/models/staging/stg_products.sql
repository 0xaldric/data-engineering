-- Staging: products — chuẩn hoá kiểu số. Materialized: view.
select
    product_id,
    product_name,
    category,
    cast(unit_cost  as double) as unit_cost,
    cast(unit_price as double) as unit_price,
    is_available
from {{ source('raw', 'products') }}
