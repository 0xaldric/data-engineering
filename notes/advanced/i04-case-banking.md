# I04 — Case: Banking Core / Payments Platform

> Mức **chính xác & compliance cao nhất** — sai một xu là sự cố. Sâu hơn fintech ledger [[c07-case-fintech]]. Khung [[c01-system-design-framework]].

## 1. Requirements
- **Functional**: account/balance, transaction (transfer/payment), **double-entry ledger**, real-time balance, fraud, regulatory reporting (báo cáo ngân hàng nhà nước), statement.
- **Consistency**: **exactly-once, không mất/trùng/sai tiền**; immutable audit; ACID mạnh.
- **Compliance**: AML (anti-money-laundering), KYC, audit trail bất biến, lưu trữ dài hạn, data residency.
- **Latency**: balance/transaction real-time; reporting batch; fraud real-time.

## 2. Nguyên tắc (chính xác là vua)
- **Double-entry ledger** ([[c07-case-fintech]]): mỗi giao dịch = debit + credit cân bằng; ledger append-only, immutable; sửa = reversing entry.
- **Idempotency tuyệt đối**: mỗi transaction có idempotency key; ghi lại = no-op ([[40-pipeline-patterns]], [[b08-explain-senior]]).
- **Exactly-once** end-to-end: transactional + dedup ([[d03-kafka-internals]] EOS).
- **Strong consistency** cho balance (không eventual — khách không được thấy balance sai).

## 3. Kiến trúc
```
Core banking (OLTP, ACID) ──CDC──► Kafka ──► lake (BRONZE immutable, audit)
        │  (ledger append-only)                    │ dbt
        ▼                                          ▼
   real-time balance (cache + ledger)        SILVER/GOLD:
        │                                     - regulatory reports (chính xác)
   fraud/AML (stream: pattern bất thường,     - reconciliation (nội bộ vs đối tác/NH)
   transaction monitoring) → alert/hold       - statement, analytics
```

## 4. Đặc thù DE
- **Reconciliation** ⭐ nhiều tầng: nội bộ ledger ↔ core banking ↔ ngân hàng đối tác ↔ payment network. FULL OUTER JOIN tìm lệch ([[c07-case-fintech]]); lệch = điều tra, không auto-fix.
- **Regulatory reporting**: số liệu phải **khớp tuyệt đối**, audit được, đúng hạn (SLA cứng pháp lý). Bitemporal cho báo cáo hồi tố ([[e04-bitemporal]]).
- **AML/fraud**: transaction monitoring (pattern rửa tiền: structuring, velocity, ngưỡng) — stream stateful ([[c03-case-fraud]]).
- **Immutability + audit**: không xoá; mọi truy cập/thay đổi logged; lineage PII ([[64-governance-pii]], [[g05-case-healthcare]]).

## 5. Tech choices & trade-off
- **Storage chính xác**: OLTP ACID (Postgres/Oracle) cho ledger/balance; lake immutable (Delta/Iceberg không VACUUM phá audit) cho reporting/analytics.
- **Chính xác > latency**: chấp nhận chậm hơn để đúng; strong consistency cho balance.
- **CDC** core→lake cho analytics không đụng core ([[51-cdc-debezium]]).
- DQ cực nghiêm: invariant (tổng debit=credit, balance=sum movements), reconciliation=0.

## 6. Scale & failure
- Recovery idempotent, không mất bản ghi.
- Reconciliation lệch → alert P1 (tiền) → điều tra thủ công.
- Replay từ Kafka/raw cho audit.

## Câu hỏi đào sâu
- "Đảm bảo không mất/trùng tiền?" → idempotency key + double-entry invariant + exactly-once + reconciliation.
- "Báo cáo hồi tố (sửa số liệu kỳ trước)?" → bitemporal (as-known vs as-valid).
- "AML real-time?" → stream transaction monitoring stateful + ngưỡng/pattern.

## ✅ "Tự mò"
🔭 Tạo ledger double-entry (entry: txn_id, account, debit, credit); viết invariant check (mỗi txn tổng=0; balance account = sum); reconciliation query (full outer join với "bank statement" giả).

➡️ Tiếp: [[i05-spark-tuning-scenarios]].
