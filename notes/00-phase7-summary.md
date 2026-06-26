# 🏁 Phase 7 — Tổng kết: Cloud & Infrastructure

> Notes-first. Trọng tâm: chạy DE trên cloud — container, AWS data stack, IaC, CI/CD, chi phí.

## Các note
| # | Chủ đề | Note |
|---|--------|------|
| T065 | Docker & containers | [53](53-docker.md) |
| T066 | docker-compose & Kubernetes | [54](54-compose-k8s.md) |
| T067 | Cloud fundamentals + S3 + IAM | [55](55-cloud-fundamentals.md) |
| T068 | AWS data stack (+GCP/Azure) | [56](56-aws-data-stack.md) |
| T069 | Terraform (IaC) | [57](57-terraform.md) |
| T070 | CI/CD cho data | [58](58-cicd.md) |
| T071 | Cost & FinOps | [59](59-cost-finops.md) |

## 📑 Cheat-Sheet Cloud/Infra
- **Docker**: image (Dockerfile, layer, cache) → container; volume cho data bền; reproducible env, đóng gói job. compose = local multi-service; **K8s** = scale/heal production (Spark on K8s, Airflow KubernetesExecutor).
- **Cloud**: IaaS/PaaS/SaaS; region/AZ. **S3** = lake (bucket/key, storage class, lifecycle, partition layout); **IAM** least privilege (role cho service, không hardcode key).
- **AWS data**: S3 + Glue (catalog/ETL) + **Athena** (SQL on S3, tính theo bytes scanned) + EMR (Spark) + Kinesis (stream) + Redshift (DW) + Lambda (event). Map GCP (GCS/Dataflow/**BigQuery**/PubSub) & Azure.
- **Terraform**: declarative IaC; resource/provider/module; init/plan/apply; **state** + remote backend+lock; đổi qua code không tay (drift).
- **CI/CD**: PR → lint+pytest+`dbt build` trên CI warehouse; dev/staging/prod; slim CI; deploy dbt/Airflow/Terraform tự động.
- **Cost/FinOps**: quét ít (Parquet+partition+chọn cột) là đòn bẩy lớn nhất; spot/auto-terminate compute; storage tiering; incremental; tag + budget alert.

## ✅ Self-assessment Phase 7
- [ ] Docker (image/container/layer/volume); vì sao DE cần.
- [ ] compose vs K8s; K8s cho data workload.
- [ ] S3 (partition layout) + IAM least privilege.
- [ ] AWS data services & map đa cloud; Athena tính tiền theo gì.
- [ ] Terraform: plan/apply/state; vì sao IaC.
- [ ] CI/CD cho dbt/pipeline; môi trường tách biệt.
- [ ] Đòn bẩy tối ưu chi phí.

## 🔭 Để "tự mò"
1. Dockerize `etl_pipeline.py` (Phase 1) + `docker run` với volume.
2. docker-compose Postgres + app Python local.
3. **LocalStack** (AWS giả, free): S3 + Glue + Athena query parquet; Terraform `apply` tạo bucket/glue rồi `destroy`.
4. Thêm `.github/workflows/ci.yml`: chạy `run_all.sh`/pytest/`dbt build` mỗi PR.

## ➡️ Tiếp theo: Phase 8 — Data Quality, Governance & Observability
Great Expectations/Soda, data contracts, lineage (OpenLineage/DataHub), monitoring/freshness, PII/GDPR. (notes-first)
