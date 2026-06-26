# 01 — SQL Fundamentals: DDL, DML, SELECT, Filtering

> Code đi kèm: [`projects/01-sql-fundamentals/01_basics.sql`](../projects/01-sql-fundamentals/01_basics.sql)
> Chạy: `python scripts/run_sql.py projects/01-sql-fundamentals/01_basics.sql`

## SQL chia làm mấy nhóm lệnh?

| Nhóm | Viết tắt | Lệnh | Mục đích |
|------|----------|------|----------|
| Data Definition | **DDL** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | Định nghĩa/đổi cấu trúc bảng |
| Data Manipulation | **DML** | `INSERT`, `UPDATE`, `DELETE`, `MERGE` | Thay đổi *dữ liệu* trong bảng |
| Data Query | **DQL** | `SELECT` | Đọc dữ liệu |
| Data Control | **DCL** | `GRANT`, `REVOKE` | Phân quyền |
| Transaction Control | **TCL** | `COMMIT`, `ROLLBACK` | Quản lý transaction |

Data Engineer dùng nhiều nhất: **SELECT** (đọc & transform) và **DDL/DML** dạng `CREATE TABLE AS SELECT` (CTAS).

## 1) DDL

```sql
CREATE OR REPLACE TABLE dim_customer AS   -- CTAS: tạo bảng từ kết quả query
SELECT customer_id, name, ... FROM customers;

ALTER TABLE dim_customer ADD COLUMN signup_year INTEGER;
DROP TABLE IF EXISTS scratch;
```

- **CTAS** (`CREATE TABLE AS SELECT`) là pattern quan trọng nhất trong analytics/ETL: "đông cứng" kết quả một query thành bảng vật lý để query sau nhanh hơn. Toàn bộ warehouse build theo kiểu này (staging → core → marts).
- `CREATE OR REPLACE` giúp script **idempotent** — chạy lại nhiều lần không lỗi "table already exists". Rất quan trọng cho pipeline (xem [[01-sql-basics]] → orchestration sau này).

## 2) Data types (kiểu dữ liệu)

Nhóm chính: số nguyên (`INTEGER`, `BIGINT`), số thực (`DOUBLE`, **`DECIMAL(p,s)`** cho tiền — không bao giờ dùng float cho tiền vì sai số làm tròn!), chuỗi (`VARCHAR`), ngày/giờ (`DATE`, `TIMESTAMP`), boolean. Xem cấu trúc bảng bằng `DESCRIBE ten_bang;`.

## 3) DML

```sql
INSERT INTO scratch_orders (order_id, customer_id, amount) VALUES (1, 10, 99.90);
UPDATE scratch_orders SET status = 'completed' WHERE amount < 100;
DELETE FROM scratch_orders WHERE customer_id = 22 AND amount < 20;
```

⚠️ **`UPDATE`/`DELETE` không có `WHERE` sẽ tác động TOÀN BỘ bảng.** Luôn `SELECT` ra trước để kiểm tra điều kiện, rồi mới `UPDATE/DELETE`.

## 4) SELECT — thứ tự logic của câu query

SQL **viết** theo thứ tự `SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT`, nhưng **thực thi** theo thứ tự khác:

```
FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```

Hệ quả quan trọng: vì `WHERE` chạy **trước** `SELECT`, ta **không** dùng được alias đặt ở `SELECT` trong `WHERE`. Còn `ORDER BY` chạy sau `SELECT` nên **dùng được** alias.

### Toán tử filter hay dùng
- So sánh: `= <> < <= > >=`
- Logic: `AND OR NOT`
- `BETWEEN a AND b` (bao gồm 2 đầu)
- `IN (...)` — thuộc tập giá trị
- `LIKE '%abc%'` — khớp mẫu (`%` = nhiều ký tự, `_` = 1 ký tự)
- `IS NULL` / `IS NOT NULL` — **bắt buộc** dùng `IS`, không dùng `= NULL` (vì `NULL = NULL` cho ra `NULL`/unknown, không phải `TRUE`)

### NULL — cạm bẫy kinh điển
NULL nghĩa là "không biết". Mọi phép tính với NULL ra NULL. `WHERE col = NULL` luôn rỗng. Dùng `IS NULL`, hoặc `COALESCE(col, default)` để thay giá trị mặc định.

## 5) DISTINCT
`SELECT DISTINCT category FROM products` — loại trùng. `DISTINCT` áp dụng cho *toàn bộ* danh sách cột được chọn, không phải một cột.

## 6) Biểu thức & CASE
```sql
CASE WHEN unit_price >= 200 THEN 'premium'
     WHEN unit_price >= 50  THEN 'mid'
     ELSE 'budget' END AS price_tier
```
`CASE` là "if-else" của SQL — dùng để phân loại, pivot thủ công, xử lý logic có điều kiện. Alias bằng `AS`.

## ✅ Tự kiểm tra
- [ ] Phân biệt được DDL vs DML vs DQL
- [ ] Hiểu CTAS và vì sao `CREATE OR REPLACE` giúp idempotent
- [ ] Giải thích được thứ tự thực thi logic và vì sao alias không dùng được trong WHERE
- [ ] Tránh được bẫy NULL (`IS NULL` vs `= NULL`)
- [ ] Biết vì sao tiền dùng `DECIMAL` chứ không `FLOAT`

➡️ Tiếp theo: [[02-sql-joins]] — kết hợp nhiều bảng.
