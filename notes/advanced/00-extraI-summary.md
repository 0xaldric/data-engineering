# 🏁 Extra I — Tổng kết

> Case mới + deep-dive thực chiến (tuning, DQ, backfill).

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| I01 | SQL set 6 (tricky/edge) | [i01](i01-sql-interview-6.md) |
| I02 | Case logistics/supply-chain | [i02](i02-case-logistics.md) |
| I03 | Case video streaming | [i03](i03-case-video-streaming.md) |
| I04 | Case banking core/payments | [i04](i04-case-banking.md) |
| I05 | Spark tuning scenarios | [i05](i05-spark-tuning-scenarios.md) |
| I06 | DQ framework chi tiết | [i06](i06-dq-framework.md) |
| I07 | Backfill & reprocessing | [i07](i07-backfill-reprocessing.md) |

## Điểm cốt lõi
- **SQL set 6**: merge intervals, NOT IN+NULL → NOT EXISTS, correlated→window, EXISTS vs IN vs JOIN.
- **Logistics**: shipment accumulating snapshot + lag; inventory semi-additive (snapshot, không SUM theo thời gian).
- **Video streaming**: QoE (rebuffering/startup) real-time; watch-time từ heartbeat (sessionize+dedup); audience retention.
- **Banking**: double-entry + idempotency key + exactly-once + reconciliation nhiều tầng + bitemporal reporting + AML.
- **Spark tuning**: triệu chứng Spark UI → nguyên nhân → fix (OOM/skew/small-files/shuffle/spill/UDF); quy trình ĐO→tìm nghẽn→fix→ĐO LẠI.
- **DQ framework**: check ở mỗi tầng medallion; GE/Soda/dbt phối hợp; DQ score; quarantine/circuit-breaker; shift-left.
- **Backfill**: idempotency là tiên quyết; partition overwrite / blue-green / replay (Kappa); kiểm soát tải (pools); verify sau.

## Mẫu hình lặp (nhận ra trong mọi case)
- Tiền/chính xác (banking/fintech) → idempotency + double-entry + reconciliation.
- Lifecycle (logistics/order) → accumulating snapshot + lag + funnel.
- Volume khổng lồ (video/clickstream) → partition + sampling + OLAP + dedup.
- Vận hành → tuning có quy trình, DQ có hệ thống, backfill an toàn.

## ✅ Self-assessment Extra I
- [ ] Giải SQL set 6; nhận anti-pattern & rewrite.
- [ ] Chẩn đoán 6 scenario Spark từ triệu chứng.
- [ ] Thiết kế DQ framework cho 1 pipeline (mỗi tầng + công cụ).
- [ ] Lên kế hoạch backfill an toàn (idempotent + blue-green + kiểm soát tải).

## ➡️ Tiếp: Extra J
Case telecom/energy/govtech; SQL set 7; deep-dive: streaming exactly-once thực chiến, lakehouse migration, data modeling case studies. Loop tự sinh.
