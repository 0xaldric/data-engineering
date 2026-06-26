# H04 — Case: Social Graph / Network Data

> Đặc trưng: dữ liệu **đồ thị** (quan hệ follow/friend), feed generation, traversal ở scale. Khung [[c01-system-design-framework]]. Tiền đề recursive [[a02-sql-pivot-hierarchical]].

## 1. Requirements
- **Functional**: lưu quan hệ (follow/friend), sinh **news feed**, gợi ý kết bạn (friend-of-friend), đếm follower, phát hiện cộng đồng/influencer; analytics engagement.
- **Scale**: tỉ user × tỉ edge (quan hệ); supernode (celebrity nhiều triệu follower).
- **Latency**: feed ~giây; gợi ý batch/near-real-time.
- **Đặc thù**: graph traversal, **fan-out** (feed), skew cực mạnh (influencer).

## 2. Lưu graph: Graph DB vs Relational
| | Graph DB (Neo4j) | Relational (edge table) |
|--|------------------|--------------------------|
| Traversal sâu (FoF, path) | **nhanh** (index-free adjacency) | nhiều self-join, chậm khi sâu |
| Scale ngang khổng lồ | hạn chế hơn | tốt (sharding) |
| Analytics aggregate | yếu hơn | mạnh (SQL) |
- Thực tế lớn (FB/Twitter): **edge table** sharded + cache, không thuần graph DB. `edges(from_id, to_id, type, ts)`.
- Traversal nông (1-2 hop) làm bằng SQL/lookup; sâu → graph engine (GraphX/Pregel) batch.

## 3. ⭐ Feed generation: Fan-out write vs read
Vấn đề kinh điển: user mở app → thấy feed từ N người họ follow. Tính lúc nào?
- **Fan-out on write** (push): khi A đăng post → **ghi vào feed của mọi follower** ngay. Đọc feed = đọc sẵn (nhanh). Nhược: **influencer** (10M follower) → 1 post = 10M ghi (write amplification khủng).
- **Fan-out on read** (pull): feed tính **lúc đọc** (query post của người mình follow, merge). Ghi rẻ. Nhược: đọc đắt (mỗi lần mở app query nhiều).
- **Hybrid** ⭐: push cho user thường; **pull cho influencer** (không fan-out post của celeb tới 10M feed, mà merge lúc đọc). Cân bằng write/read amplification.

## 4. Friend-of-friend (gợi ý)
```sql
-- FoF: bạn của bạn mà chưa là bạn mình (2-hop)
select f2.to_id as suggestion, count(*) as mutual
from edges f1 join edges f2 on f1.to_id = f2.from_id
where f1.from_id = :me and f2.to_id <> :me
  and f2.to_id not in (select to_id from edges where from_id = :me)  -- chưa kết bạn
group by f2.to_id order by mutual desc limit 10;
```
Self-join 2 lần = 2-hop traversal; sâu hơn → graph algorithm batch.

## 5. Scale & failure — supernode skew ⭐
- **Influencer** = supernode (triệu edge) → skew kinh khủng trong fan-out & traversal. Xử lý đặc biệt (hybrid feed, không fan-out, cache).
- Partition/shard graph khó (edge cắt ngang shard → cross-shard query). Hash theo user_id; quan hệ xuyên shard cần xử lý.
- Cache feed/follower count (đếm chính xác triệu follower mỗi lần = đắt → cache/approx).

## 6. Analytics
- Engagement (like/comment/share per post), virality (cascade), community detection (graph algorithm), influencer scoring (PageRank-like).
- Follower count: approx khi cực lớn ([[g08-probabilistic-ds]] HLL cho unique).

## Câu hỏi đào sâu
- "Feed cho user follow 1000 người?" → fan-out write (push) cho thường + pull cho influencer (hybrid).
- "Influencer 10M follower đăng post?" → KHÔNG fan-out write; pull lúc đọc + cache.
- "FoF recommendation scale?" → 2-hop SQL/lookup nông; sâu → batch graph (GraphX).

## ✅ "Tự mò"
🔭 Tạo `edges(from_id, to_id)` nhỏ; viết FoF query (2-hop self-join); nghĩ: nếu 1 node có 1 triệu edge thì fan-out write hỏng thế nào?

➡️ Tiếp: [[h05-trino-federation]].
