# 05 — CTEs, Subqueries & Set Operations

> Code: [`projects/01-sql-fundamentals/05_cte_subquery.sql`](../projects/01-sql-fundamentals/05_cte_subquery.sql)
> Chạy: `python scripts/run_sql.py projects/01-sql-fundamentals/05_cte_subquery.sql`

## CTE (Common Table Expression) — `WITH`
Đặt tên cho một query con để tái sử dụng và đọc **từ trên xuống** thay vì lồng nhau khó hiểu.

```sql
WITH order_value AS ( ... ),       -- bước 1
     customer_stats AS ( ... )      -- bước 2 (dùng được kết quả bước 1)
SELECT ... FROM customer_stats ...; -- bước cuối
```

**Vì sao DE thích CTE:**
- Chia logic phức tạp thành các bước có tên → dễ đọc, dễ debug (chạy thử từng CTE).
- Đây là **tư duy nền tảng của dbt**: mỗi model là một tầng transform có tên (staging → intermediate → marts) — chính là CTE ở quy mô file. Xem [[03-sql-aggregation]] → Phase 3 dbt.
- ⚠️ CTE **không** tự động nhanh hơn subquery. Ở vài DB (Postgres < 12) CTE là "optimization fence" (vật chất hóa, không đẩy filter vào trong). Hiểu rõ DB của bạn; CTE chủ yếu để **dễ đọc**.

## Recursive CTE — `WITH RECURSIVE`
Cho phép CTE tự tham chiếu → lặp. Cấu trúc luôn 2 phần nối bằng `UNION ALL`:
```
anchor  (hàng khởi đầu)
UNION ALL
recursive  (sinh hàng mới từ kết quả vòng trước, đến khi rỗng thì dừng)
```
Hai ứng dụng kinh điển:
1. **Sinh chuỗi** (calendar ngày/tháng) khi không có bảng date — rất hay dùng để "fill gap" cho time series.
2. **Duyệt cây phân cấp** (org chart, danh mục cha-con, BOM): theo dõi `level` và `path` khi đi xuống. Nhớ có điều kiện dừng, kẻo lặp vô hạn.

## Subquery — query lồng trong query
| Loại | Đặc điểm | Ví dụ |
|------|----------|-------|
| **Scalar** | trả đúng **1 giá trị** | `(SELECT AVG(price) FROM products)` |
| **Trong IN** | trả 1 cột nhiều hàng | `WHERE id IN (SELECT ...)` |
| **Correlated** | tham chiếu hàng ngoài, chạy **lặp lại mỗi hàng** | `WHERE price = (SELECT MAX(p2.price) FROM products p2 WHERE p2.category = p.category)` |
| **Derived table** | subquery trong FROM | `FROM (SELECT ...) t` |

**Correlated** mạnh nhưng có thể chậm (lặp theo từng hàng ngoài) — nhiều khi viết lại bằng window function hoặc join sẽ nhanh hơn.

## IN vs EXISTS vs JOIN
- `IN (SELECT ...)` — gọn cho tập nhỏ.
- `EXISTS (SELECT 1 ...)` — dừng ngay khi thấy 1 hàng khớp; thường **nhanh hơn** trên tập lớn.
- ⚠️ **`NOT IN` + NULL = cạm bẫy:** nếu subquery của `NOT IN` chứa dù chỉ một `NULL`, **toàn bộ** kết quả ra rỗng (vì `x <> NULL` là unknown). Dùng `NOT EXISTS` hoặc anti-join (LEFT JOIN ... IS NULL, xem [[02-sql-joins]]) thay cho `NOT IN` để an toàn.

## Set Operations — ghép theo chiều dọc
Yêu cầu các SELECT có **cùng số cột, kiểu tương thích**:
| Phép | Ý nghĩa |
|------|---------|
| `UNION` | hợp, **loại trùng** (tốn sort/hash) |
| `UNION ALL` | hợp, **giữ trùng** (nhanh hơn — mặc định nên dùng nếu chắc không trùng) |
| `INTERSECT` | giao (có ở cả hai) |
| `EXCEPT` (MINUS) | hiệu (ở A nhưng không ở B) |

`INTERSECT`/`EXCEPT` rất tiện để **so sánh 2 tập** (đối chiếu dữ liệu, kiểm thử migration: tập cũ `EXCEPT` tập mới phải rỗng).

## Khi nào dùng cái nào? (tóm tắt)
- Logic nhiều bước, cần đọc rõ → **CTE**.
- Phân cấp / chuỗi sinh ra → **recursive CTE**.
- Một giá trị tham chiếu → **scalar subquery**.
- Kiểm tra tồn tại / không tồn tại → **EXISTS / NOT EXISTS** (không phải NOT IN).
- Ghép/đối chiếu tập → **set operations**.

## ✅ Tự kiểm tra
- [ ] Refactor được query lồng 3 tầng thành CTE dễ đọc
- [ ] Viết được recursive CTE cho calendar và cho cây phân cấp
- [ ] Phân biệt scalar vs correlated subquery
- [ ] Giải thích bẫy `NOT IN` + NULL và cách thay bằng `NOT EXISTS`
- [ ] Biết `UNION` vs `UNION ALL` khác nhau ở đâu (hiệu năng)

➡️ Tiếp theo: [[06-shell-for-de]] — Shell/Linux cho Data Engineering.
