"""Build star schema cho e-commerce vào warehouse/star.duckdb.

Chạy: python projects/03-data-modeling/04_build_star.py

Triển khai thiết kế ở star_schema_design.md: dim_date (sinh lịch), dim_customer,
dim_product (surrogate key), fct_sales (grain = order line, tham chiếu surrogate
key). Sau đó query kiểm chứng số khớp gold mart đã có.
"""
from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
DB = ROOT / "warehouse" / "star.duckdb"


def main() -> None:
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB))
    # raw làm view tạm
    for name in ("customers", "products", "orders", "order_items"):
        con.execute(f"CREATE OR REPLACE VIEW v_{name} AS "
                    f"SELECT * FROM read_parquet('{RAW / (name + '.parquet')}')")

    # --- dim_date: sinh lịch từ min..max order date ----------------
    con.execute("""
        CREATE OR REPLACE TABLE dim_date AS
        SELECT CAST(strftime(d, '%Y%m%d') AS INTEGER) AS date_key,
               d                          AS full_date,
               EXTRACT(year    FROM d)    AS year,
               EXTRACT(quarter FROM d)    AS quarter,
               EXTRACT(month   FROM d)    AS month,
               strftime(d, '%B')          AS month_name,
               EXTRACT(day     FROM d)    AS day,
               EXTRACT(dayofweek FROM d)  AS weekday,
               (EXTRACT(dayofweek FROM d) IN (0, 6)) AS is_weekend
        FROM (
            SELECT unnest(generate_series(
                (SELECT MIN(CAST(order_ts AS DATE)) FROM v_orders),
                (SELECT MAX(CAST(order_ts AS DATE)) FROM v_orders),
                INTERVAL 1 DAY))::DATE AS d
        )""")

    # --- dim_customer (surrogate key) ------------------------------
    con.execute("""
        CREATE OR REPLACE TABLE dim_customer AS
        SELECT row_number() OVER (ORDER BY customer_id) AS customer_key,
               customer_id AS customer_id_nk,
               name, country, city, CAST(signup_date AS DATE) AS signup_date
        FROM v_customers""")

    # --- dim_product (surrogate key + price_tier) ------------------
    con.execute("""
        CREATE OR REPLACE TABLE dim_product AS
        SELECT row_number() OVER (ORDER BY product_id) AS product_key,
               product_id AS product_id_nk,
               product_name, category, unit_cost, unit_price,
               CASE WHEN unit_price >= 200 THEN 'premium'
                    WHEN unit_price >= 50  THEN 'mid'
                    ELSE 'budget' END AS price_tier
        FROM v_products""")

    # --- fct_sales (grain = order line, dùng surrogate key) --------
    con.execute("""
        CREATE OR REPLACE TABLE fct_sales AS
        SELECT dc.customer_key, dp.product_key, dd.date_key,
               oi.order_id,                       -- degenerate dimension
               o.status, o.channel,               -- junk
               oi.quantity, oi.unit_price, oi.discount, oi.line_total,
               dp.unit_cost,
               ROUND(oi.line_total - dp.unit_cost * oi.quantity, 2) AS gross_margin
        FROM v_order_items oi
        JOIN v_orders   o  ON o.order_id   = oi.order_id
        JOIN dim_customer dc ON dc.customer_id_nk = o.customer_id
        JOIN dim_product  dp ON dp.product_id_nk  = oi.product_id
        JOIN dim_date     dd ON dd.full_date      = CAST(o.order_ts AS DATE)""")

    # --- Báo cáo cấu trúc ------------------------------------------
    print("== Star schema trong warehouse/star.duckdb ==")
    for t in ("dim_date", "dim_customer", "dim_product", "fct_sales"):
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t:14s} {n:>7,} rows")

    # --- Kiểm chứng: doanh thu theo category (completed) -----------
    print("\n== Verify: revenue theo category (completed) — phải khớp gold mart ==")
    df = con.execute("""
        SELECT dp.category, ROUND(SUM(f.line_total), 2) AS revenue
        FROM fct_sales f
        JOIN dim_product dp ON dp.product_key = f.product_key
        WHERE f.status = 'completed'
        GROUP BY dp.category ORDER BY revenue DESC LIMIT 5""").fetchdf()
    print(df.to_string(index=False))

    grocery = con.execute("""
        SELECT ROUND(SUM(f.line_total), 2)
        FROM fct_sales f JOIN dim_product dp ON dp.product_key = f.product_key
        WHERE f.status = 'completed' AND dp.category = 'Grocery'""").fetchone()[0]
    assert grocery == 1714225.45, f"Grocery revenue lệch: {grocery}"
    print(f"\n✔ Grocery = {grocery:,.2f} KHỚP gold mart (Phase 1).")

    # --- Demo sức mạnh star: drill theo dim_date + dim_customer ----
    print("\n== Doanh thu theo quý × top country (drill qua nhiều dim) ==")
    print(con.execute("""
        SELECT dd.year, dd.quarter, dc.country, ROUND(SUM(f.line_total),0) AS rev
        FROM fct_sales f
        JOIN dim_date dd     ON dd.date_key = f.date_key
        JOIN dim_customer dc ON dc.customer_key = f.customer_key
        WHERE f.status='completed' AND dc.country IN ('VN','JP')
        GROUP BY dd.year, dd.quarter, dc.country
        ORDER BY dd.year, dd.quarter, dc.country LIMIT 6""").fetchdf().to_string(index=False))

    con.close()
    print("\nDONE ✅ star schema built & verified.")


if __name__ == "__main__":
    main()
