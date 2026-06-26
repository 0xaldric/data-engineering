# F03 — Modern Data Stack & cách chọn tool

> "Modern Data Stack" (MDS) = bộ công cụ cloud, modular, kết nối quanh warehouse/lakehouse. Hiểu bản đồ để chọn đúng & không bị ngợp.

## Bản đồ MDS (theo lớp)
```
[ NGUỒN ] OLTP, SaaS, file, event
   │
[ INGESTION ]  Fivetran/Airbyte (ELT connector), Kafka/Kinesis (stream), CDC (Debezium)
   │
[ STORAGE/COMPUTE ]  Warehouse (Snowflake/BigQuery/Redshift) hoặc Lakehouse (S3+Iceberg/Delta)
   │
[ TRANSFORM ]  dbt (SQL, ELT chữ T) / Spark
   │
[ ORCHESTRATION ]  Airflow / Dagster / Prefect
   │
[ SERVE ]  BI (Looker/Tableau/Metabase/Superset), reverse-ETL (Hightouch/Census), ML/feature store
   │
[ CROSS-CUTTING ]  Catalog/lineage (DataHub/OpenMetadata), Observability (Monte Carlo/Soda/Elementary),
                   Semantic layer (dbt/Cube), Governance
```

## Đặc trưng MDS
- **Cloud-native, serverless/managed** → ít vận hành.
- **Modular** (best-of-breed): chọn từng lớp công cụ tốt nhất, nối qua warehouse.
- **ELT-centric**: nạp thô → transform bằng SQL (dbt) trong warehouse.
- **SQL-first**: hạ rào cản (analyst làm được nhiều).

## Build vs Buy ⭐
| | Buy (managed/SaaS) | Build (tự host/code) |
|--|--------------------|----------------------|
| Tốc độ | nhanh có | chậm |
| Chi phí | phí license (tăng theo scale) | chi phí kỹ sư + vận hành |
| Kiểm soát/tuỳ biến | hạn chế | cao |
| Khi nào | team nhỏ, time-to-market, vấn đề phổ biến | scale lớn (license đắt hơn build), nhu cầu đặc thù, lock-in lo ngại |
VD: Fivetran (buy) vs Airbyte self-host (build) cho ingestion; managed Airflow (MWAA) vs tự host.

## Tiêu chí chọn tool
1. **Phù hợp vấn đề & scale** (đừng Kafka+Flink cho 1GB/ngày).
2. **Team skill** (SQL-heavy → dbt; Python-heavy → Dagster/Prefect).
3. **Tích hợp** với phần còn lại của stack.
4. **Chi phí** tổng (license + compute + vận hành) ở scale dự kiến.
5. **Lock-in** (chuẩn mở như Iceberg/dbt giảm lock-in).
6. **Cộng đồng/độ chín** (tránh tool quá mới cho production critical).

## MDS vs Lakehouse vs all-in-one
- **MDS modular**: linh hoạt nhưng nhiều mảnh phải tích hợp/quản lý.
- **Lakehouse (Databricks)**: một nền tảng (storage+compute+ML) — ít mảnh hơn.
- **All-in-one** (Snowflake mở rộng): đang hội tụ — warehouse + apps + ML.
→ Xu hướng: hội tụ + lakehouse mở (Iceberg) làm nền chung.

## Xu hướng hiện tại (bối cảnh)
- Lakehouse + table format mở (Iceberg) thành chuẩn.
- Semantic layer & metric standardization.
- Data observability/contracts trưởng thành.
- **AI/LLM**: text-to-SQL, copilot cho pipeline, tự sinh test/docs — DE dịch lên việc thiết kế/giám sát.
- "Shift-left" data quality (contract ở nguồn).

## ⚠️ Cạm bẫy
- **Tool sprawl**: mua quá nhiều công cụ, tích hợp rối, chi phí phình. Bắt đầu tối thiểu (warehouse + dbt + 1 ingestion + 1 BI).
- Chọn tool "hot" thay vì hợp vấn đề.
- Over-engineer cho scale chưa có.
- Lock-in nặng không lối thoát.

## ✅ "Tự mò"
🔭 Vẽ MDS cho một startup giả định (10 nguồn, team 2 DE, ngân sách hạn chế): chọn từng lớp + giải thích build vs buy. So với enterprise (100 nguồn, regulated).

➡️ Tiếp: [[f04-cost-cases]].
