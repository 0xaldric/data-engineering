# 45 — Streaming vs Batch & Event-driven

> Đến giờ pipeline đều **batch** (xử lý theo lô, theo lịch). **Streaming** xử lý dữ liệu **liên tục, ngay khi tới**.

## Batch vs Streaming
| | **Batch** | **Streaming** |
|--|-----------|----------------|
| Dữ liệu | bounded (hữu hạn, một lô) | unbounded (vô hạn, dòng sự kiện) |
| Khi xử lý | theo lịch (mỗi giờ/ngày) | ngay khi event tới (giây/ms) |
| Latency | cao (phút–giờ) | thấp (ms–giây) |
| Throughput | rất cao/lô | cao, liên tục |
| Độ phức tạp | thấp hơn | cao (state, late data, ordering) |
| Công cụ | Spark batch, dbt, Airflow | Kafka, Spark Streaming, Flink |
| Ví dụ | báo cáo ngày, ETL warehouse | fraud real-time, dashboard live, alert |

→ Không phải "streaming tốt hơn batch". Chọn theo **yêu cầu latency**: cần kết quả trong vài giây → streaming; báo cáo cuối ngày → batch (đơn giản & rẻ hơn).

## Event-driven architecture
Thay vì hệ thống hỏi nhau ("polling"), các thành phần **phát sự kiện** (event) và thành phần khác **phản ứng**:
```
Order Service ──(event: OrderPlaced)──► [Kafka topic] ──► Inventory Service
                                                      ├──► Email Service
                                                      └──► Analytics (stream → lakehouse)
```
- **Decoupled**: producer không cần biết ai tiêu thụ; thêm consumer mới không sửa producer.
- **Kafka** là "xương sống" (event backbone): producer ghi event vào topic, nhiều consumer đọc độc lập.
- Một event = "một sự thật đã xảy ra" (OrderPlaced, PaymentFailed) — bất biến.

## Use case cần real-time
- **Fraud detection**: chặn giao dịch gian lận trong mili-giây.
- **Monitoring/alerting**: phát hiện lỗi hệ thống ngay.
- **Real-time dashboard**: doanh thu/đơn cập nhật trực tiếp.
- **Recommendation**: cập nhật gợi ý theo hành vi vừa xảy ra.
- **CDC**: đồng bộ thay đổi DB sang warehouse gần real-time ([[51-cdc-debezium]]).

## Khái niệm sẽ gặp
- **Event time vs processing time**: lúc sự kiện *xảy ra* vs lúc hệ thống *xử lý* (lệch do trễ mạng) → cần **watermark** ([[49-stream-processing]]).
- **Stateful**: tính toán cần nhớ quá khứ (đếm theo cửa sổ, join 2 stream) → cần lưu **state**.
- **Exactly-once**: mỗi event ảnh hưởng kết quả đúng 1 lần (khó nhất) — [[47-kafka-consumers]].

## ✅ Tự kiểm tra & "tự mò"
- [ ] Batch vs streaming (bounded/unbounded, latency); chọn theo gì.
- [ ] Event-driven architecture & vì sao decoupled.
- [ ] Kể use case cần real-time.
- [ ] Event time vs processing time là gì.
- 🔭 *Tự mò:* nghĩ pipeline e-commerce đã làm — phần nào hợp batch (báo cáo ngày), phần nào hợp streaming (cảnh báo đơn giá trị lớn ngay khi đặt)?

➡️ Tiếp: [[46-kafka-core]].
