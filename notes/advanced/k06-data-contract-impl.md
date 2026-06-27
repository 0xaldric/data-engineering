# K06 — Deep-dive: Data Contract Implementation

> Từ khái niệm ([[61-data-contracts]]) → triển khai thật: định nghĩa, enforce, versioning trong pipeline.

## Định nghĩa contract (machine-readable)
```yaml
# contract cho dataset "orders" (YAML, versioned trong git)
dataset: orders
version: 1.2.0
owner: order-team
description: "Đơn hàng đã đặt"
schema:
  - name: order_id
    type: bigint
    nullable: false
    unique: true
  - name: amount
    type: decimal(10,2)
    nullable: false
    constraints: [">= 0"]
  - name: status
    type: string
    enum: [completed, shipped, cancelled, returned]
  - name: created_at
    type: timestamp
    nullable: false
sla:
  freshness: 1h
  availability: 99.9%
  completeness: ">= 99%"
semantics:
  amount: "tổng tiền đơn, đơn vị VND, đã gồm thuế"
classification:
  customer_email: PII
```
Gồm: schema (cột/kiểu/nullable/constraint), **SLA** (freshness/availability/completeness), **semantics** (ý nghĩa/đơn vị — tránh hiểu nhầm), classification (PII), owner, version.

## ⭐ Enforcement (làm sao "ép" — quan trọng nhất)
Contract chỉ là giấy nếu không enforce. 4 điểm chặn:
1. **CI schema diff** (producer): PR đổi schema producer → so với contract → **chặn merge** nếu breaking (xoá/đổi cột/kiểu) không bump major version.
2. **Runtime validation** (ingest): data vào kiểm khớp contract (pydantic/GE/Soda — [[i06-dq-framework]]); vi phạm → quarantine + alert.
3. **Schema Registry** (streaming): Avro/Protobuf compatibility check từ chối schema phá vỡ ([[48-kafka-ecosystem]]).
4. **dbt contract** (transform): `contract: {enforced: true}` trên model → build fail nếu schema lệch ([[d02-dbt-advanced]]).

## Versioning & breaking change workflow ⭐
SemVer cho contract:
- **Patch** (1.2.0→1.2.1): sửa docs/semantics, không đổi schema.
- **Minor** (1.2→1.3): thêm cột **optional** (backward compatible) → consumer cũ không vỡ.
- **Major** (1.x→2.0): **breaking** (xoá/đổi cột/kiểu) → quy trình:
```
1. Thông báo consumer + deprecation timeline
2. Chạy v1 và v2 SONG SONG (dual-publish) một thời gian
3. Consumer migrate sang v2
4. Sau hết hạn deprecate → tắt v1
```
Giống schema evolution Avro ([[10-json-avro]]) + migration ([[j06-lakehouse-migration]]).

## Producer vs Consumer responsibility
- **Producer**: cam kết giữ contract; đổi breaking phải bump major + thông báo + dual-publish; báo SLA.
- **Consumer**: dựa vào **interface công khai** (contract), không vào internal/undocumented; đăng ký để được thông báo thay đổi.
- Contract = "API của data" giữa team (như REST API contract).

## Tích hợp tổ chức
- Contract trong **git** (versioned, review qua PR).
- Gắn vào **catalog** (discoverable — [[63-lineage-catalog]]).
- Nền của **data mesh / data product** ([[f05-data-mesh]]): mỗi data product có contract.
- **Shift-left**: bắt vi phạm ở nguồn/CI, không để xuống dashboard.

## ⚠️ Cạm bẫy
- Contract chỉ là tài liệu (không enforce) → vẫn bị phá.
- Breaking change không bump version/thông báo → consumer vỡ bất ngờ.
- Không dual-publish khi major → downtime consumer.
- Contract quá cứng → cản tiến hoá; cần chính sách thay đổi.
- Không owner → contract mồ côi.

## ✅ "Tự mò"
🔭 Viết contract YAML cho `orders` (như trên) + pydantic model + GE suite khớp; thêm 1 GitHub Action so schema parquet thực tế vs contract, fail nếu thiếu cột bắt buộc.

➡️ Tiếp: [[k07-observability-tooling]].
