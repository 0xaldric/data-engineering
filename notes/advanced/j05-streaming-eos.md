# J05 — Deep-dive: Streaming Exactly-once thực chiến

> Exactly-once là khái niệm bị hiểu lầm nhiều nhất. Đây là cách đạt nó **end-to-end** thật sự. Sâu hơn [[47-kafka-consumers]], [[49-stream-processing]], [[d03-kafka-internals]].

## "Exactly-once" thực ra là gì?
Không phải "message chỉ đi qua mạng đúng 1 lần" (bất khả về mặt vật lý — phải retry). Mà là: **mỗi message ảnh hưởng kết quả/state đúng 1 lần**, dù được **gửi/xử lý nhiều lần**. = **at-least-once delivery + idempotent processing/sink**.

## Các điểm có thể MẤT / TRÙNG trong pipeline streaming
```
Producer ──[1]──► Kafka ──[2]──► Stream processor ──[3]──► Sink (DB/lake)
[1] producer retry → TRÙNG (ghi 2 lần khi ack mất)
[2] consumer commit offset trước xử lý → MẤT; sau xử lý → TRÙNG (crash giữa)
[3] xử lý xong, ghi sink, crash trước commit → reprocess → TRÙNG ở sink
```
Phải xử lý cả 3 điểm.

## Giải pháp theo từng điểm
### [1] Producer: Idempotent producer
`enable.idempotence=true` → mỗi producer có PID + sequence number/partition → broker bỏ ghi trùng khi retry. **Chống duplicate do producer retry** ([[d03-kafka-internals]]).

### [2] Kafka→Kafka: Transactions
Cho luồng "consume-process-produce" (đọc topic A → xử lý → ghi topic B):
```
beginTransaction()
  produce(B, kết quả)
  sendOffsetsToTransaction(offset của A)   ← commit offset TRONG transaction
commitTransaction()    ← ghi B + commit offset NGUYÊN TỬ (all-or-nothing)
```
Consumer downstream đặt `isolation.level=read_committed` → chỉ đọc message đã commit. → **EOS trọn vẹn cho Kafka→Kafka**.

### [3] ⭐ Sink ngoài (DB/lake) — điểm khó nhất
Transaction Kafka **không** bao trùm sink ngoài (DB/S3). Phải làm sink **idempotent**:
- **Upsert/MERGE theo unique key** (event_id) → ghi lại = update, không thêm ([[40-pipeline-patterns]], [[34-delta-lake]]).
- **Dedup theo key** trước khi ghi (giữ bản đầu/cuối).
- **Transactional sink**: ghi data + lưu offset đã xử lý trong **cùng transaction** của sink (vd ghi vào Postgres + bảng offset cùng tx) → khôi phục đọc tiếp từ offset đã lưu.
- **Idempotent write** theo deterministic id (vd partition theo event_id → ghi đè).

## Spark/Flink checkpoint
- **Checkpoint** lưu offset Kafka đã đọc + **state** → crash thì khôi phục đúng vị trí + state (windowed aggregation không mất/trùng).
- Spark Structured Streaming: checkpoint + sink hỗ trợ idempotent (Delta) → exactly-once.
- Flink: checkpoint barrier (Chandy-Lamport) + 2-phase commit sink → exactly-once mạnh ([[50-flink]]).

## ⭐ Mẫu hình thực dụng (đa số dùng)
```
Kafka (at-least-once) → stream proc (checkpoint state) → sink IDEMPOTENT (upsert theo event_id)
```
= "effectively exactly-once". Đơn giản & tin cậy hơn cố ép EOS tuyệt đối khắp nơi. **Idempotent sink là chìa khoá** — đừng dựa hoàn toàn vào EOS của Kafka cho sink ngoài.

## ⚠️ Cạm bẫy
- Tưởng idempotent producer = exactly-once end-to-end (sink ngoài vẫn cần idempotency).
- Auto-commit offset → mất/trùng.
- Sink append (không upsert) + at-least-once → trùng âm thầm.
- Quên checkpoint → mất state/exactly-once khi crash.
- State key không deterministic → dedup sai.

## ✅ "Tự mò"
🔭 Thiết kế (trên giấy) luồng order events → tính revenue/phút → ghi Delta: chỉ ra mỗi điểm [1][2][3] xử lý trùng/mất thế nào; sink dùng MERGE theo (window, category) để idempotent.

➡️ Tiếp: [[j06-lakehouse-migration]].
