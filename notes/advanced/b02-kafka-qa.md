# B02 — Streaming & Kafka Q&A

> Câu hỏi phỏng vấn Kafka/streaming + đáp án. Chi tiết: [[46-kafka-core]]→[[52-lambda-kappa]].

**Q: Topic / partition / offset?**
A: Topic = luồng event có tên; chia thành **partition** (đơn vị song song + thứ tự, log append-only); offset = vị trí message trong partition.

**Q: Key quyết định gì?**
A: `hash(key) % num_partitions` → partition. Cùng key→cùng partition→**giữ thứ tự** cho key đó. Không key → round-robin (mất đảm bảo thứ tự theo entity).

**Q: Thứ tự đảm bảo ở đâu?**
A: Chỉ **trong một partition**, không phải toàn topic. Muốn thứ tự theo entity → dùng key = entity id.

**Q: Consumer group?**
A: Nhiều consumer cùng `group.id` chia nhau partition (mỗi partition → 1 consumer trong group). #consumer ≤ #partition. Nhiều group đọc cùng topic độc lập (pub-sub).

**Q: Rebalancing?**
A: Khi consumer vào/ra group, Kafka phân bổ lại partition. Tiêu thụ tạm dừng (stop-the-world) → giảm thiểu (cooperative rebalance, static membership).

**Q: 3 delivery semantics?**
A: **At-most-once** (commit offset trước xử lý → có thể mất); **at-least-once** (commit sau → có thể trùng, phổ biến); **exactly-once** (idempotent producer + transactions). Thực dụng: at-least-once + **sink idempotent** (upsert).

**Q: Exactly-once thật sự đạt thế nào?**
A: Idempotent producer (chống ghi trùng khi retry) + transactions (đọc-xử lý-ghi nguyên tử trong Kafka). Với sink ngoài (DB/lake) vẫn cần idempotency phía sink (upsert/MERGE theo key).

**Q: acks?**
A: `acks=0` (bắn-quên, có thể mất), `acks=1` (leader nhận), `acks=all` (mọi ISR nhận, bền nhất). Production thường all + replication.factor=3.

**Q: Retention vs Compaction?**
A: Retention xoá message cũ theo time/size (hợp event stream). **Compaction** giữ message **mới nhất mỗi key** (hợp changelog/state — bảng trạng thái hiện tại).

**Q: Event time vs Processing time? Watermark?**
A: Event time = lúc xảy ra (trong message); processing time = lúc xử lý (lệch do trễ). **Watermark** = ngưỡng chờ data trễ tối đa; sau đó đóng cửa sổ & bỏ data trễ hơn. Cân bằng chính xác vs độ trễ/RAM.

**Q: Các loại window?**
A: Tumbling (cố định, không chồng), sliding (cố định, chồng nhau), session (gom theo hoạt động, đóng khi im lặng > gap).

**Q: Stateful vs stateless?**
A: Stateless (map/filter, không nhớ). Stateful (window/join stream/dedup) cần lưu state + checkpoint; watermark dọn state cũ tránh phình.

**Q: CDC là gì? Vì sao log-based?**
A: Change Data Capture bắt mọi INSERT/UPDATE/DELETE. Log-based (đọc WAL/binlog qua Debezium) bắt cả DELETE, nhẹ nguồn, gần real-time — hơn polling (bỏ sót delete, tải DB).

**Q: Lambda vs Kappa?**
A: Lambda = batch layer (chính xác, trễ) + speed layer (real-time) → trùng logic. Kappa = chỉ streaming + replay log để tính lại → một code path. Lakehouse hợp nhất batch/stream.

**Q: Spark Streaming vs Flink?**
A: Spark = micro-batch (~giây, hệ lakehouse/ML); Flink = true streaming (~ms, stateful mạnh, exactly-once). Latency thấp + stateful phức tạp → Flink.

**Q: Outbox pattern?**
A: Ghi event vào bảng `outbox` **cùng transaction** với thay đổi nghiệp vụ; CDC đọc outbox → Kafka. Tránh "dual write" không nguyên tử.

## ✅ "Tự mò"
🔭 Vẽ sơ đồ một pipeline streaming (producer→Kafka→processor→sink) và chú thích delivery semantics ở mỗi mũi tên.

➡️ Tiếp: [[b03-dbt-qa]].
