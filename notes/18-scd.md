# 18 — Slowly Changing Dimensions (SCD) ⭐

> Code: [`projects/03-data-modeling/05_scd.py`](../projects/03-data-modeling/05_scd.py)
> Chạy: `python projects/03-data-modeling/05_scd.py`

**Vấn đề:** thuộc tính dimension thay đổi theo thời gian (khách đổi địa chỉ, sản phẩm đổi category). Xử lý thế nào để **báo cáo lịch sử vẫn đúng**? Đó là SCD — một trong những khái niệm bị hỏi nhiều nhất khi phỏng vấn DE.

Kịch bản demo: khách #1 chuyển **Hanoi/VN → Tokyo/JP** ngày 2024-01-30.

## Các Type chính
| Type | Cách làm | Lịch sử | Khi nào dùng |
|------|----------|---------|--------------|
| **0** | giữ nguyên, không đổi | bất biến | thuộc tính không bao giờ đổi (ngày sinh) |
| **1** | **ghi đè** giá trị mới | ❌ mất | sửa lỗi typo, không quan tâm lịch sử |
| **2** | **thêm dòng** phiên bản mới | ✅ đầy đủ | **chuẩn vàng** — cần phân tích theo lịch sử |
| **3** | thêm **cột** previous_value | ⚠️ 1 mức | chỉ cần "trước/sau" gần nhất |
| 4 | tách bảng history riêng | ✅ | dimension đổi rất thường xuyên |
| 6 | kết hợp 1+2+3 | ✅ | hybrid |

## Type 1 — Overwrite
`UPDATE ... SET city = new`. Đơn giản nhưng **mất lịch sử**: sau update chỉ thấy Tokyo/JP, không biết khách từng ở Hanoi. → Báo cáo doanh thu "theo quốc gia khách" trong quá khứ sẽ **sai** (gán hết về JP).

## ⭐ Type 2 — Versioning (quan trọng nhất)
Mỗi thay đổi tạo **một dòng mới** với **surrogate key mới**; dòng cũ bị "hết hạn". Cột điều khiển:
- `effective_from`, `effective_to` — khoảng thời gian hiệu lực của phiên bản.
- `is_current` (hoặc flag) — đánh dấu phiên bản hiện hành.

Quy trình load (như trong code):
1. **Expire**: dòng current của khách thay đổi → set `effective_to = ngày_đổi`, `is_current = FALSE`.
2. **Insert**: thêm dòng mới với giá trị mới, `effective_from = ngày_đổi`, `effective_to = 9999-12-31`, `is_current = TRUE`, **surrogate key mới**.

Kết quả khách #1 có 2 dòng:
```
customer_key  city   country  effective_from  effective_to  is_current
     1        Hanoi  VN       2024-01-01      2024-01-30    False
     4        Tokyo  JP       2024-01-30      9999-12-31    True
```

**Vì sao cần surrogate key** ([[17-dimensional-modeling]]): cùng `customer_id=1` nhưng 2 phiên bản → fact trỏ tới `customer_key` (1 hoặc 4) sẽ gắn mỗi giao dịch với **đúng phiên bản tại thời điểm đó** → báo cáo lịch sử chính xác.

**Truy vấn "as-of"** (point-in-time): khách #1 ở đâu vào 2024-01-15?
```sql
WHERE customer_id=1 AND '2024-01-15' >= effective_from AND '2024-01-15' < effective_to
```
→ trả Hanoi/VN (đúng). Truy được trạng thái dimension tại **bất kỳ ngày nào** trong quá khứ.

> Lưu ý ranh giới: dùng `>= from AND < to` (nửa mở) để tránh trùng/lủng ngày tại điểm đổi.

## Type 3 — Previous value
Thêm cột `city_previous` cạnh `city_current`. Khi đổi: dồn current→previous, gán current=mới. Chỉ giữ **một** mức lịch sử (đổi lần 2 là mất Hanoi). Hợp khi chỉ cần so "hiện tại vs lần trước" (vd phân loại cũ/mới).

## Thực tế triển khai
- Tự viết bằng SQL `MERGE`/UPDATE+INSERT (như demo), hoặc dùng công cụ: **dbt snapshots** làm SCD2 tự động (Phase 3), Delta Lake `MERGE`, các framework ingestion.
- Cần **khoá tự nhiên** (business key) ổn định để nhận diện cùng thực thể qua các phiên bản.
- Phát hiện thay đổi: so từng cột, hoặc dùng **hash** của các thuộc tính theo dõi để so nhanh.

## ✅ Tự kiểm tra
- [ ] Phân biệt Type 0/1/2/3 và lịch sử mỗi loại giữ
- [ ] Vẽ được quy trình Type 2 (expire + insert) và vai trò `effective_from/to`, `is_current`
- [ ] Giải thích vì sao Type 2 cần surrogate key (gắn fact đúng phiên bản)
- [ ] Viết truy vấn as-of (point-in-time) với khoảng nửa mở
- [ ] Hạn chế của Type 3

➡️ Tiếp theo: [[19-fact-types]] — các loại fact table & tính cộng dồn measure.
