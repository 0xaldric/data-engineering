"""Constraints, Transactions & ACID trên DuckDB.

Chạy: python projects/03-data-modeling/02_constraints_tx.py

Demo: PK / UNIQUE / NOT NULL / CHECK / FOREIGN KEY chặn dữ liệu bẩn ngay tại DB;
transaction BEGIN/COMMIT/ROLLBACK (rollback hoàn tác toàn bộ).
"""
from __future__ import annotations

import duckdb

con = duckdb.connect(":memory:")


def try_exec(label: str, sql: str) -> None:
    """Thử chạy 1 lệnh; in OK nếu chạy được, BLOCKED nếu bị constraint chặn."""
    try:
        con.execute(sql)
        print(f"  OK      | {label}")
    except duckdb.Error as exc:
        first = str(exc).splitlines()[0][:70]
        print(f"  BLOCKED | {label} -> {type(exc).__name__}: {first}")


def section(t: str) -> None:
    print(f"\n{'=' * 60}\n{t}\n{'=' * 60}")


def main() -> None:
    section("1) Tạo bảng có RÀNG BUỘC")
    con.execute("""
        CREATE TABLE product (
            product_id INTEGER PRIMARY KEY,            -- duy nhất + không null
            sku        VARCHAR UNIQUE NOT NULL,        -- duy nhất + bắt buộc
            price      DECIMAL(10,2) CHECK (price >= 0), -- không âm
            category   VARCHAR NOT NULL
        )""")
    con.execute("INSERT INTO product VALUES (1,'SKU-1',10.00,'Books')")
    con.execute("INSERT INTO product VALUES (2,'SKU-2',20.00,'Toys')")
    print("  Đã insert 2 sản phẩm hợp lệ.")

    section("2) Constraint CHẶN dữ liệu bẩn")
    try_exec("PK trùng (product_id=1)",        "INSERT INTO product VALUES (1,'SKU-9',5,'X')")
    try_exec("UNIQUE trùng (sku='SKU-1')",     "INSERT INTO product VALUES (3,'SKU-1',5,'X')")
    try_exec("NOT NULL (sku = NULL)",          "INSERT INTO product VALUES (4,NULL,5,'X')")
    try_exec("CHECK (price = -1 < 0)",         "INSERT INTO product VALUES (5,'SKU-5',-1,'X')")
    try_exec("NOT NULL (category = NULL)",     "INSERT INTO product VALUES (6,'SKU-6',5,NULL)")
    try_exec("Hợp lệ (product_id=7)",          "INSERT INTO product VALUES (7,'SKU-7',7,'OK')")

    section("3) FOREIGN KEY — toàn vẹn tham chiếu")
    con.execute("""
        CREATE TABLE sale (
            sale_id    INTEGER PRIMARY KEY,
            product_id INTEGER REFERENCES product(product_id)  -- phải tồn tại trong product
        )""")
    try_exec("FK hợp lệ (product_id=1 tồn tại)",  "INSERT INTO sale VALUES (100, 1)")
    try_exec("FK sai (product_id=999 không có)",  "INSERT INTO sale VALUES (101, 999)")

    section("4) TRANSACTION: ROLLBACK hoàn tác, COMMIT giữ lại")
    n0 = con.execute("SELECT COUNT(*) FROM product").fetchone()[0]
    print(f"  Số product ban đầu: {n0}")

    con.execute("BEGIN TRANSACTION")
    con.execute("INSERT INTO product VALUES (50,'SKU-50',50,'Tmp')")
    n1 = con.execute("SELECT COUNT(*) FROM product").fetchone()[0]
    print(f"  Trong transaction sau INSERT: {n1}")
    con.execute("ROLLBACK")
    n2 = con.execute("SELECT COUNT(*) FROM product").fetchone()[0]
    print(f"  Sau ROLLBACK: {n2}  -> {'hoàn tác OK' if n2 == n0 else 'SAI'}")

    con.execute("BEGIN TRANSACTION")
    con.execute("INSERT INTO product VALUES (51,'SKU-51',51,'Keep')")
    con.execute("COMMIT")
    n3 = con.execute("SELECT COUNT(*) FROM product").fetchone()[0]
    print(f"  Sau COMMIT: {n3}  -> {'giữ lại OK' if n3 == n0 + 1 else 'SAI'}")

    print("\nDONE ✅ constraints & transactions chạy xong.")


if __name__ == "__main__":
    main()
