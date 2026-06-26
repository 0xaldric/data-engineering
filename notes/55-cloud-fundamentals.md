# 55 — Cloud Fundamentals + Object Storage + IAM

> Hầu hết DE production chạy trên cloud. Ba nền tảng cần nắm: mô hình cloud, **object storage** (trái tim của data lake), **IAM** (bảo mật).

## Mô hình cloud
- **IaaS** (EC2, máy ảo) — bạn quản OS trở lên. **PaaS** (RDS, BigQuery) — nhà cung cấp quản hạ tầng, bạn dùng dịch vụ. **SaaS** (Snowflake) — dùng sản phẩm hoàn chỉnh. DE hiện đại nghiêng về **PaaS/serverless** (ít vận hành).
- **Region** (vùng địa lý) chứa nhiều **Availability Zone (AZ)** (data center cách ly lỗi). Phân tán qua AZ để chịu lỗi; chọn region gần user/dữ liệu (latency, chi phí, tuân thủ dữ liệu).

## ⭐ Object Storage (S3 / GCS / Azure Blob)
Nền của data lake/lakehouse ([[36-lakehouse-arch]]):
- **Bucket** chứa **object** định danh bằng **key** (đường dẫn). Không phải filesystem thật — chỉ là key→bytes (nhưng prefix `/` mô phỏng thư mục).
- **Rẻ, gần như vô hạn, độ bền 11 số 9**; truy cập qua HTTP API.
- **Tách compute/storage**: nhiều engine (Spark/Athena/DuckDB) đọc cùng dữ liệu; bật/tắt compute độc lập.
- **Storage class**: Standard (nóng) → Infrequent Access → **Glacier** (lạnh, rẻ, lấy chậm). **Lifecycle policy** tự chuyển/expire để tiết kiệm.
- **Partition layout** ⭐: bố trí key theo cột hay lọc → cắt dữ liệu quét:
  ```
  s3://lake/orders/dt=2024-01-01/region=VN/part-0.parquet
  ```
  Engine đọc `where dt='2024-01-01'` chỉ quét prefix đó (partition pruning — [[31-partitioning-shuffle]], [[09-file-formats]]).

## ⭐ IAM (Identity & Access Management)
Ai được làm gì với tài nguyên nào:
- **User** (người), **Role** (danh tính tạm để service/máy/dịch vụ assume), **Group**.
- **Policy** (JSON): cấp/ từ chối quyền (`s3:GetObject` trên `bucket/path/*`).
- **Least privilege** ⭐: chỉ cấp quyền **tối thiểu cần thiết** — đừng `AdministratorAccess` cho job ETL.
- Dịch vụ dùng **role** (vd Glue job assume role đọc S3) thay vì nhúng access key → an toàn, xoay vòng tự động.
- Không bao giờ commit access key vào code/git ([[13-logging-config]]); dùng role/secret manager.

## Networking cơ bản (đủ dùng)
- **VPC** (mạng riêng ảo), subnet public/private; **security group** (firewall); **VPC endpoint** để truy cập S3 không qua internet. DE cần biết để đặt warehouse/DB trong private subnet, kiểm soát truy cập.

## ⚠️ Cạm bẫy
- Coi S3 như filesystem (rename "thư mục" là copy+delete tốn kém; list nhiều object chậm — small files [[33-spark-tuning]]).
- Bucket public nhầm → rò rỉ dữ liệu (cấu hình block public access).
- Quyền IAM quá rộng → rủi ro bảo mật.
- Để dữ liệu sai region → latency + phí egress xuyên region.

## ✅ Tự kiểm tra & "tự mò"
- [ ] IaaS/PaaS/SaaS; region vs AZ.
- [ ] Object storage: bucket/key, storage class, lifecycle, partition layout.
- [ ] IAM user/role/policy; least privilege; vì sao service dùng role.
- [ ] Vì sao S3 không phải filesystem (rename/list).
- 🔭 *Tự mò:* dùng **LocalStack** (S3 giả local, không tốn tiền) hoặc tài khoản AWS free tier: tạo bucket, upload parquet theo layout `dt=.../`, query bằng DuckDB `read_parquet('s3://...')`.

➡️ Tiếp: [[56-aws-data-stack]].
