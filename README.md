# 🛠️ Data Engineering — Hands-on Learning Project

Lộ trình thực hành Data Engineering từ zero → job-ready, **chạy hoàn toàn local** (Python + DuckDB, không tốn tiền cloud). Dự án này tự chạy qua một **loop tự động mỗi 30 phút**: mỗi lượt hoàn thành một task trong [`task.md`](task.md), khi hết task thì sinh batch mới từ [`ROADMAP.md`](ROADMAP.md).

## 📂 Cấu trúc

```
data-engineering/
├── ROADMAP.md          # Lộ trình đầy đủ 10 phase (0→9)
├── task.md             # Hàng đợi task của batch hiện tại (loop làm theo file này)
├── PROGRESS.md         # Nhật ký task đã xong
├── requirements.txt    # Python dependencies
├── data/
│   ├── raw/            # Dataset thô (CSV/Parquet) — gitignored
│   └── processed/      # Dữ liệu đã transform
├── warehouse/          # DuckDB databases
├── projects/           # Code thực hành theo phase (đánh số)
├── notes/              # Ghi chú lý thuyết (tiếng Việt)
└── scripts/            # Tiện ích (generator, explore...)
```

## 🚀 Setup

```bash
cd data-engineering
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Cách chạy

Sinh dataset nền (cần cho các bài SQL):
```bash
python scripts/gen_ecommerce.py
```

Chạy một file SQL trên DuckDB (qua helper):
```bash
python scripts/run_sql.py projects/01-sql-fundamentals/01_basics.sql
```

## 🔁 Loop tự động
Một loop (Claude Code `/loop 30m`) chạy mỗi 30 phút, đọc `task.md`, hoàn thành task chưa xong, tick `[x]`, log vào `PROGRESS.md`. Khi hết batch → tự sinh batch tiếp theo từ ROADMAP. Xem PROTOCOL ở đầu `task.md`.

## 📊 Tiến độ
- [x] Phase 0 — Foundations & SQL ✅ *(10/10 task)*
- [x] Phase 1 — Programming for DE ✅ *(9/9 task, ETL end-to-end)*
- [x] Phase 2 — Databases & Data Modeling ✅ *(9/9 task, star schema + SCD2)*
- [x] Phase 3 — Data Warehousing & dbt ✅ *(9/9 task, dbt project đầy đủ: models/tests/snapshots/incremental; smoke test ALL GREEN — `bash scripts/run_all.sh`)*
- [x] Phase 4 — Spark & Big Data ✅ *(9/9 notes — notes-first mode)*
- [x] Phase 5 — Orchestration (Airflow) ✅ *(9/9 notes)*
- [x] Phase 6 — Streaming (Kafka) ✅ *(9/9 notes)*
- [x] Phase 7 — Cloud & Infra ✅ *(8/8 notes)*
- [x] Phase 8 — Data Quality & Governance ✅ *(6/6 notes)*
- [x] Phase 9 — Capstone Projects ✅ *(5/5 notes)* — 🎓 **TOÀN BỘ 9/9 PHASE HOÀN TẤT**. Index: [notes/00-COURSE-COMPLETE.md](notes/00-COURSE-COMPLETE.md)

> Mọi notes bằng tiếng Việt, code/comment tiếng Anh. Triết lý: học bằng cách **build** — mỗi khái niệm = code chạy được + giải thích "tại sao".
