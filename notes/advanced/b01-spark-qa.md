# B01 — Spark & Big Data Q&A

> Câu hỏi phỏng vấn Spark + đáp án ngắn gọn chuẩn. Chi tiết: [[30-spark-model]]→[[33-spark-tuning]].

**Q: Transformation vs Action?**
A: Transformation **lazy** (mô tả, chưa chạy — `select/filter/groupBy/join`); Action **kích hoạt** thực thi DAG (`show/collect/count/write`). Spark thấy toàn pipeline trước khi chạy → tối ưu.

**Q: Narrow vs Wide transformation?**
A: Narrow: mỗi partition input→1 output, **không shuffle** (`map/filter`). Wide: cần dữ liệu nhiều partition→**shuffle** (`groupBy/join/distinct`), cắt **stage**.

**Q: Shuffle là gì, vì sao đắt?**
A: Phân phối lại dữ liệu giữa partition/node để gom theo key. Đắt vì network I/O + disk I/O (ghi shuffle files) + serialization. Tối ưu Spark = giảm số & lượng shuffle.

**Q: RDD vs DataFrame vs Dataset?**
A: RDD thấp cấp (không tối ưu); DataFrame có schema + Catalyst tối ưu (mặc định, PySpark); Dataset type-safe (Scala/Java). Dùng DataFrame.

**Q: Driver vs Executor?**
A: Driver lập kế hoạch (DAG→stage→task), điều phối, gom kết quả ("bộ não"). Executor chạy task trên partition, giữ cache ("cơ bắp"). Driver chết → job chết.

**Q: 3 chiến lược join?**
A: **Broadcast** (gửi bảng nhỏ tới mọi executor, không shuffle bảng lớn — nhanh nhất); **Sort-merge** (2 bảng lớn, sort+merge); **Shuffle-hash**. Fact×dim nhỏ → broadcast dim.

**Q: Catalyst & Tungsten?**
A: Catalyst = optimizer (logical→optimized→physical: predicate pushdown, column pruning, CBO). Tungsten = thực thi (whole-stage codegen, off-heap memory). Chạy ngầm.

**Q: AQE?**
A: Adaptive Query Execution (Spark 3) — tối ưu **lúc chạy** theo thống kê thực: gộp shuffle partition nhỏ, đổi sort-merge→broadcast, xử lý skew join. Bật mặc định 3.2+.

**Q: Data skew — nhận biết & xử lý?**
A: Một key chiếm phần lớn dữ liệu → 1 task chạy mãi (max time ≫ median trong Spark UI). Xử lý: broadcast (nếu bên nhỏ), **salting**, AQE skew join, tách hot key.

**Q: cache/persist khi nào?**
A: Khi một DataFrame **dùng lại nhiều lần** (vòng lặp ML). Không cache thứ dùng 1 lần. Storage levels: MEMORY_ONLY (mất thì tính lại), MEMORY_AND_DISK (spill). `unpersist` khi xong.

**Q: Small files problem?**
A: Triệu file nhỏ → overhead metadata, đọc chậm, driver quá tải. Trị: coalesce/repartition trước ghi, compaction (OPTIMIZE Delta).

**Q: repartition vs coalesce?**
A: repartition(n) đổi số partition **có shuffle**, cân bằng. coalesce(n) **giảm** partition **không shuffle** (gộp), rẻ hơn nhưng có thể lệch — dùng trước khi ghi.

**Q: Job chạy chậm, debug thế nào?**
A: Spark UI: stage nào lâu, task skew (max≫median), spill (disk), shuffle lớn. → giảm dữ liệu đọc (pruning/pushdown), broadcast bảng nhỏ, cân bằng partition, tránh UDF Python.

**Q: Vì sao tránh UDF Python?**
A: Phải serialize dữ liệu qua Python (chậm) + mất tối ưu Catalyst. Ưu tiên built-in `pyspark.sql.functions`/Spark SQL; bất đắc dĩ dùng **pandas UDF** (vectorized).

**Q: MapReduce vs Spark?**
A: MapReduce ghi đĩa giữa mỗi pha (chậm); Spark giữ in-memory + tối ưu DAG → nhanh hơn 10–100×, API cao cấp hơn.

## ✅ "Tự mò"
🔭 Tự trả lời lại không nhìn; với mỗi câu, nêu thêm 1 ví dụ thực tế từ pipeline e-commerce.

➡️ Tiếp: [[b02-kafka-qa]].
