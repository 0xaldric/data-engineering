{#
  Macro phân hạng giá — viết logic CASE MỘT lần, tái dùng mọi nơi (DRY).
  Dùng: {{ price_tier('unit_price') }}
#}
{% macro price_tier(price_column) %}
    case
        when {{ price_column }} >= 200 then 'premium'
        when {{ price_column }} >= 50  then 'mid'
        else 'budget'
    end
{% endmacro %}
