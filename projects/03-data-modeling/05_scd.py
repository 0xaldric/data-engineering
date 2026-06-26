"""Slowly Changing Dimensions — SCD Type 1 / 2 / 3 trên DuckDB.

Chạy: python projects/03-data-modeling/05_scd.py

Kịch bản: khách #1 ('An') chuyển từ Hanoi/VN -> Tokyo/JP vào 2024-01-30.
Áp cùng thay đổi đó theo 3 chiến lược SCD và in kết quả để thấy rõ khác biệt:
  Type 1: ghi đè (mất lịch sử)
  Type 2: versioning (giữ toàn bộ lịch sử) — chuẩn vàng của warehouse
  Type 3: lưu 1 giá trị trước (previous)
"""
from __future__ import annotations

import duckdb

con = duckdb.connect(":memory:")
INIT_DATE, CHANGE_DATE = "2024-01-01", "2024-01-30"

SRC_V1 = [(1, "An", "Hanoi", "VN"), (2, "Binh", "Hue", "VN"), (3, "Chi", "Danang", "VN")]
SRC_V2 = [(1, "An", "Tokyo", "JP"), (2, "Binh", "Hue", "VN"), (3, "Chi", "Danang", "VN")]


def section(t: str) -> None:
    print(f"\n{'=' * 60}\n{t}\n{'=' * 60}")


def setup_sources() -> None:
    for v, rows in (("src_v1", SRC_V1), ("src_v2", SRC_V2)):
        con.execute(f"CREATE TABLE {v}(customer_id INT, name VARCHAR, city VARCHAR, country VARCHAR)")
        con.executemany(f"INSERT INTO {v} VALUES (?,?,?,?)", rows)


def scd_type1() -> None:
    section("SCD Type 1 — OVERWRITE (mất lịch sử)")
    con.execute("CREATE TABLE dim_scd1 AS SELECT * FROM src_v1")
    # reload: ghi đè trực tiếp giá trị mới
    con.execute("""UPDATE dim_scd1 d SET city = s.city, country = s.country
                   FROM src_v2 s WHERE s.customer_id = d.customer_id""")
    print(con.execute("SELECT * FROM dim_scd1 WHERE customer_id = 1").fetchdf().to_string(index=False))
    print("→ Chỉ thấy Tokyo/JP. KHÔNG biết trước đó khách ở đâu (lịch sử mất).")


def scd_type2() -> None:
    section("SCD Type 2 — VERSIONING (giữ toàn bộ lịch sử) ⭐")
    con.execute("CREATE SEQUENCE seq_ck START 1")
    # Initial load: mỗi khách 1 phiên bản current
    con.execute(f"""
        CREATE TABLE dim_scd2 AS
        SELECT nextval('seq_ck') AS customer_key, customer_id, name, city, country,
               DATE '{INIT_DATE}' AS effective_from,
               DATE '9999-12-31'  AS effective_to,
               TRUE               AS is_current
        FROM src_v1""")

    # Bước 1: HẾT HẠN phiên bản hiện tại của khách có thay đổi
    con.execute(f"""
        UPDATE dim_scd2 SET effective_to = DATE '{CHANGE_DATE}', is_current = FALSE
        WHERE is_current AND customer_id IN (
            SELECT v2.customer_id FROM src_v2 v2
            JOIN dim_scd2 d ON d.customer_id = v2.customer_id AND d.is_current
            WHERE d.city <> v2.city OR d.country <> v2.country OR d.name <> v2.name)""")

    # Bước 2: CHÈN phiên bản mới cho khách thay đổi (và khách hoàn toàn mới)
    con.execute(f"""
        INSERT INTO dim_scd2
        SELECT nextval('seq_ck'), v2.customer_id, v2.name, v2.city, v2.country,
               DATE '{CHANGE_DATE}', DATE '9999-12-31', TRUE
        FROM src_v2 v2
        WHERE NOT EXISTS (
            SELECT 1 FROM dim_scd2 d WHERE d.customer_id = v2.customer_id AND d.is_current
                     AND d.city = v2.city AND d.country = v2.country AND d.name = v2.name)""")

    print("Lịch sử khách #1 (2 phiên bản):")
    print(con.execute("""SELECT customer_key, city, country, effective_from, effective_to, is_current
                         FROM dim_scd2 WHERE customer_id = 1
                         ORDER BY effective_from""").fetchdf().to_string(index=False))
    print("→ Giữ CẢ Hanoi (hết hạn) lẫn Tokyo (current). Truy được trạng thái tại bất kỳ ngày nào.")
    # Truy vấn 'as-of': khách #1 ở đâu vào 2024-01-15?
    asof = con.execute("""SELECT city, country FROM dim_scd2
        WHERE customer_id=1 AND DATE '2024-01-15' >= effective_from
          AND DATE '2024-01-15' < effective_to""").fetchone()
    print(f"   As-of 2024-01-15: khách #1 ở {asof[0]}/{asof[1]} (đúng = Hanoi/VN).")


def scd_type3() -> None:
    section("SCD Type 3 — PREVIOUS VALUE (lưu đúng 1 giá trị trước)")
    con.execute("""
        CREATE TABLE dim_scd3 AS
        SELECT customer_id, name,
               city    AS city_current,    CAST(NULL AS VARCHAR) AS city_previous,
               country AS country_current, CAST(NULL AS VARCHAR) AS country_previous
        FROM src_v1""")
    con.execute("""
        UPDATE dim_scd3 d SET
            city_previous = d.city_current,       city_current = s.city,
            country_previous = d.country_current, country_current = s.country
        FROM src_v2 s
        WHERE s.customer_id = d.customer_id
          AND (d.city_current <> s.city OR d.country_current <> s.country)""")
    print(con.execute("""SELECT customer_id, city_previous, city_current,
                                country_previous, country_current
                         FROM dim_scd3 WHERE customer_id = 1""").fetchdf().to_string(index=False))
    print("→ Biết 'trước' (Hanoi) và 'hiện tại' (Tokyo), nhưng CHỈ 1 mức — đổi lần nữa là mất Hanoi.")


def main() -> None:
    setup_sources()
    scd_type1()
    scd_type2()
    scd_type3()
    print("\nDONE ✅ SCD Type 1/2/3 demo chạy xong.")


if __name__ == "__main__":
    main()
