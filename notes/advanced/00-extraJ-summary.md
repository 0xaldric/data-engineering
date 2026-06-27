# 🏁 Extra J — Tổng kết

> Case mới (telecom/energy/govtech) + deep-dive (EOS, migration, dbt scale).

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| J01 | SQL set 7 (mixed hard) | [j01](j01-sql-interview-7.md) |
| J02 | Case telecom/CDR | [j02](j02-case-telecom.md) |
| J03 | Case energy/smart meter | [j03](j03-case-energy.md) |
| J04 | Case govtech | [j04](j04-case-govtech.md) |
| J05 | Streaming exactly-once thực chiến | [j05](j05-streaming-eos.md) |
| J06 | Lakehouse migration | [j06](j06-lakehouse-migration.md) |
| J07 | dbt at scale | [j07](j07-dbt-at-scale.md) |

## Điểm cốt lõi
- **Telecom**: mediation (chuẩn hoá+dedup CDR) + rating (SCD tariff) + charging real-time; billing chính xác.
- **Energy**: VEE (validate/estimate/edit đọc thiếu) + interval data + rollup + anomaly trộm điện.
- **Govtech**: Data Vault tích hợp đa nguồn + MDM + de-identify/k-anonymity + open data privacy.
- **Exactly-once**: = at-least-once + **idempotent sink**; xử lý 3 điểm (producer/offset/sink); Kafka EOS chỉ trọn cho Kafka→Kafka, sink ngoài cần upsert.
- **Migration**: dual-run + **validate** (row count/checksum/reconciliation) + blue-green cutover + rollback; không big-bang.
- **dbt at scale**: domain+layer structure, contracts/exposures, slim CI + incremental, semantic layer, tránh spaghetti.

## ✅ Self-assessment Extra J
- [ ] Giải SQL set 7 (time-weighted avg, conditional islands).
- [ ] Thiết kế 3 case mới qua framework.
- [ ] Giải thích exactly-once end-to-end (3 điểm + idempotent sink).
- [ ] Lập kế hoạch migration an toàn (dual-run/validate/cutover).
- [ ] Tổ chức dbt project lớn không spaghetti.

## ➡️ Tiếp: Extra K
Case insurance/real-estate/agritech; SQL set 8; deep-dive: vector DB/RAG sâu, data contract implementation, observability tooling. Loop tự sinh.
