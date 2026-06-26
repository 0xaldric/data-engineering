-- =====================================================================
-- 03_aggregation.sql — Aggregation, GROUP BY, HAVING, FILTER, ROLLUP/CUBE
-- Run: python scripts/run_sql.py projects/01-sql-fundamentals/03_aggregation.sql
-- Views: customers, products, orders, order_items
-- Lưu ý fan-out (xem 02_joins): line_total ở grain item nên SUM an toàn;
-- đếm đơn bằng COUNT(DISTINCT order_id).
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1) Aggregate cơ bản: COUNT / SUM / AVG / MIN / MAX (toàn bộ, không GROUP BY)
-- ---------------------------------------------------------------------
SELECT
    COUNT(*)                        AS n_order_items,
    COUNT(DISTINCT o.order_id)      AS n_orders,
    COUNT(DISTINCT o.customer_id)   AS n_buyers,
    ROUND(SUM(oi.line_total), 2)    AS revenue,
    ROUND(AVG(oi.line_total), 2)    AS avg_line,
    MIN(oi.line_total)              AS min_line,
    MAX(oi.line_total)              AS max_line
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed';

-- ---------------------------------------------------------------------
-- 2) GROUP BY: doanh thu theo category (join thêm products)
-- ---------------------------------------------------------------------
SELECT p.category,
       COUNT(DISTINCT o.order_id)   AS orders,
       SUM(oi.quantity)             AS units,
       ROUND(SUM(oi.line_total), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p     ON p.product_id = oi.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;

-- ---------------------------------------------------------------------
-- 3) GROUP BY theo thời gian: doanh thu theo tháng (date_trunc)
-- ---------------------------------------------------------------------
SELECT date_trunc('month', CAST(o.order_ts AS TIMESTAMP)) AS month,
       COUNT(DISTINCT o.order_id)   AS orders,
       ROUND(SUM(oi.line_total), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY month
ORDER BY month
LIMIT 6;

-- ---------------------------------------------------------------------
-- 4) WHERE vs HAVING: lọc TRƯỚC group (WHERE) vs lọc SAU group (HAVING)
--    Top customers chi tiêu > 3000 (HAVING lọc trên aggregate)
-- ---------------------------------------------------------------------
SELECT c.customer_id, c.name,
       ROUND(SUM(oi.line_total), 2) AS spend
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'          -- lọc hàng thô trước
GROUP BY c.customer_id, c.name
HAVING SUM(oi.line_total) > 3000      -- lọc nhóm sau khi gộp
ORDER BY spend DESC
LIMIT 5;

-- ---------------------------------------------------------------------
-- 5) FILTER — conditional aggregation: nhiều "lát cắt" trong MỘT hàng
--    So sánh doanh thu completed vs cancelled mà không cần join nhiều lần
-- ---------------------------------------------------------------------
SELECT p.category,
       ROUND(SUM(oi.line_total) FILTER (WHERE o.status = 'completed'), 2) AS rev_completed,
       ROUND(SUM(oi.line_total) FILTER (WHERE o.status = 'cancelled'), 2) AS rev_cancelled,
       COUNT(DISTINCT o.order_id) FILTER (WHERE o.status = 'returned')     AS returned_orders
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p     ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY rev_completed DESC
LIMIT 5;

-- ---------------------------------------------------------------------
-- 6) ROLLUP — subtotal + grand total tự động
--    Doanh thu theo (category, channel) + subtotal mỗi category + tổng chung
--    (dòng có NULL ở channel = subtotal của category; NULL cả hai = tổng chung)
-- ---------------------------------------------------------------------
SELECT p.category, o.channel,
       ROUND(SUM(oi.line_total), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p     ON p.product_id = oi.product_id
WHERE o.status = 'completed' AND p.category IN ('Electronics', 'Books')
GROUP BY ROLLUP (p.category, o.channel)
ORDER BY p.category NULLS LAST, o.channel NULLS LAST;

-- ---------------------------------------------------------------------
-- 7) GROUPING SETS — tự chọn đúng các mức tổng hợp cần (linh hoạt hơn ROLLUP)
--    Vừa tổng theo category, vừa tổng theo channel, trong cùng 1 query
-- ---------------------------------------------------------------------
SELECT p.category, o.channel,
       ROUND(SUM(oi.line_total), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p     ON p.product_id = oi.product_id
WHERE o.status = 'completed'
GROUP BY GROUPING SETS ((p.category), (o.channel))
ORDER BY p.category NULLS LAST, o.channel NULLS LAST
LIMIT 8;

-- ---------------------------------------------------------------------
-- 8) Final: tỉ trọng doanh thu mỗi category (% trên tổng) — bài toán hay gặp
-- ---------------------------------------------------------------------
SELECT p.category,
       ROUND(SUM(oi.line_total), 2) AS revenue,
       ROUND(100.0 * SUM(oi.line_total) / SUM(SUM(oi.line_total)) OVER (), 1) AS pct_of_total
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p     ON p.product_id = oi.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;
