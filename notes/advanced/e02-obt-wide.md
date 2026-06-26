# E02 — One Big Table, Wide Tables & Activity Schema

> Xu hướng modeling "phản truyền thống": denormalize **mọi thứ** vào một bảng rộng. Hợp warehouse columnar hiện đại.

## One Big Table (OBT)
Gộp fact + tất cả dimension liên quan vào **một bảng phẳng, rộng** (denormalize hoàn toàn), thay vì star schema (fact + dim join).
```
-- thay vì fct_sales JOIN dim_customer JOIN dim_product...
obt_sales: order_id, order_ts, line_total, quantity,
           customer_id, customer_name, customer_country,   ← dim nhúng thẳng
           product_id, product_name, category, price_tier  ← dim nhúng thẳng
```

## Vì sao OBT thắng (trên columnar warehouse)
- **Không join lúc query** → đơn giản, nhanh (join là thao tác đắt; OBT trả tiền 1 lần lúc build).
- **Columnar** (BigQuery/Snowflake/Parquet): cột không dùng **không bị đọc** → bảng rộng không phạt nếu chọn ít cột ([[09-file-formats]]).
- **BI tool / analyst** dễ dùng (không cần hiểu quan hệ, không join sai → không fan-out).
- Storage rẻ → chấp nhận dư thừa để đổi lấy tốc độ/đơn giản.

## OBT vs Star
| | Star schema | OBT |
|--|-------------|-----|
| Join lúc query | có (fact×dim) | **không** |
| Dư thừa | thấp | cao (chấp nhận) |
| Cập nhật dimension | sửa 1 dim | rebuild OBT (hoặc cột thay đổi) |
| BI/analyst | cần hiểu quan hệ | dễ nhất |
| Storage | ít | nhiều |
| Khi nào | nhiều fact dùng chung dim, cần linh hoạt | bảng phục vụ cụ thể, BI rộng, columnar |
→ Không "cái nào tốt hơn" tuyệt đối: nhiều team build **star ở core** rồi **OBT ở mart** (gold) cho từng use case BI.

## Wide tables
Mở rộng OBT: bảng rất nhiều cột (hàng trăm), gồm mọi attribute + feature precomputed. Phổ biến cho **feature table** (ML — [[c09-case-recsys]]) và mart BI. Columnar làm điều này khả thi.

## Activity Schema ⭐
Mô hình hoá **mọi thứ thành stream of activities** trong MỘT bảng duy nhất:
```
activity_stream:
  entity_id (customer), activity (viewed/added_to_cart/purchased),
  ts, activity_repeated_at, feature_json (thuộc tính linh hoạt)
```
- Một bảng cho mọi hành vi → query bằng "temporal join" pattern (activity X rồi activity Y trong N ngày).
- Ưu: cực linh hoạt, thêm activity mới không đổi schema; hợp customer journey/clickstream ([[c06-case-clickstream]]).
- Nhược: query pattern lạ (cần hiểu temporal join), không quen với BI truyền thống.

## ⚠️ Cạm bẫy
- OBT khi nhiều fact **chung dimension** → dim đổi phải rebuild nhiều OBT (star tránh được). Cân nhắc.
- OBT trên **row-store** (OLTP) → phạt nặng (đọc cả hàng rộng); chỉ hợp **columnar**.
- Wide table quá nhiều cột không ai dùng → vẫn tốn build/maintain.
- Coi OBT là "lười không cần modeling" → vẫn cần chọn grain & chất lượng.

## ✅ "Tự mò"
🔭 Build OBT `obt_sales` từ star schema e-commerce (join sẵn customer/product vào fct_sales); so query "revenue theo country×category" trên OBT (không join) vs star (join) — đo & cảm nhận đơn giản.

➡️ Tiếp: [[e03-event-modeling]].
