# F04 — Cost Optimization Case Studies

> Tình huống giảm chi phí thật (có số), kèm cách chẩn đoán. Tổng hợp & cụ thể hoá [[59-cost-finops]].

## Case 1: Query Athena/BigQuery giảm ~90% (bytes scanned)
**Triệu chứng:** hoá đơn query tăng vọt; một dashboard chạy `SELECT *` trên bảng event 5TB CSV, mỗi lần quét toàn bộ.
**Chẩn đoán:** Athena/BQ tính theo **bytes scanned**; CSV + không partition + `SELECT *` = quét full.
**Sửa:**
1. CSV → **Parquet** (columnar, nén): 5TB → ~1TB.
2. **Partition** theo `dt`: query 1 ngày chỉ quét 1/365.
3. Chọn **đúng cột** (5/40 cột).
**Kết quả:** mỗi query từ quét 5TB → ~3GB ≈ **giảm >99%** bytes scanned → hoá đơn giảm tương ứng. (Benchmark [[09-file-formats]] đã cho thấy Parquet nhỏ 6×, đọc 1 cột nhanh 22×.)
**Bài học:** với serverless SQL, **format + partition + chọn cột** là đòn bẩy số 1.

## Case 2: Snowflake warehouse đốt tiền khi idle
**Triệu chứng:** chi phí compute cao dù query ít.
**Chẩn đoán:** warehouse để chạy 24/7 (không auto-suspend); size XL cho query nhỏ; `WAREHOUSE_METERING_HISTORY` cho thấy nhiều giờ idle billed.
**Sửa:** `auto_suspend=60s` + `auto_resume`; right-size (XL→S cho ETL nhẹ); tách warehouse BI (nhỏ) khỏi ETL (lớn). Tận dụng result cache cho query lặp.
**Kết quả:** chỉ trả tiền khi thực chạy → **giảm 50–70%** compute cost.
**Bài học:** Snowflake tính theo **compute-time** → auto-suspend + sizing là then chốt ([[d04-snowflake]]).

## Case 3: Small files giết hiệu năng & chi phí
**Triệu chứng:** Spark/query đọc bảng chậm dần; hàng triệu file Parquet nhỏ (mỗi micro-batch streaming ghi 1 file bé).
**Chẩn đoán:** small files problem — overhead liệt kê/mở file lấn át ([[33-spark-tuning]]).
**Sửa:** **compaction** định kỳ (OPTIMIZE Delta / rewrite_data_files Iceberg) gộp thành file ~128–256MB; coalesce trước khi ghi; giảm cột partition cardinality cao.
**Kết quả:** số file giảm 100×, thời gian đọc & compute giảm mạnh.
**Bài học:** streaming/ingest sinh small files → cần compaction trong vòng đời ([[34-delta-lake]], [[d07-iceberg]]).

## Case 4: Full rebuild → Incremental
**Triệu chứng:** job dbt/Spark build lại **toàn bộ** fact 2 năm mỗi đêm → compute lớn, chậm.
**Chẩn đoán:** model materialized `table` (full refresh) trong khi chỉ có data mới mỗi ngày.
**Sửa:** chuyển sang **incremental** (chỉ xử lý ngày mới, `is_incremental()` — [[27-dbt-incremental]]); lookback window cho late data.
**Kết quả:** từ xử lý 2 năm → 1 ngày mỗi lần chạy ≈ **giảm ~99%** compute (như demo Phase 3: 547→730 rows chỉ append phần mới).
**Bài học:** đừng build lại cái không đổi; incremental cho fact lớn.

## Quy trình audit chi phí (FinOps)
```
1. Tag tài nguyên (team/project/env) → biết tiền đi đâu
2. Dashboard chi phí (Cost Explorer / metering history) → tìm top spender
3. Tìm: query đắt (bytes scanned cao), warehouse idle, storage phình, small files, full rebuild
4. Áp đòn bẩy (format/partition/suspend/incremental/compaction/tiering)
5. Set budget alert + theo dõi xu hướng
6. Văn hoá: kỹ sư thấy chi phí job mình (shift-left cost)
```

## Bảng đòn bẩy → tác động
| Đòn bẩy | Giảm gì | Tác động |
|---------|---------|----------|
| Parquet + partition + chọn cột | bytes scanned | ~90–99% (serverless SQL) |
| Auto-suspend + right-size | compute-time | 50–70% (Snowflake) |
| Compaction small files | đọc/compute | lớn |
| Incremental thay full | compute | ~90–99% |
| Storage tiering/lifecycle | storage | dần theo thời gian |

## ⚠️ Cạm bẫy
- Tối ưu cái chạy 1 lần/tháng (phí công) — ưu tiên cái chạy nghìn lần.
- Tối ưu mò không đo (đoán sai chỗ tốn).
- Không tag → không biết tiền đi đâu.

## ✅ "Tự mò"
🔭 Lấy benchmark [[09-file-formats]] (CSV 41MB vs Parquet 6MB; đọc full vs 1 cột) → tính "nếu Athena $5/TB scanned thì 1000 query/ngày tiết kiệm bao nhiêu/tháng khi chuyển Parquet+partition".

➡️ Tiếp: [[f05-data-mesh]].
