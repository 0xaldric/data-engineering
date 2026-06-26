"""Run a .sql file against an in-memory DuckDB, with raw data pre-loaded as views.

Every parquet file in data/raw/ is registered as a view named after the file
(customers, products, orders, order_items), so SQL scripts can query them
directly without boilerplate. Statements are executed in order; the result of
the final SELECT is printed.

Usage:
    python scripts/run_sql.py projects/01-sql-fundamentals/01_basics.sql
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def load_views(con: duckdb.DuckDBPyConnection) -> list[str]:
    names = []
    for pq in sorted(RAW_DIR.glob("*.parquet")):
        name = pq.stem
        con.execute(
            f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_parquet('{pq}')"
        )
        names.append(name)
    return names


def split_statements(sql: str) -> list[str]:
    # Strip '--' to-end-of-line comments BEFORE splitting on ';', so a ';' that
    # appears inside a comment can't break statement boundaries (and full-line
    # comments don't hide the statement that follows them). Good enough for these
    # teaching scripts (assumes no '--' or ';' inside string literals).
    no_comments = "\n".join(line.split("--", 1)[0] for line in sql.splitlines())
    return [s.strip() for s in no_comments.split(";") if s.strip()]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    sql_path = Path(argv[1])
    if not sql_path.exists():
        print(f"File not found: {sql_path}")
        return 1

    con = duckdb.connect(database=":memory:")
    views = load_views(con)
    print(f"Loaded views: {', '.join(views) or '(none — run gen_ecommerce.py first)'}")
    print(f"Running {sql_path} ...\n")

    statements = split_statements(sql_path.read_text())
    last_result = None
    for stmt in statements:
        try:
            cur = con.execute(stmt)
            if cur.description:  # a query that returns rows
                last_result = cur.fetchdf()
        except Exception as exc:  # noqa: BLE001 — teaching tool, surface the error
            print(f"ERROR in statement:\n{stmt[:200]}\n-> {exc}")
            return 1

    if last_result is not None:
        print("Final result (first 20 rows):")
        print(last_result.head(20).to_string(index=False))
    print(f"\nOK — executed {len(statements)} statements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
