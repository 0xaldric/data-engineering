-- =====================================================================
-- 05_cte_subquery.sql — CTEs, Recursive CTE, Subqueries, Set operations
-- Run: python scripts/run_sql.py projects/01-sql-fundamentals/05_cte_subquery.sql
-- Views: customers, products, orders, order_items
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1) CTE cơ bản (WITH) — đặt tên cho query con, đọc từ trên xuống
--    Nhiều CTE nối tiếp nhau: mỗi cái dùng được kết quả cái trước
-- ---------------------------------------------------------------------
WITH order_value AS (
    SELECT o.order_id, o.customer_id, SUM(oi.line_total) AS value
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY o.order_id, o.customer_id
),
customer_stats AS (
    SELECT customer_id,
           COUNT(*)      AS n_orders,
           SUM(value)    AS lifetime_value,
           AVG(value)    AS avg_order_value
    FROM order_value
    GROUP BY customer_id
)
SELECT c.name, s.n_orders,
       ROUND(s.lifetime_value, 2)  AS ltv,
       ROUND(s.avg_order_value, 2) AS aov
FROM customer_stats s
JOIN customers c ON c.customer_id = s.customer_id
ORDER BY s.lifetime_value DESC
LIMIT 5;

-- ---------------------------------------------------------------------
-- 2) RECURSIVE CTE (a): sinh chuỗi tháng (calendar) — không cần bảng date
-- ---------------------------------------------------------------------
WITH RECURSIVE months(month) AS (
    SELECT DATE '2023-01-01'
    UNION ALL
    SELECT month + INTERVAL 1 MONTH
    FROM months
    WHERE month < DATE '2023-06-01'
)
SELECT month FROM months ORDER BY month;

-- ---------------------------------------------------------------------
-- 3) RECURSIVE CTE (b): duyệt cây phân cấp (org chart) + đường dẫn + cấp bậc
-- ---------------------------------------------------------------------
WITH RECURSIVE org(emp_id, title, mgr_id) AS (
    SELECT * FROM (VALUES
        (1, 'CEO',       NULL),
        (2, 'VP Eng',    1),
        (3, 'VP Sales',  1),
        (4, 'Eng Mgr',   2),
        (5, 'Developer', 4)
    ) AS t(emp_id, title, mgr_id)
),
tree AS (
    -- anchor: gốc (không có sếp)
    SELECT emp_id, title, mgr_id, 1 AS level, title AS path
    FROM org WHERE mgr_id IS NULL
    UNION ALL
    -- recursive: nối con vào cha
    SELECT o.emp_id, o.title, o.mgr_id, t.level + 1, t.path || ' > ' || o.title
    FROM org o
    JOIN tree t ON o.mgr_id = t.emp_id
)
SELECT level, emp_id, title, path FROM tree ORDER BY level, emp_id;

-- ---------------------------------------------------------------------
-- 4) SCALAR subquery — query con trả 1 giá trị, nhúng vào SELECT/WHERE
--    So sánh giá sản phẩm với giá trung bình toàn bộ
-- ---------------------------------------------------------------------
SELECT product_name, unit_price,
       ROUND((SELECT AVG(unit_price) FROM products), 2) AS avg_price,
       ROUND(unit_price - (SELECT AVG(unit_price) FROM products), 2) AS diff_from_avg
FROM products
ORDER BY unit_price DESC
LIMIT 5;

-- ---------------------------------------------------------------------
-- 5) CORRELATED subquery — query con tham chiếu hàng bên ngoài (chạy mỗi hàng)
--    Sản phẩm đắt nhất TRONG category của chính nó
-- ---------------------------------------------------------------------
SELECT p.category, p.product_name, p.unit_price
FROM products p
WHERE p.unit_price = (
    SELECT MAX(p2.unit_price) FROM products p2 WHERE p2.category = p.category
)
ORDER BY p.category
LIMIT 5;

-- ---------------------------------------------------------------------
-- 6) IN vs EXISTS — lọc theo tập / theo tồn tại
--    EXISTS thường nhanh hơn IN trên tập lớn và an toàn với NULL hơn NOT IN
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS active_buyers
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.customer_id AND o.status = 'completed'
);

-- ---------------------------------------------------------------------
-- 7) SET OPERATIONS — UNION / INTERSECT / EXCEPT (trên tập cột tương thích)
--    Khách "VIP" (đã hoàn tất đơn) so với khách bị "returned"
-- ---------------------------------------------------------------------
WITH completed_buyers AS (
    SELECT DISTINCT customer_id FROM orders WHERE status = 'completed'
),
returners AS (
    SELECT DISTINCT customer_id FROM orders WHERE status = 'returned'
)
SELECT 'completed_only' AS segment, COUNT(*) AS n
FROM (SELECT customer_id FROM completed_buyers EXCEPT SELECT customer_id FROM returners)
UNION ALL
SELECT 'both_completed_and_returned', COUNT(*)
FROM (SELECT customer_id FROM completed_buyers INTERSECT SELECT customer_id FROM returners)
ORDER BY segment;
