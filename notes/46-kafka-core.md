# 46 — Apache Kafka: Core Concepts ⭐

> Kafka = nền tảng **distributed event streaming**: một "commit log" phân tán, bền, scale ngang. Xương sống của hầu hết hệ streaming.

## Mô hình cốt lõi
```
Producers ──► [ TOPIC: orders ]                         ──► Consumers
                ├ Partition 0: [m0][m1][m2][m3]...          (đọc theo offset)
                ├ Partition 1: [m0][m1][m2]...
                └ Partition 2: [m0][m1][m2][m3][m4]...
```
- **Topic**: một luồng sự kiện có tên (vd `orders`, `clicks`). Như "bảng" của streaming.
- **Partition** ⭐: topic chia thành nhiều partition — đơn vị **song song & thứ tự**. Mỗi partition là một **log chỉ-ghi-thêm** (append-only), có thứ tự.
- **Offset**: vị trí (số tăng dần) của message trong một partition. Consumer nhớ offset để biết đã đọc tới đâu.
- **Message**: `(key, value, timestamp, headers)`. Value thường Avro/JSON ([[10-json-avro]]).

## Thứ tự & key
- Thứ tự **chỉ đảm bảo trong MỘT partition**, không phải toàn topic.
- **Key quyết định partition**: `hash(key) % num_partitions`. Cùng key → cùng partition → **giữ thứ tự cho key đó** (vd mọi event của `order_id=5` vào cùng partition → đúng thứ tự đặt→trả).
- Không có key → phân phối round-robin (mất đảm bảo thứ tự theo entity).

## Broker, cluster, replication
- **Broker**: một server Kafka. **Cluster** = nhiều broker.
- **Replication**: mỗi partition có 1 **leader** + N **follower** (bản sao trên broker khác). Producer/consumer làm việc với leader; follower sao chép để chịu lỗi.
- **ISR** (In-Sync Replicas): các follower bắt kịp leader. Leader chết → một ISR lên leader → **không mất dữ liệu** (nếu cấu hình đúng).
- **`replication.factor=3`** là chuẩn production (chịu mất 2 broker).

## Producer
- `acks=0` (bắn-quên, nhanh, có thể mất), `acks=1` (leader nhận), **`acks=all`** (mọi ISR nhận → bền nhất).
- Batch + nén (snappy/zstd/lz4) để throughput cao.
- **Idempotent producer** (`enable.idempotence=true`): tránh ghi trùng khi retry → nền cho exactly-once ([[47-kafka-consumers]]).

## Vì sao Kafka mạnh
- **Bền & replay được**: message giữ theo **retention** (vd 7 ngày) — consumer có thể đọc lại từ offset cũ (khác message queue truyền thống xoá sau khi đọc). Đây là lý do Kafka làm "source of truth" cho event ([[52-lambda-kappa]] Kappa).
- **Scale ngang**: thêm partition/broker → tăng throughput.
- **Nhiều consumer độc lập**: mỗi nhóm consumer đọc cùng topic mà không ảnh hưởng nhau (pub-sub).
- Ghi tuần tự vào log đĩa → cực nhanh (tận dụng page cache, zero-copy).

## ⚠️ Cạm bẫy
- Tăng partition để scale nhưng **mất thứ tự toàn cục** — thiết kế key cẩn thận.
- Quá nhiều partition → overhead (rebalance chậm, nhiều file).
- `acks=1` + leader chết trước khi follower sao → **mất message**.
- Đổi số partition sau này làm hỏng ánh xạ key→partition.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Topic/partition/offset/broker là gì; partition cho gì (song song + thứ tự).
- [ ] Key → partition; thứ tự đảm bảo ở đâu.
- [ ] Replication/ISR/leader; `acks` các mức.
- [ ] Vì sao Kafka replay được (retention) & khác queue truyền thống.
- 🔭 *Tự mò:* `docker compose` Kafka (image bitnami/confluent), dùng `kafka-console-producer/consumer` gửi/nhận message một topic; hoặc Python `confluent-kafka`/`kafka-python` produce/consume.

➡️ Tiếp: [[47-kafka-consumers]].
