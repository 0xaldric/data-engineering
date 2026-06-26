# 17 — Dimensional Modeling (Kimball) ⭐

> Thiết kế áp dụng: [`projects/03-data-modeling/star_schema_design.md`](../projects/03-data-modeling/star_schema_design.md)
> Triển khai code: T024 (`04_build_star.py`)

**Dimensional modeling** (Ralph Kimball) là cách thiết kế warehouse tối ưu cho **đọc/phân tích** và **dễ hiểu với người dùng business**. Trái tim của analytics engineering.

## Fact & Dimension — hai loại bảng
- **Fact table** = "sự kiện đo lường được" của một quy trình nghiệp vụ (mỗi dòng = một sự kiện). Chứa **measures** (số đo: doanh thu, số lượng) + **foreign keys** trỏ tới các dimension. Dài & hẹp, rất nhiều hàng.
- **Dimension table** = "bối cảnh" mô tả (ai, cái gì, khi nào, ở đâu). Chứa **thuộc tính mô tả** dùng để **lọc/nhóm** (country, category, month). Rộng & ngắn, ít hàng.

> Mẹo phân biệt: số để **SUM/AVG** → measure (fact); thứ đứng sau **GROUP BY / WHERE** → attribute (dimension).

## ⭐ Grain — quyết định ĐẦU TIÊN và quan trọng nhất
**Grain** = "một hàng fact đại diện cho cái gì". Phải tuyên bố rõ TRƯỚC khi chọn cột. Vd: *"một hàng = một dòng sản phẩm trong một đơn"* (atomic) — nên chọn grain **nguyên tử nhất** có thể (chi tiết tối đa) để trả lời được nhiều câu hỏi. Mọi dimension & measure phải **đúng theo grain** đó (xem fan-out [[02-sql-joins]]).

## Surrogate key
Khoá thay thế **vô nghĩa** (số tự tăng) làm PK của dimension, thay vì dùng natural key (business key) từ nguồn. Vì sao:
- Tách warehouse khỏi thay đổi/định dạng khoá nguồn.
- **Cần cho SCD Type 2**: cùng một customer_id (natural) nhưng nhiều phiên bản theo thời gian → mỗi phiên bản một surrogate key. Xem [[18-scd]].
- Join số nguyên nhanh hơn. Fact chỉ giữ surrogate key của dim.

## Star schema vs Snowflake
```
        STAR (denormalized dims)              SNOWFLAKE (normalized dims)
        dim_date                               dim_date
            \                                      \
 dim_cust — FACT — dim_product          dim_cust — FACT — dim_product — dim_category
            /                                      /
        dim_channel                            dim_geo
```
- **Star**: dimension **denormalized** (phẳng, mọi thuộc tính trong 1 bảng). Ít join, nhanh, dễ hiểu → **mặc định nên dùng**.
- **Snowflake**: dimension chuẩn hoá tiếp thành nhiều bảng con. Tiết kiệm chỗ nhưng nhiều join, phức tạp → chỉ dùng khi thật cần.

## Các loại Fact table
| Loại | Mỗi hàng | Ví dụ |
|------|----------|-------|
| **Transaction** | một sự kiện tại thời điểm | mỗi dòng bán hàng |
| **Periodic snapshot** | trạng thái theo chu kỳ cố định | tồn kho cuối mỗi ngày |
| **Accumulating snapshot** | vòng đời 1 quy trình, cập nhật dần | đơn hàng: đặt→ship→giao (nhiều cột mốc) |
Chi tiết & measure additivity ở [[19-fact-types]].

## Conformed dimensions & Bus Matrix
- **Conformed dimension** = dimension **dùng chung** nhất quán across nhiều fact/quy trình (cùng `dim_date`, `dim_customer` cho Sales, Returns, Shipping). Cho phép "drill across" — so sánh các quy trình trên cùng trục.
- **Bus matrix** (Kimball): bảng **quy trình nghiệp vụ × dimension** — bản đồ tổng quan warehouse, lập kế hoạch xây từng fact mà vẫn chia sẻ dimension. Xem ma trận cụ thể trong file thiết kế.

## Degenerate & Junk dimension
- **Degenerate dimension**: mã giao dịch (order_id) nằm **thẳng trong fact**, không cần bảng dim riêng (chỉ là định danh).
- **Junk dimension**: gộp vài cờ/flag rời rạc, ít giá trị (status, channel, is_gift...) vào **một** dim nhỏ thay vì nhiều cột bool trong fact.

## Quy trình thiết kế 4 bước (Kimball)
1. Chọn **business process** (vd: bán hàng).
2. Tuyên bố **grain** (một dòng = ?).
3. Xác định **dimensions** (bối cảnh quanh grain).
4. Xác định **facts/measures** (số đo theo grain).

## ✅ Tự kiểm tra
- [ ] Phân biệt fact vs dimension (measure vs attribute)
- [ ] Giải thích grain và vì sao chọn nguyên tử nhất
- [ ] Vì sao dùng surrogate key (đặc biệt cho SCD2)
- [ ] Star vs snowflake; khi nào dùng cái nào
- [ ] Conformed dimension & bus matrix để làm gì
- [ ] Degenerate vs junk dimension

➡️ Áp dụng: [[star-schema-design]] → triển khai ở T024, rồi [[18-scd]].
