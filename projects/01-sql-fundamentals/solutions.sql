-- =====================================================================
-- solutions.sql — Lời giải 15 bài trong exercises.sql
-- Run: python scripts/run_sql.py projects/01-sql-fundamentals/solutions.sql
-- Mọi câu phải chạy đúng trên DuckDB.
-- =====================================================================

-- Bài 1. 10 sản phẩm đắt nhất
SELECT product_name, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 10;

-- Bài 2. Số khách theo quốc gia
SELECT country, COUNT(*) AS customers
FROM customers
GROUP BY country
ORDER BY customers DESC;

-- Bài 3. Tổng doanh thu completed
SELECT ROUND(SUM(oi.line_total), 2) AS revenue_completed
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed';

-- Bài 4. Doanh thu theo category
SELECT p.category, ROUND(SUM(oi.line_total), 2) AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o   ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;

-- Bài 5. Số sản phẩm không available
SELECT COUNT(*) AS unavailable_products
FROM products
WHERE is_available = FALSE;

-- Bài 6. Top 5 khách chi tiêu nhiều nhất
SELECT c.name, ROUND(SUM(oi.line_total), 2) AS total_spend
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC
LIMIT 5;

-- Bài 7. Đếm đơn theo status, pivot 1 hàng bằng FILTER
SELECT
    COUNT(*) FILTER (WHERE status = 'completed') AS completed,
    COUNT(*) FILTER (WHERE status = 'shipped')   AS shipped,
    COUNT(*) FILTER (WHERE status = 'cancelled') AS cancelled,
    COUNT(*) FILTER (WHERE status = 'returned')  AS returned
FROM orders;

-- Bài 8. Doanh thu theo tháng năm 2024
SELECT date_trunc('month', CAST(o.order_ts AS TIMESTAMP)) AS month,
       ROUND(SUM(oi.line_total), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
  AND EXTRACT(year FROM CAST(o.order_ts AS TIMESTAMP)) = 2024
GROUP BY month
ORDER BY month;

-- Bài 9. AOV = doanh thu mỗi đơn rồi lấy trung bình (CTE để tính đúng grain)
WITH order_value AS (
    SELECT o.order_id, SUM(oi.line_total) AS value
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY o.order_id
)
SELECT ROUND(AVG(value), 2) AS avg_order_value,
       COUNT(*)             AS n_orders
FROM order_value;

-- Bài 10. Sản phẩm chưa từng bán (NOT EXISTS)
SELECT p.product_id, p.product_name, p.category
FROM products p
WHERE NOT EXISTS (
    SELECT 1 FROM order_items oi WHERE oi.product_id = p.product_id
)
ORDER BY p.product_id;

-- Bài 11. Top 3 sản phẩm theo doanh thu mỗi category
WITH prod_rev AS (
    SELECT p.category, p.product_name, SUM(oi.line_total) AS revenue
    FROM order_items oi
    JOIN products p ON p.product_id = oi.product_id
    JOIN orders o   ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY p.category, p.product_name
)
SELECT category, product_name, ROUND(revenue, 2) AS revenue,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
FROM prod_rev
QUALIFY rnk <= 3
ORDER BY category, rnk
LIMIT 12;

-- Bài 12. MoM growth %
WITH monthly AS (
    SELECT date_trunc('month', CAST(o.order_ts AS TIMESTAMP)) AS month,
           SUM(oi.line_total) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY month
)
SELECT month,
       ROUND(revenue, 2) AS revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / LAG(revenue) OVER (ORDER BY month), 1) AS mom_pct
FROM monthly
ORDER BY month
LIMIT 8;

-- Bài 13. Running total theo tháng
WITH monthly AS (
    SELECT date_trunc('month', CAST(o.order_ts AS TIMESTAMP)) AS month,
           SUM(oi.line_total) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY month
)
SELECT month, ROUND(revenue, 2) AS revenue,
       ROUND(SUM(revenue) OVER (ORDER BY month
             ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_total
FROM monthly
ORDER BY month
LIMIT 8;

-- Bài 14. Tỉ lệ % đơn cancelled theo channel
SELECT channel,
       COUNT(*)                                          AS total_orders,
       COUNT(*) FILTER (WHERE status = 'cancelled')      AS cancelled,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'cancelled') / COUNT(*), 1) AS cancel_pct
FROM orders
GROUP BY channel
ORDER BY cancel_pct DESC;

-- Bài 15. NTILE(4) phân khúc khách theo chi tiêu
WITH spend AS (
    SELECT c.customer_id, SUM(oi.line_total) AS total_spend
    FROM customers c
    JOIN orders o       ON o.customer_id = c.customer_id
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id
),
bucketed AS (
    SELECT customer_id, total_spend,
           NTILE(4) OVER (ORDER BY total_spend DESC) AS quartile
    FROM spend
)
SELECT quartile,
       COUNT(*)                   AS customers,
       ROUND(MIN(total_spend), 2) AS min_spend,
       ROUND(MAX(total_spend), 2) AS max_spend
FROM bucketed
GROUP BY quartile
ORDER BY quartile;
