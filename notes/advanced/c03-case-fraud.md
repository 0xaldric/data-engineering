# C03 — Case: Real-time Fraud Detection ⭐

> Bài toán streaming + stateful kinh điển. Áp [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: chấm điểm gian lận cho **mỗi giao dịch** ngay khi xảy ra, block/cho qua/đưa review; cảnh báo.
- **Latency**: cực thấp — quyết định trong **< 100ms** (chặn trước khi tiền đi).
- **Scale**: hàng chục nghìn giao dịch/giây ở peak.
- **Consistency**: không được bỏ sót giao dịch (at-least-once); chấm điểm dựa trên feature gần real-time.
- **Accuracy**: cân bằng false positive (chặn nhầm khách thật) vs false negative (bỏ lọt gian lận).

## 2. Kiến trúc
```
Transaction ──► Kafka "transactions" ──► Stream processor (Flink) ──► decision (allow/block/review)
                                              │  tính FEATURES real-time:
                                              │  - #giao dịch của card trong 1' (windowed)
                                              │  - tổng tiền 1h, khoảng cách địa lý vs lần trước
                                              │  - velocity, device mới?
                                              ▼
                                    Feature Store (online: Redis)  ◄── offline features (batch)
                                              │
                                              ▼
                                    Model scoring (rules + ML model) ──► action
                                              │
                          ┌───────────────────┼───────────────────┐
                          ▼                   ▼                   ▼
                    block/alert        Kafka "decisions"     Lake (bronze) → batch:
                                                              huấn luyện model + label gian lận
```

## 3. Tech choices & trade-off
- **Flink** (không Spark micro-batch) vì cần latency **ms, true streaming, stateful mạnh** ([[50-flink]]). Spark Streaming ~giây là quá chậm cho block real-time.
- **Stateful windowed features**: đếm/sum theo card trong cửa sổ trượt → cần state + watermark cho late data ([[49-stream-processing]]).
- **Feature store** (online Redis cho serving ms + offline lake cho training) — đảm bảo **train/serve consistency** (cùng định nghĩa feature).
- **Rules + ML**: rules chặn nhanh case rõ ràng; ML cho tinh vi. Model train offline (batch trên lake), deploy scoring online.
- **Exactly-once-ish**: at-least-once + idempotent action (dedup theo transaction_id) — không block 2 lần ([[47-kafka-consumers]]).

## 4. Scale & failure
- Partition Kafka theo **card_id/account** → giữ thứ tự per entity + scale ngang ([[46-kafka-core]]).
- Flink checkpoint → khôi phục state khi crash không mất feature đang đếm.
- Latency budget: feature lookup + scoring < 100ms → Redis online store, model nhẹ/precomputed.
- Fallback: nếu scoring timeout → rule mặc định (vd cho qua + flag review) để không chặn toàn bộ.

## 5. Feedback loop (quan trọng)
- Quyết định + nhãn gian lận thực tế (chargeback sau này) → lake → **retrain** model định kỳ.
- Concept drift: pattern gian lận đổi → monitor model performance, retrain.

## 6. DQ & observability
- Monitor: tỉ lệ block, false positive rate, latency p99, feature freshness.
- Late/missing transaction → alert (mất giao dịch = mất tiền).
- Feature/label skew giữa train và serve.

## Câu hỏi đào sâu
- "Late data trong windowed features?" → watermark; data quá trễ chấm bằng feature có sẵn tại thời điểm đó.
- "Train/serve skew?" → feature store chung định nghĩa; log feature lúc scoring để train trên đúng cái đã thấy.
- "Vì sao Flink không Spark?" → latency ms + stateful per-event.

## ✅ "Tự mò"
🔭 Phác feature set cho fraud (velocity, geo distance, amount z-score) và viết SQL/pseudo tính chúng theo cửa sổ trượt; nghĩ cái nào online (Redis) vs offline (lake).

➡️ Tiếp: [[c04-case-iot]].
