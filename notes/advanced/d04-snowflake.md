# D04 — Snowflake deep

> Cloud data warehouse phổ biến. Hiểu kiến trúc để tối ưu hiệu năng & **chi phí** (Snowflake tính theo compute-time → dễ đốt tiền).

## Kiến trúc 3 lớp (tách hoàn toàn)
```
┌─ Cloud Services ─┐  (metadata, optimizer, security, transactions, result cache)
├─ Compute ────────┤  Virtual Warehouses (cụm compute độc lập, co giãn)
└─ Storage ────────┘  dữ liệu nén columnar trên object store (S3/GCS/Azure)
```
- **Tách compute & storage** triệt để: nhiều warehouse đọc cùng dữ liệu; scale độc lập.
- **Storage**: dữ liệu lưu **micro-partition** columnar nén, bất biến.

## Virtual Warehouse (compute)
- Cụm compute (size **XS→6XL**, mỗi bậc gấp đôi). Tính tiền theo **thời gian chạy** (giây, có min 60s).
- **Auto-suspend** (tắt khi idle vài phút) + **auto-resume** ⭐ → không trả tiền khi không dùng. Cấu hình đúng = tiết kiệm lớn.
- **Multi-cluster** (auto-scale số cụm) cho concurrency cao (nhiều user đồng thời).
- Nhiều warehouse cho workload khác nhau (ETL warehouse lớn, BI warehouse nhỏ) → cô lập, không tranh tài nguyên.

## ⭐ Micro-partitions & Pruning
- Dữ liệu tự chia **micro-partition** (~50–500MB nén, ~16MB uncompressed), columnar, **bất biến**.
- Mỗi micro-partition lưu **metadata** (min/max, distinct, null mỗi cột) → **pruning**: query lọc `where dt='...'` → bỏ qua micro-partition không khớp mà không đọc (giống zonemap Parquet — [[09-file-formats]], [[14-indexing]]).
- **Không có index thủ công** — pruning tự động + clustering.

## Clustering keys
- Dữ liệu lớn, query hay lọc theo cột X nhưng X không được sắp tự nhiên → **clustering key** sắp lại dữ liệu theo X → pruning hiệu quả hơn (data skipping).
- Tốn chi phí re-cluster (auto-clustering) → chỉ dùng cho bảng lớn + pattern query rõ. Giống Z-ordering Delta ([[34-delta-lake]]).

## Tính năng hay
- **Time travel** (0–90 ngày): query/clone dữ liệu quá khứ, undrop.
- **Zero-copy clone** ⭐: nhân bản DB/schema/table **tức thì, không tốn storage** (chỉ copy metadata, share micro-partition) → tạo môi trường dev/test từ prod rẻ.
- **Result cache**: query y hệt trong 24h → trả kết quả cache **miễn phí** (không tốn compute).
- **Streams + Tasks**: CDC nội bộ + scheduling. **Snowpark**: xử lý kiểu DataFrame/Python.

## ⭐ Tối ưu chi phí (quan trọng — tính theo compute-time)
- **Auto-suspend ngắn** (60s) + right-size warehouse (đừng XL cho query nhỏ).
- Tách warehouse theo workload; tắt warehouse dev.
- Tận dụng **result cache** (query lặp) & **materialized view** cho aggregate nóng.
- Giảm dữ liệu quét: clustering + lọc cột/partition.
- Monitor: `QUERY_HISTORY`, `WAREHOUSE_METERING_HISTORY` → tìm query/warehouse đốt tiền.

## So với BigQuery
- Snowflake: **compute-time** (virtual warehouse bạn quản size/auto-suspend). BigQuery: **bytes-scanned** (serverless slot) — xem [[d05-bigquery]].
- Snowflake cần "bật/tắt & sizing" đúng; BigQuery cần "quét ít byte".

## ⚠️ Cạm bẫy
- Warehouse để chạy hoài (quên auto-suspend) → đốt tiền.
- Warehouse quá lớn cho workload nhỏ.
- Clustering bừa (tốn re-cluster) khi không cần.
- `SELECT *` / không lọc → quét nhiều micro-partition.

## ✅ "Tự mò"
🔭 (Snowflake free trial) tạo warehouse XS auto-suspend=60s; load dataset; so query có/không clustering key; thử zero-copy clone + time travel; xem `WAREHOUSE_METERING_HISTORY`.

➡️ Tiếp: [[d05-bigquery]].
