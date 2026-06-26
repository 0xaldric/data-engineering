# 30 — Apache Spark: Kiến trúc & Execution Model ⭐

> Spark = engine xử lý dữ liệu phân tán **in-memory**, nhanh hơn MapReduce 10–100× nhờ giữ dữ liệu trong RAM và tối ưu DAG.

## Kiến trúc cluster
```
        ┌─────────────┐
        │   DRIVER    │  chạy main(), giữ SparkSession, lập kế hoạch (DAG),
        │ (SparkSession)│  chia task, gom kết quả. "Bộ não".
        └──────┬──────┘
               │ qua Cluster Manager (YARN/K8s/Standalone)
     ┌─────────┼─────────┐
     ▼         ▼         ▼
 ┌────────┐┌────────┐┌────────┐
 │EXECUTOR││EXECUTOR││EXECUTOR│  chạy task thật trên partition,
 │ (JVM)  ││ (JVM)  ││ (JVM)  │  giữ dữ liệu cache. "Cơ bắp".
 └────────┘└────────┘└────────┘
```
- **Driver**: dịch code → **DAG** → chia thành **stages** → **tasks**; điều phối; gom kết quả. Nếu driver chết → job chết.
- **Executor**: process JVM trên worker node; chạy task (mỗi task xử lý 1 partition); giữ cache. Nhiều **core** = nhiều task song song.
- **Cluster Manager**: cấp phát tài nguyên (YARN, Kubernetes, Standalone, hoặc local).
- **SparkSession**: điểm vào (gộp SparkContext, SQLContext...).

## 3 API: RDD vs DataFrame vs Dataset
| API | Mức | Tối ưu | Khi nào |
|-----|-----|--------|---------|
| **RDD** | thấp (đối tượng JVM) | KHÔNG (bạn tự lo) | điều khiển chi tiết, dữ liệu phi cấu trúc; hiếm khi cần |
| **DataFrame** | cao (bảng có schema) | ✅ Catalyst tối ưu | **mặc định** — như bảng SQL; PySpark dùng cái này |
| **Dataset** | cao + type-safe | ✅ | Scala/Java (typed); Python không có (vì động) |

→ Trong PySpark, **dùng DataFrame** (hoặc Spark SQL). RDD chỉ khi thật cần. DataFrame được Catalyst tối ưu nên thường nhanh hơn RDD viết tay.

## ⭐ Lazy evaluation: Transformation vs Action
Đây là tư tưởng cốt lõi (giống polars lazy, xem [[08-polars]]):
- **Transformation** (lazy): mô tả phép biến đổi, **chưa chạy gì** — chỉ thêm vào kế hoạch (DAG). VD: `select, filter, groupBy, join, withColumn`.
- **Action** (eager): **kích hoạt** thực thi toàn bộ DAG. VD: `show, collect, count, write, take`.

```python
df = spark.read.parquet("orders")      # transformation (lazy)
big = df.filter(df.amount > 100)        # lazy — chưa chạy
agg = big.groupBy("category").sum()     # lazy — chưa chạy
agg.show()                              # ACTION -> giờ Spark mới chạy cả chuỗi
```
Lợi ích: Spark thấy **toàn bộ** pipeline trước khi chạy → tối ưu (gộp filter, đẩy xuống nguồn, bỏ cột thừa).

### Narrow vs Wide transformation
- **Narrow**: mỗi partition input → 1 partition output, **không cần shuffle** (`map, filter, select`). Nhanh, chạy trong cùng stage.
- **Wide**: cần dữ liệu từ **nhiều** partition → **shuffle** (`groupBy, join, distinct, repartition`). Tạo **ranh giới stage**. Đắt — xem [[31-partitioning-shuffle]].

## DAG → Stages → Tasks
Driver dịch DAG thành **stages** (cắt tại mỗi shuffle/wide transformation). Mỗi stage gồm nhiều **task** (1 task/partition) chạy song song trên executor. Đếm số stage ≈ đếm số shuffle + 1.

## Code PySpark tham khảo (chỉ minh hoạ)
```python
from pyspark.sql import SparkSession, functions as F
spark = SparkSession.builder.appName("demo").getOrCreate()

df = spark.read.parquet("data/raw/order_items.parquet")
rev = (df.filter(F.col("line_total") > 0)        # narrow
         .groupBy("product_id")                   # wide -> shuffle
         .agg(F.sum("line_total").alias("rev")))
rev.explain()        # xem physical plan
rev.show(5)          # action
```

## ✅ Tự kiểm tra & "tự mò"
- [ ] Vai trò driver vs executor vs cluster manager.
- [ ] RDD vs DataFrame — vì sao DataFrame thường nhanh hơn.
- [ ] Kể 4 transformation, 4 action; phân biệt lazy/eager.
- [ ] Narrow vs wide; vì sao wide cắt stage.
- 🔭 *Tự mò:* cài Java + `pip install pyspark`, chạy local `spark.read...groupBy...show()`, gọi `.explain()` đọc plan. (Ở máy này chưa có Java — đối chiếu với polars lazy `[[08-polars]]` cùng tư tưởng.)

➡️ Tiếp: [[31-partitioning-shuffle]].
