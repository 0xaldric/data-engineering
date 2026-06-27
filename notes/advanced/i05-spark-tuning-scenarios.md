# I05 — Deep-dive: Spark Tuning thực chiến (scenarios)

> 6 tình huống tuning thật: triệu chứng (Spark UI) → chẩn đoán → fix. Sâu hơn [[d01-spark-internals]], [[33-spark-tuning]].

## Scenario 1: Executor OOM (OutOfMemory)
**Triệu chứng:** task fail `java.lang.OutOfMemoryError`, executor chết & restart.
**Chẩn đoán:**
- `collect()` dữ liệu lớn về driver? → driver OOM.
- Partition quá to (skew → 1 partition khổng lồ)? → executor OOM.
- Cache quá nhiều đẩy execution memory?
**Fix:** tránh `collect()` (dùng `write`/`take`); tăng #partition (mỗi cái nhỏ lại); xử lý skew; giảm cache/unpersist; tăng `executor.memory` (cuối cùng, không phải đầu tiên).

## Scenario 2: Skew join cực chậm ⭐
**Triệu chứng:** 1 task chạy mãi (max duration ≫ median), 99% task xong còn 1 task treo.
**Chẩn đoán:** join key lệch (vd 80% hàng có `customer_id=NULL` hoặc 1 key hot) → 1 partition khổng lồ.
**Fix:**
- Bật **AQE skew join** (`spark.sql.adaptive.skewJoin.enabled`) → tự tách.
- **Broadcast** bảng nhỏ (tránh shuffle hẳn).
- **Salting**: thêm hậu tố ngẫu nhiên vào hot key → tách thành nhiều partition, rồi gộp.
- Lọc/xử lý riêng NULL key (thường NULL không cần join).

## Scenario 3: Small files (job đọc chậm)
**Triệu chứng:** stage đọc có **hàng nghìn task tí hon**, mỗi task đọc file vài KB; driver chậm liệt kê file.
**Chẩn đoán:** nguồn nhiều file nhỏ (streaming ghi từng micro-batch).
**Fix:** `coalesce`/`repartition` trước khi ghi (file ~128–256MB); **compaction** (OPTIMIZE Delta — [[34-delta-lake]]); bật AQE coalesce.

## Scenario 4: Shuffle khổng lồ
**Triệu chứng:** "Shuffle Read/Write" rất lớn (GB-TB), stage shuffle lâu.
**Chẩn đoán:** wide transform (groupBy/join) trên dữ liệu lớn, lọc/chọn cột muộn.
**Fix:** **lọc sớm** (predicate pushdown) + **chọn cột** trước groupBy/join; broadcast bảng nhỏ; tránh `distinct`/`orderBy` không cần; pre-aggregate.

## Scenario 5: Spill to disk
**Triệu chứng:** "Spill (memory)" và "Spill (disk)" lớn trong stage.
**Chẩn đoán:** partition quá to so RAM (sort/aggregation tràn).
**Fix:** tăng #partition (`spark.sql.shuffle.partitions` hoặc AQE); giảm dữ liệu (lọc/cột); tăng executor memory.

## Scenario 6: UDF Python chậm
**Triệu chứng:** stage có UDF chạy chậm bất thường, CPU cao, không codegen.
**Chẩn đoán:** UDF Python serialize data qua Python + mất tối ưu Catalyst.
**Fix:** thay bằng **built-in** `pyspark.sql.functions`/Spark SQL; bất đắc dĩ dùng **pandas UDF** (vectorized, Arrow).

## Quy trình tuning tổng (luôn theo)
```
1. ĐO (Spark UI: stage/task/SQL/storage) — đừng đoán
2. Tìm nghẽn: stage lâu nhất? skew (max≫median)? spill? shuffle lớn? OOM?
3. Áp fix theo thứ tự: đọc ít (pushdown/cột) → ít shuffle (broadcast/lọc sớm) →
   cân bằng partition (skew/size) → cache đúng → cuối cùng tăng RAM
4. ĐO LẠI
```

## Bảng tra nhanh
| Triệu chứng | Nguyên nhân | Fix chính |
|-------------|-------------|-----------|
| OOM | collect/partition to/skew | tránh collect, tăng partition, xử skew |
| 1 task treo | **skew** | AQE/broadcast/salting |
| nghìn task nhỏ | small files | compact/coalesce |
| shuffle GB-TB | wide sớm | lọc/cột trước, broadcast |
| spill disk | partition to | tăng partition |
| UDF chậm | Python UDF | built-in/pandas UDF |

## ✅ "Tự mò"
🔭 (Java/Spark) Tạo skew cố ý (80% hàng cùng key), chạy join, xem Spark UI task treo; bật AQE skew join so sánh. Không Spark? Tư duy tương tự với polars/DuckDB EXPLAIN.

➡️ Tiếp: [[i06-dq-framework]].
