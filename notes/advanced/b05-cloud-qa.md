# B05 — Cloud & Infra Q&A

> Câu hỏi phỏng vấn cloud/infra cho DE + đáp án. Chi tiết: [[53-docker]]→[[59-cost-finops]].

**Q: Vì sao S3 "không phải filesystem"?**
A: Object store = key→bytes (không có thư mục thật). "Rename thư mục" = copy+delete (đắt); list nhiều object chậm; thao tác theo prefix. Hệ quả: small files problem, partition layout quan trọng.

**Q: Partition layout cho S3/lake?**
A: Bố trí key theo cột hay lọc: `s3://lake/orders/dt=2024-01-01/...` → query `where dt=...` chỉ quét prefix đó (partition pruning). Chọn cột lực lượng vừa phải.

**Q: IAM least privilege?**
A: Cấp quyền **tối thiểu cần thiết**; service dùng **role** (assume) thay vì nhúng access key; không commit key vào git. Row/column-level + audit cho dữ liệu nhạy cảm.

**Q: Athena/BigQuery tính tiền theo gì? Tối ưu?**
A: Theo **bytes scanned**. Tối ưu: Parquet (columnar) + partition + chọn đúng cột (không `SELECT *`) → rẻ đi 10–100×. Đây là cost = performance.

**Q: Glue vs EMR?**
A: Glue = Spark **serverless** (không quản cụm) + crawler suy schema; hợp ETL vừa. EMR = cụm Spark/Hadoop managed; hợp job lớn/tuỳ biến cao, hỗ trợ spot.

**Q: Map dịch vụ đa cloud?**
A: Storage: S3/GCS/ADLS. Warehouse: Redshift/**BigQuery**/Synapse. ETL serverless: Glue/Dataflow/Data Factory. SQL-on-lake: Athena/BigQuery/Synapse serverless. Stream: Kinesis/PubSub/Event Hubs.

**Q: ELT trên cloud DW vì sao thắng?**
A: Tách compute/storage (co giãn độc lập), serverless/managed (ít vận hành), SQL mạnh + dbt → đổ thô vào rồi transform bằng SQL.

**Q: Docker — image vs container vs layer?**
A: Image = mẫu bất biến (Dockerfile, nhiều layer cache); container = instance đang chạy của image; volume cho data bền. DE cần để reproducible env + đóng gói job.

**Q: Thứ tự Dockerfile ảnh hưởng gì?**
A: Layer cache: copy `requirements.txt` + install **trước** copy code → đổi code không cài lại lib. Slim base + multi-stage để image gọn.

**Q: docker-compose vs Kubernetes?**
A: compose = local multi-service (dev/test, 1 máy). K8s = production (nhiều máy, tự scale/heal/rolling). Spark on K8s, Airflow KubernetesExecutor.

**Q: IaC & Terraform?**
A: Hạ tầng bằng code (declarative): reproducible, versioned, review. resource/provider/module; `plan` trước `apply`; **state** + remote backend+lock. Đổi qua code không tay (tránh drift).

**Q: CI/CD cho data?**
A: PR → lint + pytest + `dbt build` trên warehouse CI (không đụng prod). dev/staging/prod tách biệt; slim CI; deploy dbt/Airflow/Terraform tự động.

**Q: Đòn bẩy tối ưu chi phí lớn nhất?**
A: **Quét ít dữ liệu** (Parquet + partition + chọn cột). Rồi: spot/auto-terminate compute, storage tiering/lifecycle, incremental, materialization hợp lý, tag + budget alert (FinOps).

**Q: VPC/networking cơ bản cho DE?**
A: Đặt warehouse/DB trong **private subnet**, security group (firewall), VPC endpoint để truy cập S3 không qua internet. Kiểm soát truy cập + data residency.

## ✅ "Tự mò"
🔭 Thiết kế (trên giấy) stack AWS cho pipeline e-commerce: nguồn→S3→Glue/Athena→dbt→Redshift→dashboard, chú thích chi phí & bảo mật.

➡️ Tiếp: [[b06-modeling-qa]].
