# K02 — Case: Insurance Data Platform

> Bảo hiểm: policy + claims, định giá rủi ro, chính xác + regulatory + **bitemporal** (sửa hồi tố). Khung [[c01-system-design-framework]]. Liên hệ [[e04-bitemporal]], [[c07-case-fintech]].

## 1. Requirements
- **Functional**: quản policy lifecycle (quote→bind→renew→cancel), xử lý claims, underwriting/risk pricing, fraud detection, **actuarial/reserving** (dự phòng bồi thường), regulatory reporting.
- **Consistency**: chính xác (tiền bồi thường + dự phòng), audit, immutable.
- **Compliance**: regulatory (Solvency, IFRS17), lưu trữ dài, audit hồi tố.
- **Đặc thù**: **bitemporal** (policy/claim sửa hồi tố — biết khi nào vs đúng khi nào), long-tail claims (claim kéo dài nhiều năm), risk modeling.

## 2. Kiến trúc
```
Core insurance (policy admin, claims) ──CDC──► lake
Quotes/web events ──► Kafka
External (weather, fraud DB, credit) ──► ingest
        │
        ▼
   BRONZE (immutable) → SILVER:
     - dim_policy (BITEMPORAL: valid time + transaction time)
     - fct_claims (accumulating snapshot: reported→assessed→paid→closed)
     - fct_premium
        │
        ▼
   GOLD: loss ratio, reserving, risk segments, fraud features
        │
        ▼
   actuarial/reporting (chính xác) + ML (pricing, fraud, claim severity)
```

## 3. ⭐ Bitemporal (vì sao insurance cần)
Claim/policy **sửa hồi tố** thường xuyên (claim được đánh giá lại, policy backdated). Cần trả lời:
- "Dự phòng (reserve) tại quý 1 là bao nhiêu **theo cái ta biết lúc đó**?" (transaction time) vs "đúng ra là bao nhiêu" (valid time).
- Báo cáo regulatory đã nộp quý trước phải tái dựng được → **bitemporal** ([[e04-bitemporal]]): valid_from/to + txn_from/to.
- Audit: ai đổi gì khi nào.

## 4. Claims = accumulating snapshot ⭐
Claim có vòng đời nhiều mốc (reported → assessed → approved → paid → closed/reopened), kéo dài (long-tail) → **accumulating snapshot** ([[19-fact-types]]): nhiều date role + lag (time-to-settle); hàng UPDATE khi claim tiến triển; có thể **reopen** (claim đóng rồi mở lại).

## 5. Metrics & analytics
- **Loss ratio** = claims paid / premium earned (sức khoẻ cốt lõi).
- **Reserving** (IBNR — Incurred But Not Reported): ước lượng dự phòng cho claim chưa báo — actuarial model, cần data lịch sử chính xác.
- **Risk segmentation/pricing**: features cho underwriting model (như recsys features — [[c09-case-recsys]]).
- **Fraud**: claim bất thường ([[c03-case-fraud]]).

## 6. Tech & DQ
- Bitemporal modeling; immutable + audit ([[g05-case-healthcare]], [[i04-case-banking]]).
- Reconciliation (claims paid khớp payment, reserve khớp actuarial).
- DQ nghiêm (sai reserve = sai báo cáo regulatory).

## Câu hỏi đào sâu
- "Báo cáo reserve quý trước tái dựng?" → bitemporal (as-known).
- "Claim long-tail model sao?" → accumulating snapshot + reopen handling.
- "Loss ratio?" → claims/premium, cẩn thận earned vs written premium.

## ✅ "Tự mò"
🔭 Thiết kế fct_claims accumulating snapshot (reported/assessed/paid/closed dates + lag) + dim_policy bitemporal; query loss ratio + time-to-settle trung bình.

➡️ Tiếp: [[k03-case-realestate]].
