#!/usr/bin/env bash
# run_all.sh — smoke test: chạy lại mọi artifact đã hoàn thành để đảm bảo
# không có gì bị hỏng (regression check). Dùng ở mỗi checkpoint cuối phase.
# Usage: bash scripts/run_all.sh
set -uo pipefail
cd "$(dirname "$0")/.."
source .venv/bin/activate

fail=0

echo "== Regenerate dataset =="
python scripts/gen_ecommerce.py >/dev/null 2>&1 && echo "  gen_ecommerce.py: OK" \
    || { echo "  gen_ecommerce.py: FAILED"; fail=1; }

echo "== SQL scripts =="
# Chạy mọi file .sql trừ 'exercises' (chỉ đề bài) và TRỪ dbt project 04-dbt
# (file dbt là Jinja/template, do `dbt build` lo riêng — không chạy bằng run_sql.py).
for f in $(find projects -name '*.sql' ! -name 'exercises.sql' ! -path '*/04-dbt/*' | sort); do
    if python scripts/run_sql.py "$f" >/dev/null 2>&1; then
        echo "  $(basename "$f"): OK"
    else
        echo "  $(basename "$f"): FAILED"; fail=1
    fi
done

echo "== Shell scripts =="
if bash scripts/explore.sh >/dev/null 2>&1; then echo "  explore.sh: OK"; else echo "  explore.sh: FAILED"; fail=1; fi

echo "== Phase 1 Python scripts =="
for f in projects/02-python-de/01_pandas_basics.py \
         projects/02-python-de/02_polars_basics.py \
         projects/02-python-de/03_formats_benchmark.py \
         projects/02-python-de/04_json_avro.py \
         projects/02-python-de/05_api_ingest.py \
         projects/02-python-de/utils.py \
         projects/02-python-de/etl_pipeline.py; do
    if python "$f" >/dev/null 2>&1; then echo "  $(basename "$f"): OK"; else echo "  $(basename "$f"): FAILED"; fail=1; fi
done

echo "== pytest =="
if python -m pytest projects/02-python-de -q >/dev/null 2>&1; then echo "  pytest: OK"; else echo "  pytest: FAILED"; fail=1; fi

echo "== Phase 2 Python scripts =="
for f in projects/03-data-modeling/02_constraints_tx.py \
         projects/03-data-modeling/04_build_star.py \
         projects/03-data-modeling/05_scd.py \
         projects/03-data-modeling/07_nosql_modeling.py; do
    if python "$f" >/dev/null 2>&1; then echo "  $(basename "$f"): OK"; else echo "  $(basename "$f"): FAILED"; fail=1; fi
done

echo "== Phase 3 dbt build (seed+run+test, trừ snapshot stateful) =="
DBT="--project-dir projects/04-dbt --profiles-dir projects/04-dbt"
if dbt build $DBT --exclude scd_customer >/dev/null 2>&1; then echo "  dbt build: OK"; else echo "  dbt build: FAILED"; fail=1; fi

echo "=========================="
if [ "$fail" -eq 0 ]; then echo "ALL GREEN ✅"; else echo "SOME CHECKS FAILED ❌"; fi
exit "$fail"
