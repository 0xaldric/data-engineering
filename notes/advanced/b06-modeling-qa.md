# B06 — Data Modeling Q&A (sâu)

> Câu hỏi modeling sâu hơn [[a07-sql-qa]]. Chi tiết: [[16-normalization]]→[[20-nosql]].

**Q: Grain là gì, vì sao chọn đầu tiên?**
A: Grain = "một hàng fact đại diện cho gì". Tuyên bố TRƯỚC khi chọn cột; mọi dimension/measure phải đúng theo grain. Chọn **nguyên tử nhất** (chi tiết tối đa) → trả lời được nhiều câu hỏi.

**Q: Fan-out là gì, tránh thế nào?**
A: Join 1-nhiều nhân hàng → SUM cột mức-trên bị cộng trùng. Tránh: pre-aggregate đúng grain, `COUNT(DISTINCT)`, chỉ SUM cột đúng grain. Luôn hỏi "sau join, 1 hàng = gì?".

**Q: SCD types & khi nào dùng?**
A: Type 0 (bất biến), Type 1 (overwrite, mất lịch sử — sửa typo), **Type 2** (versioning, giữ lịch sử — chuẩn vàng), Type 3 (1 giá trị trước). Type 2 cần surrogate key + effective_from/to + is_current.

**Q: Surrogate vs natural key?**
A: Natural = khoá nghiệp vụ từ nguồn (customer_id). Surrogate = khoá thay thế vô nghĩa (số/hash). Dùng surrogate vì: tách khỏi nguồn, **cần cho SCD2** (cùng natural key, nhiều phiên bản), join số nhanh.

**Q: 3 loại fact table?**
A: **Transaction** (mỗi sự kiện), **periodic snapshot** (trạng thái theo chu kỳ — tồn kho cuối ngày), **accumulating snapshot** (vòng đời quy trình, nhiều date role, được UPDATE).

**Q: Additivity?**
A: **Additive** (SUM mọi chiều — revenue, quantity); **semi-additive** (không theo thời gian — tồn kho, số dư → dùng last/avg); **non-additive** (đơn giá, % → tính lại từ additive). Lưu measure additive, tính tỉ lệ lúc query.

**Q: Conformed dimension?**
A: Dimension dùng chung nhất quán across nhiều fact/process (cùng dim_date, dim_customer cho Sales/Returns/Shipping) → drill-across (so sánh process trên cùng trục). Bus matrix = process × conformed dim.

**Q: Star vs Snowflake?**
A: Star = dimension denormalized (phẳng, ít join, mặc định). Snowflake = dimension chuẩn hoá thành nhiều bảng con (tiết kiệm chỗ, nhiều join).

**Q: Degenerate vs Junk dimension?**
A: Degenerate = mã giao dịch (order_id) nằm thẳng trong fact, không cần bảng dim. Junk = gộp vài cờ rời rạc (status, channel, is_gift) vào 1 dim nhỏ.

**Q: Normalize vs denormalize — khi nào?**
A: Normalize (3NF) cho OLTP (ghi an toàn, mỗi sự thật 1 chỗ). Denormalize (star) cho OLAP (đọc nhanh, ít join). DE chuyển OLTP 3NF → warehouse denormalized.

**Q: Data Vault là gì (sơ lược)?**
A: Mô hình warehouse linh hoạt: **Hub** (business key), **Link** (quan hệ), **Satellite** (thuộc tính + lịch sử). Dễ mở rộng/audit/parallel-load; phức tạp hơn star, thường dùng tầng raw vault rồi build star ở mart. (Sâu hơn ở Module E.)

**Q: Slowly changing fact?**
A: Fact thường immutable, nhưng đôi khi cần sửa (đơn bị điều chỉnh). Cách: ghi bản ghi đảo (reversing entry) thay vì update, hoặc accumulating snapshot. Giữ audit.

**Q: Late-arriving dimension?**
A: Fact tới trước khi dimension có (đơn của khách chưa kịp vào dim). Xử lý: tạo bản ghi dim "inferred/placeholder" (unknown member) rồi cập nhật sau, hoặc giữ natural key chờ.

**Q: Modeling event/clickstream khác gì?**
A: Sự kiện nhiều, schema bán cấu trúc (JSON), thường dùng One Big Table / wide event table hoặc activity schema thay star truyền thống. (Module E.)

**Q: Bridge table?**
A: Xử lý quan hệ nhiều-nhiều giữa fact và dimension (vd 1 giao dịch nhiều "sales rep") hoặc nhóm dimension (account ↔ nhiều khách) — bảng cầu với trọng số phân bổ.

## ✅ "Tự mò"
🔭 Thiết kế lại star schema e-commerce thêm dim_promotion + junk dimension (status, channel) + accumulating snapshot order lifecycle; giải thích grain mỗi fact.

➡️ Tiếp: [[b07-behavioral-star]].
