# H07 — Mock Interview: Full DE Interview Walkthrough

> Mô phỏng một vòng phỏng vấn Data Engineer hoàn chỉnh: SQL → system design → conceptual → behavioral. Tự luyện như thật. Tổng hợp Module A–F.

## Vòng 1 — SQL coding (45')
### Bài 1: "Top 2 sản phẩm doanh thu mỗi category, completed."
```sql
select category, product_name, revenue from (
  select p.category, p.product_name, sum(oi.line_total) revenue,
    row_number() over (partition by p.category order by sum(oi.line_total) desc) rn
  from order_items oi join products p using(product_id) join orders o using(order_id)
  where o.status='completed'
  group by 1,2
) where rn <= 2;
```
**Nói khi code:** "Tôi join về grain order-item, lọc completed sớm, group theo category+product, dùng ROW_NUMBER partition by category để rank, lọc rn≤2. Nếu cần giữ ties dùng RANK." → thể hiện hiểu grain + window + trade-off ([[a04-sql-interview-1]]).

### Bài 2: "Tỉ lệ khách quay lại tháng sau (retention M1)."
→ cohort theo first-month, đếm distinct user active ở month_offset=1 / cohort size ([[a03-analytics-patterns]], [[g02-sql-interview-4]]). Nói rõ định nghĩa "active".

**Tip đánh giá:** người phỏng vấn xem: đúng kết quả? hiểu **grain/ties/NULL**? nói được tư duy? tối ưu (lọc sớm)? edge case?

## Vòng 2 — System Design (45'): "Thiết kế analytics cho app giao đồ ăn"
Đi qua framework 6 bước ([[c01-system-design-framework]]) **thành tiếng**:
1. **Clarify**: real-time hay batch? metric gì (GMV, delivery time, courier utilization)? scale (orders/ngày)? latency?
2. **Scale**: 1M order/ngày × ~2KB → ~2GB/ngày + location stream lớn.
3. **Data model**: order fact (accumulating snapshot: placed→prepared→picked→delivered + lag), dim courier/restaurant/customer.
4. **Pipeline**: CDC orders→lake; location stream→Kafka→Flink (courier ETA/utilization real-time); batch dbt marts; serving warehouse + Redis cho real-time.
5. **Scale/failure**: partition theo region/order; idempotent; backfill; skew giờ cao điểm.
6. **DQ/observability**: order không đóng (thiếu delivered), reconciliation GMV vs payment, freshness.
**Nêu trade-off:** batch vs stream (chỉ stream cái cần ETA/dispatch); cost. (Giống [[c05-case-ridesharing]].)

**Tip đánh giá:** clarify trước khi vẽ? nêu trade-off? nhắc idempotency/failure/DQ? không over-engineer?

## Vòng 3 — Conceptual (30')
1. "Idempotency là gì, vì sao quan trọng?" → [[b08-explain-senior]].
2. "Shuffle trong Spark, vì sao đắt?" → 3 chi phí, giảm shuffle.
3. "Exactly-once thật sự đạt thế nào?" → at-least-once + idempotent sink.
4. "SCD Type 2 và vì sao cần surrogate key?" → [[18-scd]].
5. "Partition vs index?" → OLAP pruning vs OLTP B-tree.
→ Trả lời theo cấu trúc: định nghĩa → vì sao → cách → **trade-off** → ví dụ.

## Vòng 4 — Behavioral (30')
1. "Kể về pipeline production bị lỗi." → STAR: idempotent rerun + thêm contract ([[b07-behavioral-star]]).
2. "Quyết định kỹ thuật khó." → chọn Delta vs Iceberg / batch vs stream + lý do + điều làm khác.
→ STAR, dùng "tôi", có con số kết quả.

## Tips tổng (người phỏng vấn tìm gì)
- **Communication**: nói tư duy ra tiếng, không im lặng code.
- **Clarify**: hỏi requirements trước khi giải.
- **Trade-off**: luôn nêu đánh đổi, không tuyệt đối hoá.
- **Depth signals**: nhắc grain, idempotency, fan-out, shuffle, failure, DQ — những thứ phân biệt DE thật.
- **Honesty**: không biết thì nói + cách bạn sẽ tìm hiểu.

## ✅ "Tự mò"
🔭 Tự bấm giờ làm 2 bài SQL (45') + 1 system design nói thành tiếng (45') + ghi âm trả lời 5 câu conceptual. Nghe lại, chấm theo "tips đánh giá".

➡️ Tiếp: [[00-extraH-summary]].
