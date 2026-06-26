# 33 — Spark Performance Tuning

> Checklist thực chiến để Spark job nhanh & ổn định. Phần lớn là **giảm shuffle, cân bằng partition, đọc ít dữ liệu**.

## Các đòn bẩy chính (theo độ ưu tiên)
1. **Đọc ít dữ liệu**: chọn cột cần (`select`), lọc sớm (`filter` đẩy xuống nguồn), dùng **Parquet + partition pruning** ([[09-file-formats]], [[31-partitioning-shuffle]]). Ít dữ liệu vào = mọi thứ nhanh.
2. **Giảm shuffle**: lọc/bỏ cột trước `groupBy`/`join`; **broadcast** bảng nhỏ ([[32-joins-catalyst]]); tránh `distinct`/`orderBy` không cần thiết.
3. **Cân bằng partition**: kích thước ~128–256MB; `repartition` khi quá ít, `coalesce` khi quá nhiều; xử lý **skew** (salting/AQE).
4. **Cache đúng chỗ**: `df.cache()`/`persist()` khi một DataFrame được **dùng lại nhiều lần** (vd trong vòng lặp ML). Đừng cache thứ chỉ dùng 1 lần (tốn RAM vô ích). `unpersist()` khi xong.

## Small-files problem ⭐
Hàng nghìn/triệu file nhỏ (vd mỗi micro-batch ghi 1 file bé) → **overhead metadata khổng lồ**, đọc chậm, driver quá tải liệt kê file. Cách trị:
- `coalesce`/`repartition` trước khi ghi để gộp.
- **Compaction** định kỳ (OPTIMIZE của Delta — [[34-delta-lake]]).
- Tránh quá nhiều cột partition (mỗi tổ hợp tạo thêm file).

## Spill to disk
Khi partition quá to so với RAM executor, Spark **spill** dữ liệu trung gian ra đĩa (shuffle spill, aggregation spill) → chậm. Khắc phục: tăng partition (mỗi cái nhỏ lại), tăng RAM executor, giảm dữ liệu shuffle. Theo dõi "Spill" trong Spark UI.

## Bộ nhớ & song song
- **Executor memory & cores**: cân đối; quá nhiều core/executor → tranh RAM/GC. Thường 4–5 core/executor là ngọt.
- **`spark.sql.shuffle.partitions`** (mặc định 200): chỉnh theo kích thước dữ liệu — dữ liệu nhỏ giảm xuống (đỡ overhead), dữ liệu lớn tăng lên. AQE tự gộp giúp.
- **Tránh UDF Python**: UDF Python phải serialize dữ liệu qua Python (chậm, mất tối ưu Catalyst). Ưu tiên hàm built-in (`pyspark.sql.functions`) hoặc Spark SQL; nếu phải, dùng **pandas UDF** (vectorized, nhanh hơn).

## Storage levels (cache)
`MEMORY_ONLY` (mặc định, mất nếu thiếu RAM → tính lại), `MEMORY_AND_DISK` (spill ra đĩa khi thiếu RAM — an toàn hơn), `DISK_ONLY`, `*_SER` (nén, ít RAM hơn nhưng tốn CPU).

## Đọc Spark UI (kỹ năng debug số 1)
- **Stages tab**: stage nào lâu? task nào lệch (max time ≫ median = **skew**)?
- **SQL tab**: xem plan, kiểu join, số rows mỗi node.
- **Storage**: cache đang chiếm bao nhiêu.
- **Spill** lớn → tăng partition/RAM.

## Checklist tuning nhanh
- [ ] Chỉ đọc cột/hàng cần (pushdown).
- [ ] Broadcast bảng nhỏ trong join.
- [ ] Partition ~128–256MB, không skew.
- [ ] Bật AQE.
- [ ] Cache chỉ khi tái dùng.
- [ ] Compact small files.
- [ ] Tránh UDF Python; dùng built-in.
- [ ] Đọc Spark UI tìm điểm nghẽn.

## "Tự mò"
🔭 Phần lớn nguyên tắc này áp dụng được ngay trong **polars/DuckDB**: lọc sớm, chọn cột, partition file, tránh thao tác toàn cục. Thử đo thời gian khi `select` 2 cột vs đọc full trên parquet lớn — chính là đọc-ít-dữ-liệu.

➡️ Tiếp: [[34-delta-lake]] — table format cho lakehouse.
