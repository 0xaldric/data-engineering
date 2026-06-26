# 20 — NoSQL & khi nào dùng

> Code: [`projects/03-data-modeling/07_nosql_modeling.py`](../projects/03-data-modeling/07_nosql_modeling.py)
> Chạy: `python projects/03-data-modeling/07_nosql_modeling.py`

**NoSQL** = "Not Only SQL" — nhóm DB không theo mô hình quan hệ truyền thống, đánh đổi tính nhất quán/quan hệ để lấy **scale ngang, linh hoạt schema, hiệu năng** cho workload cụ thể.

## 4 họ NoSQL chính
| Họ | Mô hình | Truy cập | Ví dụ | Hợp cho |
|----|---------|----------|-------|---------|
| **Document** | JSON/BSON lồng | theo key + query trong document | MongoDB, Couchbase | dữ liệu bán cấu trúc, catalog, profile |
| **Key-Value** | khoá → giá trị | get/put theo key | Redis, DynamoDB | cache, session, đếm, hàng đợi |
| **Wide-Column** | họ cột, hàng thưa | theo partition key + clustering | Cassandra, HBase, Bigtable | ghi cực lớn, time-series, IoT |
| **Graph** | node + edge | duyệt quan hệ | Neo4j | mạng xã hội, gợi ý, gian lận |

## Document model — embedding vs referencing
Demo: cùng dữ liệu đơn hàng, mô hình **document** gộp (embed) customer + items + product vào **một** JSON:
```json
{ "_id": 1, "status": "completed",
  "customer": { "customer_id": 801, "country": "DE" },   // embedded
  "items": [ { "product_id": 56, "category": "Electronics", "line_total": 256.92 }, ... ],
  "order_total": 1234.5, "n_items": 4 }                    // aggregate tính sẵn
```
- **Embedding (nhúng):** để dữ liệu liên quan **trong cùng document**. Đọc 1 lần là đủ → **không cần JOIN**, nhanh cho pattern "lấy cả đơn". Đánh đổi: **dư thừa** (product info lặp ở mỗi đơn) và cập nhật product phải sửa nhiều nơi.
- **Referencing (tham chiếu):** lưu `product_id` rồi tra bảng khác — giống relational, đỡ dư thừa nhưng phải "join" ở tầng ứng dụng.

→ Quy tắc: **embed thứ đọc cùng nhau, ít đổi** (line items của đơn); **reference thứ dùng chung, hay đổi, lớn** (catalog sản phẩm). "Model theo **access pattern**" — ngược với SQL "model theo quan hệ rồi join sau".

## ⭐ SQL vs NoSQL — khác biệt cốt lõi
| | SQL (quan hệ) | NoSQL |
|--|---------------|-------|
| Schema | cố định, chặt (schema-on-write) | linh hoạt (schema-on-read) |
| Quan hệ | JOIN mạnh | hạn chế (embed/denormalize) |
| Giao dịch | ACID đầy đủ | thường BASE (eventual) — đang cải thiện |
| Scale | dọc (mạnh máy), khó scale ghi | **ngang** (thêm node) tự nhiên |
| Thiết kế | chuẩn hoá theo entity | denormalize theo query |
| Khi nào | quan hệ phức tạp, tính nhất quán, ad-hoc query | scale lớn, schema đổi, access pattern rõ |

## CAP Theorem
Hệ phân tán chỉ đạt **2 trong 3** khi có **phân vùng mạng (P)**:
- **C**onsistency (mọi node đọc ra dữ liệu mới nhất),
- **A**vailability (luôn trả lời),
- **P**artition tolerance (chịu được mất kết nối giữa node).
Vì mạng **luôn có thể phân vùng** → thực tế chọn giữa **CP** (ưu tiên nhất quán, có thể từ chối phục vụ — vd HBase, Mongo) và **AP** (luôn phục vụ, chấp nhận dữ liệu tạm cũ — vd Cassandra, Dynamo). Liên hệ **BASE** (Basically Available, Soft state, Eventual consistency) — đối lập ACID.

## Vai trò trong Data Engineering
- Nguồn dữ liệu thường gồm **cả SQL lẫn NoSQL** (Postgres cho giao dịch, Mongo cho catalog, Redis cache, Kafka log...). DE phải **ingest từ mọi loại** và đưa về warehouse phân tích.
- Warehouse/lakehouse phân tích thường vẫn **dạng bảng/columnar** (Parquet, [[09-file-formats]]) — NoSQL chủ yếu ở tầng **vận hành (OLTP-like)**, không thay thế OLAP.
- DuckDB đọc thẳng JSON lồng (`read_json_auto`, `customer.country`) → cầu nối document → phân tích.

## ✅ Tự kiểm tra
- [ ] Kể 4 họ NoSQL + use case mỗi loại
- [ ] Embedding vs referencing; "model theo access pattern"
- [ ] So sánh SQL vs NoSQL (schema, scale, giao dịch)
- [ ] Giải thích CAP (vì sao chỉ 2/3) và CP vs AP; ACID vs BASE
- [ ] Vai trò NoSQL trong bức tranh DE (nguồn vận hành, không thay OLAP)

➡️ Tiếp theo: [[00-phase2-summary]] — chốt Phase 2.
