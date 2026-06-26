# 15 — Constraints, Transactions, ACID; OLTP vs OLAP

> Code: [`projects/03-data-modeling/02_constraints_tx.py`](../projects/03-data-modeling/02_constraints_tx.py)
> Chạy: `python projects/03-data-modeling/02_constraints_tx.py`

## Constraints — bảo vệ chất lượng dữ liệu TẠI database
DB là "tuyến phòng thủ cuối". Constraint chặn dữ liệu bẩn dù app có bug:
| Constraint | Đảm bảo | Demo (đều BLOCKED) |
|------------|---------|--------------------|
| `PRIMARY KEY` | định danh duy nhất + không null | chặn PK trùng |
| `UNIQUE` | không trùng giá trị | chặn sku trùng |
| `NOT NULL` | bắt buộc có giá trị | chặn sku/category NULL |
| `CHECK (expr)` | thoả điều kiện nghiệp vụ | chặn price < 0 |
| `FOREIGN KEY` | toàn vẹn tham chiếu | chặn product_id không tồn tại |

→ Tất cả ném `ConstraintException` ngay khi insert sai. Validate ở app (pydantic, [[12-testing-de]]) là tốt, nhưng constraint ở DB mới là đảm bảo cứng.

> Lưu ý: warehouse OLAP (BigQuery, Snowflake, một số cấu hình DuckDB) thường **không enforce** PK/FK (chỉ "informational") vì chi phí kiểm tra trên dữ liệu lớn — khi đó chất lượng do pipeline/dbt tests lo (Phase 3, 8).

## Transactions & ACID
**Transaction** = nhóm thao tác "tất cả hoặc không gì cả". `BEGIN → ... → COMMIT` (chốt) hoặc `ROLLBACK` (hoàn tác). Demo: sau ROLLBACK số hàng quay về cũ (3), sau COMMIT giữ lại (4).

**ACID** = 4 tính chất của transaction tin cậy:
- **Atomicity (nguyên tử):** hoặc xong hết, hoặc không gì — lỗi giữa chừng thì rollback. (vd chuyển tiền: trừ A và cộng B phải cùng xảy ra.)
- **Consistency (nhất quán):** transaction đưa DB từ trạng thái hợp lệ này sang trạng thái hợp lệ khác (giữ mọi constraint).
- **Isolation (cô lập):** các transaction chạy đồng thời không giẫm lên nhau (như chạy tuần tự).
- **Durability (bền vững):** đã COMMIT thì còn mãi, kể cả mất điện (ghi xuống đĩa/WAL).

## Isolation levels & anomalies
Cô lập càng cao càng đúng nhưng càng chậm (khoá nhiều). Các mức (SQL chuẩn) và lỗi chúng cho phép:
| Level | Dirty read | Non-repeatable read | Phantom |
|-------|:----------:|:-------------------:|:-------:|
| Read Uncommitted | ❌ có thể | ❌ | ❌ |
| Read Committed (mặc định Postgres) | ✅ chặn | ❌ | ❌ |
| Repeatable Read | ✅ | ✅ chặn | ❌ |
| Serializable (cao nhất) | ✅ | ✅ | ✅ chặn |

- **Dirty read:** đọc dữ liệu transaction khác **chưa commit**.
- **Non-repeatable read:** đọc cùng 1 hàng 2 lần ra **khác nhau** (do TX khác update+commit giữa chừng).
- **Phantom read:** chạy lại cùng query, xuất hiện **hàng mới** (do TX khác insert).
DE cần biết để chọn mức phù hợp (vd báo cáo cần snapshot nhất quán → Repeatable Read/Serializable). MVCC (Postgres) cho phép đọc không chặn ghi.

## ⭐ OLTP vs OLAP — hai thế giới khác nhau
| | **OLTP** (Online Transaction Processing) | **OLAP** (Online Analytical Processing) |
|--|------------------------------------------|------------------------------------------|
| Mục đích | vận hành app (đặt hàng, thanh toán) | phân tích, báo cáo, BI |
| Truy vấn | nhiều, nhỏ, point read/write theo khoá | ít, lớn, quét & aggregate nhiều hàng |
| Đơn vị | 1 bản ghi / vài hàng | hàng triệu hàng, vài cột |
| Lưu trữ | **row-store** | **column-store** |
| Chuẩn hoá | 3NF (tránh trùng, ghi nhanh) | denormalized / star schema (đọc nhanh) |
| Ví dụ | Postgres, MySQL, Oracle | BigQuery, Snowflake, Redshift, DuckDB |
| Index | B-tree then chốt | zonemap/pruning, ít index ([[14-indexing]]) |

### Row-store vs Column-store
- **Row-store:** lưu nguyên hàng cạnh nhau → lấy/sửa **cả bản ghi** nhanh (OLTP). Quét 1 cột phải đọc cả hàng.
- **Column-store:** lưu từng cột → quét/aggregate **vài cột trên triệu hàng** cực nhanh, nén tốt (OLAP). Sửa 1 hàng đắt hơn.

→ Vì sao tách warehouse khỏi production DB: workload analytics (quét nặng) sẽ làm nghẽn OLTP đang phục vụ người dùng. Data Engineer **chuyển** dữ liệu OLTP → OLAP (ETL/ELT) để phân tích an toàn. Đây là lý do tồn tại của cả nghề DE.

## ✅ Tự kiểm tra
- [ ] Kể 5 loại constraint & chúng chặn gì
- [ ] Giải thích ACID bằng ví dụ chuyển tiền
- [ ] Phân biệt dirty/non-repeatable/phantom read và mức isolation chặn chúng
- [ ] So sánh OLTP vs OLAP (workload, lưu trữ, chuẩn hoá)
- [ ] Giải thích vì sao tách warehouse khỏi production DB

➡️ Tiếp theo: [[16-normalization]] — chuẩn hoá 1NF→3NF & khi nào denormalize.
