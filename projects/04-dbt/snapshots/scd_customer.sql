{#
  Snapshot = SCD Type 2 TỰ ĐỘNG của dbt. Mỗi lần `dbt snapshot`, dbt so dữ liệu
  hiện tại với bản đã lưu; nếu check_cols đổi -> đóng phiên bản cũ
  (dbt_valid_to) và chèn phiên bản mới. Tự thêm: dbt_valid_from, dbt_valid_to,
  dbt_scd_id, dbt_updated_at.

  Để DEMO thay đổi (nguồn parquet vốn tĩnh): biến `move_customer_1` ép country
  của khách #1 thành 'ZZ'. Chạy lần 2 với --vars '{move_customer_1: true}'.
#}
{% snapshot scd_customer %}
{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='check',
      check_cols=['country', 'city']
    )
}}

select
    customer_id,
    customer_name,
    {% if var('move_customer_1', false) %}
    case when customer_id = 1 then 'ZZ' else country end as country,
    {% else %}
    country,
    {% endif %}
    city
from {{ ref('stg_customers') }}

{% endsnapshot %}
