# 57 — Infrastructure as Code: Terraform ⭐

> Tạo hạ tầng cloud bằng **code** (khai báo), không click tay trên console → tái lập, version, review, tự động.

## Vì sao IaC?
Click tay trên console: không tái lập được, không biết ai đổi gì, dễ "drift" giữa môi trường, không rollback. **IaC** = mô tả hạ tầng trong file → `apply` để tạo/sửa:
- **Reproducible**: dựng lại y hệt dev/staging/prod.
- **Version control**: hạ tầng trong git, review qua PR, lịch sử thay đổi.
- **Tự động**: chạy trong CI/CD.
- **Documentation sống**: file code = trạng thái hạ tầng mong muốn.

## Terraform — declarative, multi-cloud
Công cụ IaC phổ biến nhất; hỗ trợ AWS/GCP/Azure/... qua **provider**. Bạn khai báo **trạng thái mong muốn**, Terraform tính diff và áp dụng.
```hcl
provider "aws" { region = "ap-southeast-1" }

resource "aws_s3_bucket" "lake" {
  bucket = "my-de-lake"
}

resource "aws_glue_catalog_database" "analytics" {
  name = "analytics"
}

variable "env" { default = "dev" }
```
- **Resource**: một thứ hạ tầng (bucket, DB, role...).
- **Provider**: plugin cho một cloud/dịch vụ.
- **Variable/output**: tham số hoá & xuất giá trị.
- **Module**: gói tái dùng (vd module "data-lake" tạo bucket + catalog + IAM) → DRY.

## Workflow
```
terraform init      # tải provider, chuẩn bị
terraform plan      # XEM TRƯỚC sẽ tạo/sửa/xoá gì (an toàn)
terraform apply     # áp dụng thay đổi
terraform destroy   # xoá sạch (tránh đốt tiền khi học)
```
`plan` trước `apply` là thói quen sống còn — luôn xem diff trước khi đổi production.

## ⭐ State
Terraform lưu **state** (ánh xạ resource khai báo ↔ resource thật trên cloud) trong `terraform.tfstate`.
- State là **nguồn sự thật** để tính diff. Mất/hỏng state → Terraform "quên" những gì đã tạo.
- **Remote backend** (S3 + DynamoDB lock, Terraform Cloud): để team chia sẻ state + **locking** (tránh 2 người apply cùng lúc). Không commit state vào git (chứa secret + xung đột).

## Declarative vs imperative
Bạn mô tả "muốn có gì" (declarative), không phải "làm từng bước" (imperative). Terraform tự tính cần tạo/sửa/xoá gì để đạt trạng thái đó. Giống dbt mô tả model đích, không phải thủ tục.

## Liên hệ DE
- Tạo S3 bucket, Glue catalog, Redshift, IAM role, MSK (Kafka), MWAA (Airflow) bằng Terraform.
- Hạ tầng pipeline versioned + tái lập per-môi-trường.
- Khác **config management** (Ansible) — Terraform tạo *hạ tầng*, Ansible cấu hình *bên trong máy*.

## ⚠️ Cạm bẫy
- Sửa tay trên console → **drift** khỏi state → lần apply sau bất ngờ. Quy tắc: đổi qua Terraform, không tay.
- Commit `tfstate` (có secret) vào git → rò rỉ; dùng remote backend.
- Không `plan` trước `apply` → xoá nhầm tài nguyên.
- Hardcode secret trong `.tf` → dùng variable + secret manager.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Vì sao IaC (reproducible/version/automate) hơn click tay.
- [ ] resource/provider/variable/module.
- [ ] init/plan/apply/destroy; vì sao plan trước apply.
- [ ] State để làm gì; vì sao remote backend + lock.
- 🔭 *Tự mò:* `terraform` + **LocalStack** (AWS giả local): viết `.tf` tạo S3 bucket + Glue database, `plan` → `apply` → `destroy`. Không tốn tiền.

➡️ Tiếp: [[58-cicd]].
