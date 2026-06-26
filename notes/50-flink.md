# 50 — Apache Flink & So sánh engines

> Flink là engine streaming "true" (xử lý từng event), đối thủ chính của Spark Structured Streaming cho real-time độ trễ thấp.

## Flink khác gì?
- **True streaming** (event-at-a-time): xử lý **từng event ngay khi tới**, không gom micro-batch → latency **mili-giây** (Spark micro-batch ~giây).
- **Stateful-first**: state là công dân hạng nhất; quản lý state lớn hiệu quả (RocksDB backend), **checkpoint/savepoint** để khôi phục & nâng cấp không mất state.
- **Exactly-once** mạnh nhờ checkpoint barrier (Chandy-Lamport).
- **Event time & watermark** là lõi (giống khái niệm [[49-stream-processing]] nhưng Flink thiết kế quanh nó từ đầu).
- API: DataStream (thấp, linh hoạt), Table API/Flink SQL (cao). Cũng có batch (unified batch+stream).

## Khi nào Flink > Spark Streaming?
- Cần **latency rất thấp** (sub-giây), per-event.
- **Stateful phức tạp**: CEP (complex event processing), stream-stream join lớn, state khổng lồ.
- Streaming là **trọng tâm** của hệ thống (không chỉ phụ trợ batch).

## Khi nào Spark Structured Streaming > Flink?
- Đã có hệ **Spark/batch** → tái dùng kỹ năng/code, một engine cho cả batch lẫn stream.
- Latency ~giây là đủ (đa số use case).
- Tích hợp lakehouse (Delta) + ML mượt.

## So sánh nhanh
| | **Spark Structured Streaming** | **Apache Flink** |
|--|-------------------------------|------------------|
| Mô hình | micro-batch (có continuous) | true streaming (event-at-a-time) |
| Latency | ~giây | ~mili-giây |
| State | hỗ trợ, đủ dùng | **rất mạnh** (RocksDB, savepoint) |
| Batch + stream | unified (mạnh batch) | unified (mạnh stream) |
| Hệ sinh thái | lớn (Spark/lakehouse/ML) | mạnh real-time, đang lớn |
| Học/việc làm | phổ biến hơn | chuyên real-time |

→ Cũng có **Kafka Streams/ksqlDB** ([[48-kafka-ecosystem]]) cho stream-processing nhẹ gắn Kafka, không cần cụm Spark/Flink riêng.

## Khái niệm chung mọi engine streaming
Dù Spark/Flink/Kafka Streams, ý tưởng giống nhau (học một cái → hiểu cái khác):
- Event time + **watermark** + windowing.
- **State** + checkpoint để fault tolerance & exactly-once.
- Late data handling.
- Backpressure (nguồn nhanh hơn xử lý → cơ chế ghìm).

## ⚠️ Cạm bẫy
- Chọn Flink "vì ngầu" khi micro-batch giây là đủ → tăng độ phức tạp vận hành không cần thiết.
- Bỏ qua quản lý state/savepoint → nâng cấp job mất state.

## ✅ Tự kiểm tra & "tự mò"
- [ ] True streaming vs micro-batch (latency).
- [ ] Vì sao Flink mạnh stateful/exactly-once.
- [ ] Khi nào chọn Flink vs Spark Streaming vs Kafka Streams.
- [ ] Khái niệm chung: watermark, state, checkpoint, backpressure.
- 🔭 *Tự mò:* đọc Flink SQL docs, viết thử một `CREATE TABLE ... WITH ('connector'='kafka')` + `TUMBLE` window query trên giấy; so cú pháp với Spark `window()`.

➡️ Tiếp: [[51-cdc-debezium]].
