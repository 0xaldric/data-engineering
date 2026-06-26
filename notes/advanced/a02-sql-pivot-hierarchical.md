# A02 — Advanced SQL II: Pivot, Hierarchical, Dedup

> Tiếp [[a01-sql-gaps-islands]]. Pivot/unpivot, đệ quy cây/đồ thị, và các chiến lược khử trùng.

## PIVOT / UNPIVOT
**Pivot** = xoay hàng thành cột (long → wide). Cách phổ thông nhất: **conditional aggregation**.
```sql
-- doanh thu theo category (hàng) x status (cột)
select category,
  sum(case when status='completed' then line_total else 0 end) as completed,
  sum(case when status='shipped'   then line_total else 0 end) as shipped,
  sum(case when status='cancelled' then line_total else 0 end) as cancelled
from sales
group by category;
```
- Dùng `FILTER (WHERE ...)` (Postgres/DuckDB) gọn hơn CASE ([[03-sql-aggregation]]).
- Có `PIVOT`/`UNPIVOT` cú pháp riêng (DuckDB, SQL Server, Snowflake). **Pivot động** (số cột không biết trước) → phải sinh SQL bằng code/macro (dbt Jinja loop — [[25-dbt-macros]]) vì SQL thuần không tự sinh cột.
- **Unpivot** = wide → long: `UNPIVOT` hoặc `UNION ALL` từng cột thành hàng.

## Hierarchical / Recursive (cây & đồ thị)
Recursive CTE ([[05-sql-cte]]) duyệt quan hệ cha–con:
```sql
with recursive tree as (
  select id, parent_id, name, 1 as depth, name as path
  from category where parent_id is null         -- anchor: gốc
  union all
  select c.id, c.parent_id, c.name, t.depth+1, t.path || ' > ' || c.name
  from category c join tree t on c.parent_id = t.id   -- đi xuống
)
select * from tree order by path;
```
Ứng dụng: cây danh mục, org chart, BOM (bill of materials), đồ thị phụ thuộc.
- **Phát hiện chu trình**: giữ mảng `visited`, dừng nếu node lặp (tránh vòng vô hạn). Postgres có `CYCLE` clause.
- **Closure table** (lưu sẵn mọi cặp tổ tiên–con cháu) là cách tránh đệ quy lúc query khi cây ít đổi.

## ⭐ Dedup — 3 chiến lược (biết khi nào dùng cái nào)
| Cách | Khi nào | Lưu ý |
|------|---------|-------|
| `DISTINCT` | bỏ hàng **giống hệt** toàn bộ | không chọn được "giữ bản nào" |
| `GROUP BY` + agg | gộp + tính tổng hợp | đổi grain |
| `ROW_NUMBER()...WHERE rn=1` ⭐ | giữ **1 bản theo tiêu chí** (mới nhất/đúng nhất) | linh hoạt nhất, dùng nhiều trong ETL |
```sql
-- giữ bản ghi MỚI NHẤT mỗi khoá (dedup chuẩn của DE)
select * from (
  select *, row_number() over (partition by id order by updated_at desc) as rn
  from raw
) where rn = 1;
```
- `QUALIFY rn = 1` (DuckDB/Snowflake/BigQuery) gọn hơn, khỏi bọc subquery.
- Phân biệt **trùng hoàn toàn** (DISTINCT đủ) vs **trùng theo khoá nhưng khác giá trị** (cần ROW_NUMBER chọn bản đúng).

## Conditional aggregation nâng cao
- Đếm có điều kiện: `count(*) filter (where status='completed')`.
- Nhiều metric một lần quét (pivot) — đã trên.
- First/last value theo điều kiện: `max(case when rn=1 then value end)` hoặc `FIRST_VALUE() ... ignore nulls`.

## ⚠️ Cạm bẫy
- Pivot động bằng SQL thuần — không làm được, cần code sinh SQL.
- Recursive không có điều kiện dừng/anti-cycle → vòng vô hạn.
- Dùng `DISTINCT` để "sửa" fan-out join thay vì sửa grain → che giấu bug ([[02-sql-joins]]).
- `ROW_NUMBER` dedup quên `PARTITION BY` đúng khoá hoặc `ORDER BY` không xác định (tie ngẫu nhiên → kết quả không ổn định).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Pivot bằng conditional aggregation; vì sao pivot động cần code.
- [ ] Recursive CTE duyệt cây + chống chu trình.
- [ ] 3 chiến lược dedup & khi nào dùng; QUALIFY.
- 🔭 *Tự mò:* tạo bảng category cha-con nhỏ, viết recursive CTE in ra path + depth; thử thêm 1 vòng lặp (cycle) xem cần chặn thế nào.

➡️ Tiếp: [[a03-analytics-patterns]].
