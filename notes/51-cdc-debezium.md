# 51 — Change Data Capture (CDC) & Debezium

> Bài toán: đồng bộ **mọi thay đổi** của database vận hành (Postgres) sang warehouse/lake **gần real-time**, không làm nặng DB nguồn. Lời giải: **CDC**.

## CDC là gì?
**Change Data Capture** = bắt mọi `INSERT/UPDATE/DELETE` ở DB nguồn và phát thành dòng sự kiện.
Hai cách:
- **Query-based (polling)**: định kỳ `SELECT ... WHERE updated_at > last`. ❌ Bỏ sót DELETE, bỏ sót thay đổi trung gian, tải DB, trễ.
- **Log-based** ⭐: đọc **transaction log** của DB (Postgres **WAL**, MySQL **binlog**, Mongo oplog). ✅ Bắt **mọi** thay đổi kể cả DELETE, **không** query bảng (nhẹ nguồn), gần real-time, đúng thứ tự. Đây là cách chuẩn.

## Debezium
Bộ **CDC connector** (chạy trên Kafka Connect — [[48-kafka-ecosystem]]) đọc log DB → phát event vào Kafka topic.
```
Postgres ──(WAL)──► Debezium (Kafka Connect source) ──► Kafka topic "dbserver.public.orders"
                                                              │
                                                              ▼
                                          Sink (S3/Delta) hoặc stream processing → lakehouse
```
Mỗi event mô tả thay đổi: `op` (c=create, u=update, d=delete), `before`, `after`, metadata (LSN, ts, table). Consumer dựng lại trạng thái bảng ở đích (thường **upsert/MERGE** theo key + xử lý delete — [[40-pipeline-patterns]], [[34-delta-lake]]).

## Vì sao CDC quan trọng cho DE
- **Near-real-time sync** OLTP → lakehouse/warehouse mà không chạy batch dump nặng mỗi đêm.
- Bắt được **DELETE** (batch query-based hay bỏ sót → warehouse "ma").
- Ít tải DB nguồn (đọc log, không quét bảng).
- Nguồn cho streaming analytics, search index, cache invalidation, microservice sync.

## Outbox pattern
Vấn đề: service vừa ghi DB vừa muốn phát event Kafka — làm 2 việc nguyên tử thế nào (tránh "ghi DB xong, gửi Kafka fail")? **Outbox**: trong **cùng transaction** với thay đổi nghiệp vụ, ghi thêm một dòng vào bảng `outbox`. CDC (Debezium) đọc bảng `outbox` → phát Kafka. → Event và thay đổi DB **nguyên tử** (cùng transaction), không mất/trùng. Tránh "dual write" không tin cậy.

## Event sourcing (liên quan)
Thay vì lưu **trạng thái hiện tại**, lưu **chuỗi sự kiện** bất biến (OrderPlaced, ItemAdded, OrderPaid). Trạng thái = replay sự kiện. Kafka (retention/compaction) hợp làm event store. CDC là "event sourcing nhẹ" áp lên DB CRUD sẵn có.

## ⚠️ Cạm bẫy
- Polling thay log-based → bỏ sót delete/thay đổi trung gian, tải DB.
- Sink không idempotent → CDC at-least-once gây trùng (phải upsert theo key).
- Schema thay đổi ở nguồn → cần Schema Registry + xử lý evolution ([[48-kafka-ecosystem]], [[10-json-avro]]).
- Initial snapshot (bảng lớn) + streaming changes phải nối liền mạch (Debezium lo, nhưng cần hiểu).
- Dual write (ghi DB + Kafka riêng) → dùng **outbox** thay thế.

## ✅ Tự kiểm tra & "tự mò"
- [ ] CDC là gì; query-based vs log-based (vì sao log-based thắng).
- [ ] Debezium đọc WAL → Kafka → sink; event có before/after/op.
- [ ] Vì sao sink cần upsert/idempotent.
- [ ] Outbox pattern giải quyết dual-write thế nào.
- 🔭 *Tự mò:* docker-compose Postgres + Kafka + Debezium connect; bật logical replication Postgres; `INSERT/UPDATE/DELETE` một bảng → xem event xuất hiện trong Kafka topic.

➡️ Tiếp: [[52-lambda-kappa]].
