# 16 — Normalization (1NF → 3NF → BCNF)

> Code: [`projects/03-data-modeling/03_normalization.sql`](../projects/03-data-modeling/03_normalization.sql)
> Chạy: `python scripts/run_sql.py projects/03-data-modeling/03_normalization.sql`

**Chuẩn hoá** = tổ chức dữ liệu để **giảm dư thừa** và **tránh bất thường (anomaly)** khi cập nhật. Là nền tảng thiết kế DB giao dịch (OLTP).

## Functional Dependency (FD) — viên gạch nền
`A → B`: biết A thì xác định duy nhất B. Ví dụ `customer_id → customer_name`. Mọi normal form đều định nghĩa qua FD. **Khoá (key)** = tập cột xác định toàn bộ hàng.

## Ba bất thường (anomaly) của bảng dư thừa
Trên `flat_orders` (khách 'An' lặp 3 dòng):
- **Update anomaly:** An đổi thành phố → phải sửa **mọi** dòng có An; sót 1 dòng → dữ liệu **mâu thuẫn**.
- **Insert anomaly:** không thêm được khách/sản phẩm mới nếu **chưa có đơn** (thiếu phần khoá).
- **Delete anomaly:** xoá đơn cuối của Binh → **mất luôn** thông tin khách Binh.

Chuẩn hoá loại bỏ ba bất thường này bằng cách tách mỗi "sự thật" về đúng một chỗ.

## Các Normal Form (tăng dần)
| NF | Yêu cầu | Loại bỏ |
|----|---------|---------|
| **1NF** | giá trị **nguyên tử**, không nhóm lặp / cột đa trị | cột kiểu `"A,B,C"`, mảng |
| **2NF** | 1NF + không **phụ thuộc bộ phận** vào khoá tổng hợp | non-key phụ thuộc *một phần* khoá |
| **3NF** | 2NF + không **phụ thuộc bắc cầu** (non-key → non-key) | `id → city → country` |
| **BCNF** | 3NF chặt hơn: mọi determinant phải là **siêu khoá** | vài ca hiếm 3NF chưa xử |

Câu thần chú 3NF: *"non-key phụ thuộc **khoá, toàn bộ khoá, và chỉ khoá**"* (the key, the whole key, nothing but the key).

### Áp dụng trong demo
- **1NF:** mỗi dòng 1 sản phẩm/đơn (đã đạt; không có cột "A,B,C").
- **2NF:** PK = (order_id, product_id). `customer_*`/`order_date` phụ thuộc *order_id* (bộ phận) → tách `orders`; `product_*`/`unit_price` phụ thuộc *product_id* (bộ phận) → tách `products`; `quantity` phụ thuộc **cả** khoá → ở lại `order_lines`.
- **3NF:** trong `orders`, `customer_id → customer_name, customer_city` rồi `customer_city → country` (bắc cầu) → tách `customers` và `cities`.
- Kết quả 5 bảng: `orders3, order_lines, products2, customers3, cities3`.

## Lossless decomposition (phân rã không mất mát) ⭐
Tách bảng phải **join lại được nguyên gốc**, không mất/thừa hàng. Demo: join 5 bảng 3NF tái tạo `flat_orders`, kết quả `flat_rows=4, recon_rows=4, diff_rows=0` → **lossless**. Và 'An' giờ chỉ lưu **1 lần** (`customers_unique=2`) thay vì 3 → hết dư thừa, hết update anomaly.

## ⭐ Khi nào KHÔNG chuẩn hoá (denormalize)?
Chuẩn hoá tối ưu cho **ghi** (OLTP): mỗi sự thật một chỗ, cập nhật an toàn. Nhưng:
- Truy vấn phân tích phải **join nhiều bảng** → chậm trên dữ liệu lớn.
- **OLAP/warehouse cố tình DENORMALIZE**: gộp dữ liệu vào **star schema** (fact + dimension) để đọc nhanh, ít join. Dư thừa được chấp nhận vì warehouse **đọc nhiều, ghi theo batch** (không có update lẻ kiểu OLTP).

| | Chuẩn hoá (3NF) | Denormalized (star) |
|--|-----------------|---------------------|
| Tối ưu | ghi (OLTP) | đọc (OLAP) |
| Join | nhiều | ít |
| Dư thừa | tối thiểu | chấp nhận có kiểm soát |
| Cập nhật | an toàn, 1 chỗ | qua ETL/SCD |

→ DE phải biết **cả hai**: nguồn OLTP thường 3NF; warehouse đích thường denormalized. Tiếp theo học cách thiết kế denormalized đúng cách. Xem [[17-dimensional-modeling]].

## ✅ Tự kiểm tra
- [ ] Định nghĩa FD và khoá
- [ ] Kể 3 anomaly với ví dụ cụ thể
- [ ] Phân biệt 1NF/2NF/3NF (phụ thuộc bộ phận vs bắc cầu)
- [ ] Hiểu lossless decomposition (join lại đúng gốc)
- [ ] Giải thích vì sao OLAP denormalize dù chuẩn hoá là "đúng" cho OLTP

➡️ Tiếp theo: [[17-dimensional-modeling]] — Kimball star schema.
