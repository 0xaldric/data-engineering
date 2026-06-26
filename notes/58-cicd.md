# 58 — CI/CD cho Data Pipelines

> Đưa kỹ thuật phần mềm (test tự động, deploy tự động) vào pipeline dữ liệu → thay đổi an toàn, nhanh, lặp lại được.

## CI/CD là gì (trong ngữ cảnh data)
- **CI (Continuous Integration)**: mỗi push/PR → tự **lint + test + build** → bắt lỗi sớm trước khi merge.
- **CD (Continuous Delivery/Deployment)**: merge → tự **deploy** (dbt models, Airflow DAGs, Terraform infra) lên môi trường.
- Mục tiêu: thay đổi nhỏ, thường xuyên, được kiểm thử & rollback được.

## Pipeline CI/CD điển hình cho data (GitHub Actions)
```yaml
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: ruff check .          # lint
      - run: pytest                # unit test transform (xem [[12-testing-de]])
      - run: dbt build --target ci # build + test dbt trên warehouse CI ([[24-dbt-tests]])
```
- Chạy trên **dữ liệu mẫu / warehouse CI riêng** (không đụng prod).
- Test gồm: lint (ruff/black), **unit test** (pytest cho logic Python), **dbt build/test** (data quality), kiểm SQL compile, terraform `plan`.

## Kiểm thử theo tầng (xem lại)
- **Code**: pytest cho transform thuần ([[12-testing-de]]).
- **Data/SQL**: dbt tests (unique/not_null/relationships) ([[24-dbt-tests]]).
- **Infra**: `terraform plan`/`validate` ([[57-terraform]]).
- **Integration**: chạy pipeline trên container/DuckDB tạm.

## Môi trường dev / staging / prod
Tách môi trường (config theo env — [[13-logging-config]], [[42-airflow-resources]]):
- Dev: thử nghiệm tự do, dữ liệu nhỏ.
- Staging: giống prod, chạy CI/integration trước khi release.
- Prod: dữ liệu thật, chỉ deploy qua pipeline đã pass.
dbt dùng **targets** (dev/ci/prod profiles); Airflow deploy DAG theo branch/tag.

## Deploy data assets
- **dbt**: merge → CI `dbt build` trên staging → prod chạy theo lịch (Airflow gọi). "Slim CI": chỉ build model **thay đổi** (`state:modified+`) để nhanh.
- **Airflow DAGs**: sync thư mục `dags/` (git-sync, S3, image) lên môi trường.
- **Terraform**: `plan` ở PR, `apply` khi merge (có approval cho prod).
- **Blue-green / atomic swap**: build bảng mới rồi swap (giống atomic publish [[40-pipeline-patterns]]) để deploy không downtime.

## ⚠️ Cạm bẫy
- Test trên/đụng dữ liệu prod → nguy hiểm; luôn có warehouse/dataset CI riêng.
- Không có CI cho dbt → model lỗi merge vào prod, dashboard sai.
- Deploy thủ công (copy file tay) → không lặp lại, dễ sai; tự động hoá.
- CI quá chậm (build full mỗi lần) → dùng slim CI (chỉ phần đổi).
- Secret trong CI log → dùng GitHub Secrets, mask.

## ✅ Tự kiểm tra & "tự mò"
- [ ] CI vs CD; vì sao cần cho data (bắt lỗi data sớm).
- [ ] Viết job GitHub Actions: lint + pytest + dbt build.
- [ ] Test theo tầng (code/data/infra/integration).
- [ ] dev/staging/prod + dbt targets; slim CI.
- 🔭 *Tự mò:* thêm `.github/workflows/ci.yml` vào project: chạy `pytest projects/02-python-de` + `dbt build` (DuckDB) trên mỗi PR. (Chính là `run_all.sh` Phase 0–3 đưa lên CI!)

➡️ Tiếp: [[59-cost-finops]].
