-- =====================================================================
-- 03_normalization.sql — Chuẩn hoá 1NF -> 2NF -> 3NF (lossless)
-- Run: python scripts/run_sql.py projects/03-data-modeling/03_normalization.sql
-- Dùng dữ liệu nhỏ tự tạo để thấy rõ redundancy & anomaly.
-- =====================================================================

-- ---------------------------------------------------------------------
-- Bảng "phẳng" nhiều dư thừa. PK = (order_id, product_id).
-- Functional dependencies (FD):
--   order_id          -> order_date, customer_id
--   customer_id       -> customer_name, customer_city
--   customer_city     -> city_country          (TRANSITIVE!)
--   product_id        -> product_name, category, unit_price
--   (order_id,product_id) -> quantity
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE flat_orders AS
SELECT * FROM (VALUES
  (1, DATE '2024-01-05', 10, 'An',   'Hanoi', 'VN', 100, 'Book', 'Media',  12.0, 2),
  (1, DATE '2024-01-05', 10, 'An',   'Hanoi', 'VN', 200, 'Pen',  'Office',  3.0, 5),
  (2, DATE '2024-01-06', 10, 'An',   'Hanoi', 'VN', 100, 'Book', 'Media',  12.0, 1),
  (3, DATE '2024-01-07', 20, 'Binh', 'Hue',   'VN', 300, 'Mug',  'Home',    8.0, 3)
) AS t(order_id, order_date, customer_id, customer_name, customer_city, city_country,
       product_id, product_name, category, unit_price, quantity);

-- Redundancy: thông tin khách 'An'/'Hanoi'/'VN' lặp lại nhiều dòng.
-- => UPDATE anomaly: An đổi thành phố phải sửa nhiều dòng, sót 1 dòng -> mâu thuẫn.
-- => INSERT anomaly: không thể thêm khách/sản phẩm mới nếu chưa có đơn (thiếu PK).
-- => DELETE anomaly: xoá đơn cuối của Binh -> mất luôn thông tin khách Binh.
SELECT customer_name, customer_city, city_country, COUNT(*) AS so_dong_lap
FROM flat_orders
GROUP BY customer_name, customer_city, city_country
ORDER BY so_dong_lap DESC;

-- ---------------------------------------------------------------------
-- 1NF: giá trị nguyên tử, không nhóm lặp. Bảng trên ĐÃ ở 1NF
-- (mỗi dòng 1 sản phẩm/đơn; không có cột kiểu "A,B,C").
-- ---------------------------------------------------------------------

-- ---------------------------------------------------------------------
-- 2NF: loại PHỤ THUỘC BỘ PHẬN vào khoá tổng hợp (order_id, product_id).
--   - customer_*, order_date phụ thuộc order_id (một phần khoá) -> tách ra
--   - product_*, unit_price phụ thuộc product_id (một phần khoá) -> tách ra
--   - quantity phụ thuộc CẢ khoá -> ở lại bảng order_lines
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE orders2 AS          -- vẫn còn customer_* (chưa 3NF)
SELECT DISTINCT order_id, order_date, customer_id,
       customer_name, customer_city, city_country
FROM flat_orders;

CREATE OR REPLACE TABLE products2 AS
SELECT DISTINCT product_id, product_name, category, unit_price FROM flat_orders;

CREATE OR REPLACE TABLE order_lines AS
SELECT order_id, product_id, quantity FROM flat_orders;

-- ---------------------------------------------------------------------
-- 3NF: loại PHỤ THUỘC BẮC CẦU (non-key -> non-key).
--   orders2: customer_id -> customer_name, customer_city -> city_country
--   => tách customer ra bảng riêng; city -> country tách tiếp.
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE customers3 AS
SELECT DISTINCT customer_id, customer_name, customer_city FROM orders2;

CREATE OR REPLACE TABLE cities3 AS         -- customer_city -> country (bắc cầu)
SELECT DISTINCT customer_city AS city, city_country AS country FROM orders2;

CREATE OR REPLACE TABLE orders3 AS          -- chỉ còn FK, hết phụ thuộc bắc cầu
SELECT DISTINCT order_id, order_date, customer_id FROM orders2;

-- ---------------------------------------------------------------------
-- LOSSLESS CHECK: join các bảng 3NF lại phải tái tạo ĐÚNG flat_orders
-- (không mất, không thừa hàng).
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE reconstructed AS
SELECT o.order_id, o.order_date, c.customer_id, c.customer_name,
       c.customer_city, ci.country AS city_country,
       p.product_id, p.product_name, p.category, p.unit_price, ol.quantity
FROM orders3 o
JOIN order_lines ol ON ol.order_id = o.order_id
JOIN products2  p  ON p.product_id = ol.product_id
JOIN customers3 c  ON c.customer_id = o.customer_id
JOIN cities3    ci ON ci.city = c.customer_city;

SELECT
  (SELECT COUNT(*) FROM flat_orders)    AS flat_rows,
  (SELECT COUNT(*) FROM reconstructed)  AS recon_rows,
  (SELECT COUNT(*) FROM (SELECT * FROM flat_orders EXCEPT SELECT * FROM reconstructed)) AS diff_rows,
  (SELECT COUNT(*) FROM customers3)     AS customers_unique;  -- 'An' giờ chỉ còn 1 dòng
