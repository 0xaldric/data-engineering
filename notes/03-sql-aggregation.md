# 03 — Aggregation & GROUP BY

> Code: [`projects/01-sql-fundamentals/03_aggregation.sql`](../projects/01-sql-fundamentals/03_aggregation.sql)
> Chạy: `python scripts/run_sql.py projects/01-sql-fundamentals/03_aggregation.sql`

Aggregation = gộp nhiều hàng thành một giá trị tóm tắt. Là trái tim của mọi báo cáo/analytics.

## Hàm aggregate cơ bản
| Hàm | Ý nghĩa | Bỏ qua NULL? |
|-----|---------|--------------|
| `COUNT(*)` | đếm **hàng** | không (đếm cả hàng có NULL) |
| `COUNT(col)` | đếm giá trị **không NULL** của cột | có |
| `COUNT(DISTINCT col)` | đếm giá trị **khác nhau** | có |
| `SUM / AVG / MIN / MAX(col)` | tổng / trung bình / nhỏ / lớn nhất | có |

⭐ **NULL trong aggregate** là điểm hay sai:
- `AVG(col)` chia cho số phần tử **không NULL**, không phải tổng số hàng → khác với `SUM(col)/COUNT(*)`.
- `COUNT(*)` ≠ `COUNT(col)` khi cột có NULL.
- `SUM` của toàn NULL ra `NULL` (không phải 0). Dùng `COALESCE(SUM(col), 0)` nếu cần 0.

## GROUP BY
Chia hàng thành nhóm theo (các) cột, rồi tính aggregate **trên từng nhóm**.

**Quy tắc vàng:** mọi cột trong `SELECT` mà không nằm trong hàm aggregate thì **bắt buộc** phải có trong `GROUP BY`. (Postgres báo lỗi nếu vi phạm; vài DB cho qua nhưng ra kết quả khó lường.)

```sql
SELECT p.category, SUM(oi.line_total) AS revenue
FROM ... GROUP BY p.category;   -- category phải có trong GROUP BY
```

GROUP BY theo thời gian dùng `date_trunc('month', ts)` để gom theo tháng/tuần/ngày.

## WHERE vs HAVING ⭐ (câu hỏi phỏng vấn kinh điển)
| | WHERE | HAVING |
|--|-------|--------|
| Lọc cái gì | từng **hàng thô** | từng **nhóm** sau khi gộp |
| Chạy khi nào | **trước** GROUP BY | **sau** GROUP BY |
| Dùng được aggregate? | ❌ không | ✅ có (`HAVING SUM(...) > 1000`) |

Nhớ thứ tự thực thi: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`.
→ Lọc hàng (status, ngày...) đưa vào `WHERE` để **giảm dữ liệu sớm** (nhanh hơn); chỉ điều kiện trên kết quả aggregate mới để `HAVING`.

## FILTER — conditional aggregation (rất mạnh)
Tính nhiều "lát cắt" trong **một** lần quét, không cần join/subquery nhiều lần:
```sql
SUM(line_total) FILTER (WHERE status = 'completed') AS rev_completed,
SUM(line_total) FILTER (WHERE status = 'cancelled') AS rev_cancelled
```
Tương đương cũ: `SUM(CASE WHEN status='completed' THEN line_total END)`. `FILTER` gọn và rõ hơn. Đây là cách "pivot" dữ liệu phổ biến nhất trong analytics.

## ROLLUP / CUBE / GROUPING SETS — đa mức tổng hợp
Sinh nhiều mức tổng trong một query (đỡ phải UNION nhiều câu):
- `ROLLUP(a, b)` → các mức: `(a,b)`, `(a)`, `()`. Dùng cho **subtotal phân cấp** + grand total. Hàng subtotal có `NULL` ở cột bị gộp.
- `CUBE(a, b)` → **mọi** tổ hợp: `(a,b)`, `(a)`, `(b)`, `()`.
- `GROUPING SETS((a),(b))` → chỉ đúng các mức bạn liệt kê (linh hoạt nhất).

Dùng `GROUPING(col)` hoặc `ORDER BY col NULLS LAST` để phân biệt/ sắp dòng subtotal.

## Bài toán "% trên tổng" (teaser window function)
```sql
100.0 * SUM(line_total) / SUM(SUM(line_total)) OVER () AS pct_of_total
```
`SUM(...) OVER ()` là window function chạy **sau** GROUP BY, cho mẫu số = tổng toàn bảng. Sẽ học kỹ ở [[04-sql-window]].

## ✅ Tự kiểm tra
- [ ] Giải thích WHERE vs HAVING và thứ tự thực thi
- [ ] Phân biệt `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`
- [ ] Biết AVG bỏ qua NULL (khác SUM/COUNT(*))
- [ ] Viết được conditional aggregation bằng `FILTER`
- [ ] Hiểu ROLLUP sinh subtotal thế nào

➡️ Tiếp theo: [[04-sql-window]] — Window functions (phần "ăn tiền" nhất của SQL).
