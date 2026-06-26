# D05 — BigQuery deep

> Cloud DW serverless của GCP. Khác Snowflake ở mô hình tính tiền (**bytes-scanned**) → tối ưu = quét ít byte. So sánh [[d04-snowflake]].

## Kiến trúc (serverless, tách compute/storage)
```
Query ──► Dremel (execution, cây slot song song) ──► Colossus (storage columnar: Capacitor format)
              ▲ slots (đơn vị compute ảo)              ▲ Jupiter network (băng thông cực lớn nối compute↔storage)
```
- **Serverless**: không quản cụm (khác Snowflake virtual warehouse). Google tự cấp **slot** (đơn vị compute).
- **Dremel**: chia query thành cây thực thi song song trên hàng nghìn slot.
- **Colossus**: lưu dữ liệu columnar nén (Capacitor); tách hẳn compute.
- **Jupiter**: mạng băng thông khổng lồ → compute đọc storage nhanh dù tách rời.

## ⭐ Tính tiền: 2 mô hình
- **On-demand**: trả theo **bytes scanned** (dữ liệu query đọc) — query không tối ưu = hoá đơn sốc.
- **Capacity (slot reservation)**: mua slot theo thời gian (flat-rate) — hợp tải lớn ổn định, dự đoán chi phí.
→ Đa số bắt đầu on-demand → **tối ưu = quét ít byte**.

## ⭐ Tối ưu bytes-scanned (quan trọng nhất)
1. **Partition** bảng (theo DATE/timestamp/integer range) → query lọc partition chỉ quét partition đó.
2. **Cluster** (tối đa 4 cột) → sắp dữ liệu trong partition, data-skipping theo cột cluster.
3. **Chọn cột** (columnar): `SELECT col` không `SELECT *` → chỉ đọc cột cần.
4. **Lọc sớm** trên cột partition/cluster.
5. Tránh `SELECT *` trong subquery/CTE; dùng `--dry-run` xem bytes ước tính trước khi chạy.
→ Cùng query có thể rẻ đi 10–100× (giống Athena — [[56-aws-data-stack]], [[59-cost-finops]]).

## Tính năng
- **Materialized views**: tự refresh incremental, query dùng MV tự động → tăng tốc + giảm bytes aggregate nóng.
- **BI Engine**: cache in-memory cho dashboard tương tác.
- **Streaming inserts / Storage Write API**: nạp real-time.
- **Time travel** (7 ngày), snapshots, clone.
- **BigQuery ML**: train model bằng SQL trong BigQuery.
- **External tables / BigLake**: query thẳng file trên GCS (lakehouse), hỗ trợ Iceberg.

## Partition vs Cluster (phân biệt)
- **Partition**: chia bảng vật lý theo cột (DATE) → pruning ở mức partition; giới hạn ~4000 partition; có thể set `require_partition_filter`.
- **Cluster**: sắp xếp dữ liệu trong partition theo tối đa 4 cột → data-skipping mịn hơn, không giới hạn cardinality như partition.
- Kết hợp: partition theo ngày + cluster theo cột hay lọc (customer_id, category).

## So sánh Snowflake vs BigQuery
| | **Snowflake** | **BigQuery** |
|--|---------------|--------------|
| Compute | virtual warehouse (bạn quản size/suspend) | serverless slot (Google quản) |
| Tính tiền | compute-time | **bytes-scanned** (on-demand) |
| Tối ưu chính | sizing + auto-suspend | quét ít byte (partition/cluster/cột) |
| Đa cloud | có | GCP (BigLake mở rộng) |
| Tách compute/storage | có | có |

## ⚠️ Cạm bẫy
- `SELECT *` trên bảng lớn → quét toàn bộ → tốn tiền (dùng `--dry-run` kiểm trước).
- Quên partition/cluster → mọi query full scan.
- Không `require_partition_filter` → dev quên lọc → bill lớn.
- Streaming insert nhiều → chi phí + quota; cân nhắc batch load.

## ✅ "Tự mò"
🔭 (BigQuery sandbox free) tạo bảng partition by date + cluster by customer; chạy `--dry-run` so bytes scanned khi `SELECT *` vs chọn cột + lọc partition.

➡️ Tiếp: [[d06-airflow-advanced]].
