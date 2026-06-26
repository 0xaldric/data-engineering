{#
  Demo Jinja for-loop: pivot doanh thu theo status thành nhiều cột mà KHÔNG
  phải viết tay từng cột. set = biến, for = lặp, loop.last để bỏ dấu phẩy cuối.
  (Lưu ý: KHÔNG đặt cú pháp tag Jinja trong comment SQL '--' vì Jinja vẫn parse nó.)
#}
{% set statuses = ['completed', 'shipped', 'cancelled', 'returned'] %}

select
    dp.category,
    {% for s in statuses %}
    round(sum(case when f.status = '{{ s }}' then f.line_total else 0 end), 2) as revenue_{{ s }}{{ "," if not loop.last else "" }}
    {% endfor %}
from {{ ref('fct_sales') }} f
join {{ ref('dim_product') }} dp on dp.product_key = f.product_key
group by dp.category
order by dp.category
