"""JSON/JSONL semi-structured + Avro schema evolution.

Chạy: python projects/02-python-de/04_json_avro.py

- JSON & JSONL: đọc/ghi, flatten dữ liệu lồng bằng pd.json_normalize + explode.
- Avro: ghi/đọc bằng fastavro; minh hoạ SCHEMA EVOLUTION (thêm field có default,
  đọc dữ liệu cũ bằng schema mới vẫn OK).
"""
from __future__ import annotations

import io
import json
from pathlib import Path

import fastavro
import pandas as pd

OUT = Path(__file__).resolve().parents[2] / "data" / "processed" / "json_avro"
OUT.mkdir(parents=True, exist_ok=True)


def section(t: str) -> None:
    print(f"\n{'=' * 60}\n{t}\n{'=' * 60}")


# Dữ liệu LỒNG (nested) — đơn hàng có customer lồng + danh sách items
ORDERS = [
    {"order_id": 1, "customer": {"id": 10, "country": "VN"},
     "items": [{"sku": "A", "qty": 2}, {"sku": "B", "qty": 1}]},
    {"order_id": 2, "customer": {"id": 22, "country": "JP"},
     "items": [{"sku": "C", "qty": 5}]},
]


def json_demo() -> None:
    section("1) JSON vs JSONL: ghi & đọc")
    # JSON: một mảng lớn (phải đọc cả file mới parse được)
    (OUT / "orders.json").write_text(json.dumps(ORDERS, indent=2))
    # JSONL: mỗi dòng 1 object -> stream/append từng dòng được (hợp big data)
    with (OUT / "orders.jsonl").open("w") as f:
        for rec in ORDERS:
            f.write(json.dumps(rec) + "\n")
    print("orders.json  bytes:", (OUT / "orders.json").stat().st_size)
    print("orders.jsonl bytes:", (OUT / "orders.jsonl").stat().st_size)
    print("Đọc lại JSONL từng dòng:")
    with (OUT / "orders.jsonl").open() as f:
        for line in f:
            r = json.loads(line)
            print("  order", r["order_id"], "->", len(r["items"]), "items")

    section("2) Flatten nested: json_normalize + explode")
    # mỗi item thành 1 hàng, kèm order_id & customer.country (meta)
    flat = pd.json_normalize(
        ORDERS, record_path="items",
        meta=["order_id", ["customer", "country"]],
    )
    print(flat.to_string(index=False))


def avro_demo() -> None:
    section("3) Avro: ghi & đọc bằng fastavro")
    schema_v1 = {
        "type": "record", "name": "Order",
        "fields": [
            {"name": "order_id", "type": "long"},
            {"name": "amount", "type": "double"},
        ],
    }
    records_v1 = [{"order_id": 1, "amount": 99.9}, {"order_id": 2, "amount": 250.0}]
    buf = io.BytesIO()
    fastavro.writer(buf, schema_v1, records_v1)
    raw = buf.getvalue()
    print(f"Ghi {len(records_v1)} record với schema v1, {len(raw)} bytes (schema nhúng trong file).")
    # đọc lại bình thường
    got = list(fastavro.reader(io.BytesIO(raw)))
    print("Đọc lại:", got)

    section("4) ⭐ SCHEMA EVOLUTION: đọc dữ liệu CŨ bằng schema MỚI")
    # v2 thêm field 'currency' CÓ DEFAULT -> backward compatible
    schema_v2 = {
        "type": "record", "name": "Order",
        "fields": [
            {"name": "order_id", "type": "long"},
            {"name": "amount", "type": "double"},
            {"name": "currency", "type": "string", "default": "USD"},  # field mới + default
        ],
    }
    # đọc lại bytes cũ (ghi bằng v1) nhưng dùng reader_schema = v2
    evolved = list(fastavro.reader(io.BytesIO(raw), reader_schema=schema_v2))
    print("Reader v2 đọc data v1 -> field mới lấy default:")
    for r in evolved:
        print(" ", r)
    assert all(r["currency"] == "USD" for r in evolved), "schema evolution failed"
    print("✔ Backward compatible: thêm field có default đọc được data cũ.")

    print("\nDONE ✅ json/avro demo chạy xong.")


def main() -> None:
    json_demo()
    avro_demo()


if __name__ == "__main__":
    main()
