# Star Schema Design — E-commerce Sales

Thiết kế dimensional model cho dataset e-commerce (`data/raw/`). Triển khai ở T024 (`04_build_star.py` → `warehouse/star.duckdb`). Lý thuyết: [`notes/17-dimensional-modeling.md`](../../notes/17-dimensional-modeling.md).

## 4 bước Kimball
1. **Business process:** Bán hàng (Sales).
2. **Grain:** *một hàng = một dòng sản phẩm trong một đơn* (atomic, theo `order_items`).
3. **Dimensions:** Date, Customer, Product (+ status/channel xử lý dạng degenerate/junk).
4. **Facts/measures:** quantity, unit_price, discount, line_total, unit_cost, gross_margin.

## Sơ đồ Star Schema
```
                       ┌──────────────────┐
                       │     dim_date     │
                       │  date_key (PK)   │
                       │  full_date,year, │
                       │  quarter,month,  │
                       │  day,weekday,    │
                       │  is_weekend      │
                       └────────┬─────────┘
                                │ date_key
  ┌──────────────────┐   ┌──────┴───────────────────┐   ┌────────────────────┐
  │   dim_customer   │   │        fct_sales         │   │    dim_product     │
  │ customer_key(PK) │   │  (grain: order line)     │   │ product_key (PK)   │
  │ customer_id (NK) │◄──┤  customer_key  (FK)      ├──►│ product_id  (NK)   │
  │ name,country,    │   │  product_key   (FK)      │   │ product_name,      │
  │ city,signup_date │   │  date_key      (FK)      │   │ category,          │
  │ -- SCD2 cols --  │   │  order_id (degenerate)   │   │ unit_cost,         │
  │ effective_from,  │   │  status,channel (junk)   │   │ unit_price,        │
  │ effective_to,    │   │  ── measures ──          │   │ price_tier         │
  │ is_current       │   │  quantity, unit_price,   │   └────────────────────┘
  └──────────────────┘   │  discount, line_total,   │
                         │  unit_cost, gross_margin │
                         └──────────────────────────┘
```

## fct_sales (fact — transaction grain)
| Cột | Loại | Ghi chú |
|-----|------|---------|
| `customer_key` | FK → dim_customer | surrogate |
| `product_key` | FK → dim_product | surrogate |
| `date_key` | FK → dim_date | dạng YYYYMMDD |
| `order_id` | degenerate dimension | mã đơn, không cần bảng riêng |
| `status`, `channel` | junk dimension | cờ rời rạc (có thể tách dim_junk) |
| `quantity` | measure (additive) | |
| `line_total` | measure (additive) | doanh thu dòng |
| `unit_price`,`discount` | measure (non/semi-additive) | đơn giá không cộng dồn được |
| `gross_margin` | measure (additive) | line_total − unit_cost×quantity |

**Additivity:** `quantity`, `line_total`, `gross_margin` cộng được theo mọi dimension (additive); `unit_price` **không** additive (đừng SUM giá). Xem [[19-fact-types]].

## Dimensions
- **dim_date** — sinh từ lịch (mọi ngày trong khoảng dữ liệu). `date_key` = số nguyên YYYYMMDD (smart key). Thuộc tính: year, quarter, month, month_name, day, weekday, is_weekend → cho phép phân tích theo thời gian không cần hàm.
- **dim_customer** — surrogate `customer_key`, natural `customer_id`. **Áp SCD Type 2**: thêm `effective_from/effective_to/is_current` để giữ lịch sử khi khách đổi country/city (T025).
- **dim_product** — surrogate `product_key`, natural `product_id`. Thêm `price_tier` (premium/mid/budget) tính sẵn.

## Bus Matrix (process × conformed dimension)
| Business process | Date | Customer | Product | Channel |
|------------------|:----:|:--------:|:-------:|:-------:|
| **Sales** (fct_sales) | ✅ | ✅ | ✅ | ✅ |
| Returns | ✅ | ✅ | ✅ | ✅ |
| Inventory snapshot | ✅ | — | ✅ | — |
| Shipping | ✅ | ✅ | — | ✅ |

→ `dim_date`, `dim_customer`, `dim_product` là **conformed** (dùng lại y hệt cho mọi process) → drill-across được (so sánh Sales vs Returns trên cùng trục Product/Date).

## Truy vấn kiểm chứng (sẽ chạy ở T024)
Doanh thu theo `dim_product.category` từ star schema phải **khớp** gold mart đã có (`Grocery = 1,714,225.45`) → thiết kế đúng, không lệch grain.
