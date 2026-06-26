# 49 — Stream Processing: Windowing & Watermarks ⭐

> Đọc message từ Kafka mới là bước 1. **Stream processing** = biến đổi/aggregate dòng vô hạn (đếm theo cửa sổ, join stream, phát hiện pattern).

## Spark Structured Streaming
Mở rộng DataFrame API sang stream: viết gần như batch, Spark lo phần "chạy liên tục".
- **Micro-batch**: gom dữ liệu mới thành lô nhỏ (vd mỗi vài giây) rồi xử lý như batch → đơn giản, throughput cao, latency ~giây (đủ cho hầu hết). (Có chế độ continuous latency thấp hơn nhưng ít dùng.)
- Code giống batch:
```python
df = (spark.readStream.format("kafka")
        .option("subscribe", "orders").load())
agg = (df.groupBy(window("event_time", "5 minutes"), "category")
         .agg(sum("amount")))
agg.writeStream.format("delta").outputMode("update").start()
```

## ⭐ Windowing — gộp theo cửa sổ thời gian
Stream vô hạn → phải gộp theo **cửa sổ**:
| Loại | Mô tả | Ví dụ |
|------|-------|-------|
| **Tumbling** | cửa sổ cố định, không chồng | doanh thu mỗi 5 phút (00–05, 05–10) |
| **Sliding** | cố định nhưng **chồng nhau** | trung bình 5 phút, cập nhật mỗi 1 phút |
| **Session** | gom theo hoạt động, đóng khi "im lặng" > gap | phiên truy cập user (đóng sau 30' không click) |

## ⭐ Event time vs Processing time + Watermark
- **Event time**: lúc sự kiện *thực sự xảy ra* (đóng trong message). Đây là cái ta muốn gộp theo.
- **Processing time**: lúc engine *xử lý* — lệch do trễ mạng/queue.
- **Late data**: event time cũ tới muộn (vd điện thoại offline rồi gửi bù).
- **Watermark** ⭐: ngưỡng "ta sẽ chờ dữ liệu trễ tối đa bao lâu". `withWatermark("event_time", "10 minutes")` = chấp nhận trễ ≤10', sau đó **đóng cửa sổ** và bỏ data trễ hơn. Cân bằng giữa **độ chính xác** (chờ lâu) và **độ trễ kết quả + bộ nhớ state** (chờ ngắn).

```
event_time của cửa sổ [10:00–10:05]
watermark 10' → đóng & chốt kết quả lúc event_time đạt 10:15
event tới với time 10:03 lúc watermark đã qua 10:15 → bị bỏ (too late)
```

## Stateful vs Stateless
- **Stateless**: mỗi event xử lý độc lập (map/filter). Không nhớ gì.
- **Stateful**: cần nhớ quá khứ — windowed aggregation, **stream-stream join**, deduplication, running count. Engine lưu **state** (RAM + checkpoint ra đĩa/đối tượng để phục hồi). Watermark giúp **dọn state cũ** (không phình vô hạn).

## Output modes (Spark)
- **append**: chỉ thêm hàng mới (hợp khi cửa sổ đã chốt).
- **update**: cập nhật hàng thay đổi (aggregation đang chạy).
- **complete**: ghi lại toàn bộ bảng kết quả mỗi lần (chỉ cho aggregation nhỏ).

## Fault tolerance
**Checkpoint** + **write-ahead log**: lưu offset Kafka đã đọc + state → crash thì khôi phục, đạt **exactly-once** (kết hợp sink idempotent — [[47-kafka-consumers]]).

## ⚠️ Cạm bẫy
- Gộp theo **processing time** thay vì event time → kết quả sai khi có trễ.
- Không đặt watermark → state phình vô hạn (OOM).
- Watermark quá ngắn → bỏ nhiều data trễ (kết quả thiếu); quá dài → trễ kết quả + tốn RAM.
- Quên checkpoint → mất exactly-once.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Micro-batch của Spark Structured Streaming.
- [ ] Tumbling vs sliding vs session window.
- [ ] Event time vs processing time; watermark cân bằng gì.
- [ ] Stateless vs stateful; vì sao cần dọn state.
- [ ] Output modes; checkpoint cho exactly-once.
- 🔭 *Tự mò:* (cần Java/Spark) `readStream` từ rate source, `groupBy(window(...))`, ghi console; thử thêm `withWatermark` và bơm data trễ.

➡️ Tiếp: [[50-flink]].
