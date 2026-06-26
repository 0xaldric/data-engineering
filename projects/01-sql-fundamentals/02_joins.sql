-- =====================================================================
-- 02_joins.sql — SQL JOINs: tất cả các loại + cạm bẫy
-- Run: python scripts/run_sql.py projects/01-sql-fundamentals/02_joins.sql
-- Views có sẵn: customers, products, orders, order_items
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1) INNER JOIN — chỉ giữ hàng khớp ở CẢ hai bảng
--    Doanh thu mỗi đơn = join orders với order_items
-- ---------------------------------------------------------------------
SELECT o.order_id, o.status, COUNT(oi.order_item_id) AS n_items,
       ROUND(SUM(oi.line_total), 2) AS order_value
FROM orders o
INNER JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, o.status
ORDER BY order_value DESC
LIMIT 5;

-- ---------------------------------------------------------------------
-- 2) LEFT JOIN — giữ TẤT CẢ hàng bảng trái, bên phải thiếu thì NULL
--    Khách + tổng số đơn (kể cả khách chưa mua → 0)
-- ---------------------------------------------------------------------
SELECT c.customer_id, c.name,
       COUNT(o.order_id) AS n_orders   -- COUNT(cột) bỏ qua NULL → khách 0 đơn ra 0
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY n_orders ASC, c.customer_id
LIMIT 5;

-- ---------------------------------------------------------------------
-- 3) ANTI-JOIN (LEFT JOIN + IS NULL) — tìm hàng KHÔNG khớp
--    Khách chưa từng đặt đơn nào (rất hay dùng trong thực tế)
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS customers_without_orders
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;

-- ---------------------------------------------------------------------
-- 4) RIGHT JOIN — giữ tất cả bảng phải (đối xứng với LEFT)
--    Thường viết lại thành LEFT cho dễ đọc; ở đây minh hoạ cú pháp
-- ---------------------------------------------------------------------
SELECT p.category, COUNT(oi.order_item_id) AS times_sold
FROM order_items oi
RIGHT JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY times_sold DESC
LIMIT 5;

-- ---------------------------------------------------------------------
-- 5) FULL OUTER JOIN — giữ hàng không khớp ở CẢ hai phía
--    Đối chiếu 2 tập product_id: trong catalog vs đã từng bán
-- ---------------------------------------------------------------------
WITH sold AS (SELECT DISTINCT product_id FROM order_items)
SELECT
    COUNT(*) FILTER (WHERE p.product_id IS NULL) AS sold_but_not_in_catalog,
    COUNT(*) FILTER (WHERE s.product_id IS NULL) AS in_catalog_never_sold
FROM products p
FULL OUTER JOIN sold s ON s.product_id = p.product_id;

-- ---------------------------------------------------------------------
-- 6) CROSS JOIN — tích Descartes (mọi cặp). Cẩn thận: bùng nổ số hàng!
--    Tạo ma trận category x channel để làm khung báo cáo
-- ---------------------------------------------------------------------
SELECT cat.category, ch.channel
FROM (SELECT DISTINCT category FROM products) cat
CROSS JOIN (SELECT DISTINCT channel FROM orders) ch
ORDER BY cat.category, ch.channel
LIMIT 6;

-- ---------------------------------------------------------------------
-- 7) SELF JOIN — join một bảng với chính nó
--    Cặp sản phẩm cùng category (p1.id < p2.id để khỏi trùng/đảo cặp)
-- ---------------------------------------------------------------------
SELECT p1.category, p1.product_name AS prod_a, p2.product_name AS prod_b
FROM products p1
JOIN products p2
  ON p1.category = p2.category
 AND p1.product_id < p2.product_id
ORDER BY p1.category, prod_a
LIMIT 5;

-- ---------------------------------------------------------------------
-- 8) ⚠️ CẠM BẪY FAN-OUT — join 1-nhiều làm nhân đôi hàng & SAI tổng
--    orders.order_id là 1, order_items nhiều dòng/đơn → SUM bị thổi phồng.
--    So sánh: tổng "đúng" (đếm đơn distinct) vs tổng "sai" (đếm sau join).
-- ---------------------------------------------------------------------
SELECT
    COUNT(DISTINCT o.order_id) AS orders_correct,   -- số đơn thật
    COUNT(o.order_id)          AS rows_after_join    -- bị nhân theo số item → lớn hơn
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id;
