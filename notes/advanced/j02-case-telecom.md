# J02 — Case: Telecom / CDR Platform

> Telco xử lý **Call Detail Records** (CDR) khối lượng khổng lồ: billing chính xác + network analytics. Khung [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: thu CDR (mỗi cuộc gọi/SMS/data session), **rating & charging** (tính tiền), billing, network usage analytics, dropped-call/QoS, churn prediction, fraud (SIM box).
- **Scale**: tỉ CDR/ngày (mỗi thuê bao nhiều event); hàng triệu thuê bao.
- **Latency**: charging real-time (prepaid trừ tiền ngay); billing batch (cuối kỳ); analytics batch.
- **Đặc thù**: **billing chính xác** (tiền), high volume, mediation (chuẩn hoá CDR từ nhiều thiết bị mạng).

## 2. Kiến trúc
```
Network elements (switch/MSC) ──► CDR files/stream ──► MEDIATION (chuẩn hoá, dedup, validate)
        │
        ┌───────────────────┼─────────────────────┐
        ▼ real-time          ▼                      ▼ batch
  Online charging        Kafka                 S3 BRONZE (raw CDR)
  (prepaid: trừ balance) (rated events)             │ Spark/dbt
        │                                            ▼
  balance store          RATING (áp giá cước)  SILVER: rated CDR, sessionize data
        │                                      GOLD: billing, usage analytics, churn features
        ▼                                            │
  charging real-time                           billing run (cuối kỳ) + BI + ML
```

## 3. ⭐ Mediation & Rating (đặc thù telco)
- **Mediation**: CDR từ nhiều loại thiết bị mạng (format khác nhau) → chuẩn hoá về schema chung, **dedup** (cùng cuộc gọi báo từ nhiều element), validate. Như ingestion + DQ ([[i06-dq-framework]]).
- **Rating**: áp bảng giá cước (theo plan, thời điểm, roaming...) lên mỗi CDR → số tiền. SCD cho plan/tariff đổi theo thời gian ([[18-scd]]).
- **Charging**: prepaid (trừ balance real-time, như ledger — [[i04-case-banking]]) vs postpaid (cộng dồn, billing cuối kỳ).

## 4. Phân tích đặc thù
- **Network usage** (peak, congestion theo cell/time), **dropped call rate**, QoS.
- **Churn prediction**: usage giảm, complaint, competitor signals → ML.
- **Fraud**: SIM box (gọi quốc tế giả nội địa), velocity bất thường → stream detection ([[c03-case-fraud]]).
- **Data session**: sessionize data usage ([[a01-sql-gaps-islands]]).

## 5. Tech choices & trade-off
- **Billing chính xác** → CDR không mất/trùng (dedup ở mediation, idempotent), reconciliation revenue.
- **Volume**: partition CDR theo ngày/hour + Parquet; sampling cho phân tích thăm dò; OLAP cho dashboard.
- Real-time charging (prepaid) tách khỏi batch billing.

## 6. DQ & observability
- CDR completeness (mất CDR = mất doanh thu) — volume reconciliation vs network counters.
- Dedup hiệu quả (CDR trùng = tính tiền 2 lần).
- Rating đúng (sample audit so bảng cước).

## Câu hỏi đào sâu
- "Đảm bảo không mất/trùng CDR (billing)?" → mediation dedup + idempotent + volume reconciliation.
- "Rating với tariff đổi?" → SCD2 tariff, áp giá theo thời điểm CDR.
- "Prepaid real-time charging?" → balance store + trừ ngay (như ledger), tách batch billing.

## ✅ "Tự mò"
🔭 Thiết kế CDR schema (caller, callee, start_ts, duration, type, cell_id); dedup query; rating đơn giản (duration × rate theo plan); usage analytics theo cell/giờ.

➡️ Tiếp: [[j03-case-energy]].
