# 04 — Window Functions ⭐

> Code: [`projects/01-sql-fundamentals/04_window.sql`](../projects/01-sql-fundamentals/04_window.sql)
> Chạy: `python scripts/run_sql.py projects/01-sql-fundamentals/04_window.sql`

**Window function** tính toán trên một "cửa sổ" các hàng liên quan **nhưng vẫn giữ nguyên từng hàng** — khác hẳn `GROUP BY` (gộp lại làm mất chi tiết). Đây là kỹ năng SQL phân biệt người mới với người giỏi, và bị hỏi rất nhiều khi phỏng vấn DE.

## Cú pháp
```
func() OVER (
    PARTITION BY <cột chia nhóm>   -- tùy chọn: reset window theo nhóm
    ORDER BY <cột sắp xếp>          -- tùy chọn: thứ tự trong window
    <frame>                        -- tùy chọn: ROWS/RANGE BETWEEN ... AND ...
)
```
- **PARTITION BY** — chia dữ liệu thành các nhóm độc lập (như GROUP BY nhưng không gộp hàng). Bỏ qua = cả bảng là 1 window.
- **ORDER BY** (trong OVER) — sắp thứ tự để tính ranking, LAG/LEAD, running total.
- **frame** — giới hạn tập hàng tính aggregate quanh hàng hiện tại.

## Các nhóm hàm

### 1. Ranking
| Hàm | Hành vi khi trùng giá trị |
|-----|---------------------------|
| `ROW_NUMBER()` | đánh số duy nhất 1,2,3,4 (trùng vẫn khác số) |
| `RANK()` | trùng cùng hạng, **nhảy số**: 1,1,3,4 |
| `DENSE_RANK()` | trùng cùng hạng, **không nhảy**: 1,1,2,3 |
| `NTILE(n)` | chia đều thành n nhóm (quartile, decile...) |

Pattern **top-N mỗi nhóm**: `ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC)` rồi lọc `<= 3`. DuckDB/Snowflake có `QUALIFY` để lọc trực tiếp trên window func; DB khác phải bọc subquery/CTE.

### 2. Offset: LAG / LEAD
Lấy giá trị hàng **trước** (`LAG`) / **sau** (`LEAD`) theo ORDER BY → tính so sánh kỳ trước:
```sql
revenue - LAG(revenue) OVER (ORDER BY month)   -- chênh lệch so tháng trước (MoM)
```
Dùng cho: tăng trưởng MoM/YoY, phát hiện thay đổi, tính khoảng cách giữa các sự kiện.

### 3. Aggregate dạng window: SUM/AVG/COUNT/MIN/MAX OVER
- **Không** có ORDER BY → áp cho **cả partition** (vd % của nhóm: `revenue / SUM(revenue) OVER (PARTITION BY category)`).
- **Có** ORDER BY + frame → tích lũy (running total) hoặc trượt (moving average).

## ⭐ Frame clause — điểm hay sai nhất
Frame xác định "cửa sổ" hàng tính aggregate quanh hàng hiện tại:
```
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW   -- từ đầu → hiện tại = running total
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW           -- 3 hàng = moving average 3 kỳ
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING    -- hiện tại → cuối
```

**Bẫy ngầm:** khi có `ORDER BY` mà **không ghi frame**, mặc định là `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. Với giá trị ORDER BY trùng nhau, `RANGE` gộp **tất cả hàng cùng giá trị** vào một bậc → running total nhảy cục, sai với kỳ vọng. → Khi làm running total/moving average hãy **ghi rõ `ROWS`** thay vì để mặc định RANGE.

## ⚠️ Không GROUP BY trực tiếp trên window function
Window func chạy **sau** `GROUP BY` ở **cùng cấp** query. Muốn gộp theo kết quả window (vd đếm khách mỗi quartile của `NTILE`) phải tính window ở **CTE/subquery riêng** rồi mới GROUP BY ở tầng ngoài. (Đây chính là lỗi đã gặp khi viết bài này.)

Thứ tự thực thi: `... GROUP BY → HAVING → window functions → SELECT/QUALIFY → ORDER BY`.

## Ứng dụng thực tế trong Data Engineering
- **Deduplication** (cực phổ biến trong ETL): giữ 1 bản ghi "mới nhất"/"đúng nhất" mỗi khóa:
  ```sql
  ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) ... WHERE rn = 1
  ```
  Dùng để xử lý dữ liệu trùng từ nguồn, lấy snapshot mới nhất, làm SCD.
- **Sessionization**: dùng LAG để đo khoảng cách thời gian giữa các event, đánh dấu session mới.
- **Running metrics**: tồn kho lũy kế, doanh thu cộng dồn, retention.
- **Top-N per group**: sản phẩm bán chạy nhất mỗi danh mục/khu vực.

## ✅ Tự kiểm tra
- [ ] Phân biệt ROW_NUMBER vs RANK vs DENSE_RANK (hành vi khi trùng)
- [ ] Viết được top-3 mỗi nhóm bằng ROW_NUMBER + lọc
- [ ] Dùng LAG để tính tăng trưởng MoM
- [ ] Giải thích `ROWS` vs `RANGE` và vì sao nên ghi rõ frame
- [ ] Biết vì sao không GROUP BY trực tiếp trên window func
- [ ] Viết được dedup pattern (ROW_NUMBER ... WHERE rn = 1)

➡️ Tiếp theo: [[05-sql-cte]] — CTEs, subqueries, set operations.
