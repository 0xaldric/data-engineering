# D01 — Spark Internals deep ⭐

> Sâu hơn [[30-spark-model]]→[[33-spark-tuning]]: bên trong Spark chạy thế nào để debug/tối ưu ở mức senior.

## Memory management (Unified Memory Model)
Executor JVM heap chia (Spark 1.6+, unified):
```
┌─────────────── Executor heap ───────────────┐
│ Reserved (300MB)                             │
│ ┌─ Unified region (spark.memory.fraction ~0.6) ─┐ │
│ │  Execution memory  ⇄  Storage memory          │ │  ← mượn lẫn nhau (dynamic)
│ │  (shuffle/sort/join/agg)  (cache/broadcast)   │ │
│ └───────────────────────────────────────────────┘ │
│ User memory (~0.4: cấu trúc dữ liệu của bạn, UDF) │
└──────────────────────────────────────────────┘
```
- **Execution** (shuffle, sort, join, aggregation) và **Storage** (cache, broadcast) **chia sẻ** vùng unified, mượn lẫn nhau. Execution được ưu tiên (có thể đẩy storage cache ra).
- **Spill**: khi execution memory không đủ → ghi tạm ra **đĩa** (spill) → chậm. Thấy "Spill (memory/disk)" trong Spark UI = dấu hiệu thiếu RAM / partition quá to → tăng partition (mỗi cái nhỏ lại) hoặc tăng executor memory.
- **OOM** thường do: partition quá to, collect() về driver dữ liệu lớn, skew, quá nhiều cache.

## Tungsten (execution engine)
Tối ưu CPU/memory dưới Catalyst:
- **Whole-stage code generation**: gộp nhiều toán tử trong một stage thành **một hàm Java** (bytecode) → bỏ overhead gọi hàm/iterator ảo, chạy như code viết tay. Thấy `*(n)` trong plan = codegen stage.
- **Off-heap memory** (UnsafeRow): quản lý bộ nhớ nhị phân ngoài heap → tránh overhead GC, layout cache-friendly.
- **Columnar / vectorized reader** cho Parquet.

## AQE (Adaptive Query Execution) — sâu
Spark 3 tối ưu **runtime** dựa trên thống kê thực của shuffle (không chỉ ước lượng trước):
1. **Coalesce shuffle partitions**: gộp nhiều partition shuffle nhỏ → giảm task overhead (thay vì cứng 200 partition).
2. **Skew join handling**: phát hiện partition lệch → **tách** thành nhiều sub-partition chạy song song → trị skew tự động ([[31-partitioning-shuffle]]).
3. **Dynamically switch join**: sort-merge → **broadcast** nếu runtime thấy một bên thực sự nhỏ.
Bật: `spark.sql.adaptive.enabled=true` (mặc định 3.2+).

## Debug job chậm — quy trình (Spark UI)
```
1. Jobs/Stages: stage nào lâu nhất? bao nhiêu task?
2. Trong stage: task lệch? (max duration ≫ median = SKEW)
3. Spill (memory/disk) lớn? → thiếu RAM / partition to
4. Shuffle read/write lớn? → giảm shuffle (lọc sớm, broadcast)
5. SQL tab: kiểu join (broadcast vs sort-merge), rows mỗi node, scan đọc bao nhiêu
6. GC time cao? → quá nhiều object / cache → off-heap, giảm cache
```

## Bảng triệu chứng → nguyên nhân → cách trị
| Triệu chứng (UI) | Nguyên nhân | Trị |
|------------------|-------------|-----|
| 1 task lâu, còn lại xong | **skew** | salting, AQE skew, broadcast |
| Spill disk lớn | partition to / thiếu RAM | tăng #partition, RAM |
| Shuffle write khổng lồ | wide transform sớm | lọc/chọn cột trước, broadcast |
| GC time cao | nhiều object/cache | off-heap, unpersist, ít UDF Python |
| Stage nhiều task tí hon | quá nhiều partition | coalesce / AQE |
| Đọc cả TB cho query nhỏ | thiếu pruning | partition + predicate pushdown |

## ⚠️ Cạm bẫy
- `collect()` dữ liệu lớn về driver → OOM driver.
- Cache mọi thứ → đẩy execution memory, spill nhiều.
- Quá nhiều UDF Python → serialize + mất codegen.
- Cứng `spark.sql.shuffle.partitions=200` cho mọi job → bật AQE.

## ✅ "Tự mò"
🔭 (cần Java/Spark) Chạy một job join+groupby, mở Spark UI: tìm stage lâu nhất, xem skew (max vs median task), thử bật/tắt AQE so sánh. Không có Spark? Đọc plan polars/DuckDB `EXPLAIN` cùng tư duy.

➡️ Tiếp: [[d02-dbt-advanced]].
