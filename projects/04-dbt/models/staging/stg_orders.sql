-- Staging: orders — tách timestamp & date, giữ status/channel. Materialized: view.
select
    order_id,
    customer_id,
    cast(order_ts as timestamp) as order_ts,
    cast(order_ts as date)      as order_date,
    status,
    channel
from {{ source('raw', 'orders') }}
