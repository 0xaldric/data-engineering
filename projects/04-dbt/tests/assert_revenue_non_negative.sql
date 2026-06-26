-- Singular test: doanh thu mỗi category KHÔNG được âm.
-- dbt coi test PASS nếu query trả về 0 hàng (không có vi phạm).
select category, revenue
from {{ ref('mart_revenue_by_category') }}
where revenue < 0
