-- Staging: customers — rename + cast, 1 model / 1 source. Materialized: view.
select
    customer_id,
    name                       as customer_name,
    email,
    country,
    city,
    cast(signup_date as date)  as signup_date,
    is_active
from {{ source('raw', 'customers') }}
