# 🏁 Module A — Tổng kết: SQL Mastery & Analytics Patterns

> Track 2 nâng cao. SQL từ "biết dùng" → "thành thạo phỏng vấn & phân tích thực chiến".

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| A01 | Gaps & islands, sessionization | [a01](a01-sql-gaps-islands.md) |
| A02 | Pivot, hierarchical, dedup | [a02](a02-sql-pivot-hierarchical.md) |
| A03 | Analytics: funnel, cohort, RFM | [a03](a03-analytics-patterns.md) |
| A04 | SQL interview problems set 1 | [a04](a04-sql-interview-1.md) |
| A05 | SQL interview problems set 2 | [a05](a05-sql-interview-2.md) |
| A06 | SQL performance & optimization | [a06](a06-sql-optimization.md) |
| A07 | SQL conceptual Q&A | [a07](a07-sql-qa.md) |

## 📑 Cheat-Sheet SQL nâng cao
- **Gaps & islands**: `value − ROW_NUMBER()` = hằng số trong đảo → GROUP BY neo đó.
- **Sessionization**: LAG đo gap → cờ session mới → `SUM(cờ) OVER` = session_id.
- **Dedup**: `ROW_NUMBER() PARTITION BY key ORDER BY updated_at DESC ... WHERE rn=1` (hoặc QUALIFY).
- **Pivot**: conditional aggregation (`SUM(CASE...)` / `FILTER`); pivot **động** cần code-gen.
- **Top-N/group**: ROW_NUMBER + PARTITION BY + lọc rn≤N.
- **nth-highest**: DENSE_RANK (không ROW_NUMBER vì ties).
- **Median**: `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)`.
- **Funnel/Cohort/RFM**: 3 pattern analytics chuẩn ([[a03-analytics-patterns]]).
- **Frame**: luôn ghi `ROWS` cho running/moving (tránh RANGE gộp ties).
- **Window filter**: bọc CTE/subquery hoặc QUALIFY (không trong WHERE).
- **Optimization**: sargable (cột trần), tránh `SELECT *`/`NOT IN`+NULL/function-on-column; EXPLAIN tìm nghẽn; pruning/pushdown cho OLAP.

## ✅ Self-assessment Module A
- [ ] Giải được 20 bài interview (A04+A05) không nhìn đáp án.
- [ ] Viết gaps&islands, sessionization, funnel, cohort, RFM từ đầu.
- [ ] Đọc EXPLAIN, nhận ra anti-pattern & rewrite.
- [ ] Trả lời trôi 20 câu Q&A (A07).

## 🔭 Để "tự mò"
Lấy dataset e-commerce (`data/raw`) chạy thật trên DuckDB: cohort retention triangle, RFM segment, Pareto 80/20, product affinity, sessionization từ order_ts. Tự đặt thêm biến thể.

## ➡️ Tiếp theo: Module B — DE Interview Prep (conceptual)
Q&A theo chủ đề (SQL/modeling, Spark, streaming/Kafka, dbt, orchestration, cloud), behavioral STAR, "explain like senior". (Loop sẽ sinh Batch #12.)
