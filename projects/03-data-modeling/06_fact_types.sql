-- =====================================================================
-- 06_fact_types.sql — Các loại fact table + tính cộng dồn (additivity)
-- Run: python scripts/run_sql.py projects/03-data-modeling/06_fact_types.sql
-- Views: customers, products, orders, order_items
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1) TRANSACTION fact (đã có fct_sales ở T024): mỗi hàng = 1 sự kiện bán.
--    Measures additive: line_total, quantity. Đây là loại chi tiết nhất.
-- ---------------------------------------------------------------------

-- ---------------------------------------------------------------------
-- 2) PERIODIC SNAPSHOT: mỗi hàng = trạng thái theo CHU KỲ CỐ ĐỊNH (mỗi ngày).
--    Dùng để theo dõi xu hướng; measures additive (revenue, units, orders).
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE fct_daily_sales AS
SELECT CAST(o.order_ts AS DATE)          AS snapshot_date,
       COUNT(DISTINCT o.order_id)        AS orders,
       SUM(oi.quantity)                  AS units,
       ROUND(SUM(oi.line_total), 2)      AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY snapshot_date;

SELECT snapshot_date, orders, units, revenue
FROM fct_daily_sales ORDER BY snapshot_date LIMIT 5;

-- ---------------------------------------------------------------------
-- 3) ACCUMULATING SNAPSHOT: mỗi hàng = 1 quy trình có nhiều MỐC thời gian,
--    hàng được CẬP NHẬT khi đơn tiến triển. Nhiều cột ngày (date roles).
--    (mốc ship/delivered/returned được suy ra từ status để minh hoạ cấu trúc)
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE fct_order_lifecycle AS
SELECT o.order_id,
       o.status,
       CAST(o.order_ts AS DATE)                          AS order_date,
       -- DATE + số_nguyên -> DATE (hiệu hai DATE = số ngày, dùng được ROUND/AVG)
       CASE WHEN o.status IN ('shipped','completed','returned')
            THEN CAST(o.order_ts AS DATE) + 2  END AS ship_date,
       CASE WHEN o.status IN ('completed','returned')
            THEN CAST(o.order_ts AS DATE) + 5  END AS delivered_date,
       CASE WHEN o.status = 'returned'
            THEN CAST(o.order_ts AS DATE) + 12 END AS returned_date
FROM orders o;

-- Lag measures: thời gian giữa các mốc (chỉ tính khi mốc đã đạt)
SELECT
    COUNT(*)                                                   AS total_orders,
    COUNT(ship_date)                                           AS reached_shipped,
    COUNT(delivered_date)                                      AS reached_delivered,
    COUNT(returned_date)                                       AS reached_returned,
    ROUND(AVG(delivered_date - order_date), 1)                 AS avg_days_to_deliver
FROM fct_order_lifecycle;

-- "Funnel" vòng đời: bao nhiêu đơn đạt mỗi mốc (đặc trưng accumulating snapshot)
SELECT 'placed'    AS milestone, COUNT(*)                AS n FROM fct_order_lifecycle
UNION ALL SELECT 'shipped',   COUNT(ship_date)      FROM fct_order_lifecycle
UNION ALL SELECT 'delivered', COUNT(delivered_date) FROM fct_order_lifecycle
UNION ALL SELECT 'returned',  COUNT(returned_date)  FROM fct_order_lifecycle
ORDER BY n DESC;

-- ---------------------------------------------------------------------
-- 4) ADDITIVITY — minh hoạ SEMI-ADDITIVE.
--    revenue (additive): cộng được theo MỌI chiều, kể cả thời gian.
--    Số khách lũy kế tới mỗi ngày (kiểu "balance/snapshot") là SEMI-ADDITIVE:
--    cộng theo thời gian là SAI (đếm trùng); chỉ lấy giá trị cuối kỳ / trung bình.
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE daily_active AS
SELECT CAST(signup_date AS DATE) AS d, COUNT(*) AS new_customers
FROM customers GROUP BY d;

-- additive: tổng khách mới qua cả kỳ = ĐÚNG (cộng theo thời gian được)
SELECT SUM(new_customers) AS total_new_customers FROM daily_active;

-- Final: snapshot lũy kế (running total) — giá trị mỗi ngày đúng, KHÔNG được SUM theo ngày
SELECT d AS day,
       new_customers,
       SUM(new_customers) OVER (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_customers
FROM daily_active
ORDER BY d
LIMIT 5;
