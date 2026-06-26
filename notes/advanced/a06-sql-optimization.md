# A06 — SQL Performance & Query Optimization

> Viết query **đúng** là một chuyện; viết **nhanh** trên dữ liệu lớn là kỹ năng senior. Tiền đề [[14-indexing]].

## Quy trình tối ưu một query chậm
1. **Đo**: `EXPLAIN ANALYZE` — tìm toán tử tốn nhất (full scan lớn, sort/hash spill, nested loop, cardinality estimate sai).
2. **Giảm dữ liệu sớm**: lọc & chọn cột trước khi join/aggregate.
3. **Đúng index / partition** cho cột lọc & join.
4. **Rewrite** nếu plan tệ (đổi cấu trúc query, tránh anti-pattern).
5. **Đo lại**.

## ⭐ Sargable predicates (dùng được index)
"SARGable" = Search ARGument able — điều kiện cho phép DB dùng index. **Đừng bọc hàm quanh cột lọc**:
```sql
-- ❌ không sargable: function trên cột -> bỏ qua index, full scan
where year(order_ts) = 2024
where lower(email) = 'a@x.com'
where amount * 1.1 > 100

-- ✅ sargable: để cột "trần", biến đổi sang vế phải
where order_ts >= '2024-01-01' and order_ts < '2025-01-01'
where email = 'a@x.com'                  -- (hoặc index trên lower(email))
where amount > 100/1.1
```
Nguyên tắc: **cột một bên, biến đổi bên kia**. (Hoặc tạo index biểu thức / cột tính sẵn.)

## Anti-patterns hay gặp
| Anti-pattern | Vấn đề | Thay bằng |
|--------------|--------|-----------|
| `SELECT *` | đọc thừa cột (đắt với columnar — [[09-file-formats]]) | chọn đúng cột |
| `function(col)` trong WHERE | mất index | sargable / index biểu thức |
| `NOT IN (subquery có NULL)` | trả rỗng âm thầm | `NOT EXISTS` / anti-join ([[02-sql-joins]]) |
| `OR` trên cột khác nhau | khó dùng index | `UNION ALL` 2 nhánh, hoặc `IN` |
| `DISTINCT` để "sửa" fan-out | che bug + sort đắt | sửa grain/join ([[02-sql-joins]]) |
| Correlated subquery chạy mỗi hàng | chậm | JOIN / window |
| `COUNT(DISTINCT)` trên dữ liệu lớn | tốn RAM/shuffle | approx (`approx_count_distinct`) nếu chấp nhận sai số |
| Join rồi mới filter | shuffle/đọc nhiều | filter trước (predicate pushdown) |

## Join optimization
- **Lọc trước khi join**, chọn cột cần.
- Bảng nhỏ + bảng lớn → DB (hoặc Spark) **broadcast** bảng nhỏ ([[32-joins-catalyst]]).
- Join key nên có **index** (OLTP) / cùng phân vùng (OLAP).
- Tránh **fan-out** ngoài ý muốn (kiểm grain) — [[02-sql-joins]].
- Thứ tự join: optimizer thường tự lo (CBO), nhưng cần **statistics** cập nhật (`ANALYZE`).

## CTE vs Subquery vs Temp table
- **CTE** chủ yếu để **đọc rõ**; ở vài DB cũ là "optimization fence" (vật chất hoá, không đẩy filter vào trong) → có thể chậm. Postgres ≥12 thường inline.
- **Temp table / vật chất hoá**: hữu ích khi một kết quả trung gian **dùng lại nhiều lần** & nặng (tính 1 lần). Đánh đổi: tốn ghi.
- Hiểu DB của bạn xử lý CTE thế nào (đọc plan) trước khi kết luận.

## OLAP-specific (warehouse/lakehouse)
- **Partition pruning** + **predicate pushdown**: lọc theo cột partition để quét ít file ([[31-partitioning-shuffle]], [[09-file-formats]]).
- **Columnar**: chọn ít cột; tránh `SELECT *`.
- **Bytes scanned = tiền** (Athena/BigQuery) → tối ưu = tiết kiệm chi phí ([[59-cost-finops]]).
- **Materialization** hợp lý (table vs view vs incremental — [[23-dbt-marts]], [[27-dbt-incremental]]).
- **Z-order/clustering** gom giá trị gần nhau để data-skipping ([[34-delta-lake]]).

## Đọc EXPLAIN — checklist
- Toán tử scan: index scan (tốt) vs seq/full scan (xem có nên không).
- `Filters:` đã pushdown chưa.
- Join type: hash/broadcast (ok) vs nested loop (cẩn thận trên dữ liệu lớn).
- `rows` ước lượng vs thực tế lệch nhiều → statistics cũ → `ANALYZE`.
- Sort/aggregate có **spill** (disk) → tăng RAM/giảm dữ liệu.

## ⚠️ Cạm bẫy
- Tối ưu mò mà không `EXPLAIN` (đoán sai chỗ nghẽn).
- Thêm index vô tội vạ → chậm ghi ([[14-indexing]]).
- Tối ưu query chạy 1 lần/tháng (phí công — [[59-cost-finops]]).
- Quên cập nhật statistics → optimizer chọn plan tệ.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Sargable là gì; viết lại `year(ts)=2024` cho sargable.
- [ ] Kể 5 anti-pattern + cách thay.
- [ ] Khi nào CTE/temp giúp; OLAP pruning/pushdown.
- [ ] Đọc EXPLAIN tìm nghẽn (scan/join/spill/cardinality).
- 🔭 *Tự mò:* trên DuckDB, `EXPLAIN ANALYZE` một query join+groupby; thử thêm `WHERE year(order_ts)=2024` vs `order_ts >= '2024-01-01'` xem plan/đo khác nhau.

➡️ Tiếp: [[a07-sql-qa]].
