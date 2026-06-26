# 🏁 Phase 0 — Tổng kết: Foundations & SQL

Hoàn thành Phase 0. Đây là nền tảng: **SQL thành thạo + môi trường + shell**. Mọi phase sau đều dựa trên đây.

## Đã làm gì (Batch #1)
| # | Chủ đề | Artifact |
|---|--------|----------|
| T001 | Cấu trúc dự án, README | `README.md` |
| T002 | Dataset e-commerce synthetic (42k rows) | `scripts/gen_ecommerce.py`, `scripts/run_sql.py` |
| T003 | SQL: DDL/DML/SELECT/filter | `01_basics.sql`, `notes/01-sql-basics.md` |
| T004 | SQL: JOINs + fan-out | `02_joins.sql`, `notes/02-sql-joins.md` |
| T005 | SQL: Aggregation/GROUP BY | `03_aggregation.sql`, `notes/03-sql-aggregation.md` |
| T006 | SQL: Window functions ⭐ | `04_window.sql`, `notes/04-sql-window.md` |
| T007 | SQL: CTE/Subquery/Set ops | `05_cte_subquery.sql`, `notes/05-sql-cte.md` |
| T008 | Shell/Linux cho DE | `scripts/explore.sh`, `notes/06-shell-for-de.md` |
| T009 | 15 bài tập SQL + lời giải | `exercises.sql`, `solutions.sql` |
| T010 | Review + smoke test | file này, `scripts/run_all.sh` |

**Kiểm chứng:** `bash scripts/run_all.sh` → regen data + 6 file SQL (58 statements) + shell = **ALL GREEN ✅**.

---

## 📑 SQL Cheat-Sheet

### Thứ tự thực thi logic (HỌC THUỘC)
```
FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → window → QUALIFY → ORDER BY → LIMIT
```
Hệ quả: alias ở SELECT **không** dùng được trong WHERE/GROUP BY/HAVING (chạy trước SELECT), **dùng được** trong ORDER BY.

### JOIN
- `INNER` = giao; `LEFT` = giữ trọn bảng trái; `FULL` = giữ cả hai; `CROSS` = mọi cặp.
- **Anti-join** tìm cái không khớp: `LEFT JOIN ... WHERE right.key IS NULL` (≈ `NOT EXISTS`).
- ⚠️ **Fan-out:** join 1-nhiều nhân hàng → `COUNT(DISTINCT)` & chỉ SUM cột đúng grain.

### Aggregation
- `WHERE` lọc hàng (trước GROUP BY) · `HAVING` lọc nhóm (sau, dùng được aggregate).
- `COUNT(*)` đếm hàng · `COUNT(col)`/`SUM`/`AVG` bỏ qua NULL.
- Conditional: `SUM(x) FILTER (WHERE cond)`.
- Đa mức: `ROLLUP` (subtotal), `GROUPING SETS` (tùy chọn).

### Window functions
```sql
func() OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN ... )
```
- Ranking: `ROW_NUMBER`(duy nhất) / `RANK`(nhảy) / `DENSE_RANK`(không nhảy) / `NTILE(n)`.
- Offset: `LAG`/`LEAD` → MoM/YoY.
- Tích lũy/trượt: `SUM/AVG OVER (ORDER BY ... ROWS BETWEEN ...)`.
- ⚠️ Ghi rõ `ROWS` (không để mặc định `RANGE`). Không `GROUP BY` trực tiếp trên window → tách CTE.
- Top-N/nhóm & dedup: `ROW_NUMBER() ... QUALIFY rn <= N` / `WHERE rn = 1`.

### CTE & Subquery
- `WITH name AS (...)` chia bước, dễ đọc (nền tảng tư duy dbt).
- `WITH RECURSIVE` cho chuỗi/cây phân cấp.
- Tồn tại → `EXISTS`/`NOT EXISTS` (KHÔNG dùng `NOT IN` nếu có NULL).
- Set ops: `UNION`(loại trùng) / `UNION ALL`(giữ) / `INTERSECT` / `EXCEPT`.

### Shell một dòng hay dùng
```bash
cut -d',' -f4 f.csv | tail -n +2 | sort | uniq -c | sort -rn      # phân phối 1 cột
awk -F',' 'NR>1{s+=$7}END{print s}' items.csv                      # tổng 1 cột
awk -F',' 'NR>1{a[$6]+=$7}END{for(k in a)print k,a[k]}' items.csv  # group-by
```

---

## ✅ Self-assessment Phase 0 (job-ready check)
- [ ] Viết được truy vấn join nhiều bảng + aggregate mà không cần tra cứu
- [ ] Giải thích fan-out và cách tránh tính sai số liệu
- [ ] Thành thạo window functions (ranking, LAG/LEAD, running total, dedup)
- [ ] Phân biệt WHERE/HAVING, hiểu thứ tự thực thi
- [ ] Refactor query phức tạp bằng CTE; biết khi nào recursive
- [ ] Tránh bẫy NULL (`IS NULL`, `NOT IN`, AVG bỏ NULL)
- [ ] Dùng shell để soi nhanh file dữ liệu

> Nếu còn ô trống → đọc lại notes tương ứng + làm lại `exercises.sql`.

## ➡️ Tiếp theo: Phase 1 — Programming for Data Engineering
Python data stack (pandas/polars), file formats (Parquet ⭐), ingestion từ API, code sạch + test. Loop sẽ sinh **Batch #2** ngay sau task này.
