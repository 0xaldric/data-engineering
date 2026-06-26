-- =====================================================================
-- 01_basics.sql — SQL Fundamentals: DDL, DML, SELECT, filtering
-- Run with: python scripts/run_sql.py projects/01-sql-fundamentals/01_basics.sql
-- The runner pre-loads parquet from data/raw/ as views: customers, products,
-- orders, order_items.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1) DDL — CREATE: materialize a real table from a view (CTAS)
--    CREATE TABLE AS SELECT is the workhorse of analytics: snapshot a query.
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE dim_customer AS
SELECT customer_id, name, email, country, city,
       CAST(signup_date AS DATE) AS signup_date,
       is_active
FROM customers;

-- DDL — ALTER: add a derived column, then backfill it with DML UPDATE
ALTER TABLE dim_customer ADD COLUMN signup_year INTEGER;
UPDATE dim_customer SET signup_year = EXTRACT(year FROM signup_date);

-- ---------------------------------------------------------------------
-- 2) Data types — DuckDB infers types; inspect them
-- ---------------------------------------------------------------------
DESCRIBE dim_customer;

-- ---------------------------------------------------------------------
-- 3) DML — INSERT / UPDATE / DELETE on a scratch table
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE scratch_orders (
    order_id   INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount     DECIMAL(10,2),
    status     VARCHAR DEFAULT 'pending'
);

INSERT INTO scratch_orders (order_id, customer_id, amount) VALUES
    (1, 10, 99.90),
    (2, 10, 15.00),
    (3, 22, 250.00);

INSERT INTO scratch_orders VALUES (4, 22, 12.50, 'completed');

-- UPDATE: mark small orders completed
UPDATE scratch_orders SET status = 'completed' WHERE amount < 100;

-- DELETE: remove cancelled-equivalent rows
DELETE FROM scratch_orders WHERE customer_id = 22 AND amount < 20;

-- ---------------------------------------------------------------------
-- 4) SELECT basics — projection, WHERE, ORDER BY, LIMIT
-- ---------------------------------------------------------------------
-- Filtering with comparison + logical operators
SELECT product_id, product_name, category, unit_price
FROM products
WHERE category = 'Electronics' AND unit_price BETWEEN 50 AND 300
ORDER BY unit_price DESC
LIMIT 5;

-- IN, LIKE, IS NULL / IS NOT NULL
SELECT customer_id, name, country
FROM customers
WHERE country IN ('VN', 'JP', 'KR')
  AND email LIKE '%gmail%'
  AND city IS NOT NULL
ORDER BY customer_id
LIMIT 5;

-- ---------------------------------------------------------------------
-- 5) DISTINCT — unique values / combinations
-- ---------------------------------------------------------------------
SELECT DISTINCT category FROM products ORDER BY category;

-- ---------------------------------------------------------------------
-- 6) Expressions, CASE, aliasing, computed columns
-- ---------------------------------------------------------------------
SELECT
    product_id,
    product_name,
    unit_price,
    unit_cost,
    ROUND(unit_price - unit_cost, 2)                       AS margin_abs,
    ROUND((unit_price - unit_cost) / unit_price * 100, 1)  AS margin_pct,
    CASE
        WHEN unit_price >= 200 THEN 'premium'
        WHEN unit_price >= 50  THEN 'mid'
        ELSE 'budget'
    END                                                    AS price_tier
FROM products
ORDER BY margin_pct DESC
LIMIT 10;

-- Final SELECT (its result is printed by the runner): a quick sanity summary
SELECT
    (SELECT COUNT(*) FROM dim_customer)   AS customers,
    (SELECT COUNT(*) FROM products)       AS products,
    (SELECT COUNT(*) FROM orders)         AS orders,
    (SELECT COUNT(*) FROM scratch_orders) AS scratch_rows_left;
