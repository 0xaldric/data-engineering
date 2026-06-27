"""Text-to-SQL pipeline với GUARDRAIL — vai trò DE trong NL2SQL.

LLM sinh SQL từ câu hỏi tiếng Việt → nhưng KHÔNG tin SQL mù quáng. DE bọc lớp an toàn:
  schema linking → mock-LLM sinh SQL → GUARDRAIL (chỉ SELECT, chặn DROP/DELETE, ép LIMIT)
  → VALIDATE (EXPLAIN/parse trước khi chạy) → SANDBOX execute (read-only) → kết quả.

Chạy: python projects/06-ai-data-engineering/text_to_sql.py
(Mock LLM bằng template — KHÔNG cần API. Logic guardrail/validate/sandbox là thật.)
"""
from __future__ import annotations

import re
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"

# Schema context (đưa cho LLM để "schema linking" — biết bảng/cột nào có)
SCHEMA = """
customers(customer_id, name, email, country, city, signup_date, is_active)
products(product_id, product_name, category, unit_cost, unit_price, is_available)
orders(order_id, customer_id, order_ts, status, channel)
order_items(order_item_id, order_id, product_id, quantity, unit_price, discount, line_total)
"""

# Mock LLM: ánh xạ câu hỏi -> SQL (LLM thật dùng schema context để sinh). Có 1 câu "độc".
MOCK = {
    "doanh thu theo category": """
        SELECT p.category, ROUND(SUM(oi.line_total),2) AS revenue
        FROM order_items oi JOIN products p USING(product_id)
        JOIN orders o USING(order_id) WHERE o.status='completed'
        GROUP BY p.category ORDER BY revenue DESC""",
    "top 5 khách chi nhiều nhất": """
        SELECT c.name, ROUND(SUM(oi.line_total),2) AS spend
        FROM customers c JOIN orders o USING(customer_id)
        JOIN order_items oi USING(order_id) WHERE o.status='completed'
        GROUP BY c.customer_id, c.name ORDER BY spend DESC LIMIT 5""",
    "đếm số đơn completed": "SELECT COUNT(*) AS n FROM orders WHERE status='completed'",
    "xóa bảng orders đi":  "DROP TABLE orders",                    # ⚠️ độc hại
    "cập nhật giá sản phẩm": "UPDATE products SET unit_price = 0",  # ⚠️ độc hại
}

# ---------------------------- GUARDRAIL ------------------------------
DANGER = re.compile(r"\b(drop|delete|update|insert|alter|create|attach|truncate|grant|copy|pragma)\b", re.I)


def guardrail(sql: str) -> tuple[bool, str]:
    """Chỉ cho SELECT đọc; chặn lệnh sửa/xoá; một câu lệnh; ép LIMIT."""
    s = sql.strip().rstrip(";").strip()
    if ";" in s:
        return False, "nhiều câu lệnh (SQL injection risk)"
    if DANGER.search(s):
        return False, f"chứa lệnh nguy hiểm: {DANGER.search(s).group()}"
    if not re.match(r"(?is)^\s*(with|select)\b", s):
        return False, "không phải SELECT (chỉ cho phép đọc)"
    if re.search(r"(?is)\blimit\b", s) is None:
        s += "\nLIMIT 100"          # ép LIMIT để tránh trả về quá nhiều
    return True, s


# ---------------------------- VALIDATE -------------------------------
def validate(con, sql: str) -> tuple[bool, str]:
    """Parse/EXPLAIN trước khi chạy thật — bắt SQL sai cú pháp/cột không tồn tại."""
    try:
        con.execute("EXPLAIN " + sql)
        return True, "ok"
    except duckdb.Error as e:
        return False, str(e).splitlines()[0][:80]


# ---------------------------- PIPELINE -------------------------------
def ask(con, question: str) -> None:
    print(f"\nQ: {question}")
    sql = MOCK.get(question, "SELECT 1")          # LLM thật: gọi model với schema context
    ok, res = guardrail(sql)                       # 1. guardrail
    if not ok:
        print(f"  🚫 BLOCKED (guardrail): {res}")
        return
    sql = res
    ok, msg = validate(con, sql)                   # 2. validate
    if not ok:
        print(f"  ❌ INVALID SQL: {msg}")
        return
    df = con.execute(sql).fetchdf()                # 3. sandbox execute (read-only views)
    print(f"  ✅ {len(df)} rows:")
    print("    " + df.head(3).to_string(index=False).replace("\n", "\n    "))


def main() -> None:
    con = duckdb.connect(":memory:")               # read-only sandbox: chỉ tạo VIEW từ parquet
    for n in ("customers", "products", "orders", "order_items"):
        con.execute(f"CREATE VIEW {n} AS SELECT * FROM read_parquet('{RAW / (n+'.parquet')}')")
    print("== Text-to-SQL pipeline (schema linking + guardrail + validate + sandbox) ==")
    print("Schema context cho LLM:", SCHEMA.strip()[:60], "...")
    for q in MOCK:
        ask(con, q)
    print("\nDONE ✅ text-to-sql chạy xong — 2 câu độc hại bị guardrail chặn.")


if __name__ == "__main__":
    main()
