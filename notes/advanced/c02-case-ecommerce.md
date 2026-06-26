# C02 — Case: E-commerce Analytics Platform

> Áp [[c01-system-design-framework]]. Mở rộng chính project đã build lên quy mô lớn.

## 1. Requirements
- **Functional**: dashboard doanh thu/đơn/khách (theo category/region/thời gian), cohort/retention, RFM, near-real-time inventory & top-selling.
- **Users**: BI (analyst), marketing (segment), ops (inventory).
- **Scale**: ~50M event/ngày (view/cart/order), 10M khách, catalog 1M sản phẩm. Giữ 3 năm lịch sử.
- **SLA**: dashboard analytics tươi trong 1h; inventory/top-selling tươi trong ~1 phút.
- **Consistency**: analytics gần đúng OK; **đơn hàng/doanh thu phải chính xác**.

## 2. Scale ước lượng
50M × 1KB ≈ 50GB/ngày ≈ 18TB/năm raw → lakehouse trên object store; warehouse cho lớp serving nóng. Peak event ~vài nghìn/s → Kafka đủ.

## 3. Kiến trúc
```
┌─ OLTP (orders, Postgres) ──CDC(Debezium)──┐
├─ Web/App events ──────────► Kafka ─────────┤
└─ Product catalog (API/file) ──────────────┘
        │                         │
        │ batch ingest            │ stream
        ▼                         ▼
  S3 BRONZE (raw Parquet)   Spark/Flink Streaming
        │  Spark/dbt              │ (inventory rollup, top-selling 1')
        ▼                         ▼
  SILVER (clean, SCD2 dim)   serving store (Redis/Postgres) ─► real-time widgets
        │  dbt marts
        ▼
  GOLD: fct_sales, dim_*, mart_revenue/cohort/RFM (warehouse)
        │
        ▼
  BI dashboard (Metabase/Looker)   + reverse-ETL segment → marketing tool
Orchestration: Airflow (batch daily + dbt build + DQ gates)
```

## 4. Tech choices & trade-off
- **CDC (Debezium) cho orders** thay vì batch dump → bắt cả DELETE, near-real-time, nhẹ OLTP ([[51-cdc-debezium]]).
- **Lakehouse (Delta/Iceberg) + warehouse**: lake rẻ cho lịch sử/ML, warehouse nhanh cho BI nóng ([[36-lakehouse-arch]]).
- **dbt** cho transform (medallion, tests, SCD2 snapshot) ([[21-warehouse-dbt]]).
- **Streaming nhánh riêng** chỉ cho thứ cần real-time (inventory, top-selling) — đừng stream hoá mọi thứ (over-engineer).
- **SCD2** cho dim_customer/product (phân tích theo thuộc tính lúc mua) ([[18-scd]]).

## 5. Scale & failure
- Partition fact theo **ngày** (pruning); compaction small files.
- CDC fail → replay từ Kafka offset; batch fail → backfill idempotent theo ngày.
- Bad records → quarantine, không chặn cả pipeline.
- Hot product (skew) trong top-selling → pre-aggregate.

## 6. DQ & observability
- dbt tests (unique order_id, FK fact→dim, accepted status), DQ gate trước GOLD.
- Freshness check (gold tươi < 1h), volume anomaly (đơn tụt bất thường), lineage cho impact.
- Cross-check: tổng doanh thu khớp giữa nguồn OLTP và warehouse (reconciliation).

## Câu hỏi đào sâu hay gặp
- "Inventory real-time thế nào?" → stream order events → giảm tồn theo product, ghi serving store; eventual consistency chấp nhận.
- "Doanh thu khớp với tài chính?" → reconciliation job đối soát OLTP vs warehouse, alert nếu lệch.
- "Khách đổi địa chỉ, báo cáo cũ có đổi?" → SCD2 giữ phiên bản.

## ✅ "Tự mò"
🔭 Bạn đã có sẵn ETL+dbt+star cho case này (Phase 1–3)! Thử thêm nhánh "top-selling 1 phút" bằng cách aggregate order_items theo cửa sổ (mô phỏng stream bằng batch nhỏ).

➡️ Tiếp: [[c03-case-fraud]].
