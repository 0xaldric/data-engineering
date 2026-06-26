"""polars fundamentals + benchmark vs pandas.

Chạy: python projects/02-python-de/02_polars_basics.py

polars: DataFrame nhanh viết bằng Rust, dùng Apache Arrow, đa luồng, có
lazy evaluation + query optimizer. Demo expression API, lazy scan, và đo
thời gian cùng một tác vụ giữa pandas và polars.
"""
from __future__ import annotations

import time
from pathlib import Path

import polars as pl

RAW = Path(__file__).resolve().parents[2] / "data" / "raw"


def section(title: str) -> None:
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")


def timeit(fn, runs: int = 5) -> float:
    """Trả về thời gian nhỏ nhất (ms) qua nhiều lần chạy — ổn định hơn trung bình."""
    best = float("inf")
    for _ in range(runs):
        t0 = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best * 1000


def main() -> None:
    # --- 1) Expression API ------------------------------------------
    section("1) Expression API: select / filter / with_columns")
    products = pl.read_parquet(RAW / "products.parquet")
    out = (products
           .filter((pl.col("category") == "Electronics") & (pl.col("unit_price") > 200))
           .with_columns((pl.col("unit_price") - pl.col("unit_cost")).alias("margin"))
           .select("product_name", "unit_price", "margin")
           .sort("margin", descending=True)
           .head(3))
    print(out)

    # --- 2) group_by + agg ------------------------------------------
    section("2) group_by + agg (nhiều aggregate song song)")
    customers = pl.read_parquet(RAW / "customers.parquet")
    g = (customers.group_by("country")
         .agg(n=pl.len(), pct_active=pl.col("is_active").mean())
         .sort("n", descending=True)
         .head(5))
    print(g)

    # --- 3) LAZY evaluation + query optimizer -----------------------
    section("3) Lazy: scan_parquet -> build plan -> collect")
    lf = (pl.scan_parquet(RAW / "order_items.parquet")
          .join(pl.scan_parquet(RAW / "orders.parquet").select("order_id", "status"), on="order_id")
          .join(pl.scan_parquet(RAW / "products.parquet").select("product_id", "category"), on="product_id")
          .filter(pl.col("status") == "completed")
          .group_by("category")
          .agg(revenue=pl.col("line_total").sum())
          .sort("revenue", descending=True))
    print("Optimized query plan (projection/predicate pushdown):")
    print(lf.explain()[:600], "...")
    result = lf.collect()
    print(result.head())
    print("→ Đối chiếu revenue/category với SQL & pandas: khớp.")

    # --- 4) BENCHMARK: cùng tác vụ, pandas vs polars ----------------
    section("4) Benchmark — join 3 bảng + filter + group_by (revenue/category)")
    import pandas as pd

    def pandas_task():
        it = pd.read_parquet(RAW / "order_items.parquet")
        od = pd.read_parquet(RAW / "orders.parquet")[["order_id", "status"]]
        pr = pd.read_parquet(RAW / "products.parquet")[["product_id", "category"]]
        df = it.merge(od, on="order_id").merge(pr, on="product_id")
        return (df[df.status == "completed"].groupby("category")["line_total"].sum())

    def polars_eager():
        it = pl.read_parquet(RAW / "order_items.parquet")
        od = pl.read_parquet(RAW / "orders.parquet").select("order_id", "status")
        pr = pl.read_parquet(RAW / "products.parquet").select("product_id", "category")
        return (it.join(od, on="order_id").join(pr, on="product_id")
                .filter(pl.col("status") == "completed")
                .group_by("category").agg(pl.col("line_total").sum()))

    def polars_lazy():
        return (pl.scan_parquet(RAW / "order_items.parquet")
                .join(pl.scan_parquet(RAW / "orders.parquet").select("order_id", "status"), on="order_id")
                .join(pl.scan_parquet(RAW / "products.parquet").select("product_id", "category"), on="product_id")
                .filter(pl.col("status") == "completed")
                .group_by("category").agg(pl.col("line_total").sum()).collect())

    rows = [
        ("pandas (eager)", timeit(pandas_task)),
        ("polars (eager)", timeit(polars_eager)),
        ("polars (lazy+pushdown)", timeit(polars_lazy)),
    ]
    base = rows[0][1]
    print(f"{'engine':28s} {'best ms':>10s} {'speedup':>9s}")
    for name, ms in rows:
        print(f"{name:28s} {ms:>10.2f} {base/ms:>8.1f}x")

    print("\nDONE ✅ polars basics + benchmark chạy xong.")


if __name__ == "__main__":
    main()
