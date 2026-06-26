# H03 — Case: SaaS / Subscription Metrics Platform

> Đo sức khoẻ kinh doanh SaaS: MRR/ARR/churn/LTV. Chính xác (báo cáo nhà đầu tư). Khung [[c01-system-design-framework]]. Tiền đề [[a03-analytics-patterns]], [[18-scd]].

## 1. Requirements
- **Functional**: tính **MRR/ARR**, churn, expansion/contraction, LTV/CAC, cohort retention; dashboard cho exec/đầu tư; chính xác (số lên board).
- **Scale**: vừa (so analytics khác) nhưng **chính xác là vua**.
- **Đặc thù**: subscription **events** (subscribe/upgrade/downgrade/cancel/reactivate); plan thay đổi theo thời gian → **SCD**; recognition theo kỳ.

## 2. Nguồn & kiến trúc
```
Billing system (Stripe/Chargebee) ──CDC/API──► subscription events
        │
        ▼
   BRONZE: raw subscription events (immutable)
        │  build subscription state theo thời gian (SCD2 cho plan changes)
        ▼
   SILVER: dim_subscription (SCD2: plan, mrr, status theo khoảng), dim_customer
        │
        ▼
   GOLD: 
     - mrr_movement (new/expansion/contraction/churn/reactivation mỗi tháng)
     - mrr_snapshot (MRR cuối mỗi tháng — periodic snapshot)
     - cohort retention / LTV
        │
        ▼
   BI exec dashboard
```

## 3. ⭐ MRR & MRR movement (cốt lõi, dễ sai)
**MRR** = doanh thu định kỳ hàng tháng (normalize annual → /12). **MRR movement** phân rã thay đổi MRR giữa 2 kỳ:
```
MRR cuối = MRR đầu + New + Expansion − Contraction − Churn + Reactivation
```
| Loại | Nghĩa |
|------|-------|
| **New** | khách mới subscribe |
| **Expansion** | upgrade / thêm seat (MRR tăng) |
| **Contraction** | downgrade (MRR giảm nhưng còn) |
| **Churn** | hủy (MRR → 0) |
| **Reactivation** | khách cũ quay lại |
→ Phân rã này là báo cáo SaaS quan trọng nhất. Cần **SCD2** trên subscription để biết MRR mỗi khách theo thời gian.

## 4. Churn (2 loại — đừng lẫn)
- **Logo churn**: % **số khách** rời / tổng khách.
- **Revenue churn**: % **MRR** mất / tổng MRR (quan trọng hơn — mất khách lớn ≠ khách nhỏ). **Net revenue churn** = churn − expansion (có thể âm = "negative churn" tốt: expansion bù churn).

## 5. Metrics khác
- **ARR** = MRR × 12. **ARPA** = MRR/khách.
- **LTV** = ARPA × gross margin / churn rate. **CAC** = chi phí marketing/sales per khách mới. **LTV/CAC** > 3 là tốt.
- **Cohort retention** (theo tháng subscribe — [[a03-analytics-patterns]]); **NRR** (Net Revenue Retention).

## 6. Tech & DQ
- **SCD2** cho subscription/plan ([[18-scd]]) — MRR đúng theo thời điểm; **periodic snapshot** MRR cuối kỳ ([[19-fact-types]]).
- **Chính xác**: reconciliation với billing system (MRR tính khớp Stripe?); số lên board không được sai.
- DQ: MRR movement cân bằng (đầu + movements = cuối); không âm vô lý.

## Câu hỏi đào sâu
- "MRR movement tính sao?" → SCD2 subscription, so MRR mỗi khách giữa 2 kỳ, phân loại new/exp/contr/churn.
- "Logo vs revenue churn?" → đếm khách vs đếm MRR; revenue churn quan trọng hơn.
- "Negative churn?" → expansion > churn → MRR tăng dù không thêm khách.

## ✅ "Tự mò"
🔭 Tạo bảng subscription events (subscribe/upgrade/cancel) cho vài khách; build SCD2 trạng thái MRR theo tháng; tính MRR movement (new/expansion/churn) giữa 2 tháng.

➡️ Tiếp: [[h04-case-social-graph]].
