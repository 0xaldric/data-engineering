# A07 — SQL Conceptual Q&A (interview)

> 20+ câu hỏi phỏng vấn SQL hay gặp + **trả lời ngắn gọn chuẩn**. Dùng để ôn nhanh. Link tới note chi tiết.

## Cơ bản & ngữ nghĩa
**Q: Thứ tự thực thi logic của câu SELECT?**
A: `FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → window → ORDER BY → LIMIT`. Hệ quả: alias ở SELECT không dùng được trong WHERE/GROUP BY (chạy trước), dùng được trong ORDER BY. ([[01-sql-basics]])

**Q: WHERE vs HAVING?**
A: WHERE lọc **hàng thô trước** GROUP BY (không dùng aggregate); HAVING lọc **nhóm sau** GROUP BY (dùng được aggregate). ([[03-sql-aggregation]])

**Q: Các loại JOIN?**
A: INNER (giao), LEFT/RIGHT (giữ trọn một bên), FULL (cả hai), CROSS (tích Descartes), SELF (bảng với chính nó). Anti-join = LEFT + `IS NULL`. ([[02-sql-joins]])

**Q: NULL hành xử thế nào?**
A: NULL = "không biết". Mọi phép tính với NULL ra NULL; `= NULL` luôn unknown → dùng `IS NULL`. Aggregate (SUM/AVG/COUNT(col)) **bỏ qua** NULL; `COUNT(*)` thì không. ([[01-sql-basics]])

**Q: UNION vs UNION ALL?**
A: UNION loại trùng (tốn sort/hash); UNION ALL giữ trùng (nhanh hơn, mặc định nên dùng nếu chắc không trùng).

## Window & aggregation
**Q: Window function vs GROUP BY?**
A: GROUP BY gộp hàng (mất chi tiết); window tính trên "cửa sổ" nhưng **giữ từng hàng**. ([[04-sql-window]])

**Q: ROW_NUMBER vs RANK vs DENSE_RANK?**
A: Khi trùng giá trị: ROW_NUMBER đánh số duy nhất (1,2,3,4); RANK nhảy số (1,1,3,4); DENSE_RANK không nhảy (1,1,2,3).

**Q: ROWS vs RANGE trong frame?**
A: ROWS theo số hàng vật lý; RANGE theo giá trị order-by (gộp ties). Mặc định có ORDER BY mà không ghi frame = RANGE → running total có thể sai với ties → **ghi rõ ROWS**. ([[a01-sql-gaps-islands]])

**Q: Lọc trên kết quả window thế nào?**
A: Không lọc được trong WHERE (window chạy sau WHERE); bọc subquery/CTE rồi lọc, hoặc dùng `QUALIFY` (DuckDB/Snowflake/BigQuery).

## Modeling & database
**Q: OLTP vs OLAP?**
A: OLTP = vận hành (row-store, 3NF, point read/write nhỏ); OLAP = phân tích (column-store, denormalized/star, quét lớn). ([[15-oltp-olap-acid]])

**Q: Normalization 3NF?**
A: 1NF (nguyên tử) → 2NF (hết phụ thuộc bộ phận vào khoá tổng hợp) → 3NF (hết phụ thuộc bắc cầu non-key→non-key). OLAP cố tình denormalize để đọc nhanh. ([[16-normalization]])

**Q: Star schema? Surrogate key?**
A: Fact (measures + FK) ở giữa, dimension (thuộc tính mô tả) xung quanh; denormalized, ít join. Surrogate key = khoá thay thế vô nghĩa, cần cho SCD2. ([[17-dimensional-modeling]])

**Q: SCD Type 2?**
A: Giữ lịch sử bằng cách thêm dòng phiên bản mới + `effective_from/to` + `is_current`, mỗi phiên bản 1 surrogate key. ([[18-scd]])

**Q: Index — khi nào giúp/hại?**
A: Giúp: point lookup, join key, cột lọc selective, bảng lớn. Hại: chậm ghi (INSERT/UPDATE), cột ít selective, bảng nhỏ. B-tree cho range+equality, hash chỉ equality. ([[14-indexing]])

**Q: ACID?**
A: Atomicity (all-or-nothing), Consistency (giữ ràng buộc), Isolation (TX đồng thời không giẫm nhau), Durability (đã commit là bền). ([[15-oltp-olap-acid]])

## Nâng cao
**Q: Recursive CTE để làm gì?**
A: Duyệt phân cấp (cây/đồ thị) hoặc sinh chuỗi (calendar); cấu trúc anchor + UNION ALL + recursive, có điều kiện dừng/anti-cycle. ([[05-sql-cte]], [[a02-sql-pivot-hierarchical]])

**Q: NOT IN nguy hiểm khi nào?**
A: Khi subquery chứa NULL → toàn bộ kết quả rỗng (vì `x <> NULL` là unknown). Dùng `NOT EXISTS`/anti-join. ([[02-sql-joins]])

**Q: Sargable predicate?**
A: Điều kiện cho phép dùng index — không bọc hàm quanh cột lọc (`year(ts)=2024` ❌ → `ts >= '2024-01-01'` ✅). ([[a06-sql-optimization]])

**Q: Dedup giữ bản mới nhất?**
A: `ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC) ... WHERE rn=1`. ([[a02-sql-pivot-hierarchical]])

**Q: Tính median trong SQL?**
A: `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)`; hoặc trick window lấy hàng giữa. ([[a04-sql-interview-1]])

**Q: Tìm top-N mỗi nhóm?**
A: `ROW_NUMBER() PARTITION BY group ORDER BY metric DESC` rồi lọc `rn<=N` (hoặc QUALIFY).

**Q: CTE có làm query nhanh hơn không?**
A: Không nhất thiết — chủ yếu để **dễ đọc**. Ở vài DB là optimization fence (vật chất hoá). Hiểu DB của bạn qua EXPLAIN. ([[a06-sql-optimization]])

## ✅ Tự kiểm tra & "tự mò"
- [ ] Trả lời trôi chảy 20 câu trên (không nhìn đáp án).
- [ ] Câu nào chưa chắc → mở note link tới đọc sâu.
- 🔭 *Tự mò:* tự thêm câu hỏi từ các phase khác (Spark shuffle, Kafka exactly-once, dbt incremental) và viết câu trả lời 2–3 câu cho mỗi cái.

➡️ Tiếp: [[00-moduleA-summary]].
