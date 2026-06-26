# 27 — dbt Incremental Models

> Code: [`models/marts/fct_daily_sales_inc.sql`](../projects/04-dbt/models/marts/fct_daily_sales_inc.sql)
> Chạy: full-refresh (cutoff) rồi incremental → rows **547 → 730**

**Vấn đề:** fact table lớn (tỉ hàng). Mỗi lần `dbt run` mà build **lại toàn bộ** → chậm & tốn tiền compute. **Incremental** chỉ xử lý/ghi **phần dữ liệu mới** kể từ lần chạy trước.

## Cách hoạt động
```sql
{{ config(materialized='incremental', unique_key='date_key',
          incremental_strategy='delete+insert') }}

select ... from {{ ref('int_sales_enriched') }}
{% if is_incremental() %}
  where date_key > (select max(date_key) from {{ this }})  -- chỉ ngày mới
{% endif %}
```
- **Lần đầu** (bảng chưa có) hoặc `--full-refresh`: `is_incremental()` = **false** → build full.
- **Lần sau**: `is_incremental()` = **true** → chỉ lấy hàng thoả điều kiện lọc (mới hơn watermark) rồi **append/merge** vào bảng cũ.
- **`{{ this }}`** = chính bảng đang build → đọc watermark (max date_key) đã có.

Demo: RUN1 (cutoff 2024-06-30) = 547 ngày; RUN2 incremental (bỏ cutoff) → chỉ thêm ngày sau 2024-06-30, **730 ngày**, **không** đụng lại 547 hàng cũ.

## Incremental strategies ⭐
| Strategy | Cách ghi | Đặc điểm |
|----------|----------|----------|
| **append** | chèn thẳng hàng mới | nhanh nhất; **không** chống trùng — chỉ dùng khi data append-only (log/event) |
| **merge** | `MERGE` theo `unique_key` (update nếu trùng, insert nếu mới) | upsert; chống trùng; mặc định ở nhiều warehouse |
| **delete+insert** | xoá key trùng rồi insert | thay cho merge khi engine không hỗ trợ merge tốt (dùng ở demo) |
| **insert_overwrite** | ghi đè theo **partition** (vd theo ngày) | reprocess cả 1 partition — hợp backfill theo ngày |

`unique_key` quyết định "trùng" để merge/delete — phải là khoá định danh hàng.

## Chọn điều kiện incremental (watermark) cho đúng
- Theo **thời gian**: `where event_ts > (select max(event_ts) from {{ this }})`. Đơn giản nhưng coi chừng **late-arriving data** (dữ liệu đến trễ với timestamp cũ) sẽ bị bỏ sót.
- An toàn hơn: **lookback window** — xử lý lại N ngày gần nhất (`>= max - interval '3 days'`) để bắt dữ liệu trễ/cập nhật, kết hợp `merge` để không trùng.
- Idempotency: với `merge`/`delete+insert` + `unique_key`, chạy lại cùng dữ liệu **không** tạo trùng (xem [[11-api-ingestion]] idempotency).

## Khi nào dùng incremental?
✅ Fact/event table **lớn**, append/ít sửa quá khứ, build full quá chậm/đắt.
❌ Bảng nhỏ (build full vẫn nhanh — đơn giản hơn), hoặc dimension hay đổi toàn bộ. Đừng tối ưu sớm: bắt đầu bằng `table`, chuyển `incremental` khi thật sự chậm.

## Vận hành
- `dbt run` (incremental) hằng ngày chỉ thêm phần mới.
- `dbt run --full-refresh` để **rebuild** khi đổi logic/schema (incremental không tự áp dụng thay đổi cột vào hàng cũ).
- Theo dõi: nếu logic đổi mà quên full-refresh → hàng cũ giữ logic cũ (bug âm thầm).

## ✅ Tự kiểm tra
- [ ] Giải thích `is_incremental()` và `{{ this }}` (watermark)
- [ ] 4 strategy (append/merge/delete+insert/insert_overwrite) & khi nào dùng
- [ ] Vai trò `unique_key`; vì sao merge giúp idempotent
- [ ] Bẫy late-arriving data & cách lookback window
- [ ] Khi nào KHÔNG nên incremental; vì sao cần `--full-refresh` khi đổi logic

➡️ Tiếp theo: [[28-dbt-docs-lineage]] — docs, lineage, seeds.
