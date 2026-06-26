# 12 — Clean & Tested Code cho Data Engineering

> Code: [`transforms.py`](../projects/02-python-de/transforms.py) · [`tests/test_transforms.py`](../projects/02-python-de/tests/test_transforms.py)
> Chạy: `pytest projects/02-python-de -q` → **14 passed**

DE thường bị xem nhẹ chuyện test ("chỉ là script"). Nhưng pipeline sai = dữ liệu sai = quyết định sai, mà lỗi data lại **âm thầm** (không crash). Code có test là khác biệt giữa junior và senior DE.

## Nguyên tắc vàng: tách Pure logic khỏi I/O ⭐
```
[ đọc API/DB/file ]  →  [ TRANSFORM thuần ]  →  [ ghi warehouse ]
     I/O (khó test)        pure (DỄ test)          I/O (khó test)
```
- **Pure function**: cùng input luôn ra cùng output, không đọc file/gọi mạng, không side-effect.
- Gom logic nghiệp vụ (tính toán, validate, biến đổi) vào hàm pure trong `transforms.py`; để I/O ở `etl_pipeline.py`. Khi đó test chỉ cần truyền dữ liệu nhỏ vào hàm và so kết quả — **không cần DB/mạng**.

## Type hints + validation
- **Type hints** (`def f(x: float) -> str`) — tài liệu sống, bắt lỗi sớm bằng `mypy`, IDE gợi ý tốt.
- **pydantic** — validate schema lúc runtime tại "cửa ngõ" dữ liệu:
  ```python
  class OrderItemRecord(BaseModel):
      quantity: int
      @field_validator("quantity")
      def _positive(cls, v):
          if v <= 0: raise ValueError("quantity must be > 0")
          return v
  ```
  Bắt dữ liệu bẩn ngay khi vào, kèm thông báo lỗi rõ. `dataclass` hợp cho object nội bộ đơn giản; `pydantic` khi cần validate/parse.

## Mẫu "soft validation" (gom lỗi thay vì gãy)
`validate_records` trả về `(valid, errors)` thay vì raise ở record đầu tiên hỏng → pipeline xử lý được phần tốt, cách ly phần xấu (quarantine), vẫn báo cáo lỗi. Rất hợp ingestion thực tế (dữ liệu nguồn luôn có rác).

## pytest — nền tảng
```python
def test_basic():
    assert compute_line_total(100, 2, 0.1) == 180.0

def test_raises():
    with pytest.raises(ValueError, match="quantity"):
        compute_line_total(10, 0)
```
- **Assertion thường** (`assert`) — pytest tự diễn giải khi fail.
- **`pytest.raises`** — kiểm tra hàm ném đúng lỗi.
- **`@pytest.mark.parametrize`** — chạy 1 test với nhiều bộ input (kiểm **ranh giới**: 200→premium, 199.99→mid...). Test biên là nơi bug hay trốn.
- **`@pytest.fixture`** — dữ liệu/khởi tạo dùng chung, tạo data test nhỏ (vài hàng đủ kiểm logic).

## Test gì trong một pipeline DE?
| Loại | Kiểm gì | Công cụ |
|------|---------|---------|
| **Unit** | logic transform (hàm pure) | pytest |
| **Schema/contract** | cột, kiểu, ràng buộc | pydantic, pandera |
| **Data quality** | NULL, unique, range, FK trên dữ liệu thật | Great Expectations, dbt tests (Phase 8) |
| **Integration** | pipeline đầu-cuối với DB tạm | pytest + DuckDB/container |

## Test data nhỏ & cố định
Dùng **vài hàng tự tạo** (như fixture `items`/`products`), không phụ thuộc dataset thật/lớn → test nhanh, deterministic, dễ suy luận kết quả mong đợi. Test biên: fan-out (inner join loại product lạ), làm tròn (9.99*3=29.97), discount ngoài [0,1].

## Bonus: chất lượng code
- `ruff`/`black` — lint & format tự động.
- `mypy` — kiểm type tĩnh.
- Cấu trúc: hàm nhỏ, một việc; tên rõ; tránh side-effect ẩn.
- CI chạy `pytest` mỗi PR (Phase 7).

## ✅ Tự kiểm tra
- [ ] Giải thích vì sao tách pure logic khỏi I/O giúp test được
- [ ] Viết pydantic model + validator bắt dữ liệu bẩn
- [ ] Dùng `parametrize` test ranh giới, `pytest.raises` test lỗi, `fixture` tạo data nhỏ
- [ ] Phân biệt unit / schema / data-quality / integration test
- [ ] Hiểu "soft validation" (gom lỗi, quarantine) cho ingestion

➡️ Tiếp theo: [[13-logging-config]] — logging, config, error handling.
