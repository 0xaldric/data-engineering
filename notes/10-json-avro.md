# 10 — JSON/JSONL & Avro (schema evolution)

> Code: [`projects/02-python-de/04_json_avro.py`](../projects/02-python-de/04_json_avro.py)
> Chạy: `python projects/02-python-de/04_json_avro.py`

## JSON & JSONL
- **JSON** — một object/array lớn. Phải đọc & parse **cả file** mới dùng được → không hợp file lớn / streaming.
- **JSONL (JSON Lines / NDJSON)** — **mỗi dòng một JSON object**. Đọc/ghi **từng dòng** (append được, stream được, chia nhỏ song song được). Đây là dạng chuẩn cho log, export big data, message. Trong demo JSONL (208B) còn gọn hơn JSON pretty (386B).

### Semi-structured & flatten
Dữ liệu từ API/NoSQL thường **lồng nhau** (nested object + array). DE phải "làm phẳng" về dạng bảng:
```python
pd.json_normalize(orders, record_path="items",
                  meta=["order_id", ["customer", "country"]])
```
- `record_path` — mảng cần "nổ" (explode) thành nhiều hàng (mỗi item 1 hàng).
- `meta` — field ở cấp trên muốn kéo theo; path lồng viết dạng list `["customer","country"]` → cột `customer.country`.
- Kết quả: 1 đơn 2 items → 2 hàng, kèm `order_id` và `customer.country`. Đây là bước "shred" nested → relational rất hay gặp.

## Avro ⭐
**Avro** = định dạng **row-based, binary, có schema**. Đặc điểm quan trọng nhất: **schema đi kèm dữ liệu** (nhúng trong file, hoặc quản lý qua Schema Registry).

- Compact (binary, nhỏ hơn JSON nhiều), nhanh.
- Row-based → hợp **ghi/append theo bản ghi** và **streaming** (khác Parquet columnar hợp đọc-phân-tích).
- Là **chuẩn de-facto cho Apache Kafka** (Phase 6): producer/consumer trao đổi message Avro + Schema Registry.

### Schema Evolution — vì sao Avro mạnh
Dữ liệu thật thay đổi theo thời gian (thêm/bớt field). Avro cho phép **writer schema** (lúc ghi) khác **reader schema** (lúc đọc) và tự "hoà giải" (resolution):
- **Thêm field có `default`** → **backward compatible**: reader mới đọc data cũ, field thiếu lấy default.
  ```python
  # data ghi bằng v1 (order_id, amount), đọc bằng v2 (thêm currency default "USD")
  fastavro.reader(buf, reader_schema=schema_v2)  # -> currency = "USD"
  ```
  Demo chạy đúng: data v1 đọc bằng reader v2 ra `currency="USD"`.
- **Xoá field có default** → **forward compatible**: reader cũ đọc data mới, bỏ qua field thừa.
- Quy tắc an toàn: **thêm field luôn kèm `default`**, đừng đổi kiểu/đổi tên (rename = xoá+thêm).

Tương thích:
| Loại | Ý nghĩa |
|------|---------|
| Backward | schema mới đọc được data cũ (phổ biến nhất) |
| Forward | schema cũ đọc được data mới |
| Full | cả hai chiều |

## So sánh nhanh: chọn định dạng nào?
| Định dạng | Kiểu | Schema | Hợp cho |
|-----------|------|--------|---------|
| CSV | row, text | không | trao đổi đơn giản, người đọc |
| JSON/JSONL | row, text | không (lỏng) | API, log, nested data |
| **Avro** | row, binary | **có, evolve tốt** | streaming/Kafka, ghi-append |
| **Parquet** | **columnar**, binary | có | **analytics/warehouse** (đọc-phân-tích) |

Mẫu hình điển hình: **Avro cho đường streaming/ingest** → chuyển thành **Parquet cho lớp analytics**. Xem [[09-file-formats]] và [[ROADMAP]] Phase 6.

## ✅ Tự kiểm tra
- [ ] Phân biệt JSON vs JSONL và vì sao JSONL hợp big data/streaming
- [ ] Flatten nested bằng `json_normalize` (record_path + meta)
- [ ] Giải thích vì sao Avro gắn liền với Kafka (schema + row + binary)
- [ ] Backward vs forward compatibility; quy tắc "thêm field phải có default"
- [ ] Biết khi nào Avro (streaming) vs Parquet (analytics)

➡️ Tiếp theo: [[11-api-ingestion]] — ingest dữ liệu từ REST API (resilient).
