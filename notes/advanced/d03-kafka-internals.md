# D03 — Kafka Internals deep

> Sâu hơn [[46-kafka-core]]→[[48-kafka-ecosystem]]: bên trong Kafka để tuning & trả lời "vì sao Kafka nhanh/bền".

## Storage: log segments
Mỗi partition = một **log** trên đĩa, chia thành **segment** files:
```
partition-0/
├── 00000000000000000000.log     ← data (messages)
├── 00000000000000000000.index   ← offset → vị trí byte
├── 00000000000000000000.timeindex
└── 00000000000000099999.log     ← segment mới khi segment cũ đầy
```
- Ghi **append-only tuần tự** vào segment active → cực nhanh (đĩa tuần tự ~ RAM ngẫu nhiên).
- **Page cache** OS: Kafka đọc/ghi qua page cache (không tự cache trong JVM heap) → tận dụng RAM OS, ít GC.
- **Zero-copy** (`sendfile`): gửi data từ page cache thẳng ra socket, không copy qua app → throughput cao.
- Retention/compaction xoá theo **segment** (xem [[48-kafka-ecosystem]]).

## Vì sao Kafka nhanh (tóm)
Sequential I/O + page cache + zero-copy + batching + nén → throughput rất cao trên phần cứng thường.

## Replication protocol
- Mỗi partition: 1 **leader** + N **follower**. Producer/consumer chỉ làm việc leader.
- Follower **fetch** từ leader (như consumer) để sao chép.
- **ISR** (In-Sync Replicas): follower bắt kịp leader (trong `replica.lag.time.max.ms`).
- **High Watermark (HW)**: offset cao nhất đã được **mọi ISR** sao chép → consumer chỉ đọc tới HW (đảm bảo đọc dữ liệu đã bền). Message > HW chưa "committed".
- **Leader epoch**: tránh mất/phân kỳ dữ liệu khi leader đổi (sửa lỗi truncation cũ).
- Leader chết → controller chọn leader mới từ ISR → không mất data (nếu `acks=all` + `min.insync.replicas≥2`).

## ⭐ Exactly-once semantics (EOS) — sâu
3 mảnh ghép:
1. **Idempotent producer** (`enable.idempotence=true`): mỗi producer có PID + sequence number/partition → broker phát hiện & bỏ **ghi trùng** khi retry. Chống duplicate do retry.
2. **Transactions** (`transactional.id`): ghi nhiều partition + commit offset **nguyên tử** (all-or-nothing). Dùng cho "consume-process-produce" (đọc topic A, xử lý, ghi topic B + commit offset trong 1 transaction).
3. **Consumer `isolation.level=read_committed`**: chỉ đọc message đã commit (bỏ qua message của transaction abort/đang mở).
→ EOS chỉ trọn vẹn cho luồng **Kafka→Kafka**. Sink ngoài (DB/lake) vẫn cần idempotency phía sink ([[47-kafka-consumers]]).

## Tuning chính
| Mục tiêu | Tham số |
|----------|---------|
| Throughput producer | `batch.size`↑, `linger.ms`↑ (gom batch), `compression.type` (lz4/zstd) |
| Độ bền | `acks=all`, `min.insync.replicas=2`, `replication.factor=3` |
| Độ trễ | `linger.ms`↓ |
| Scale tiêu thụ | tăng **partitions** (≥ #consumer) |
| Consumer throughput | `fetch.min.bytes`, `max.poll.records` |
| Tránh rebalance giả | `max.poll.interval.ms`↑, xử lý nhanh / cooperative rebalance |

## Số partition — chọn thế nào
- Nhiều partition → throughput & song song cao hơn, **nhưng**: nhiều file/handle, rebalance chậm, end-to-end latency tăng, mỗi partition cần RAM ở broker.
- Quy tắc thô: partition ≥ peak throughput / throughput-một-partition; và ≥ #consumer mong muốn. Khó **giảm** partition sau (vỡ ánh xạ key→partition) → chọn dư có tính toán.

## ⚠️ Cạm bẫy
- `acks=1` + leader chết trước khi follower sao → **mất** message.
- Tưởng idempotent producer = exactly-once end-to-end (sink ngoài vẫn cần idempotency).
- Quá nhiều partition → latency & overhead tăng.
- Đổi số partition của topic có key → mất thứ tự/ánh xạ.

## ✅ "Tự mò"
🔭 Kafka qua Docker: tạo topic replication.factor=3, set `acks=all` + `min.insync.replicas=2`, kill 1 broker xem vẫn ghi/đọc được; bật idempotent producer.

➡️ Tiếp: [[d04-snowflake]].
