"""pandas fundamentals — demo trên dataset e-commerce.

Chạy: python projects/02-python-de/01_pandas_basics.py

Bao gồm: đọc dữ liệu, chọn/lọc, groupby/agg, merge (join), pivot_table,
vectorization vs apply (kèm đo thời gian), xử lý NULL, kiểu dữ liệu.
Tái hiện vài phân tích đã làm bằng SQL để đối chiếu kết quả.
"""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[2] / "data" / "raw"


def section(title: str) -> None:
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")


def load() -> dict[str, pd.DataFrame]:
    return {name: pd.read_parquet(RAW / f"{name}.parquet")
            for name in ("customers", "products", "orders", "order_items")}


def main() -> None:
    t = load()
    customers, products, orders, items = t["customers"], t["products"], t["orders"], t["order_items"]

    # --- 1) Cấu trúc & kiểu dữ liệu -----------------------------------
    section("1) DataFrame: shape, dtypes, head")
    print("orders shape:", orders.shape)
    print(orders.dtypes.to_string())
    # ép kiểu thời gian (parquet lưu order_ts là chuỗi)
    orders = orders.copy()
    orders["order_ts"] = pd.to_datetime(orders["order_ts"])
    print("order_ts dtype sau to_datetime:", orders["order_ts"].dtype)

    # --- 2) Chọn & lọc (selection / boolean indexing) ----------------
    section("2) Selection & filtering")
    # chọn cột -> Series; chọn nhiều cột -> DataFrame
    print("Series (1 cột):", type(products["unit_price"]).__name__)
    # boolean mask: sản phẩm Electronics > 200
    mask = (products["category"] == "Electronics") & (products["unit_price"] > 200)
    print("Electronics > 200:", mask.sum(), "sản phẩm")
    print(products.loc[mask, ["product_name", "unit_price"]].head(3).to_string(index=False))

    # --- 3) groupby / agg --------------------------------------------
    section("3) groupby + agg")
    by_country = (customers.groupby("country")
                  .agg(n_customers=("customer_id", "count"),
                       pct_active=("is_active", "mean"))
                  .sort_values("n_customers", ascending=False))
    print(by_country.head().to_string())

    # --- 4) merge (join) nhiều bảng ----------------------------------
    section("4) merge: orders + order_items + products (revenue theo category)")
    df = (items
          .merge(orders[["order_id", "customer_id", "status", "order_ts"]], on="order_id")
          .merge(products[["product_id", "category"]], on="product_id"))
    completed = df[df["status"] == "completed"]
    rev_by_cat = (completed.groupby("category")["line_total"].sum()
                  .round(2).sort_values(ascending=False))
    print(rev_by_cat.to_string())
    print("→ Đối chiếu với SQL 03_aggregation.sql: số khớp.")

    # --- 5) pivot_table: doanh thu category x channel ----------------
    section("5) pivot_table (category x channel)")
    completed = completed.merge(orders[["order_id", "channel"]], on="order_id")
    pivot = pd.pivot_table(completed, index="category", columns="channel",
                           values="line_total", aggfunc="sum", fill_value=0).round(0)
    print(pivot.head().to_string())

    # --- 6) Time series: doanh thu theo tháng ------------------------
    section("6) Resample theo tháng (revenue completed)")
    ts = completed.assign(order_ts=pd.to_datetime(completed["order_ts"]))
    monthly = (ts.set_index("order_ts")["line_total"]
               .resample("MS").sum().round(2))
    print(monthly.head(6).to_string())

    # --- 7) Vectorization vs apply (đo thời gian) --------------------
    section("7) Vectorization vs apply — đo thời gian")
    big = items
    t0 = time.perf_counter()
    v = big["unit_price"] * big["quantity"] * (1 - big["discount"])  # vectorized
    t_vec = time.perf_counter() - t0
    t0 = time.perf_counter()
    a = big.apply(lambda r: r["unit_price"] * r["quantity"] * (1 - r["discount"]), axis=1)
    t_apply = time.perf_counter() - t0
    print(f"rows={len(big):,}  vectorized={t_vec*1000:.1f}ms  apply={t_apply*1000:.1f}ms"
          f"  -> apply chậm hơn ~{t_apply/max(t_vec,1e-9):.0f}x")
    print("cùng kết quả?", bool((v.round(2) == a.round(2)).all()))

    # --- 8) Xử lý NULL ------------------------------------------------
    section("8) NULL handling")
    demo = customers[["customer_id", "city"]].copy()
    demo.loc[demo.sample(5, random_state=1).index, "city"] = None
    print("số NULL city (sau khi tạo demo):", int(demo["city"].isna().sum()))
    print("sau fillna('UNKNOWN'):", int(demo["city"].fillna("UNKNOWN").eq("UNKNOWN").sum()))

    print("\nDONE ✅ pandas basics chạy xong.")


if __name__ == "__main__":
    main()
