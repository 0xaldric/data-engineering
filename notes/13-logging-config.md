# 13 — Logging, Config & Error Handling

> Code: [`projects/02-python-de/utils.py`](../projects/02-python-de/utils.py)
> Chạy: `python projects/02-python-de/utils.py` · đã refactor [`05_api_ingest.py`](../projects/02-python-de/05_api_ingest.py) dùng module này.

Pipeline chạy **không người trông** (đêm, theo lịch). Khi hỏng, thứ duy nhất ta có để điều tra là **log**. Logging/config/error-handling tốt là yêu cầu production, không phải tuỳ chọn.

## Logging (không dùng `print`)
- `print` không có level, không timestamp, không định tuyến được, khó tắt/bật. **Dùng `logging`**.
- Levels: `DEBUG` (chi tiết debug) < `INFO` (mốc bình thường) < `WARNING` (bất thường nhưng chạy tiếp) < `ERROR` (thất bại) < `CRITICAL`. Production thường chạy `INFO`, bật `DEBUG` khi điều tra.
- Format nên có **timestamp + level + tên logger + message**: `2026-06-26 04:37 [INFO ] api_ingest: ...`.
- `get_logger()` phải **idempotent** — kiểm `if not logger.handlers` để khỏi gắn handler trùng (gọi nhiều lần → log nhân đôi là bug kinh điển). Đặt `propagate=False` để không lọt lên root logger.

### Structured logging (nâng cao)
Production hay log dạng **JSON** (key-value) thay vì text, để hệ thống (ELK, Datadog, CloudWatch) **parse & truy vấn** được: `{"ts":..., "level":"INFO", "event":"page_fetched", "page":3, "rows":20}`. Lib: `structlog`, `python-json-logger`. Lợi ích: filter/aggregate log theo field.

## ⚠️ KHÔNG BAO GIỜ log secret
Mật khẩu, token, API key, PII **không** được vào log (log thường lưu lâu, nhiều người xem). Luôn **redact** trước khi log:
```python
redact({"user":"admin","password":"hunter2"})  # -> {"user":"admin","password":"***"}
```
Đây là lỗi bảo mật rất phổ biến (log connection string kèm mật khẩu). Xem [[ROADMAP]] Phase 8 (governance/PII).

## Config tách khỏi code ⭐
**Đừng hardcode** URL, đường dẫn, tham số. Tách ra để đổi môi trường (dev/staging/prod) mà không sửa code. Thứ tự ưu tiên chuẩn:
```
defaults  <  file config (YAML)  <  biến môi trường (env)
```
- **YAML/TOML** cho config có cấu trúc, versioned trong repo (KHÔNG để secret trong này).
- **Env vars** cho giá trị theo môi trường & **secret** (12-factor app). `DE_PAGE_SIZE=50` override `page_size`.
- **Secret thật** → secret manager (Vault, AWS Secrets Manager), không commit, không log.
- `dataclass` Config giúp có **default + ép kiểu + gợi ý IDE**.

## Error handling
- **Custom exception** phân tầng: `PipelineError` → `ExtractError`/`TransformError`/`LoadError`. Bắt theo loại để xử lý khác nhau (extract lỗi → retry; transform lỗi → quarantine record).
- **Retry decorator** tái dùng: bọc bất kỳ hàm "có thể lỗi tạm thời" với `@retry(...)` thay vì lặp lại logic backoff khắp nơi (DRY). Đã refactor `http_get_json` trong api_ingest từ vòng lặp tay → `@retry` của utils.
- **Fail fast vs fail soft**: lỗi cấu hình/code → fail ngay; lỗi 1 record dữ liệu bẩn → cô lập, tiếp tục (xem soft-validation ở [[12-testing-de]]).
- **Không nuốt lỗi im lặng**: `except: pass` là cấm kỵ — tối thiểu phải log.

## Tái sử dụng (DRY)
Gom logging/config/retry/exception vào **một** `utils.py` dùng chung → mọi script nhất quán, sửa một chỗ. Đây là khác biệt giữa "đống script rời" và "codebase pipeline".

## ✅ Tự kiểm tra
- [ ] Dùng `logging` thay `print`; hiểu các level
- [ ] Viết `get_logger` idempotent (không nhân đôi handler)
- [ ] Không log secret — biết redact
- [ ] Config theo thứ tự defaults < YAML < env; secret qua env/secret manager
- [ ] Custom exception phân tầng + retry decorator tái dùng
- [ ] Hiểu fail-fast vs fail-soft, cấm nuốt lỗi im lặng

➡️ Tiếp theo: [[14-etl-capstone]] — ghép tất cả thành pipeline ETL end-to-end.
