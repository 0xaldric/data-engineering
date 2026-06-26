# 48 — Kafka Ecosystem: Connect, Schema Registry, Retention

> Quanh Kafka core có hệ sinh thái biến nó thành nền tảng dữ liệu hoàn chỉnh.

## Kafka Connect — ingest/egress không cần code
Framework chạy **connector** để bơm dữ liệu vào/ra Kafka mà không tự viết producer/consumer:
- **Source connector**: hệ ngoài → Kafka (vd Debezium đọc Postgres → topic, [[51-cdc-debezium]]; JDBC source).
- **Sink connector**: Kafka → hệ ngoài (vd S3 sink ghi parquet, Elasticsearch, JDBC sink, Snowflake).
- Chạy distributed, có offset management, retry, scaling sẵn → đỡ viết glue code.
→ Pattern phổ biến: **CDC source (Debezium) → Kafka → S3/lakehouse sink** = đồng bộ DB sang lake gần real-time.

## Schema Registry — hợp đồng dữ liệu cho stream ⭐
Message Kafka là bytes; producer/consumer cần thống nhất **schema**. **Schema Registry** lưu schema (thường **Avro**, cũng Protobuf/JSON Schema) và gán ID:
- Producer đăng ký schema → gửi message kèm **schema ID** (nhỏ gọn).
- Consumer lấy schema theo ID để giải mã.
- **Kiểm tra tương thích** khi đăng ký schema mới (backward/forward/full — xem [[10-json-avro]]) → chặn producer đẩy schema phá vỡ consumer. Đây là **data contract** cho streaming.

## Retention vs Compaction ⭐
Kafka giữ message theo chính sách:
- **Retention theo time/size**: xoá message cũ hơn `retention.ms` (vd 7 ngày) hoặc vượt `retention.bytes`. Hợp **event stream** (clicks, logs) — chỉ cần dữ liệu gần đây + replay trong cửa sổ.
- **Log compaction** (`cleanup.policy=compact`): giữ **message MỚI NHẤT cho mỗi key**, xoá bản cũ cùng key. Biến topic thành "bảng trạng thái hiện tại theo key" (vd profile user mới nhất). Dùng cho **changelog / state**.
```
Trước compaction:  (k1,v1)(k2,v1)(k1,v2)(k1,v3)(k2,v2)
Sau compaction:    (k1,v3)(k2,v2)        ← chỉ bản mới nhất mỗi key
```

## Kafka Streams & ksqlDB
Xử lý stream **ngay trong Kafka** (không cần Spark/Flink):
- **Kafka Streams**: thư viện Java để build app stream-processing (map/filter/join/window/aggregate) đọc-ghi topic. State lưu trong local + changelog topic.
- **ksqlDB**: viết stream processing bằng **SQL** trên Kafka (`CREATE STREAM ... SELECT ...`). Nhanh để prototype.
→ Cùng họ với Spark Structured Streaming/Flink ([[49-stream-processing]], [[50-flink]]) nhưng gắn chặt Kafka, nhẹ hơn.

## ⚠️ Cạm bẫy
- Không dùng Schema Registry → schema trôi, consumer vỡ âm thầm.
- Nhầm retention với compaction (event stream vs changelog).
- Retention quá ngắn → mất khả năng replay/backfill từ Kafka.
- Tự viết connector trong khi đã có connector sẵn (tốn công, ít tin cậy hơn).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Kafka Connect source vs sink; pattern CDC→Kafka→lake.
- [ ] Schema Registry để làm gì; tương thích schema = data contract.
- [ ] Retention vs compaction; khi nào dùng compaction.
- [ ] Kafka Streams/ksqlDB là gì.
- 🔭 *Tự mò:* với Kafka local, tạo topic `cleanup.policy=compact`, gửi nhiều message cùng key, đọc lại sau compaction xem chỉ còn bản mới nhất.

➡️ Tiếp: [[49-stream-processing]].
