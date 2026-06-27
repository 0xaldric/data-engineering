# 🏁 Extra K — Tổng kết

> Case mới (insurance/real-estate/agritech) + deep-dive AI/contract/observability.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| K01 | SQL set 8 (mixed) | [k01](k01-sql-interview-8.md) |
| K02 | Case insurance | [k02](k02-case-insurance.md) |
| K03 | Case real estate/PropTech | [k03](k03-case-realestate.md) |
| K04 | Case agritech | [k04](k04-case-agritech.md) |
| K05 | Vector DB & RAG sâu | [k05](k05-vector-rag-deep.md) |
| K06 | Data contract implementation | [k06](k06-data-contract-impl.md) |
| K07 | Data observability tooling | [k07](k07-observability-tooling.md) |

## Điểm cốt lõi
- **SQL set 8**: max concurrent (event +1/−1 running sum), **as-of join** (nearest theo thời gian), hierarchical rollup (recursive node-ancestor), divide-by-zero/NULL handling.
- **Insurance**: bitemporal (reserve hồi tố) + accumulating snapshot claims (long-tail, reopen) + loss ratio.
- **Real estate**: MDM address + SCD2 price history + AVM as-of comparables (không leakage).
- **Agritech**: đa dạng data (sensor time-series + imagery NDVI + weather) + edge buffer + yield ML.
- **Vector/RAG**: ANN index (HNSW/IVF) + chunking + **hybrid search** (vector+BM25+rerank) + RAG eval + incremental re-embed.
- **Data contract impl**: YAML schema+SLA+semantics; enforce 4 điểm (CI/runtime/registry/dbt); SemVer + dual-publish breaking change.
- **Observability tooling**: 5 trụ đo cụ thể; rule vs anomaly; Elementary (dbt-native)/Soda/Monte Carlo; SLO + incident.

## ✅ Self-assessment Extra K
- [ ] SQL set 8 (max concurrent, as-of join).
- [ ] 3 case mới qua framework (bitemporal/MDM/multi-modal).
- [ ] Vector DB internals + hybrid search + RAG eval.
- [ ] Triển khai contract (enforce 4 điểm + versioning).
- [ ] Triển khai observability (5 trụ + tooling + SLO).

## ➡️ Tiếp: Extra L
Case HR/people analytics, manufacturing, retail omnichannel; SQL set 9; deep-dive: data catalog impl, FinOps sâu, schema evolution patterns. Loop tự sinh.
