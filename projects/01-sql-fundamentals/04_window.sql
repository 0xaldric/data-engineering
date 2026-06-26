-- =====================================================================
-- 04_window.sql — Window Functions (phần "ăn tiền" nhất của SQL)
-- Run: python scripts/run_sql.py projects/01-sql-fundamentals/04_window.sql
-- Views: customers, products, orders, order_items
--
-- Window function: tính toán TRÊN một "cửa sổ" hàng liên quan, NHƯNG vẫn
-- giữ nguyên từng hàng (khác GROUP BY — gộp mất chi tiết).
-- Cú pháp: func() OVER (PARTITION BY ... ORDER BY ... <frame>)
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1) RANKING: ROW_NUMBER vs RANK vs DENSE_RANK
--    Xếp hạng sản phẩm theo doanh thu TRONG TỪNG category (PARTITION BY)
-- ---------------------------------------------------------------------
WITH prod_rev AS (
    SELECT p.category, p.product_name,
           ROUND(SUM(oi.line_total), 2) AS revenue
    FROM order_items oi
    JOIN products p ON p.product_id = oi.product_id
    JOIN orders o   ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY p.category, p.product_name
)
SELECT category, product_name, revenue,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS row_num,
       RANK()       OVER (PARTITION BY category ORDER BY revenue DESC) AS rank,
       DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS dense_rank
FROM prod_rev
QUALIFY row_num <= 3          -- QUALIFY: lọc trên window func (DuckDB) → top 3 mỗi category
ORDER BY category, row_num
LIMIT 9;

-- ---------------------------------------------------------------------
-- 2) LAG / LEAD: so với hàng trước/sau → tăng trưởng theo tháng (MoM growth)
-- ---------------------------------------------------------------------
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
       ROUND(LAG(revenue) OVER (ORDER BY month), 2) AS prev_month,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / LAG(revenue) OVER (ORDER BY month), 1) AS mom_growth_pct
FROM monthly
ORDER BY month
LIMIT 8;

-- ---------------------------------------------------------------------
-- 3) RUNNING TOTAL & MOVING AVERAGE — dùng ORDER BY trong OVER + frame
-- ---------------------------------------------------------------------
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
       -- running total: từ đầu tới hàng hiện tại
       ROUND(SUM(revenue) OVER (ORDER BY month
             ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_total,
       -- moving average 3 tháng: 2 hàng trước + hàng hiện tại
       ROUND(AVG(revenue) OVER (ORDER BY month
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m
FROM monthly
ORDER BY month
LIMIT 8;

-- ---------------------------------------------------------------------
-- 4) NTILE — chia khách thành 4 nhóm (quartile) theo mức chi tiêu
-- ---------------------------------------------------------------------
-- LƯU Ý: không GROUP BY trực tiếp trên window func (nó chạy SAU GROUP BY cùng
-- cấp). Phải tính NTILE ở một tầng (CTE) riêng, rồi mới gộp ở tầng ngoài.
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
       COUNT(*)                  AS customers,
       ROUND(MIN(total_spend),2) AS min_spend,
       ROUND(MAX(total_spend),2) AS max_spend
FROM bucketed
GROUP BY quartile
ORDER BY quartile;

-- ---------------------------------------------------------------------
-- 5) % của nhóm: share doanh thu của sản phẩm trong category
--    (window aggregate KHÔNG cần ORDER BY → áp cho cả partition)
-- ---------------------------------------------------------------------
WITH prod_rev AS (
    SELECT p.category, p.product_name,
           SUM(oi.line_total) AS revenue
    FROM order_items oi
    JOIN products p ON p.product_id = oi.product_id
    JOIN orders o   ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY p.category, p.product_name
)
SELECT category, product_name,
       ROUND(revenue, 2) AS revenue,
       ROUND(100.0 * revenue / SUM(revenue) OVER (PARTITION BY category), 1) AS pct_of_category
FROM prod_rev
ORDER BY category, revenue DESC
LIMIT 6;

-- ---------------------------------------------------------------------
-- 6) DEDUP pattern (cực hay dùng trong ETL): giữ 1 hàng "mới nhất" mỗi nhóm
--    Lấy đơn GẦN NHẤT của mỗi khách bằng ROW_NUMBER rồi lọc = 1
-- ---------------------------------------------------------------------
WITH ranked AS (
    SELECT o.customer_id, o.order_id, o.order_ts, o.status,
           ROW_NUMBER() OVER (PARTITION BY o.customer_id
                              ORDER BY CAST(o.order_ts AS TIMESTAMP) DESC) AS rn
    FROM orders o
)
SELECT customer_id, order_id, order_ts, status
FROM ranked
WHERE rn = 1                 -- chỉ giữ đơn mới nhất / khách
ORDER BY customer_id
LIMIT 8;
