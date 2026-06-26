# 14 — Indexing & Query Optimization

> Code: [`projects/03-data-modeling/01_explain_index.sql`](../projects/03-data-modeling/01_explain_index.sql)
> Chạy: `python scripts/run_sql.py projects/03-data-modeling/01_explain_index.sql`

## EXPLAIN — đọc query plan
`EXPLAIN <query>` cho biết DB **dự định** thực thi thế nào; `EXPLAIN ANALYZE` chạy thật và kèm **thời gian + số hàng** mỗi toán tử. Đọc plan **từ dưới lên** (lá → gốc).

Plan point-lookup thật (DuckDB) cho `WHERE order_id=5000`:
```
┌───────────────────────────┐
│         SEQ_SCAN          │   <- quét bảng
│      Table: orders_t      │
│          Filters:         │
│       order_id=5000       │   <- FILTER PUSHDOWN: lọc ngay trong scan
│           ~1 row          │   <- ước lượng cardinality
└───────────────────────────┘
```
Plan join + group by:
```
PROJECTION  ->  HASH_GROUP_BY (Groups #0, Aggregates sum(#1))  ->  HASH_JOIN  ->  SEQ_SCAN x2
```
Những thứ cần để ý khi đọc plan:
- **Toán tử scan**: Sequential/Seq Scan (quét toàn bộ) vs Index Scan (dùng index).
- **Filter pushdown**: điều kiện được đẩy xuống sát scan để đọc ít dữ liệu (thấy `Filters:` ngay trong SEQ_SCAN).
- **Kiểu join**: **Hash Join** (build bảng băm từ phía nhỏ, probe phía lớn) vs **Merge Join** (2 phía đã sort) vs **Nested Loop** (chậm, tránh trên dữ liệu lớn).
- **Cardinality estimate** (`~N rows`): optimizer đoán số hàng để chọn kế hoạch. Đoán sai (do thiếu statistics) → kế hoạch tệ. `ANALYZE`/cập nhật statistics giúp đoán đúng.

## Index — tăng tốc truy cập
Index là cấu trúc dữ liệu phụ giúp tìm hàng **không cần quét cả bảng**.

| Loại | Cấu trúc | Hợp cho |
|------|----------|---------|
| **B-tree** | cây cân bằng, có thứ tự | `=`, `<`, `>`, `BETWEEN`, `ORDER BY`, prefix `LIKE 'abc%'` (mặc định ở Postgres) |
| **Hash** | bảng băm | chỉ `=` (bằng), không cho range |
| **Composite** | nhiều cột `(a,b)` | filter theo `a` hoặc `a,b` — **theo thứ tự trái→phải** (left-most prefix) |
| **Partial** | index kèm `WHERE` | chỉ index phần dữ liệu quan tâm (vd `WHERE status='active'`) → nhỏ, nhanh |
| **Covering** | gồm cả cột cần `SELECT` | trả kết quả **chỉ từ index**, khỏi đọc bảng (index-only scan) |
| **Unique** | + ràng buộc duy nhất | vừa enforce unique vừa tăng tốc |

### Composite index — quy tắc left-most prefix ⭐
Index `(status, order_ts)` dùng được cho filter `status=...` và `status=... AND order_ts=...`, **nhưng không** cho filter chỉ theo `order_ts`. Thứ tự cột trong composite index rất quan trọng: đặt cột lọc bằng (`=`) trước, cột range sau.

## Khi nào index GIÚP / HẠI
✅ Giúp: point lookup, join key, cột trong `WHERE`/`ORDER BY` có **độ chọn lọc cao** (selective — ít hàng khớp), bảng lớn.
❌ Hại: 
- Mỗi index làm **chậm `INSERT/UPDATE/DELETE`** (phải cập nhật index) và tốn dung lượng.
- Cột **độ chọn lọc thấp** (vd boolean, ít giá trị) — index gần như vô dụng, optimizer vẫn seq scan.
- Bảng nhỏ — quét cả bảng còn nhanh hơn đi qua index.
- Quá nhiều index → ghi chậm, optimizer rối.

## ⭐ OLTP index vs OLAP (DuckDB)
- **OLTP (Postgres, row-store):** index B-tree là **then chốt** — truy vấn lấy vài hàng theo khoá, index tránh quét triệu hàng.
- **OLAP (DuckDB, columnar):** index ít quan trọng hơn. Engine cột dựa vào **quét cột + zonemap/min-max mỗi row group** (≈ "index vùng" tự nhiên) + nén + vectorization. Trong demo, point lookup vẫn ra `SEQ_SCAN` — columnar tối ưu cho **quét & quét lọc** chứ không cho point lookup kiểu OLTP. → Đừng bê tư duy index OLTP nguyên xi sang warehouse; ở OLAP, **partitioning, sort/clustering, file pruning** mới là đòn bẩy (xem [[09-file-formats]] predicate pushdown, [[ROADMAP]] Phase 4 Z-order).

## ✅ Tự kiểm tra
- [ ] Đọc được query plan (scan/join/filter pushdown/cardinality), từ dưới lên
- [ ] Phân biệt B-tree vs hash; hiểu composite left-most prefix
- [ ] Nêu khi nào index giúp vs hại (selectivity, chi phí ghi)
- [ ] Hiểu vì sao OLAP columnar ít cần index hơn OLTP (zonemap, pruning)

➡️ Tiếp theo: [[15-oltp-olap-acid]] — constraints, transactions, ACID, OLTP vs OLAP.
