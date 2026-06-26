# 56 — AWS Data Stack (+ map GCP/Azure) ⭐

> Các dịch vụ AWS hay dùng nhất cho DE, và ánh xạ sang GCP/Azure (hiểu một cloud → suy ra cloud khác).

## Bản đồ dịch vụ theo vai trò
| Vai trò | **AWS** | **GCP** | **Azure** |
|---------|---------|---------|-----------|
| Object storage (lake) | **S3** | GCS | ADLS / Blob |
| Catalog (metadata) | **Glue Data Catalog** | Dataplex/BQ | Purview / Unity |
| ETL serverless | **Glue (Spark)** | Dataflow | Data Factory |
| SQL on lake (serverless) | **Athena** | BigQuery (ext) | Synapse serverless |
| Managed Spark | **EMR** | Dataproc | HDInsight/Synapse |
| Streaming | **Kinesis** | Pub/Sub + Dataflow | Event Hubs |
| Warehouse | **Redshift** | **BigQuery** | Synapse |
| Function/event ETL | **Lambda** | Cloud Functions | Functions |
| Orchestration (managed Airflow) | **MWAA** | Cloud Composer | Data Factory/MWAA |

## Các dịch vụ AWS cốt lõi
- **S3** — data lake (mọi thứ đổ về đây), rẻ/bền ([[55-cloud-fundamentals]]).
- **Glue Data Catalog** — kho **metadata/schema** (bảng trỏ tới dữ liệu S3); các engine (Athena/EMR/Redshift Spectrum) dùng chung catalog này. Cũng là catalog cho table format ([[35-table-formats]]).
- **Glue (ETL)** — chạy Spark **serverless** (không quản cụm) + **crawler** tự suy schema từ S3.
- **Athena** ⭐ — chạy **SQL trực tiếp trên file S3** (Presto/Trino), serverless, **tính tiền theo dữ liệu quét** → Parquet + partition để rẻ. Tuyệt cho ad-hoc query lake.
- **EMR** — cụm **Spark/Hadoop managed** cho job lớn; chạy trên EC2/EKS, hỗ trợ spot instance (rẻ).
- **Kinesis** — streaming (Data Streams ~ Kafka, Firehose = nạp thẳng vào S3/Redshift). Đối thủ Kafka managed (MSK = Kafka managed của AWS).
- **Redshift** — data warehouse (MPP, columnar); Redshift Spectrum query S3.
- **Lambda** — chạy code theo **sự kiện** (file mới vào S3 → trigger Lambda transform/đăng ký). ETL nhẹ, glue giữa dịch vụ.

## Kiến trúc tham chiếu AWS (batch lakehouse)
```
Nguồn ─► (Lambda/Glue ingest) ─► S3 bronze (raw)
       ─► Glue/EMR Spark transform ─► S3 silver/gold (Parquet/Iceberg) + Glue Catalog
       ─► Athena (ad-hoc) / Redshift (BI) / QuickSight (dashboard)
       ─► Airflow(MWAA) orchestrate; dbt transform; CDC qua DMS/Debezium→MSK
```

## Chọn dịch vụ thế nào
- Ad-hoc SQL trên lake, ít quản → **Athena**.
- ETL Spark không muốn quản cụm → **Glue**; job lớn/tuỳ biến cao → **EMR**.
- BI warehouse hiệu năng cao, nhiều user → **Redshift** (hoặc Snowflake/BigQuery).
- ETL theo sự kiện nhẹ → **Lambda**.
- Streaming → **Kinesis/MSK**.
→ Xu hướng **serverless** (Athena/Glue/Lambda/BigQuery): trả theo dùng, ít vận hành.

## ⚠️ Cạm bẫy
- Athena/BigQuery tính theo **bytes scanned** → CSV/không partition = hoá đơn sốc; dùng Parquet + partition + chọn cột ([[59-cost-finops]]).
- EMR cluster để chạy hoài (quên tắt) → đốt tiền; dùng auto-terminate/spot.
- Khoá chặt vào dịch vụ độc quyền (lock-in) → cân nhắc table format mở (Iceberg) để dễ chuyển.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Map vai trò → dịch vụ AWS; tương đương GCP/Azure.
- [ ] Glue Catalog/Athena/EMR/Kinesis/Redshift/Lambda mỗi cái cho gì.
- [ ] Athena tính tiền theo gì → tối ưu thế nào.
- [ ] Vẽ kiến trúc batch lakehouse trên AWS.
- 🔭 *Tự mò:* AWS free tier hoặc LocalStack: S3 + Glue crawler + Athena query parquet; hoặc trên giấy thiết kế stack AWS cho pipeline e-commerce đã build.

➡️ Tiếp: [[57-terraform]].
