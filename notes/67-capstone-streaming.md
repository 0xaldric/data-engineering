# 67 — Capstone B: Streaming Pipeline

> Dự án real-time để chứng minh kỹ năng Kafka + stream processing (Phase 6). Khác biệt rõ với batch → portfolio nổi bật.

## Bài toán
"Xử lý dòng sự kiện đơn hàng real-time: tính doanh thu theo cửa sổ 1 phút, phát hiện đơn giá trị bất thường ngay, cập nhật dashboard live." Bonus: đồng bộ DB sang lake bằng CDC.

## Kiến trúc
```
Event generator (producer) ──► Kafka topic "orders"
   (sinh đơn liên tục)              │  (partition theo customer_id giữ thứ tự)
                                    ▼
                    Spark Structured Streaming / Flink / Kafka Streams
                    - windowed aggregation (tumbling 1') + watermark
                    - anomaly: amount > ngưỡng → alert topic
                                    │
                    ┌───────────────┼────────────────┐
                    ▼               ▼                 ▼
              sink: Delta      sink: Postgres     alert (Slack)
              (gold real-time)  (serving)
                    │
                    ▼
              dashboard live (Streamlit/Grafana)

BONUS CDC:  Postgres ──(WAL)──► Debezium ──► Kafka ──► lake (đồng bộ near-real-time)
```

## Thành phần & kiến thức nền
| Phần | Note |
|------|------|
| Kafka topic/partition/key | [[46-kafka-core]] |
| Consumer group, delivery, idempotent sink | [[47-kafka-consumers]] |
| Windowing + watermark + state | [[49-stream-processing]] |
| Spark Streaming vs Flink | [[50-flink]] |
| CDC/Debezium | [[51-cdc-debezium]] |
| Kappa architecture | [[52-lambda-kappa]] |

## docker-compose stack (local, không tốn tiền)
```
services: kafka, zookeeper(/kraft), kafka-ui,
          producer (Python confluent-kafka sinh event),
          spark (hoặc faust/kafka-streams app),
          postgres (sink + nguồn CDC), debezium-connect, streamlit
```
→ Một `docker compose up` dựng cả pipeline streaming để demo ([[54-compose-k8s]]).

## Checklist build
1. **Producer**: Python sinh event đơn hàng (key=customer_id để giữ thứ tự) → topic `orders`. Có thể tái dùng schema dataset e-commerce.
2. **Stream processor**: windowed aggregation (doanh thu/phút theo category) + **watermark** xử lý late data; nhánh anomaly (amount lớn → alert).
3. **Sink idempotent**: ghi Delta/Postgres bằng upsert theo key (at-least-once → idempotent — [[47-kafka-consumers]]).
4. **Dashboard live**: Streamlit/Grafana đọc sink, refresh.
5. **Bonus CDC**: Debezium đọc Postgres WAL → Kafka → đồng bộ lake.
6. **Exactly-once**: checkpoint + sink idempotent.

## Thách thức để "ghi điểm" (và nói khi phỏng vấn)
- Event time vs processing time + watermark (xử lý đơn tới trễ).
- Delivery semantics: vì sao chọn at-least-once + idempotent sink.
- Partition key để giữ thứ tự theo entity.
- Backpressure khi producer nhanh hơn consumer.

## Tiêu chí đạt
- [ ] `docker compose up` chạy producer→Kafka→processor→sink→dashboard.
- [ ] Windowed aggregation đúng, có watermark.
- [ ] Sink idempotent (chạy lại không trùng).
- [ ] (Bonus) CDC Postgres→Kafka hoạt động.
- [ ] README + sơ đồ + giải thích semantics.

## ⚠️ Lưu ý môi trường
Máy này không có Java → Spark/Flink không chạy local. Phương án **chạy được**:
- Dùng **Kafka qua Docker** + **Python consumer** (`confluent-kafka`) làm "stream processor" (tự windowing trong Python với state dict + timer) — đủ minh hoạ.
- Hoặc **Kafka Streams/ksqlDB** trong container. Hoặc cài Java khi làm thật.

## 🔭 "Tự mò"
Bắt đầu: docker-compose Kafka + Python producer/consumer; consumer gom theo cửa sổ 1 phút (dùng event timestamp) in doanh thu. Thêm watermark đơn giản (bỏ event trễ > N giây).

➡️ Tiếp: [[68-capstone-lakehouse]].
