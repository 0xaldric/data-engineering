# 32 — Joins at Scale & Catalyst Optimizer

> Join là thao tác đắt nhất (shuffle nặng). Spark có nhiều chiến lược join + một optimizer thông minh chọn giúp bạn.

## 3 chiến lược join trong Spark
| Chiến lược | Cách làm | Khi nào | Chi phí |
|-----------|----------|---------|---------|
| **Broadcast hash join** | gửi (broadcast) bảng **nhỏ** tới mọi executor, join cục bộ | một bảng đủ nhỏ (< ~10MB, chỉnh `spark.sql.autoBroadcastJoinThreshold`) | **không shuffle** bảng lớn → rất nhanh ⭐ |
| **Sort-merge join** | sort cả 2 bảng theo key rồi merge | 2 bảng **lớn** | shuffle + sort 2 bên → đắt |
| **Shuffle hash join** | shuffle rồi build hash table mỗi partition | bảng vừa, không sort được | shuffle, tốn RAM |

→ **Broadcast** là vũ khí số 1: join fact lớn với dimension nhỏ → broadcast dimension, tránh shuffle bảng fact khổng lồ.
```python
from pyspark.sql.functions import broadcast
fct.join(broadcast(dim_product), "product_id")   # ép broadcast bảng nhỏ
```

## Data skew trong join
Key lệch (xem [[31-partitioning-shuffle]]) làm sort-merge join chậm. Xử lý: broadcast (nếu được), salting key, hoặc bật **AQE skew join** (Spark 3 tự tách partition lệch).

## ⭐ Catalyst Optimizer
"Bộ não" tối ưu của Spark SQL/DataFrame. Biến query của bạn qua các bước:
```
SQL/DataFrame
   ↓ parse
Unresolved Logical Plan
   ↓ analyze (resolve tên cột/bảng từ catalog)
Logical Plan
   ↓ optimize (rule-based: predicate pushdown, column pruning, constant folding, ...)
Optimized Logical Plan
   ↓ chọn Physical Plan (cost-based: chọn kiểu join, ...)
Physical Plan
   ↓ codegen (Tungsten)
RDDs thực thi
```
Các tối ưu quan trọng Catalyst tự làm:
- **Predicate pushdown**: đẩy `filter` xuống sát nguồn (đọc ít hàng).
- **Projection/column pruning**: chỉ đọc cột cần (mạnh với Parquet — [[09-file-formats]]).
- **Constant folding**, gộp filter, reorder join.
- **Cost-based optimization (CBO)**: dùng statistics để chọn thứ tự join & chiến lược join.

→ Vì có Catalyst, viết DataFrame/SQL "ngây thơ" vẫn nhanh; bạn tập trung vào logic, optimizer lo phần lớn.

## Tungsten
Lớp thực thi hiệu năng cao dưới Catalyst: **whole-stage code generation** (sinh bytecode Java gộp nhiều toán tử, giảm overhead), quản lý **bộ nhớ off-heap** (tránh GC), bố trí dữ liệu cache-friendly (columnar). Bạn không viết Tungsten — nó chạy ngầm.

## AQE — Adaptive Query Execution (Spark 3+)
Tối ưu **lúc chạy** dựa trên thống kê thực tế (không chỉ ước lượng trước):
- Tự **gộp partition** shuffle nhỏ.
- Tự đổi sort-merge → **broadcast** nếu phát hiện một bên thực sự nhỏ.
- Tự xử lý **skew join** (tách partition lệch).
Bật: `spark.sql.adaptive.enabled=true` (mặc định true ở Spark 3.2+).

## Đọc plan
`df.explain()` (hoặc `EXPLAIN` trong SQL) cho **physical plan** — tìm `BroadcastHashJoin` vs `SortMergeJoin`, `*(n)` (codegen stage), `PushedFilters`. (Ở [[14-indexing]] đã đọc plan DuckDB — cùng cách tư duy: scan → filter pushdown → join.)

## ✅ Tự kiểm tra & "tự mò"
- [ ] 3 chiến lược join & khi nào dùng; vì sao broadcast tránh shuffle.
- [ ] Các bước Catalyst (logical→physical); predicate pushdown/column pruning.
- [ ] Tungsten & AQE giúp gì.
- [ ] Đọc được `.explain()` để biết kiểu join.
- 🔭 *Tự mò:* trong DuckDB chạy `EXPLAIN` cho join fact×dim, tìm filter pushdown; tưởng tượng bảng dim nhỏ → Spark sẽ broadcast.

➡️ Tiếp: [[33-spark-tuning]].
