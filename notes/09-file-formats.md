# 09 — File Formats: CSV vs Parquet ⭐

> Code: [`projects/02-python-de/03_formats_benchmark.py`](../projects/02-python-de/03_formats_benchmark.py)
> Chạy: `python projects/02-python-de/03_formats_benchmark.py`

Chọn đúng định dạng lưu trữ là một trong những quyết định ảnh hưởng lớn nhất tới hiệu năng & chi phí của một hệ thống dữ liệu. Đây là kiến thức DE cốt lõi.

## Kết quả benchmark (1.2M hàng, đo thật)
| | CSV | Parquet (snappy) | Parquet (zstd) |
|--|-----|------------------|----------------|
| Dung lượng | 41.3 MB (1.00x) | 9.8 MB (0.24x) | **6.3 MB (0.15x)** |
| Đọc full | 185 ms | **19 ms (9.6× nhanh)** | — |
| Đọc 1 cột | 121 ms | **5.5 ms (22× nhanh)** | — |

→ Parquet **nhỏ hơn ~4–6×** và **đọc nhanh ~10–22×**. Trên cloud (S3) nhỏ hơn = rẻ hơn cả lưu trữ lẫn truyền/scan.

## Row-based vs Columnar — khác biệt gốc rễ
- **Row-based (CSV, JSON, Avro):** lưu lần lượt từng *hàng* (a1,b1,c1, a2,b2,c2...). Tốt khi ghi/đọc cả bản ghi (OLTP, streaming append).
- **Columnar (Parquet, ORC):** lưu lần lượt từng *cột* (a1,a2,a3..., b1,b2,b3...). Tốt cho analytics (OLAP) vì:
  1. **Column pruning** — chỉ đọc cột cần (query analytics thường dùng vài cột trong hàng chục). Benchmark: Parquet đọc 1 cột nhanh hơn full 3.5×; **CSV gần như không đổi (1.5×)** vì vẫn phải quét cả file.
  2. **Nén tốt hơn** — giá trị cùng cột giống nhau → encoding (dictionary, RLE) + compression hiệu quả hơn nhiều.
  3. **Vectorized scan** — đọc nguyên cột vào mảng, xử lý SIMD.

## Cấu trúc Parquet (vì sao nó thông minh)
```
File
 └─ Row Group (vd mỗi ~1M hàng — benchmark có 2 row groups)
     └─ Column Chunk (mỗi cột trong row group)
         └─ Page (đơn vị nén/encode nhỏ nhất)
     └─ + statistics mỗi cột: min/max/null_count
 └─ Footer: schema + metadata + vị trí các row group
```
- **Row group** cho phép đọc/xử lý song song và bỏ qua cả nhóm.
- **Statistics (min/max)** mỗi column chunk cho phép **predicate pushdown**: query `WHERE discount > 0.1` → bỏ qua row group có max ≤ 0.1 mà không cần đọc. Benchmark: lọc khi đọc ra 204k hàng chỉ 3.9 ms.
- **Encoding**: dictionary (giá trị lặp), run-length (RLE), delta — trước cả khi nén.

## Compression codecs
| Codec | Tỉ lệ nén | Tốc độ | Khi nào |
|-------|-----------|--------|---------|
| **snappy** | vừa (0.24x) | rất nhanh | mặc định, cân bằng |
| **zstd** | tốt nhất (0.15x) | nhanh | xu hướng mới, nén cao mà vẫn nhanh |
| gzip | tốt (0.20x) | chậm hơn | khi cần tương thích rộng |
| none | — (0.25x) | nhanh nhất | hiếm; vẫn nhỏ hơn CSV nhờ encoding |

→ Thực tế nên dùng **zstd** hoặc **snappy**.

## Các định dạng khác (xem [[10-json-avro]])
- **JSON/JSONL** — semi-structured, dễ đọc, từ API; cồng kềnh, chậm. JSONL (mỗi dòng 1 JSON) hợp cho streaming/append.
- **Avro** — row-based + **schema kèm theo**, mạnh về **schema evolution**; chuẩn de-facto cho Kafka (Phase 6).
- **ORC** — columnar giống Parquet, phổ biến trong hệ Hive.
- **Delta/Iceberg** — *table format* xây TRÊN Parquet, thêm ACID/time-travel (Phase 4).

## Quy tắc thực hành cho DE
- Lưu **raw/landing** (bronze): giữ nguyên gốc (thường JSON/CSV từ nguồn).
- Lưu **analytics/silver-gold**: luôn **Parquet** (hoặc Delta/Iceberg).
- Partition file theo cột hay lọc (vd ngày) để cắt giảm dữ liệu quét.
- Tránh "small files problem": nhiều file nhỏ → đọc chậm; gộp thành file/row-group đủ lớn (~128–512MB).

## ✅ Tự kiểm tra
- [ ] Giải thích row-based vs columnar và vì sao columnar thắng cho analytics
- [ ] Nêu 3 cơ chế Parquet: column pruning, predicate pushdown (min/max), encoding+compression
- [ ] Vẽ được cấu trúc Parquet (row group → column chunk → page)
- [ ] Chọn codec phù hợp (snappy/zstd)
- [ ] Biết quy tắc raw=gốc, analytics=Parquet, và small-files problem

➡️ Tiếp theo: [[10-json-avro]] — JSON/JSONL & Avro schema evolution.
