# 19 — Fact Table Types & Additivity

> Code: [`projects/03-data-modeling/06_fact_types.sql`](../projects/03-data-modeling/06_fact_types.sql)
> Chạy: `python scripts/run_sql.py projects/03-data-modeling/06_fact_types.sql`

## Ba loại Fact table (Kimball)
| Loại | Mỗi hàng = | Hàng có bị UPDATE? | Grain ví dụ |
|------|-----------|--------------------|-------------|
| **Transaction** | một sự kiện tại một thời điểm | Không (chỉ insert) | một dòng bán hàng |
| **Periodic snapshot** | trạng thái theo **chu kỳ cố định** | Không (mỗi kỳ 1 hàng mới) | doanh thu mỗi **ngày** |
| **Accumulating snapshot** | một **quy trình** nhiều mốc | **Có** — cập nhật khi tiến triển | vòng đời 1 đơn hàng |

### Transaction fact
Chi tiết nhất, atomic. `fct_sales` ở [[17-dimensional-modeling]] (grain = order line). Chỉ thêm, không sửa. Trả lời được hầu hết câu hỏi vì ở grain thấp nhất.

### Periodic snapshot
Gộp theo chu kỳ đều (ngày/tuần/tháng) — `fct_daily_sales`: mỗi ngày một hàng với `orders, units, revenue`. Tốt để **theo dõi xu hướng/KPI theo thời gian** mà không phải quét lại bảng transaction khổng lồ. Measures thường additive.

### Accumulating snapshot ⭐
Theo dõi một **quy trình có nhiều mốc** (đặt → ship → giao → trả). Đặc trưng: **nhiều cột ngày** (date roles) + **lag measures** (khoảng cách giữa các mốc). Hàng được **UPDATE** mỗi khi đơn sang mốc mới. `fct_order_lifecycle`:
```
order_date → ship_date → delivered_date → returned_date
```
Funnel thực tế (đo được): placed **10,000** → shipped **8,343** → delivered **6,688** → returned **1,586**; avg ngày giao = **5.0**. Dùng để phân tích **thời gian xử lý, nghẽn ở đâu, tỉ lệ rớt mỗi bước** (pipeline/SLA).

## ⭐ Additivity — measure cộng dồn được tới đâu?
Phân loại CỰC kỳ quan trọng để không tính sai:
| Loại | Cộng (SUM) theo | Ví dụ | Lưu ý |
|------|-----------------|-------|-------|
| **Additive** | **mọi** dimension (kể cả thời gian) | revenue, quantity, gross_margin | thoải mái SUM |
| **Semi-additive** | một số dimension, **KHÔNG theo thời gian** | số dư tài khoản, tồn kho, headcount, "khách lũy kế" | qua thời gian dùng **last/avg**, không SUM |
| **Non-additive** | **không** cộng được | đơn giá, %, tỉ lệ, ratio | phải tính lại từ thành phần additive |

- **Semi-additive** là bẫy hay gặp: tồn kho mỗi ngày 100 đơn vị, **cộng 30 ngày ≠ 3000** (đếm trùng cùng một lượng hàng). Đúng: lấy giá trị **cuối kỳ** hoặc **trung bình**. Demo: "số khách lũy kế mỗi ngày" — cộng các giá trị lũy kế theo ngày là vô nghĩa; chỉ `new_customers` (mỗi ngày) mới additive.
- **Non-additive** (vd `unit_price`): đừng bao giờ `SUM(unit_price)`. Muốn giá trung bình thì `SUM(line_total)/SUM(quantity)` — tính từ các measure additive.

→ Quy tắc thiết kế: **lưu measure ở dạng additive** (line_total, quantity) trong fact; tỉ lệ/đơn giá để **tính lúc query** từ chúng. Tránh lưu sẵn % trong fact.

## Liên hệ
- Transaction fact là nguồn để **dẫn xuất** periodic snapshot (gộp theo kỳ).
- Accumulating snapshot hợp với quy trình có vòng đời rõ ([[ROADMAP]] Phase 6 CDC giúp cập nhật mốc real-time).

## ✅ Tự kiểm tra
- [ ] Phân biệt transaction / periodic / accumulating (grain & có UPDATE không)
- [ ] Đặc trưng accumulating snapshot: nhiều date role + lag measure + funnel
- [ ] Phân loại additive / semi-additive / non-additive với ví dụ
- [ ] Vì sao không SUM tồn kho/số dư theo thời gian, không SUM đơn giá
- [ ] Quy tắc: lưu measure additive, tính tỉ lệ lúc query

➡️ Tiếp theo: [[20-nosql]] — NoSQL & khi nào dùng.
