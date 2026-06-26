# H02 — Case: Marketplace / Two-sided Platform

> Như Airbnb/eBay/Etsy/Grab: **hai phía** (buyer + seller) cần cân bằng. Khung [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: listing (seller), search/discovery (buyer), transaction, review/trust, payout seller; analytics cả 2 phía: GMV, take rate, supply-demand, conversion, seller/buyer retention; search ranking; fraud.
- **Scale**: triệu listing, triệu user 2 phía, nhiều event search/view/transaction.
- **Latency**: search/ranking ~giây; analytics batch; fraud real-time.
- **Đặc thù**: **two-sided** (sức khoẻ phụ thuộc cân bằng cung-cầu), cold start (seller/listing mới), trust/review.

## 2. Kiến trúc
```
Buyer events (search/view/click) ──► Kafka ──► lake + stream (ranking signals)
Seller events (list/update/fulfill) ─┘
Transactions (OLTP) ──CDC──► lake (GMV, payout — chính xác như fintech)
        │
        ▼
   BRONZE → SILVER (sessionize, conform) → GOLD:
     - GMV, take rate, AOV theo category/region
     - supply (listing active) vs demand (search/view) theo segment
     - seller cohort (retention, GMV per seller), buyer cohort
     - search ranking features (CTR, conversion, freshness)
        │
        ▼
   BI (marketplace health) + search ranking (online) + fraud + payout reconciliation
```

## 3. Metrics & analytics đặc thù two-sided ⭐
- **GMV** (Gross Merchandise Value): tổng giá trị giao dịch. **Take rate** = revenue/GMV (% nền tảng giữ).
- **Supply-demand balance**: listing active (supply) vs search/intent (demand) theo segment/region/time → phát hiện thiếu cung (search nhiều, ít listing → cần thêm seller) hoặc thừa.
- **Liquidity**: % listing bán được / % search ra kết quả thoả mãn.
- **Hai cohort**: seller cohort (GMV theo tháng tham gia, seller retention) + buyer cohort. Sức khoẻ = cả hai.
- **Cross-side network effect**: nhiều seller → nhiều buyer → đo vòng lặp.

## 4. Search ranking (data cho ML)
- Features: CTR, conversion rate, giá, review, freshness, personalization. Feature pipeline (giống recsys — [[c09-case-recsys]]).
- Feedback loop: ranking ảnh hưởng cái buyer thấy → bias (chỉ thấy cái rank cao). Cần exploration + logging đầy đủ.

## 5. Tech choices & trade-off
- **CDC transactions** → GMV/payout chính xác ([[c07-case-fintech]] reconciliation cho payout).
- **Stream** cho ranking signals + fraud; **batch** cho cohort/GMV analytics.
- Lakehouse medallion; star/OBT cho mart 2 phía.

## 6. Scale & failure
- Skew: seller/category lớn (Amazon-like top seller) → skew trong aggregate.
- Cold start listing/seller → fallback ranking.
- Fraud (fake listing/review) → detection ([[c03-case-fraud]]).
- Payout reconciliation (tiền seller) phải đúng.

## Câu hỏi đào sâu
- "Đo sức khoẻ marketplace?" → GMV + take rate + supply-demand balance + cả 2 cohort + liquidity.
- "Thiếu cung ở đâu?" → demand (search) cao + supply (listing) thấp theo segment.
- "Search ranking feedback bias?" → exploration + log mọi impression.

## ✅ "Tự mò"
🔭 Coi e-commerce như marketplace (thêm seller_id giả cho product): tính GMV theo category, supply (listing active) vs demand (orders) theo category — phát hiện mất cân bằng.

➡️ Tiếp: [[h03-case-saas-metrics]].
