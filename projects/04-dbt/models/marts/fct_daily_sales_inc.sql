{#
  Incremental model: chỉ xử lý/ghi phần dữ liệu MỚI thay vì build lại toàn bộ.
  - Lần đầu (hoặc --full-refresh): build full.
  - Lần sau: is_incremental() = true -> chỉ lấy ngày mới hơn max đã có.
  Demo "dữ liệu tăng dần" bằng var cutoff_date (nguồn parquet vốn tĩnh):
    run 1: --full-refresh --vars '{cutoff_date: "2024-06-30"}'
    run 2: (không cutoff) -> incremental append phần còn lại.
#}
{{
    config(
      materialized='incremental',
      unique_key='date_key',
      incremental_strategy='delete+insert'
    )
}}

with daily as (
    select
        cast(strftime(order_date, '%Y%m%d') as integer) as date_key,
        order_date,
        round(sum(line_total), 2)  as revenue,
        count(distinct order_id)   as orders
    from {{ ref('int_sales_enriched') }}
    where status = 'completed'
    {% if var('cutoff_date', none) is not none %}
      and order_date <= date '{{ var("cutoff_date") }}'
    {% endif %}
    group by 1, 2
)

select * from daily

{% if is_incremental() %}
-- Chỉ giữ ngày MỚI hơn ngày lớn nhất đã có trong bảng -> không xử lý lại quá khứ.
where date_key > (select max(date_key) from {{ this }})
{% endif %}
