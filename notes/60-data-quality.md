# 60 — Data Quality: Dimensions & Testing ⭐

> Dữ liệu sai còn tệ hơn không có dữ liệu (vì người ta tin nó để ra quyết định). Data quality là trách nhiệm cốt lõi của DE — và lỗi data thường **âm thầm** (không crash).

## 6 chiều chất lượng dữ liệu ⭐
| Chiều | Câu hỏi | Ví dụ test |
|-------|---------|------------|
| **Completeness** | có thiếu không? | `not_null`, tỉ lệ NULL < X% |
| **Uniqueness** | có trùng không? | `unique` khoá, dedup |
| **Validity** | đúng định dạng/miền? | `accepted_values`, regex email, range |
| **Accuracy** | có khớp thực tế? | đối chiếu nguồn tin cậy |
| **Consistency** | nhất quán giữa hệ thống? | tổng con = tổng cha, FK toàn vẹn |
| **Timeliness** | có tươi/đúng hạn? | freshness: max(ts) trong vòng X giờ |

→ Khi thiết kế test, soi qua 6 chiều này để khỏi bỏ sót.

## Công cụ
### dbt tests ([[24-dbt-tests]])
Sẵn trong pipeline transform: `unique/not_null/relationships/accepted_values` + singular + dbt_utils (`accepted_range`, `not_null_proportion`, `expression_is_true`). Là lớp DQ rẻ & gần dữ liệu nhất.

### Great Expectations (GE)
Thư viện DQ mạnh: định nghĩa **Expectation Suite** (tập kỳ vọng) trên dataset, validate, sinh **data docs** (báo cáo HTML).
```python
# minh hoạ ý tưởng
expect_column_values_to_not_be_null("order_id")
expect_column_values_to_be_between("discount", 0, 1)
expect_column_values_to_be_in_set("status", ["completed","shipped","cancelled","returned"])
```
Hợp validate dữ liệu ở **ranh giới ingestion** (trước khi nạp) hoặc trong pipeline.

### Soda
Khai báo check bằng **SodaCL** (YAML) gọn:
```yaml
checks for orders:
  - row_count > 0
  - missing_count(order_id) = 0
  - invalid_percent(discount) < 1%:
      valid min: 0
      valid max: 1
```
Nhẹ, dễ tích hợp CI/scheduler.

## Anomaly detection
Ngoài rule cố định, phát hiện **bất thường thống kê**: row count đột biến (±X% so với trung bình lịch sử), phân phối lệch, tỉ lệ NULL tăng vọt. Công cụ observability ([[62-observability]]) tự học baseline & cảnh báo.

## Xử lý dữ liệu bẩn (không chỉ phát hiện)
- **Fail fast**: chặn pipeline nếu DQ critical fail (dùng `dbt build` chặn downstream — [[24-dbt-tests]]).
- **Quarantine**: tách bản ghi xấu ra bảng riêng, xử lý phần tốt (soft validation — [[12-testing-de]]).
- **Alert**: báo người phụ trách (DQ check trong orchestrator — [[43-airflow-reliability]]).
- **Circuit breaker**: dừng publish nếu chất lượng dưới ngưỡng.

## Shift-left
Bắt lỗi **càng sớm càng tốt** (tại nguồn/ingestion/contract — [[61-data-contracts]]) thay vì để xuống dashboard mới phát hiện. Rẻ hơn nhiều khi sửa sớm.

## ⚠️ Cạm bẫy
- Chỉ test "có chạy không", không test "dữ liệu có đúng không".
- Test quá nhiều/quá nhạy → alert fatigue → bị phớt lờ.
- Phát hiện nhưng không có quy trình xử lý (chỉ log rồi quên).
- Quên timeliness/freshness (dữ liệu đúng nhưng cũ → vẫn sai quyết định).

## ✅ Tự kiểm tra & "tự mò"
- [ ] 6 chiều chất lượng + test tương ứng.
- [ ] dbt tests vs Great Expectations vs Soda — khi nào dùng.
- [ ] Anomaly detection vs rule cố định.
- [ ] Fail fast / quarantine / alert / circuit breaker.
- [ ] Shift-left nghĩa là gì.
- 🔭 *Tự mò:* `pip install great_expectations` (đã có trong requirements!), tạo suite cho `data/raw/order_items.parquet` (discount 0–1, quantity>0, order_id not null), chạy validate. Hoặc thêm dbt_utils `accepted_range` cho discount.

➡️ Tiếp: [[61-data-contracts]].
