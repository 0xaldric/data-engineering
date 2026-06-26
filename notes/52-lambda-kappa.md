# 52 — Lambda vs Kappa Architecture

> Hai kiến trúc tổng hợp batch + streaming. Câu hỏi: làm sao vừa có kết quả real-time vừa có kết quả chính xác/đầy đủ?

## Lambda Architecture
Hai lớp song song, gộp kết quả khi truy vấn:
```
                ┌─► BATCH layer  (xử lý lại TOÀN BỘ dữ liệu, chính xác, trễ)  ─┐
Nguồn (raw log) ┤                                                              ├─► SERVING (gộp) ─► query
                └─► SPEED layer  (streaming, gần real-time, gần đúng)        ─┘
```
- **Batch layer**: tính lại từ toàn bộ dữ liệu lịch sử → **chính xác, đầy đủ** nhưng trễ (chạy định kỳ).
- **Speed layer**: streaming xử lý dữ liệu mới → **real-time** nhưng có thể gần đúng (chưa gồm late data, sửa sau).
- **Serving layer**: gộp kết quả batch (cho quá khứ) + speed (cho hiện tại) khi query.
- ❌ Nhược: **trùng logic** ở 2 nơi (batch & stream) → tốn công, dễ lệch, khó bảo trì.

## Kappa Architecture
Bỏ batch layer — **chỉ streaming**, mọi thứ là stream:
```
Nguồn ─► [ LOG bất biến: Kafka, giữ lâu/đủ ] ─► Stream processing ─► Serving
                         ▲ reprocess: phát lại từ offset đầu khi cần tính lại
```
- Một **code path** duy nhất (streaming) cho cả real-time lẫn "tính lại lịch sử".
- **Reprocess** = phát lại (replay) toàn bộ log từ đầu qua chính job streaming (chạy job mới đọc từ offset 0, ghi sang bảng mới, rồi swap). Nhờ Kafka **giữ & replay được** ([[46-kafka-core]]).
- ✅ Đơn giản hơn (1 logic), ✅ nhất quán. ❌ Phụ thuộc log đủ lớn/giữ đủ lâu; tính lại nặng có thể chậm.

## So sánh
| | **Lambda** | **Kappa** |
|--|-----------|-----------|
| Lớp | batch + speed (2 code path) | chỉ streaming (1 code path) |
| Logic | lặp ở 2 nơi (dễ lệch) | một nơi |
| Tính lại lịch sử | batch layer | replay log |
| Phức tạp vận hành | cao | thấp hơn |
| Phụ thuộc | hệ batch + stream | log bền (Kafka) + engine stream |

## Xu hướng hiện đại
- **Streaming-first / Kappa-style** được ưa hơn khi engine (Flink/Spark) + log (Kafka) + **lakehouse** đủ mạnh.
- **Lakehouse hợp nhất batch & stream**: Delta/Iceberg ([[34-delta-lake]], [[35-table-formats]]) cho cùng một bảng vừa nhận ghi streaming vừa query batch → mờ ranh giới Lambda/Kappa. Spark/Flink "unified batch+stream" cùng một API.
- Thực tế nhiều hệ vẫn lai: streaming cho lớp nóng + batch (dbt) cho lớp phân tích chuẩn hoá — chọn theo yêu cầu, không giáo điều.

## ⚠️ Cạm bẫy
- Lambda: để logic batch & stream lệch nhau → 2 con số khác nhau cho cùng metric.
- Kappa: retention Kafka quá ngắn → không replay/tính lại được.
- Chọn kiến trúc phức tạp khi batch thuần đã đủ (đa số báo cáo không cần real-time).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Vẽ Lambda (batch+speed+serving) & nhược điểm trùng logic.
- [ ] Kappa: vì sao chỉ cần streaming + replay log.
- [ ] So sánh & xu hướng (lakehouse hợp nhất batch/stream).
- [ ] Khi nào KHÔNG cần streaming (batch đủ).
- 🔭 *Tự mò:* với pipeline e-commerce, phác kiến trúc Kappa: Kafka topic `orders` → stream processing (window doanh thu) → Delta gold; muốn tính lại tháng trước thì làm gì?

➡️ Tiếp: [[00-phase6-summary]].
