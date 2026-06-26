-- Dimension: product. Surrogate key bằng dbt_utils (hash, ổn định hơn row_number),
-- price_tier bằng macro tự viết. Materialized: table.
select
    {{ dbt_utils.generate_surrogate_key(['product_id']) }} as product_key,  -- hash surrogate
    product_id,                                                              -- natural key
    product_name,
    category,
    unit_cost,
    unit_price,
    {{ price_tier('unit_price') }} as price_tier   -- macro tự viết (DRY)
from {{ ref('stg_products') }}
