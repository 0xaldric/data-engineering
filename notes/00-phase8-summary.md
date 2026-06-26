# 🏁 Phase 8 — Tổng kết: Data Quality, Governance & Observability

> Notes-first. Trọng tâm: làm dữ liệu **đáng tin, quan sát được, tuân thủ** — phần phân biệt DE "chạy được" với DE production.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| T073 | Data quality dimensions & testing | [60](60-data-quality.md) |
| T074 | Data contracts | [61](61-data-contracts.md) |
| T075 | Data observability | [62](62-observability.md) |
| T076 | Lineage & catalog | [63](63-lineage-catalog.md) |
| T077 | Governance, PII, GDPR, security | [64](64-governance-pii.md) |

## 📑 Cheat-Sheet
- **Data quality** — 6 chiều: completeness, uniqueness, validity, accuracy, consistency, timeliness. Công cụ: dbt tests / Great Expectations / Soda + anomaly detection. Xử lý bẩn: fail fast / quarantine / alert. **Shift-left**.
- **Data contracts** — schema+semantics+SLA+owner+versioning giữa producer/consumer; enforce bằng schema registry / CI / runtime validation / dbt contracts; chống breaking change âm thầm.
- **Observability** — 5 trụ: freshness, volume, schema, distribution, lineage. Khác monitoring hệ thống (job "success" vẫn có thể ra rác). SLA/SLO cho data; incident: detect→triage→resolve→postmortem (TTD/TTR).
- **Lineage & catalog** — lineage (table & column level) cho impact analysis/root-cause/audit (OpenLineage, dbt DAG); catalog (DataHub/OpenMetadata) cho discovery/metadata/glossary; quan trọng khi scale.
- **Governance/PII** — phân loại + minimization; mask/tokenize/hash/encrypt; RBAC/ABAC + row/column-level + least privilege + audit; **GDPR** (consent, right to access/erasure, residency, retention) — erasure khó cần lineage + table-format DELETE.

## ✅ Self-assessment Phase 8
- [ ] 6 chiều chất lượng + công cụ; cách xử lý dữ liệu bẩn.
- [ ] Data contract gồm gì & enforce thế nào.
- [ ] 5 trụ observability; khác monitoring hệ thống.
- [ ] Lineage (impact analysis) & catalog (discovery).
- [ ] PII/masking/RBAC/GDPR; vì sao right-to-be-forgotten khó.

## 🔭 Để "tự mò"
1. Great Expectations suite cho `data/raw/order_items.parquet` (discount 0–1, quantity>0, not null) → validate + xem data docs.
2. Viết data contract YAML cho `orders` + pydantic/GE khớp.
3. Script tính 5 metric observability (freshness/volume/schema/NULL%/range) trên `data/raw`.
4. `dbt docs serve` xem lineage; tạo view masked PII cho `dim_customer`.

## ➡️ Tiếp theo: Phase 9 — Capstone Projects
Ghép tất cả thành 3 dự án portfolio: batch analytics, streaming, lakehouse. (notes-first: hướng dẫn kiến trúc + checklist để tự build)
