# G08 — Probabilistic Data Structures & Approximate Queries

> Khi dữ liệu quá lớn để tính **chính xác** rẻ → chấp nhận **gần đúng** với sai số nhỏ + bộ nhớ tí hon. DE thực dùng nhiều hơn bạn nghĩ.

## Vì sao cần approx?
- `COUNT(DISTINCT user_id)` trên tỉ hàng = tốn RAM/shuffle khổng lồ (phải giữ mọi distinct value).
- Percentile chính xác cần sort toàn bộ.
- "X có trong tập Y không" trên tỉ phần tử = tốn bộ nhớ.
→ Probabilistic DS đổi **độ chính xác tuyệt đối** lấy **bộ nhớ & tốc độ** (sai số kiểm soát được, vd ±2%). Đa số analytics chấp nhận.

## ⭐ HyperLogLog (HLL) — approx count distinct
Ước lượng số phần tử **distinct** với bộ nhớ **cố định nhỏ** (KB) thay vì lưu mọi giá trị.
- Ý tưởng: hash mỗi value → đếm số 0 dẫn đầu tối đa → suy ra cardinality (nhiều distinct → có hash với nhiều 0 dẫn đầu).
- Sai số ~1-2%; **mergeable** (gộp HLL của nhiều partition → distinct toàn cục mà không shuffle giá trị thật).
- SQL: `approx_count_distinct(user_id)` (BigQuery `APPROX_COUNT_DISTINCT`, Spark, DuckDB, Redshift). Nhanh hơn `COUNT(DISTINCT)` hàng chục lần trên dữ liệu lớn.
```sql
select approx_count_distinct(user_id) from events;  -- ~±2%, rẻ hơn nhiều
```

## ⭐ Bloom Filter — membership test
"X có **chắc chắn không** trong tập, hay **có thể có**?" với bộ nhớ tí hon.
- Bit array + k hash. Add: set k bit. Check: nếu một bit = 0 → **chắc chắn không**; nếu mọi bit = 1 → **có thể có** (false positive, không false negative).
- Dùng thực tế: **LSM-tree** (bỏ qua SSTable không chứa key — [[g07-dsa-for-de]]); **join** (lọc trước key không khớp, giảm shuffle); cache (tránh query DB cho key chắc chắn không tồn tại); Parquet/Iceberg bloom filter cho data skipping.

## t-digest / Quantile sketch — approx percentile
Ước lượng percentile (p50/p95/p99) trên stream/dữ liệu lớn mà không sort toàn bộ, bộ nhớ nhỏ, mergeable.
- Dùng cho latency p99 (observability — [[62-observability]]), SLA.
- SQL: `approx_quantile(latency, 0.99)` (DuckDB/Spark/BigQuery `APPROX_QUANTILES`).

## Count-Min Sketch — approx frequency
Đếm tần suất phần tử (top-K, heavy hitters) với bộ nhớ nhỏ; có thể over-count (không under). Dùng cho "sản phẩm/từ khoá hot" trên stream lớn.

## Khi nào dùng approx (và khi nào KHÔNG)
| Dùng approx | KHÔNG approx |
|-------------|--------------|
| analytics/dashboard (±2% OK) | tài chính/đếm tiền ([[c07-case-fintech]]) |
| cardinality/percentile trên tỉ hàng | báo cáo compliance cần chính xác |
| real-time (cần nhanh, RAM ít) | khi sai số dẫn tới quyết định sai nghiêm trọng |
→ Hỏi: "sai 1-2% có sao không?" Nếu không → approx tiết kiệm khổng lồ.

## ⚠️ Cạm bẫy
- Dùng approx cho tiền/compliance (cần exact).
- Quên approx là **gần đúng** → trình bày như chính xác.
- Bloom filter: hiểu sai (false positive có, false negative KHÔNG) → dùng sai chỗ.
- Không tận dụng approx khi `COUNT(DISTINCT)` làm chậm query trên dữ liệu lớn.

## ✅ "Tự mò"
🔭 Trên DuckDB: so `count(distinct user_id)` vs `approx_count_distinct(user_id)` trên dataset lớn (nhân e-commerce lên triệu hàng) — đo thời gian & sai số. Thử `approx_quantile(line_total, 0.99)`.

➡️ Hết Extra G. Xem [[00-INDEX]].
