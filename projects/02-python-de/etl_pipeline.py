"""Capstone P1 — ETL end-to-end theo kiến trúc medallion (bronze→silver→gold).

  EXTRACT  : đọc raw parquet (bronze) từ data/raw/
  TRANSFORM: clean + enrich bằng polars (silver), build marts (gold)
  LOAD     : ghi gold ra warehouse/de.duckdb (+ export Parquet)

Ghép mọi thứ Phase 1: polars (T012), transforms thuần (T016), logging/
exceptions/retry (T017). Idempotent: CREATE OR REPLACE -> chạy lại ra cùng kết quả.

Chạy: python projects/02-python-de/etl_pipeline.py
"""
from __future__ import annotations

from pathlib import Path

import duckdb
import polars as pl

from utils import ExtractError, LoadError, TransformError, get_logger

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
GOLD_DIR = ROOT / "data" / "processed" / "gold"
DB_PATH = ROOT / "warehouse" / "de.duckdb"

log = get_logger("etl")
VALID_STATUS = ["completed", "shipped", "cancelled", "returned"]


# --------------------------- EXTRACT ---------------------------------
def extract() -> dict[str, pl.DataFrame]:
    try:
        tables = {name: pl.read_parquet(RAW / f"{name}.parquet")
                  for name in ("customers", "products", "orders", "order_items")}
        log.info("EXTRACT: %s", {k: v.height for k, v in tables.items()})
        return tables
    except Exception as exc:  # noqa: BLE001
        raise ExtractError(f"không đọc được raw: {exc}") from exc


# --------------------------- TRANSFORM (silver) ----------------------
def transform_silver(raw: dict[str, pl.DataFrame]) -> dict[str, pl.DataFrame]:
    try:
        orders = (raw["orders"]
                  .with_columns(pl.col("order_ts").str.to_datetime())
                  .filter(pl.col("status").is_in(VALID_STATUS)))
        # fact ở grain order_item, enrich category + status + tháng
        fct = (raw["order_items"]
               .join(orders.select("order_id", "customer_id", "status", "order_ts"), on="order_id")
               .join(raw["products"].select("product_id", "category"), on="product_id")
               .with_columns(pl.col("order_ts").dt.truncate("1mo").alias("order_month")))
        # quality gate: không có null ở khoá & line_total
        bad = fct.select(pl.col("order_id").is_null().sum().alias("oid_null"),
                         pl.col("line_total").is_null().sum().alias("lt_null"))
        if bad.row(0) != (0, 0):
            raise TransformError(f"quality gate fail: {bad.to_dicts()}")
        log.info("TRANSFORM silver: fct_order_items=%d hàng (sau lọc status hợp lệ)", fct.height)
        return {"orders": orders, "fct_order_items": fct,
                "customers": raw["customers"], "products": raw["products"]}
    except TransformError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise TransformError(f"transform lỗi: {exc}") from exc


# --------------------------- TRANSFORM (gold marts) ------------------
def build_gold(silver: dict[str, pl.DataFrame]) -> dict[str, pl.DataFrame]:
    fct = silver["fct_order_items"]
    completed = fct.filter(pl.col("status") == "completed")

    mart_rev_category = (completed.group_by("category")
                         .agg(revenue=pl.col("line_total").sum().round(2),
                              units=pl.col("quantity").sum(),
                              orders=pl.col("order_id").n_unique())
                         .sort("revenue", descending=True))

    mart_monthly = (completed.group_by("order_month")
                    .agg(revenue=pl.col("line_total").sum().round(2),
                         orders=pl.col("order_id").n_unique())
                    .sort("order_month"))

    mart_customer_ltv = (completed.group_by("customer_id")
                         .agg(lifetime_value=pl.col("line_total").sum().round(2),
                              orders=pl.col("order_id").n_unique())
                         .sort("lifetime_value", descending=True))

    log.info("TRANSFORM gold: %d marts", 3)
    return {"mart_revenue_by_category": mart_rev_category,
            "mart_monthly_revenue": mart_monthly,
            "mart_customer_ltv": mart_customer_ltv}


# --------------------------- LOAD ------------------------------------
def load(tables: dict[str, pl.DataFrame], db_path: Path) -> None:
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        GOLD_DIR.mkdir(parents=True, exist_ok=True)
        con = duckdb.connect(str(db_path))
        for name, df in tables.items():
            arrow = df.to_arrow()
            con.register("tmp", arrow)
            con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM tmp")  # idempotent
            con.unregister("tmp")
            df.write_parquet(GOLD_DIR / f"{name}.parquet")                       # export gold
        con.close()
        log.info("LOAD: %d bảng -> %s (+ Parquet ở data/processed/gold/)",
                 len(tables), db_path.relative_to(ROOT))
    except Exception as exc:  # noqa: BLE001
        raise LoadError(f"load DuckDB lỗi: {exc}") from exc


# --------------------------- ORCHESTRATE -----------------------------
def main() -> None:
    log.info("===== ETL pipeline bắt đầu =====")
    raw = extract()
    silver = transform_silver(raw)
    gold = build_gold(silver)
    load(gold, DB_PATH)

    # Summary: đọc lại từ DuckDB để xác nhận đã ghi
    con = duckdb.connect(str(DB_PATH))
    print("\n--- Bảng trong warehouse/de.duckdb ---")
    tbls = con.execute("SELECT table_name FROM information_schema.tables ORDER BY 1").fetchall()
    for (t,) in tbls:
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t:28s} {n:>6,} rows")
    print("\n--- Top doanh thu theo category (từ DuckDB) ---")
    print(con.execute(
        "SELECT category, revenue FROM mart_revenue_by_category LIMIT 5").fetchdf().to_string(index=False))
    con.close()
    log.info("===== ETL hoàn tất ✅ (idempotent: chạy lại ra cùng kết quả) =====")


if __name__ == "__main__":
    main()
