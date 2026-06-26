# F01 — Data Testing Strategy toàn diện

> Tổng hợp & nâng cao [[12-testing-de]], [[24-dbt-tests]], [[60-data-quality]]: một **chiến lược test** mạch lạc cho cả pipeline, không phải vài test rời rạc.

## Kim tự tháp test cho Data (testing pyramid)
```
          ▲  ít, chậm, đắt
   ┌──────────────┐
   │ E2E / pipeline│   chạy pipeline thật trên data mẫu, kiểm output cuối
   ├──────────────┤
   │ Integration  │   nhiều bước + DB/warehouse tạm (DuckDB/container)
   ├──────────────┤
   │ Data quality │   trên DỮ LIỆU THẬT: not_null/unique/relationships/range/freshness
   ├──────────────┤
   │ Schema/contract│  schema khớp contract (pydantic/dbt contract/Schema Registry)
   ├──────────────┤
   │  Unit (logic) │   hàm transform thuần (pytest) — nhiều, nhanh, rẻ
   └──────────────┘
          ▼  nhiều, nhanh, rẻ
```
Cân bằng: nhiều unit (rẻ) ở đáy, ít e2e (đắt) ở đỉnh.

## 2 loại test khác nhau (đừng lẫn)
| | Test **CODE** | Test **DATA** |
|--|---------------|---------------|
| Kiểm | logic transform đúng không | dữ liệu thật có đúng/sạch không |
| Khi | mỗi commit/PR (CI) | mỗi lần pipeline chạy (runtime) |
| Công cụ | pytest | dbt tests / GE / Soda |
| Dữ liệu | mẫu nhỏ cố định | data production |
→ Cần **cả hai**. Code đúng vẫn có thể nuốt data bẩn; data sạch vẫn có thể bị logic sai biến đổi.

## Test ở đâu trong pipeline (shift-left)
```
Nguồn → [contract/schema test] → ingest → [DQ: freshness/volume] → 
   bronze → [schema] → silver → [DQ: not_null/unique/relationships] →
   gold → [business rule + reconciliation] → BI
```
Bắt lỗi **càng sớm càng tốt** (contract ở nguồn) → rẻ hơn nhiều khi sửa muộn ([[61-data-contracts]]).

## 6 chiều chất lượng (checklist khi viết test)
completeness (not_null) · uniqueness (unique) · validity (range/accepted_values/regex) · accuracy (đối chiếu nguồn/reconciliation) · consistency (FK relationships, tổng con=cha) · timeliness (freshness). ([[60-data-quality]])

## Phối hợp công cụ
- **pytest**: unit cho `transforms.py` (logic thuần).
- **dbt tests**: data quality trong transform layer (`dbt build` chặn downstream khi fail).
- **Great Expectations / Soda**: DQ ở ranh giới ingest + report.
- **Schema Registry / dbt contract / pydantic**: schema/contract.
- **CI**: chạy unit + `dbt build` trên data mẫu mỗi PR ([[58-cicd]]).

## Test data tổng hợp
Dùng data mẫu **nhỏ, cố định, deterministic** (như `gen_ecommerce.py` seed=42) cho unit/integration → nhanh, lặp lại được, kiểm được kết quả mong đợi. Không phụ thuộc data production cho test logic.

## Xử lý khi test fail
fail fast (chặn `dbt build`) · quarantine record xấu · alert · circuit breaker (dừng publish nếu DQ dưới ngưỡng). Test phát hiện phải đi kèm **quy trình xử lý** ([[60-data-quality]], [[f02-reliability-sre]]).

## ⚠️ Cạm bẫy
- Chỉ test "pipeline chạy xong", không test "data đúng".
- Test quá nhạy → alert fatigue.
- Không có test data cố định → test flaky.
- Test data mà không test code (hoặc ngược lại).
- Phát hiện nhưng không có runbook xử lý.

## ✅ "Tự mò"
🔭 Vẽ kim tự tháp test cho pipeline e-commerce đã build; map từng tầng vào công cụ (pytest 14 test có rồi, dbt 17 test có rồi, thêm GE ở ingest + freshness check).

➡️ Tiếp: [[f02-reliability-sre]].
