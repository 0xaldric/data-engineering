-- Dimension: customer. Surrogate key bằng dbt_utils.generate_surrogate_key
-- (hash từ natural key — ổn định, nhất quán với dim_product). Materialized: table.
select
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_key,  -- hash surrogate
    customer_id,                                                              -- natural key
    customer_name,
    country,
    city,
    signup_date
from {{ ref('stg_customers') }}
