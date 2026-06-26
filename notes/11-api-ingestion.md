# 11 — Data Ingestion từ REST API (resilient)

> Code: [`projects/02-python-de/05_api_ingest.py`](../projects/02-python-de/05_api_ingest.py)
> Chạy: `python projects/02-python-de/05_api_ingest.py`

Ingestion = đưa dữ liệu từ nguồn ngoài (API, DB, file, queue) vào hệ thống. Nguồn ngoài **không đáng tin** (mạng chập chờn, rate limit, lỗi tạm thời) → code ingest phải **resilient**.

## Các trụ cột của một ingestion job tốt

### 1. Timeout
Luôn đặt `timeout=` cho request. Không có timeout → một request treo có thể làm kẹt cả pipeline vô hạn.

### 2. Retry + Exponential Backoff
Lỗi mạng/5xx/timeout thường **tạm thời** → thử lại. Nhưng thử lại ngay lập tức làm quá tải server → **giãn cấp số nhân**:
```python
wait = backoff * (2 ** (attempt - 1))   # 0.5s, 1s, 2s, 4s...
```
Chỉ retry lỗi **tạm thời** (timeout, connection, 5xx, 429). **Không** retry lỗi 4xx khác (400/401/404 — sai request, thử lại vô ích). Thực tế thêm **jitter** (ngẫu nhiên nhỏ) để tránh "thundering herd". Lib `tenacity` làm sẵn việc này.

### 3. Pagination
API trả dữ liệu theo trang. Các kiểu: `?_page=&_limit=` (offset), cursor/token (`next_cursor`), hoặc `Link` header. Lặp tới khi trang rỗng / hết cursor. Đặt **giới hạn trang tối đa** để tránh vòng lặp vô hạn do bug.

### 4. Rate limiting
API giới hạn số request/giây. Tôn trọng header `Retry-After`, `X-RateLimit-Remaining`; thêm sleep giữa các trang nếu cần. Bị 429 → backoff.

### 5. Lưu RAW trước (bronze / landing) ⭐
Ghi **dữ liệu thô y nguyên** xuống storage **trước khi** transform:
- **Replay được**: logic transform sai → chạy lại từ raw, không phải gọi API lại.
- **Audit/lineage**: giữ bằng chứng nguồn.
- Đây là tầng **bronze** trong kiến trúc medallion (bronze → silver → gold). Sau đó normalize raw → Parquet (silver).

### 6. Idempotency
Chạy lại job **không** tạo trùng/sai. Cách làm: ghi đè theo key xác định (vd path theo ngày `posts/2024-06-26.json`), hoặc upsert/MERGE theo khoá. Quan trọng cho retry & backfill (xem [[ROADMAP]] Phase 5).

### 7. Incremental
Đừng kéo lại toàn bộ mỗi lần. Dùng watermark (timestamp/id lớn nhất đã lấy) để chỉ lấy phần mới (`?updated_since=...`). Giảm tải nguồn & chi phí.

## Resilient fallback (trong demo)
Bọc toàn bộ extract trong try/except: API lỗi/ rỗng → **fallback sang mock data** để pipeline luôn hoàn tất, và **log rõ nguồn** (`_source = api | mock-fallback`) ghi thẳng vào dữ liệu để truy vết. Đã verify cả 2 nhánh:
- Online: 100 records, `source=api`.
- Ép host hỏng: sau retry/backoff thất bại → 100 records mock, `source=mock-fallback`.

> Lưu ý: fallback-mock hợp cho demo/dev. Production thường cho job **fail rõ ràng + alert** thay vì âm thầm dùng mock — tuỳ yêu cầu, nhưng nguyên tắc "không gãy im lặng" thì giống nhau: phải log/đánh dấu nguồn.

## Lineage nhỏ nhưng quan trọng
Ghi metadata vào dữ liệu: `_source`, `_ingested_at`, `_batch_id`. Sau này debug "dòng này từ đâu, lúc nào" cực nhanh. Tiền đề cho data lineage (Phase 8).

## ✅ Tự kiểm tra
- [ ] Luôn đặt timeout; phân biệt lỗi nên/không nên retry
- [ ] Viết exponential backoff (+hiểu vì sao cần jitter)
- [ ] Xử lý pagination có giới hạn trang
- [ ] Giải thích vì sao lưu RAW trước khi transform (bronze, replay)
- [ ] Idempotency & incremental (watermark)

➡️ Tiếp theo: [[12-testing-de]] — viết code sạch + test cho transform.
