# 47 — Consumer Groups & Delivery Semantics ⭐

> Cách Kafka chia tải đọc cho nhiều consumer, và đảm bảo "mỗi message được xử lý mấy lần".

## Consumer & Consumer Group ⭐
- **Consumer**: đọc message từ partition theo offset.
- **Consumer group**: nhiều consumer cùng `group.id` **chia nhau** các partition của topic để xử lý song song.
```
Topic orders (3 partitions)      Consumer Group "billing"
  P0 ─────────────────────────►  Consumer A   (đọc P0)
  P1 ─────────────────────────►  Consumer B   (đọc P1)
  P2 ─────────────────────────►  Consumer C   (đọc P2)
```
Quy tắc: **mỗi partition chỉ giao cho 1 consumer trong group** tại một thời điểm.
- #consumer ≤ #partition (thừa consumer → ngồi không). Muốn scale tiêu thụ → tăng partition.
- **Nhiều group** đọc cùng topic độc lập (group "billing" và group "analytics" mỗi nhóm đọc trọn topic) → pub-sub.

## Rebalancing
Khi consumer vào/ra group (thêm/chết/scale), Kafka **phân bổ lại** partition cho các consumer còn lại. Trong lúc rebalance, tiêu thụ **tạm dừng** (stop-the-world) → nên giảm thiểu (dùng cooperative rebalancing, static membership). Consumer chết → partition của nó giao cho consumer khác → **không mất** (đọc tiếp từ offset đã commit).

## Offset & commit
Consumer **commit offset** để đánh dấu "đã xử lý tới đây". Khi restart, đọc tiếp từ offset đã commit.
- **Auto-commit** (định kỳ): tiện nhưng dễ sai (commit trước khi xử lý xong → mất; sau → có thể trùng).
- **Manual commit**: commit **sau khi** xử lý thành công → kiểm soát semantics.

## ⭐ Delivery semantics (rất hay bị hỏi)
| Mức | Nghĩa | Cách đạt | Rủi ro |
|-----|-------|----------|--------|
| **At-most-once** | mỗi message xử lý **≤1** lần | commit offset **trước** khi xử lý | **mất** message nếu crash giữa chừng |
| **At-least-once** | **≥1** lần (mặc định phổ biến) | commit **sau** khi xử lý | **trùng** message nếu crash sau xử lý, trước commit |
| **Exactly-once** | đúng **1** lần | idempotent producer + **transactions** + consumer đọc-xử-lý-ghi trong 1 transaction | phức tạp, chậm hơn |

→ Thực tế: **at-least-once + idempotent consumer** là cách phổ biến & thực dụng nhất. "Exactly-once" của Kafka (EOS) dùng transaction cho luồng Kafka→xử lý→Kafka; với sink ngoài (DB/lakehouse) thường vẫn cần **idempotency phía sink** (upsert/MERGE — [[40-pipeline-patterns]], [[34-delta-lake]]).

## Idempotency phía consumer
Vì at-least-once có thể trùng, consumer/sink nên **idempotent**: dùng key duy nhất (event_id) + upsert/dedup → xử lý lại không nhân đôi. Đây là cùng nguyên tắc idempotency của batch ([[40-pipeline-patterns]]).

## ⚠️ Cạm bẫy
- Auto-commit + xử lý chậm → commit trước khi xử lý xong → mất message khi crash.
- Coi at-least-once là exactly-once → dữ liệu trùng âm thầm.
- Quá nhiều consumer > partition → consumer thừa vô dụng.
- Xử lý nặng/lâu trong consumer → rebalance tưởng nó chết → vòng lặp rebalance.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Consumer group chia partition thế nào; #consumer vs #partition.
- [ ] Rebalancing là gì, ảnh hưởng gì.
- [ ] Commit offset trước/sau xử lý → semantics nào.
- [ ] 3 delivery semantics; vì sao at-least-once + idempotent là thực dụng.
- 🔭 *Tự mò:* chạy 2 consumer cùng group trên topic 2 partition → thấy mỗi consumer 1 partition; tắt 1 consumer → partition chuyển sang consumer kia (rebalance).

➡️ Tiếp: [[48-kafka-ecosystem]].
