# 🏁 Phase 6 — Tổng kết: Streaming & Real-time (Kafka)

> Notes-first. Trọng tâm: Kafka + xử lý dòng dữ liệu vô hạn + CDC.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| T056 | Streaming vs batch & event-driven | [45](45-streaming-intro.md) |
| T057 | Kafka core | [46](46-kafka-core.md) |
| T058 | Consumer groups & delivery semantics | [47](47-kafka-consumers.md) |
| T059 | Kafka ecosystem (Connect/Schema Registry/retention) | [48](48-kafka-ecosystem.md) |
| T060 | Stream processing (windowing/watermark) | [49](49-stream-processing.md) |
| T061 | Flink & engines | [50](50-flink.md) |
| T062 | CDC & Debezium | [51](51-cdc-debezium.md) |
| T063 | Lambda vs Kappa | [52](52-lambda-kappa.md) |

## 📑 Cheat-Sheet Streaming
- **Batch** (bounded, theo lịch) vs **streaming** (unbounded, ngay khi tới). Chọn theo yêu cầu latency.
- **Kafka**: topic → **partition** (đơn vị song song + thứ tự) → offset. **Key → partition** (giữ thứ tự cho key). Replication + ISR + `acks=all` để bền. Replay được (retention).
- **Consumer group** chia partition (#consumer ≤ #partition); rebalancing; commit offset.
- **Delivery**: at-most / **at-least** (mặc định) / exactly-once. Thực dụng = at-least-once + **sink idempotent** (upsert).
- **Ecosystem**: Connect (source/sink, Debezium), **Schema Registry** (data contract Avro), retention vs **compaction** (changelog theo key), Kafka Streams/ksqlDB.
- **Stream processing**: windowing (tumbling/sliding/session); **event time + watermark** (xử lý late data, dọn state); stateful + checkpoint → exactly-once.
- **Flink** (true streaming, ms, stateful mạnh) vs **Spark Structured Streaming** (micro-batch, ~giây, hệ lakehouse). Khái niệm chung: watermark/state/checkpoint/backpressure.
- **CDC** (log-based, Debezium WAL→Kafka) đồng bộ OLTP→lake near-real-time; bắt cả DELETE; **outbox** tránh dual-write.
- **Lambda** (batch+speed, trùng logic) vs **Kappa** (chỉ stream + replay log); lakehouse hợp nhất batch/stream.

## ✅ Self-assessment Phase 6
- [ ] Batch vs streaming; event-driven architecture.
- [ ] Kafka: partition/offset/key/replication; vì sao replay được.
- [ ] Consumer group & 3 delivery semantics; idempotent sink.
- [ ] Connect/Schema Registry/retention vs compaction.
- [ ] Windowing + event time + watermark + state.
- [ ] Spark Streaming vs Flink.
- [ ] CDC/Debezium/outbox.
- [ ] Lambda vs Kappa.

## 🔭 Để "tự mò"
1. docker-compose Kafka; `kafka-console-producer/consumer`; Python `confluent-kafka` produce/consume; thử 2 consumer cùng group.
2. Topic compaction: gửi nhiều message cùng key, xem chỉ còn bản mới nhất.
3. (Java/Spark) Structured Streaming từ rate/kafka source + `window()` + `withWatermark`.
4. docker-compose Postgres+Kafka+Debezium: INSERT/UPDATE/DELETE → xem CDC event.

## ➡️ Tiếp theo: Phase 7 — Cloud & Infrastructure
Docker, AWS data stack (S3/Glue/Athena/EMR/Kinesis/Redshift/Lambda), Terraform (IaC), CI/CD. (notes-first)
