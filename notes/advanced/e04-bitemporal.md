# E04 — Bitemporal Modeling

> Nâng cao SCD: theo dõi **hai trục thời gian** cùng lúc. Cần cho audit/tài chính/bảo hiểm — "sự thật là gì" vs "ta biết khi nào".

## Hai trục thời gian
- **Valid time** (effective/business time): sự thật **đúng trong khoảng nào ngoài đời thực**. VD: lương của An là 1000 từ 2024-01-01 đến 2024-06-30.
- **Transaction time** (system/knowledge time): hệ thống **biết/ghi nhận** sự thật đó **khi nào**. VD: ta nhập mức lương này vào hệ thống ngày 2024-02-15 (trễ).

SCD2 thường chỉ theo dõi **một** trục (valid time qua effective_from/to — [[18-scd]]). **Bitemporal** theo dõi **cả hai**.

## Vì sao cần bitemporal?
Trả lời 2 loại câu hỏi cùng lúc:
- "Lương An **thực sự** là bao nhiêu vào 2024-03 (as-of valid time)?"
- "Vào 2024-02-10, **hệ thống nghĩ** lương An tháng 3 là bao nhiêu (as-of transaction time)?"

Tình huống: **backdated correction** (sửa hồi tố). Ngày 2024-05 ta phát hiện lương An từ tháng 1 sai, sửa lại. Câu hỏi audit: "báo cáo chạy tháng 3 (lúc đó hệ thống chưa biết) ra số gì?" → cần transaction time để **tái dựng cái hệ thống đã biết tại thời điểm đó**.

## Cấu trúc bảng bitemporal
```
salary(emp_id, amount,
       valid_from, valid_to,        ← khoảng đúng ngoài đời
       txn_from,  txn_to)           ← khoảng hệ thống biết (txn_to=NULL = bản hiện hành)
```
Ví dụ sau khi sửa hồi tố:
```
emp  amount  valid_from  valid_to   txn_from    txn_to       ghi chú
An   1000    2024-01-01  9999       2024-02-15  2024-05-10   bản CŨ (đã bị thay)
An   1200    2024-01-01  9999       2024-05-10  9999         bản ĐÚNG (sau sửa hồi tố)
```
→ Truy vấn "as-of valid=2024-03 AND as-of known=2024-04" trả 1000 (cái hệ thống biết lúc đó); "as-of known=now" trả 1200 (đã sửa).

## Truy vấn bi-temporal (as-of cả 2 trục)
```sql
select amount from salary
where emp_id = 'An'
  and date '2024-03-01' >= valid_from and date '2024-03-01' < valid_to   -- valid time
  and date '2024-04-01' >= txn_from   and date '2024-04-01' < txn_to;    -- transaction time
```

## So với SCD2
| | SCD2 | Bitemporal |
|--|------|------------|
| Trục thời gian | 1 (valid) | **2** (valid + transaction) |
| Backdated correction | mất "cái đã biết trước đó" | giữ được → tái dựng báo cáo cũ |
| Độ phức tạp | vừa | cao |
| Khi nào | đa số analytics | audit/regulated (tài chính, bảo hiểm, pháp lý) |

## ⚠️ Cạm bẫy
- Dùng bitemporal khi không cần (đa số chỉ cần SCD2) → phức tạp thừa.
- Nhầm valid time với transaction time.
- Quên đóng `txn_to` khi sửa hồi tố → 2 bản hiện hành chồng.
- Truy vấn thiếu một trong hai trục → kết quả sai.

## ✅ "Tự mò"
🔭 Tạo bảng salary bitemporal, mô phỏng: nhập lương (txn_from=hôm nhập), rồi sửa hồi tố sau 3 tháng; viết query trả "số hệ thống biết tại tháng 2" vs "số đúng hiện tại".

➡️ Tiếp: [[e05-semantic-layer]].
