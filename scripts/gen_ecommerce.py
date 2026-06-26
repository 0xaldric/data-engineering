"""Synthetic e-commerce dataset generator.

Generates a small but realistic relational e-commerce dataset used across the
SQL / modeling exercises in this project. Tables (with valid foreign keys):

    customers   (~2,000)  -> orders.customer_id
    products    (~300)    -> order_items.product_id
    orders      (~10,000) -> order_items.order_id
    order_items (~30,000)

Outputs both CSV and Parquet to data/raw/ so we can compare row vs columnar
formats later. Deterministic via a fixed seed for reproducibility.

Usage:
    python scripts/gen_ecommerce.py
"""
from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

SEED = 42
N_CUSTOMERS = 2_000
N_PRODUCTS = 300
N_ORDERS = 10_000
MAX_ITEMS_PER_ORDER = 5

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

CATEGORIES = [
    "Electronics", "Books", "Clothing", "Home & Kitchen", "Sports",
    "Toys", "Beauty", "Grocery", "Automotive", "Garden",
]
COUNTRIES = ["VN", "US", "JP", "DE", "SG", "AU", "FR", "GB", "KR", "IN"]
ORDER_STATUS = ["completed", "completed", "completed", "shipped", "cancelled", "returned"]
CHANNELS = ["web", "mobile_app", "marketplace"]

fake = Faker()
Faker.seed(SEED)
random.seed(SEED)

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)


def _rand_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def gen_customers() -> pd.DataFrame:
    rows = []
    for cid in range(1, N_CUSTOMERS + 1):
        signup = _rand_date(START_DATE, END_DATE)
        rows.append({
            "customer_id": cid,
            "name": fake.name(),
            "email": f"user{cid}@{fake.free_email_domain()}",
            "country": random.choice(COUNTRIES),
            "city": fake.city(),
            "signup_date": signup.date().isoformat(),
            "is_active": random.random() > 0.15,
        })
    return pd.DataFrame(rows)


def gen_products() -> pd.DataFrame:
    rows = []
    for pid in range(1, N_PRODUCTS + 1):
        category = random.choice(CATEGORIES)
        cost = round(random.uniform(2, 400), 2)
        margin = random.uniform(1.15, 2.5)
        rows.append({
            "product_id": pid,
            "product_name": f"{fake.word().capitalize()} {fake.word().capitalize()}",
            "category": category,
            "unit_cost": cost,
            "unit_price": round(cost * margin, 2),
            "is_available": random.random() > 0.1,
        })
    return pd.DataFrame(rows)


def gen_orders_and_items(products: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    orders, items = [], []
    product_ids = products["product_id"].tolist()
    price_map = dict(zip(products["product_id"], products["unit_price"]))
    item_id = 0
    for oid in range(1, N_ORDERS + 1):
        cid = random.randint(1, N_CUSTOMERS)
        order_ts = _rand_date(START_DATE, END_DATE)
        status = random.choice(ORDER_STATUS)
        n_items = random.randint(1, MAX_ITEMS_PER_ORDER)
        chosen = random.sample(product_ids, n_items)
        for pid in chosen:
            item_id += 1
            qty = random.randint(1, 4)
            unit_price = price_map[pid]
            discount = random.choice([0, 0, 0, 0.05, 0.1, 0.2])
            items.append({
                "order_item_id": item_id,
                "order_id": oid,
                "product_id": pid,
                "quantity": qty,
                "unit_price": unit_price,
                "discount": discount,
                "line_total": round(unit_price * qty * (1 - discount), 2),
            })
        orders.append({
            "order_id": oid,
            "customer_id": cid,
            "order_ts": order_ts.isoformat(sep=" ", timespec="seconds"),
            "status": status,
            "channel": random.choice(CHANNELS),
        })
    return pd.DataFrame(orders), pd.DataFrame(items)


def write_table(df: pd.DataFrame, name: str) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RAW_DIR / f"{name}.csv"
    pq_path = RAW_DIR / f"{name}.parquet"
    df.to_csv(csv_path, index=False)
    df.to_parquet(pq_path, index=False)
    print(f"  {name:12s} {len(df):>7,} rows -> {csv_path.name}, {pq_path.name}")


def main() -> None:
    print("Generating synthetic e-commerce dataset (seed=%d)..." % SEED)
    customers = gen_customers()
    products = gen_products()
    orders, items = gen_orders_and_items(products)

    write_table(customers, "customers")
    write_table(products, "products")
    write_table(orders, "orders")
    write_table(items, "order_items")

    total = len(customers) + len(products) + len(orders) + len(items)
    print(f"Done. {total:,} total rows across 4 tables in {RAW_DIR}")


if __name__ == "__main__":
    main()
