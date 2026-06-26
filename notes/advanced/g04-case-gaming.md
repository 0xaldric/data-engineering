# G04 — Case: Gaming Telemetry Platform

> Game gửi telemetry người chơi: real-time leaderboard, A/B test, anti-cheat, retention. Khung [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: track player events (login, match, purchase, level-up, item); real-time **leaderboard**; A/B test (balance/monetization); **anti-cheat** (phát hiện bất thường); analytics retention/economy.
- **Scale**: triệu player đồng thời, hàng triệu event/giây ở peak (game hot).
- **Latency**: leaderboard & anti-cheat ~giây; analytics batch.
- **Đặc thù**: bursty (giờ vàng), sessionization (match/session), economy (virtual currency phải chính xác như tiền).

## 2. Kiến trúc
```
Game clients/servers ──► Kafka "events" (partition by player/match)
                            │
        ┌───────────────────┼─────────────────────┐
        ▼ real-time          ▼                      ▼ batch
  Stream proc:          Anti-cheat (stateful:    S3 BRONZE → Spark/dbt
  - leaderboard         feature bất thường       SILVER: sessionize match/session
    (Redis sorted set)  per player) → flag       GOLD: retention, DAU/MAU, economy, A/B
  - real-time counters  
        │                                              │
  dashboard live                                 BI + A/B analysis + ML (churn/cheat model)
```

## 3. Tech choices & trade-off
- **Leaderboard**: Redis **sorted set** (ZADD/ZRANGE) — O(log n) update/rank, real-time. Không dùng warehouse (quá chậm cho mỗi update).
- **Anti-cheat**: stream processing stateful (giống fraud — [[c03-case-fraud]]): feature per player (tốc độ kill, headshot %, tài nguyên/giờ) trong cửa sổ → flag bất thường → review/ban.
- **Economy (virtual currency)**: phải chính xác như fintech ([[c07-case-fintech]]) — idempotency, audit, không tạo/mất currency. Ledger cho giao dịch in-game.
- **Sessionization**: match = session tự nhiên; player session (gap > N phút). [[a01-sql-gaps-islands]].

## 4. Scale & failure
- Partition Kafka theo player_id (sessionization + thứ tự per player) hoặc match_id.
- Bursty giờ vàng → Kafka buffer + auto-scale consumer; backpressure.
- At-least-once → dedup event theo id (đếm sai = leaderboard/economy sai).
- Hot match/streamer (nhiều viewer event) → skew.

## 5. Analytics đặc thù game
- **Retention** (D1/D7/D30 — sống còn với game) — retention curve ([[g02-sql-interview-4]]).
- **A/B test**: gán variant, đo engagement/monetization, ý nghĩa thống kê.
- **Funnel** (tutorial → level X → purchase).
- **Economy balance**: sink/source currency (lạm phát ảo?).

## 6. DQ & observability
- Event volume anomaly (drop = client/tracking lỗi; spike = exploit/bot).
- Economy invariant (tổng currency hợp lệ — như reconciliation).
- Leaderboard consistency (eventual OK, nhưng không sai lớn).

## Câu hỏi đào sâu
- "Leaderboard real-time triệu player?" → Redis sorted set, không query warehouse mỗi lần.
- "Anti-cheat?" → stateful stream features + ML, giống fraud.
- "Virtual currency chính xác?" → ledger + idempotency như fintech.

## ✅ "Tự mò"
🔭 Thiết kế: Redis sorted set cho leaderboard (lệnh ZADD/ZREVRANGE); feature anti-cheat (kill/phút, accuracy) tính theo cửa sổ; retention D1/D7/D30 SQL.

➡️ Tiếp: [[g05-case-healthcare]].
