# 🏁 Extra H — Tổng kết

> Case mới + engine deep-dive + mock interview.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| H01 | SQL set 5 (window edge cases) | [h01](h01-sql-interview-5.md) |
| H02 | Case marketplace two-sided | [h02](h02-case-marketplace.md) |
| H03 | Case SaaS metrics | [h03](h03-case-saas-metrics.md) |
| H04 | Case social graph | [h04](h04-case-social-graph.md) |
| H05 | Trino/Presto & federation | [h05](h05-trino-federation.md) |
| H06 | Real-time OLAP (ClickHouse/Druid) | [h06](h06-realtime-olap.md) |
| H07 | Mock interview đầy đủ | [h07](h07-mock-interview.md) |

## Điểm cốt lõi
- **SQL window edge cases**: LAST_VALUE cần frame mở; ROWS vs RANGE với ties; carry-forward (LOCF) bằng count-group trick; tie-break deterministic cho pagination.
- **Marketplace**: two-sided → GMV/take-rate + supply-demand balance + 2 cohort.
- **SaaS**: MRR movement (new/expansion/contraction/churn); logo vs **revenue churn**; SCD2 subscription.
- **Social graph**: fan-out write/read/**hybrid** feed; supernode skew; edge table vs graph DB.
- **Trino**: MPP không storage, **federation** (join across nguồn), interactive — bổ sung Spark (ETL).
- **Real-time OLAP**: ClickHouse/Druid cho **sub-giây + user-facing + real-time ingest** — song song warehouse.
- **Mock interview**: clarify → tư duy thành tiếng → trade-off → depth signals (grain/idempotency/shuffle/DQ).

## ✅ Self-assessment tổng (sẵn sàng phỏng vấn?)
- [ ] SQL: giải trôi 50 bài (A04/A05/G01/G02/H01) + window edge cases.
- [ ] System design: đi framework cho case lạ, nêu trade-off + failure + DQ.
- [ ] Conceptual: giải thích sâu 10+ khái niệm có trade-off ([[b08-explain-senior]]).
- [ ] Behavioral: 5 câu chuyện STAR có số.
- [ ] Mock interview H07 tự chấm đạt.

## ➡️ Tiếp: Extra I
Case mới (logistics/supply-chain, video streaming, banking core...), SQL set 6, deep-dive (Spark tuning thực chiến, data quality framework chi tiết). Loop tự sinh.
