# C07 — Case: Fintech Ledger + Reconciliation ⭐

> Đặc trưng: **chính xác tuyệt đối** — không được mất/trùng/sai một đồng. Đây là case "consistency là vua", ngược với analytics "gần đúng OK".

## 1. Requirements
- **Functional**: sổ cái (ledger) mọi giao dịch tiền; số dư tài khoản; báo cáo tài chính; **reconciliation** (đối soát với ngân hàng/đối tác); audit.
- **Consistency**: **exactly-once, không mất/trùng**, immutable audit trail, **double-entry** (mỗi giao dịch ghi nợ + có cân bằng).
- **Compliance**: lưu trữ lâu dài, audit được, GDPR/PII, không sửa lịch sử.
- **Scale**: vừa (so với clickstream) nhưng **độ chính xác > tốc độ**.

## 2. Nguyên tắc thiết kế (khác analytics!)
- **Immutability**: ledger là **append-only**, KHÔNG update/delete. Sửa = ghi **bút toán đảo** (reversing entry). Giữ toàn bộ lịch sử.
- **Double-entry**: mỗi transaction = ≥2 entry (debit + credit) tổng = 0. Bất biến kế toán → tự kiểm tra.
- **Idempotency tuyệt đối** ⭐: mỗi giao dịch có **idempotency key** duy nhất; ghi lại cùng key → no-op, không trùng tiền ([[40-pipeline-patterns]]).
- **Exactly-once** end-to-end: at-least-once + dedup theo transaction_id + transaction DB ([[47-kafka-consumers]], [[b08-explain-senior]]).

## 3. Kiến trúc
```
Payment events ──► Kafka (idempotency key) ──► Ledger writer (transactional, dedup)
                                                   │ append-only ledger (Postgres/immutable store)
                                                   │  double-entry: debit + credit
                                                   ▼
                            CDC (Debezium) ──► lake (BRONZE immutable) ──► dbt ──► báo cáo tài chính
                                                   │
                                                   ▼
                            RECONCILIATION job: đối soát ledger nội bộ vs sao kê ngân hàng/đối tác
                                                   → khớp / lệch → alert + điều tra
```

## 4. Reconciliation ⭐ (trái tim fintech DE)
Đối soát 2 nguồn độc lập phải khớp:
```sql
-- tìm giao dịch lệch giữa ledger nội bộ và sao kê ngân hàng
select coalesce(l.txn_id, b.txn_id) as txn_id, l.amount as ledger_amt, b.amount as bank_amt
from ledger l
full outer join bank_statement b on l.txn_id = b.txn_id
where l.txn_id is null            -- có ở bank, thiếu ở ledger
   or b.txn_id is null            -- có ở ledger, thiếu ở bank
   or l.amount <> b.amount;       -- số tiền lệch
```
FULL OUTER JOIN ([[02-sql-joins]]) tìm 3 loại lệch: missing bên A, missing bên B, amount khác. Lệch → alert + điều tra (không tự sửa tiền).

## 5. Tech choices & trade-off
- **Storage chính xác**: Postgres (ACID mạnh) cho ledger; lake immutable (Delta/Iceberg, không VACUUM phá lịch sử) cho audit/analytics.
- **Exactly-once > latency**: chấp nhận chậm hơn để chắc chắn đúng. Transaction, 2PC nếu cần.
- **Audit/time-travel**: Delta time travel + append-only → tái dựng trạng thái bất kỳ thời điểm ([[34-delta-lake]]).
- **PII/compliance**: mã hoá, masking, retention dài, right-to-be-forgotten khó (cân với yêu cầu lưu trữ tài chính) ([[64-governance-pii]]).

## 6. DQ & observability
- **Invariant checks**: tổng debit = tổng credit (double-entry); số dư không âm (trừ khi cho phép); reconciliation lệch = 0.
- Alert ngay khi reconciliation lệch (tiền = nghiêm trọng).
- Audit log mọi truy cập.

## Câu hỏi đào sâu
- "Đảm bảo không trùng tiền?" → idempotency key + dedup + transactional write; at-least-once + idempotent sink.
- "Sửa giao dịch sai?" → KHÔNG update; ghi reversing entry, giữ audit.
- "Reconciliation lệch xử lý?" → alert, điều tra thủ công, không auto-fix tiền.

## ✅ "Tự mò"
🔭 Viết reconciliation query (full outer join) trên 2 bảng giao dịch giả lệch nhau; thêm invariant check tổng debit=credit.

➡️ Tiếp: [[c08-case-adtech]].
