# F06 — DataOps & CI/CD nâng cao

> DataOps = áp DevOps + Agile + lean vào data: tự động hoá, test, monitor, lặp nhanh & tin cậy. Sâu hơn [[58-cicd]].

## DataOps là gì
Văn hoá + thực hành đưa **kỹ thuật phần mềm** vào vòng đời data: version control, CI/CD, automated testing, monitoring, môi trường tách biệt, lặp nhanh. Mục tiêu: **thay đổi data pipeline nhanh & an toàn** (giảm "thời gian từ ý tưởng → production" + giảm lỗi).

## 3 trụ (giống DevOps áp cho data)
1. **Automation**: pipeline, test, deploy tự động (không tay).
2. **Testing/monitoring liên tục**: test code + data ([[f01-testing-strategy]]) + observability ([[62-observability]]).
3. **Collaboration + version control**: code, config, **và data definition** trong git; review qua PR.

## CI/CD pipeline đầy đủ cho data
```
Dev commit/PR
   │
CI:  lint (ruff/sqlfluff) → unit test (pytest) → build dbt trên data mẫu/CI warehouse
     → dbt test (data quality) → schema/contract check → (slim CI: chỉ model đổi)
   │ merge
CD:  deploy → staging (chạy trên data giống prod) → smoke/integration test
     → prod (deploy dbt models, Airflow DAGs, Terraform infra)
   │
Monitor: observability (freshness/volume/quality) + alert + rollback nếu cần
```

## Môi trường tách biệt (dev/staging/prod)
- **Dev**: thử nghiệm, data nhỏ/sample; dbt target dev (schema riêng per dev).
- **Staging**: giống prod, chạy CI/integration trước release.
- **Prod**: data thật, chỉ deploy qua pipeline đã pass.
- dbt **targets** + **schema riêng** (vd `dbt_<user>`); **zero-copy clone** (Snowflake) tạo môi trường từ prod rẻ ([[d04-snowflake]]).

## Deploy data an toàn
- **Blue-green / atomic swap**: build bảng mới (vd `table__new`) → test → **swap** (rename) → consumer không downtime, không thấy data nửa vời (giống atomic publish — [[40-pipeline-patterns]]).
- **Backward-compatible schema change** + contract → không phá downstream ([[61-data-contracts]]).
- **Rollback**: time travel (Delta/Snowflake) hoặc redeploy version cũ.

## Version everything
- **Code** (transform, DAG) → git.
- **Data definitions** (dbt models, schema, contract, semantic layer) → git.
- **Infra** (Terraform) → git ([[57-terraform]]).
- **Data** bản thân: table format time travel/snapshot (Delta/Iceberg) = "git cho data" (version, rollback, time travel — [[34-delta-lake]]).

## Automation cụ thể
- Pre-commit hooks (lint SQL/Python).
- CI mỗi PR (test + dbt build slim).
- Auto-deploy khi merge (dbt Cloud / GitHub Actions).
- Auto data quality + freshness monitoring → alert.
- Auto docs/lineage (`dbt docs generate`).

## DataOps vs MLOps vs DevOps
- **DevOps**: ship code/app.
- **DataOps**: ship data pipeline + đảm bảo data đúng (thêm chiều "data quality/observability" mà DevOps không có).
- **MLOps**: ship model (thêm training/serving/drift) — chồng lấn DataOps ở feature pipeline ([[c09-case-recsys]]).

## ⚠️ Cạm bẫy
- Test/deploy đụng prod data → nguy hiểm; cần CI warehouse/sample.
- Deploy thủ công (copy file) → không lặp lại, dễ sai.
- Version code nhưng quên version data definition/infra.
- CI chậm dần (full build) → slim CI.
- Quên monitor sau deploy (CD không có "monitor" = mù).

## ✅ "Tự mò"
🔭 Thêm `.github/workflows/ci.yml` cho project: lint + pytest + `dbt build` (DuckDB) mỗi PR; nghĩ cách "blue-green" cho 1 mart (build `__new` rồi swap).

➡️ Tiếp: [[f07-career-roadmap]].
