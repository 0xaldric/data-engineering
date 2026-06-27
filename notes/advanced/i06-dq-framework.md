# I06 — Deep-dive: Data Quality Framework chi tiết

> Triển khai DQ **end-to-end** như một hệ thống, không phải vài test rời. Sâu hơn [[60-data-quality]], [[f01-testing-strategy]].

## Kiến trúc DQ trong pipeline (theo tầng medallion)
```
Nguồn → [contract/schema check] → BRONZE
   → [DQ gate: freshness, volume, parse rate] → SILVER
   → [DQ gate: not_null/unique/relationships/range] → GOLD
   → [DQ gate: business rule, reconciliation] → BI
        │ fail → quarantine + alert + (circuit breaker dừng publish)
        ▼
   DQ results store → dashboard + report + trend
```
DQ check **ở mỗi ranh giới tầng**; fail thì chặn lan (fail fast).

## 6 chiều + check cụ thể (nhắc [[60-data-quality]])
completeness (not_null, null%) · uniqueness (unique, dedup) · validity (range, accepted_values, regex) · accuracy (reconciliation vs nguồn) · consistency (FK, tổng con=cha) · timeliness (freshness, max ts).

## Công cụ phối hợp
| Lớp | Công cụ | Vai trò |
|-----|---------|---------|
| Contract/schema | pydantic / dbt contract / Schema Registry | chặn schema sai ở cửa ngõ |
| Transform DQ | **dbt tests** | gắn trong build, chặn downstream |
| Ranh giới ingest | **Great Expectations / Soda** | suite + report HTML + validation |
| Anomaly | observability (Elementary/Monte Carlo) | học baseline, cảnh báo |

### Great Expectations (suite)
```python
# expectation suite cho order_items
expect_column_values_to_not_be_null("order_id")
expect_column_values_to_be_between("discount", 0, 1)
expect_column_values_to_be_in_set("status", ["completed","shipped","cancelled","returned"])
expect_column_values_to_be_unique("order_item_id")
expect_table_row_count_to_be_between(min_value=1)
```
### Soda (SodaCL YAML)
```yaml
checks for order_items:
  - missing_count(order_id) = 0
  - invalid_percent(discount) < 1%: { valid min: 0, valid max: 1 }
  - duplicate_count(order_item_id) = 0
  - freshness(loaded_at) < 1h
```

## ⭐ Data Quality Score
Tổng hợp nhiều check thành **điểm** (vd % check pass, weighted theo severity) per dataset → dashboard "sức khoẻ data"; trend theo thời gian; SLA "DQ score ≥ 95%". Giúp prioritize + giao tiếp với business.

## Xử lý khi fail (không chỉ phát hiện)
- **Fail fast**: critical check fail → `dbt build` dừng → data bẩn không xuống dashboard.
- **Quarantine**: tách record xấu ra bảng riêng, xử lý phần tốt (soft validation — [[12-testing-de]]).
- **Circuit breaker**: DQ score dưới ngưỡng → dừng publish/serving.
- **Alert** người phụ trách (hành động được, không fatigue).
- **Severity**: warn (cảnh báo, không chặn) vs error (chặn).

## Quy trình triển khai
```
1. Profile data (hiểu phân phối, NULL%, distinct) → biết check gì hợp lý
2. Định nghĩa expectation/contract per dataset (theo 6 chiều)
3. Gắn check vào pipeline (mỗi tầng) + CI
4. DQ results → store + dashboard + alert
5. Trend & cải tiến (thêm check khi gặp incident)
```

## ⚠️ Cạm bẫy
- Test "pipeline chạy", không test "data đúng".
- Quá nhiều/quá nhạy → alert fatigue.
- Phát hiện nhưng không quy trình xử lý (chỉ log).
- Ngưỡng cứng cho data có mùa vụ (volume Tết khác ngày thường) → anomaly-based.
- DQ chỉ ở gold (muộn) → shift-left về nguồn.

## ✅ "Tự mò"
🔭 `great_expectations` (đã trong requirements): tạo suite cho `data/raw/order_items.parquet` (5+ expectation theo 6 chiều), validate, xem data docs; tính "DQ score" = % expectation pass.

➡️ Tiếp: [[i07-backfill-reprocessing]].
