# 31 — Partitioning & Shuffle ⭐

> 90% vấn đề hiệu năng Spark đến từ **shuffle** và **skew**. Hiểu chương này là hiểu cách tối ưu Spark.

## Partition là gì?
Dữ liệu Spark chia thành **partitions** — mỗi partition là một mảnh xử lý bởi **một task** trên **một core**. Số partition = mức độ song song.
- Quá ít partition → không tận dụng hết core, partition to → spill/OOM.
- Quá nhiều partition → overhead lập lịch, nhiều file nhỏ.
- Rule of thumb: mỗi partition ~**128–256MB**; tổng số partition ≈ 2–4× số core cluster.

## ⭐ Shuffle — vì sao đắt
**Shuffle** = phân phối lại dữ liệu **giữa các partition/node** để gom theo key (cho `groupBy`, `join`, `distinct`, `orderBy`). Nó tốn:
1. **Network I/O** — dữ liệu bay qua mạng giữa node.
2. **Disk I/O** — Spark ghi "shuffle files" ra đĩa giữa stage.
3. **Serialization** — đóng/mở gói dữ liệu.

```
Stage 1 (map)          SHUFFLE          Stage 2 (reduce)
[p1][p2][p3]   ─── gom theo key ───►   [pA][pB][pC]
   (ghi shuffle files ra đĩa, đọc qua mạng)
```
→ Mỗi shuffle tạo **ranh giới stage**. Tối ưu Spark = **giảm số shuffle & lượng dữ liệu shuffle**.

## Narrow vs Wide (nhắc lại [[30-spark-model]])
- **Narrow** (`map/filter/select`): không shuffle → rẻ.
- **Wide** (`groupBy/join/distinct/orderBy/repartition`): shuffle → đắt.
Mẹo: lọc (`filter`) và bỏ cột (`select`) **trước** khi `groupBy`/`join` để shuffle ít dữ liệu hơn.

## repartition vs coalesce
- **`repartition(n)`**: đổi số partition (tăng/giảm), **có shuffle**, phân bố đều. Dùng khi cần tăng song song hoặc cân bằng lại.
- **`coalesce(n)`**: **giảm** số partition, **không shuffle** (gộp partition kề nhau) → rẻ hơn nhưng có thể lệch. Dùng để gộp trước khi ghi (giảm small files).
- Ghi theo cột: `df.write.partitionBy("date")` → tạo thư mục theo giá trị (partition pruning khi đọc).

## ⭐ Data skew — kẻ giết hiệu năng âm thầm
Một key chiếm phần lớn dữ liệu (vd 80% đơn ở 1 quốc gia) → một task xử lý mãi, các task khác xong sớm ngồi chờ → job chậm dù cluster lớn. Dấu hiệu: 1 task chạy lâu bất thường trong Spark UI.
Cách xử lý:
- **Broadcast join** nếu một bên nhỏ (tránh shuffle hẳn — xem [[32-joins-catalyst]]).
- **Salting**: thêm hậu tố ngẫu nhiên vào key lệch để tách thành nhiều partition, rồi gộp lại.
- **AQE** (Adaptive Query Execution) của Spark 3 tự phát hiện & tách partition lệch.
- Lọc/tách riêng "hot key" xử lý riêng.

## Partition pruning (đọc)
Nếu dữ liệu đã `partitionBy("date")` trên đĩa, query `where date='2024-01-01'` chỉ đọc thư mục đó → **bỏ qua** phần còn lại. Cùng tư tưởng predicate pushdown của Parquet ([[09-file-formats]]). Chọn cột partition theo **cột hay lọc**, **lực lượng vừa phải** (đừng partition theo cột có triệu giá trị).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Partition liên quan core/task thế nào; kích thước hợp lý.
- [ ] Vì sao shuffle đắt (3 chi phí); thao tác nào gây shuffle.
- [ ] repartition vs coalesce.
- [ ] Nhận biết & xử lý data skew (salting/broadcast/AQE).
- 🔭 *Tự mò:* trong DuckDB/pyarrow, ghi parquet `partition_by=['category']` rồi đọc lọc 1 category, so thời gian với đọc full — đó chính là partition pruning. Nghĩ Spark `partitionBy` tương tự.

➡️ Tiếp: [[32-joins-catalyst]].
