"""NoSQL data modeling — Document model vs Relational (embedding vs referencing).

Chạy: python projects/03-data-modeling/07_nosql_modeling.py

Lấy dữ liệu đơn hàng quan hệ (orders + items + product + customer) rồi mô hình
hoá lại thành DOCUMENT (1 order = 1 JSON lồng, denormalized/embedded). So sánh
hai cách tiếp cận và minh hoạ pattern truy cập của document store.
"""
from __future__ import annotations

import json
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed" / "nosql"
OUT.mkdir(parents=True, exist_ok=True)
SAMPLE = 200  # số đơn lấy mẫu cho rõ


def section(t: str) -> None:
    print(f"\n{'=' * 60}\n{t}\n{'=' * 60}")


def build_documents(con: duckdb.DuckDBPyConnection) -> list[dict]:
    """RELATIONAL -> DOCUMENT: gộp (embed) customer + items + product vào 1 đơn."""
    rows = con.execute(f"""
        SELECT o.order_id, o.order_ts, o.status, o.channel,
               c.customer_id, c.name, c.country,
               oi.product_id, p.product_name, p.category,
               oi.quantity, oi.unit_price, oi.line_total
        FROM read_parquet('{RAW}/orders.parquet') o
        JOIN read_parquet('{RAW}/customers.parquet') c   ON c.customer_id = o.customer_id
        JOIN read_parquet('{RAW}/order_items.parquet') oi ON oi.order_id = o.order_id
        JOIN read_parquet('{RAW}/products.parquet') p     ON p.product_id = oi.product_id
        WHERE o.order_id <= {SAMPLE}
        ORDER BY o.order_id""").fetchall()

    docs: dict[int, dict] = {}
    for (oid, ts, status, channel, cid, cname, country,
         pid, pname, cat, qty, price, line_total) in rows:
        doc = docs.setdefault(oid, {
            "_id": oid,
            "order_ts": str(ts),
            "status": status,
            "channel": channel,
            "customer": {"customer_id": cid, "name": cname, "country": country},  # embedded
            "items": [],                                                            # nested array
        })
        doc["items"].append({
            "product_id": pid, "product_name": pname, "category": cat,
            "quantity": qty, "unit_price": float(price), "line_total": float(line_total),
        })
    # measure tính sẵn trong document (denormalized aggregate)
    for d in docs.values():
        d["order_total"] = round(sum(i["line_total"] for i in d["items"]), 2)
        d["n_items"] = len(d["items"])
    return list(docs.values())


def main() -> None:
    con = duckdb.connect(":memory:")
    docs = build_documents(con)

    section("1) DOCUMENT model — 1 order = 1 JSON lồng (embedded)")
    path = OUT / "orders.jsonl"
    with path.open("w") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"Ghi {len(docs)} documents -> {path.relative_to(ROOT)}")
    print("Ví dụ 1 document:")
    print(json.dumps(docs[0], ensure_ascii=False, indent=2)[:600], "...")

    section("2) Đọc lại & query kiểu document store (không JOIN)")
    loaded = [json.loads(line) for line in path.open()]
    # toàn bộ đơn nằm trong 1 document -> đọc 1 lần là đủ, không cần join nhiều bảng
    big = [d for d in loaded if d["order_total"] > 2000]
    print(f"Đơn có order_total > 2000: {len(big)}")
    # aggregate xuyên document (như map-reduce / aggregation pipeline)
    from collections import Counter
    cat_rev: Counter = Counter()
    for d in loaded:
        for it in d["items"]:
            cat_rev[it["category"]] += it["line_total"]
    print("Top 3 category theo doanh thu (gộp xuyên documents):")
    for cat, rev in sorted(cat_rev.items(), key=lambda x: -x[1])[:3]:
        print(f"  {cat:14s} {rev:12,.2f}")

    section("3) DuckDB đọc thẳng JSON lồng (read_json_auto)")
    out = con.execute(f"""
        SELECT _id, customer.country AS country, n_items, order_total
        FROM read_json_auto('{path}')
        ORDER BY order_total DESC LIMIT 3""").fetchdf()
    print(out.to_string(index=False))
    print("→ Cùng dữ liệu, lưu lồng (document) vs phẳng-nhiều-bảng (relational).")

    print("\nDONE ✅ nosql document modeling chạy xong.")


if __name__ == "__main__":
    main()
