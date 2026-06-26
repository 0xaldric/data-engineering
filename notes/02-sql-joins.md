# 02 — SQL JOINs

> Code: [`projects/01-sql-fundamentals/02_joins.sql`](../projects/01-sql-fundamentals/02_joins.sql)
> Chạy: `python scripts/run_sql.py projects/01-sql-fundamentals/02_joins.sql`

JOIN = ghép hàng từ nhiều bảng dựa trên điều kiện (thường là khóa ngoại). Đây là kỹ năng dùng **mỗi ngày** của Data Engineer.

## Các loại JOIN

| Loại | Giữ hàng nào | Hình dung (A ⋈ B) |
|------|--------------|---------|
| `INNER JOIN` | Chỉ hàng khớp ở **cả hai** | Giao A∩B |
| `LEFT [OUTER] JOIN` | **Tất cả** A + B khớp (B thiếu = NULL) | Toàn bộ A |
| `RIGHT [OUTER] JOIN` | Tất cả B + A khớp | Toàn bộ B |
| `FULL [OUTER] JOIN` | Tất cả hàng cả hai, không khớp = NULL | Hợp A∪B |
| `CROSS JOIN` | **Mọi cặp** (tích Descartes) | A×B |
| SELF JOIN | Bảng join với chính nó | — |

```
INNER          LEFT            FULL
  A  B          A  B            A  B
  ●──●          ●──●            ●──●
     ●          ●  ·(NULL)      ●  ·
  ●──●          ●──●            ·  ●
```

## Khi nào dùng cái nào?
- **INNER** — chỉ cần bản ghi có quan hệ đầy đủ (đơn hàng *có* sản phẩm).
- **LEFT** — cần giữ trọn bảng gốc, kể cả khi không có dữ liệu liên quan (mọi khách hàng, kể cả khách 0 đơn). Đây là loại dùng nhiều nhất trong ETL.
- **RIGHT** — hiếm khi cần; thường đổi vị trí 2 bảng rồi viết LEFT cho dễ đọc.
- **FULL OUTER** — đối chiếu/reconcile 2 tập dữ liệu (cái nào thừa/thiếu bên nào).
- **CROSS** — sinh khung đầy đủ mọi tổ hợp (vd ma trận ngày × sản phẩm để fill 0 cho ngày không bán). Cẩn thận bùng nổ hàng.
- **SELF** — quan hệ trong cùng bảng (cấp trên–cấp dưới, cặp cùng nhóm, so sánh hàng kề nhau).

## Pattern cực hữu ích: ANTI-JOIN (tìm cái KHÔNG khớp)
```sql
SELECT ... FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;   -- khách CHƯA từng đặt đơn
```
LEFT JOIN rồi lọc `WHERE khóa_phải IS NULL` = "những hàng bên trái không có cặp bên phải". Dùng để: khách chưa mua, sản phẩm chưa bán, bản ghi mới chưa đồng bộ... (Tương đương `NOT EXISTS`.)

## ⚠️ Hai cạm bẫy chết người

### 1. FAN-OUT (nhân hàng) — sai số liệu thầm lặng
Join 1-nhiều làm **nhân bản** hàng bên "1". Trong demo: 10.000 đơn nhưng sau khi join với `order_items` thành **30.135 hàng**. Nếu lỡ `SUM` một cột mức-đơn-hàng (vd phí ship lưu ở `orders`) sau join này → **cộng trùng nhiều lần**, ra số sai mà không báo lỗi.

**Cách tránh:**
- Aggregate ở đúng grain trước rồi mới join (pre-aggregate), hoặc
- `COUNT(DISTINCT order_id)` thay vì `COUNT(*)`, và chỉ `SUM` các cột ở đúng grain của bảng nhiều (vd `oi.line_total`), không SUM cột của bảng một.
- Luôn tự hỏi: "sau join này, **một hàng = một cái gì**?" (grain).

### 2. NULL trong điều kiện & OUTER JOIN
- Sau LEFT JOIN, cột bên phải có thể NULL. `COUNT(cot)` bỏ qua NULL (nên khách 0 đơn ra 0), nhưng `COUNT(*)` thì không → chọn đúng biến thể.
- Đặt điều kiện lọc bảng phải vào `ON` hay `WHERE` cho kết quả **khác nhau** với OUTER JOIN: điều kiện ở `WHERE` chạy sau join sẽ loại luôn các hàng NULL, vô tình biến LEFT JOIN thành INNER JOIN. Muốn lọc mà vẫn giữ tính "outer" thì để điều kiện trong `ON`.

## Lưu ý hiệu năng (preview Phase 4)
JOIN trên dữ liệu lớn là điểm nóng performance: hash join vs sort-merge join, broadcast bảng nhỏ, và **data skew** (một khóa quá nhiều hàng). Sẽ đào sâu ở [[04-sql-window]] → Spark.

## ✅ Tự kiểm tra
- [ ] Vẽ được Venn cho INNER/LEFT/FULL
- [ ] Viết được anti-join tìm hàng không khớp
- [ ] Giải thích fan-out và cách `COUNT(DISTINCT)`/pre-aggregate cứu số liệu
- [ ] Biết vì sao để điều kiện ở `ON` vs `WHERE` đổi kết quả OUTER JOIN

➡️ Tiếp theo: [[03-sql-aggregation]] — GROUP BY & hàm tổng hợp.
