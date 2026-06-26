# 63 — Data Lineage & Catalog

> Khi có hàng trăm bảng/pipeline: "Bảng này từ đâu ra? Đổi cột này hỏng cái gì? Dữ liệu nào đáng tin?" → cần **lineage** và **catalog**.

## Data Lineage
**Lineage** = bản đồ **dòng chảy dữ liệu**: nguồn → bảng trung gian → bảng đích → dashboard.
```
postgres.orders ─► stg_orders ─► int_sales ─► fct_sales ─► mart_revenue ─► dashboard "Revenue"
```
- **Table-level**: bảng nào sinh ra bảng nào (đã thấy ở dbt DAG — [[28-dbt-docs-lineage]]).
- **Column-level** ⭐: cột đích đến từ cột nguồn nào (chi tiết hơn, cho impact analysis chính xác).

Dùng để:
- **Impact analysis**: đổi/xoá cột nguồn → biết **chính xác** dashboard/model nào ảnh hưởng (trước khi đổi).
- **Root cause**: dashboard sai → lần ngược upstream tìm bảng/nguồn lỗi.
- **Triage incident** ([[62-observability]]): nguồn lỗi → ai bị ảnh hưởng.
- **Audit/compliance**: dữ liệu PII chảy tới đâu ([[64-governance-pii]]).

## Công cụ lineage
- **OpenLineage** — chuẩn mở thu thập lineage từ Airflow/Spark/dbt; **Marquez** là backend tham chiếu.
- dbt sinh lineage tự động từ `ref()` (manifest — [[28-dbt-docs-lineage]]).
- Tích hợp trong catalog (DataHub/OpenMetadata) — gom lineage từ nhiều công cụ.

## Data Catalog
"Danh bạ" mọi dataset trong tổ chức — giúp **khám phá & tin tưởng** dữ liệu:
- **Discovery/search**: tìm bảng theo tên/tag/chủ đề ("doanh thu ở bảng nào?").
- **Metadata**: schema, mô tả, owner, tần suất cập nhật, độ tin cậy.
- **Lineage** tích hợp.
- **Glossary**: định nghĩa thuật ngữ business ("active customer" nghĩa là gì) — thống nhất ngôn ngữ.
- **Usage/popularity**: bảng nào được dùng nhiều (đáng tin hơn), bảng nào "chết".

## Công cụ catalog
- **DataHub** (LinkedIn), **OpenMetadata** — open-source, lineage + discovery + governance.
- **Amundsen** (Lyft) — discovery.
- AWS Glue Catalog ([[56-aws-data-stack]]), Unity Catalog (Databricks) — thiên kỹ thuật/metadata.
- dbt docs — catalog nhẹ cho dbt project ([[28-dbt-docs-lineage]]).

## Vì sao quan trọng (khi scale)
Tổ chức nhỏ: hỏi nhau là biết. Tổ chức lớn (nghìn bảng, nhiều team): không có catalog/lineage → "data discovery" bằng cách hỏi vòng quanh, dữ liệu trùng lặp, không ai dám tin bảng nào, đổi gì cũng sợ vỡ. Catalog + lineage = **khả năng quản trị & tin tưởng** dữ liệu ở quy mô.

## ⚠️ Cạm bẫy
- Catalog không cập nhật/không owner → metadata cũ, không ai tin → bỏ.
- Chỉ table-level lineage khi cần column-level (impact analysis thiếu chính xác).
- Mua công cụ catalog nhưng không có văn hoá tài liệu hoá → vỏ rỗng.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Lineage table-level vs column-level; 3 use case (impact/root-cause/audit).
- [ ] OpenLineage/Marquez; dbt sinh lineage thế nào.
- [ ] Catalog gồm gì (discovery/metadata/glossary/usage).
- [ ] Vì sao cần khi scale.
- 🔭 *Tự mò:* `dbt docs generate && dbt docs serve` (project Phase 3) → click xem **lineage graph** + data dictionary. Đó là catalog+lineage mini cho project của bạn.

➡️ Tiếp: [[64-governance-pii]].
