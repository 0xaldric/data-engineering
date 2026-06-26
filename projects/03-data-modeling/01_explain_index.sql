-- =====================================================================
-- 01_explain_index.sql — EXPLAIN, query plan, indexing trên DuckDB
-- Run: python scripts/run_sql.py projects/03-data-modeling/01_explain_index.sql
-- Views có sẵn: customers, products, orders, order_items
-- Lưu ý: KHÔNG index được view -> phải materialize thành TABLE trước.
-- =====================================================================

-- 1) Materialize tables từ view (chỉ table mới tạo index được)
CREATE OR REPLACE TABLE orders_t AS SELECT * FROM orders;
CREATE OR REPLACE TABLE order_items_t AS SELECT * FROM order_items;

-- 2) EXPLAIN — xem PHYSICAL PLAN của point lookup TRƯỚC khi có index
--    (đọc từ dưới lên: SCAN -> FILTER -> PROJECTION)
EXPLAIN SELECT * FROM orders_t WHERE order_id = 5000;

-- 3) Tạo index trên khoá tra cứu
CREATE INDEX idx_orders_id ON orders_t(order_id);

-- 4) EXPLAIN ANALYZE — chạy thật + đo thời gian/sốhàng từng toán tử SAU index
EXPLAIN ANALYZE SELECT * FROM orders_t WHERE order_id = 5000;

-- 5) EXPLAIN một JOIN — quan sát HASH JOIN (build phía nhỏ, probe phía lớn)
--    và filter pushdown (status='completed' đẩy xuống sát scan)
EXPLAIN SELECT o.order_id, SUM(oi.line_total) AS rev
FROM orders_t o
JOIN order_items_t oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY o.order_id;

-- 6) Composite index (nhiều cột) — phục vụ filter theo (status, order_ts)
CREATE INDEX idx_orders_status_ts ON orders_t(status, order_ts);

-- 7) Final SELECT bình thường để runner in kết quả gọn
SELECT 'explain/index demo done' AS note,
       COUNT(*) AS n_orders,
       COUNT(DISTINCT status) AS n_status
FROM orders_t;
