"""File formats benchmark — CSV vs Parquet (size, read speed, column pruning, codecs).

Chạy: python projects/02-python-de/03_formats_benchmark.py

Nhân bản order_items lên ~1.2M hàng để khác biệt đủ rõ, rồi ghi ra nhiều
định dạng và đo: dung lượng, thời gian đọc full, đọc-một-cột (columnar
pruning), predicate pushdown, và so các codec nén của Parquet.
"""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed" / "bench"
OUT.mkdir(parents=True, exist_ok=True)

REPLICATE = 40  # 30k * 40 ≈ 1.2M hàng


def mb(path: Path) -> float:
    return path.stat().st_size / 1e6


def timeit(fn, runs: int = 5) -> float:
    best = float("inf")
    for _ in range(runs):
        t0 = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best * 1000  # ms


def main() -> None:
    base = pd.read_parquet(RAW / "order_items.parquet")
    df = pd.concat([base] * REPLICATE, ignore_index=True)
    print(f"Benchmark dataframe: {len(df):,} hàng x {df.shape[1]} cột\n")

    # --- Ghi ra các định dạng + đo dung lượng ------------------------
    paths = {
        "csv":              OUT / "items.csv",
        "parquet-snappy":   OUT / "items_snappy.parquet",
        "parquet-zstd":     OUT / "items_zstd.parquet",
        "parquet-gzip":     OUT / "items_gzip.parquet",
        "parquet-none":     OUT / "items_none.parquet",
    }
    df.to_csv(paths["csv"], index=False)
    df.to_parquet(paths["parquet-snappy"], compression="snappy", index=False)
    df.to_parquet(paths["parquet-zstd"], compression="zstd", index=False)
    df.to_parquet(paths["parquet-gzip"], compression="gzip", index=False)
    df.to_parquet(paths["parquet-none"], compression=None, index=False)

    csv_mb = mb(paths["csv"])
    print("== Dung lượng file ==")
    print(f"{'format':20s} {'size MB':>9s} {'vs CSV':>8s}")
    for name, p in paths.items():
        print(f"{name:20s} {mb(p):>9.2f} {mb(p)/csv_mb:>7.2f}x")

    # --- Thời gian đọc FULL: CSV vs Parquet --------------------------
    print("\n== Đọc FULL (tất cả cột) ==")
    pq_path = paths["parquet-snappy"]
    t_csv = timeit(lambda: pd.read_csv(paths["csv"]))
    t_pq = timeit(lambda: pd.read_parquet(pq_path))
    print(f"{'read csv':28s} {t_csv:>9.1f} ms")
    print(f"{'read parquet (snappy)':28s} {t_pq:>9.1f} ms   -> nhanh hơn {t_csv/t_pq:.1f}x")

    # --- Column pruning: chỉ đọc 1 cột -------------------------------
    print("\n== Đọc 1 cột (line_total) — columnar pruning ==")
    t_csv_col = timeit(lambda: pd.read_csv(paths["csv"], usecols=["line_total"]))
    t_pq_col = timeit(lambda: pd.read_parquet(pq_path, columns=["line_total"]))
    print(f"{'csv usecols':28s} {t_csv_col:>9.1f} ms  (vẫn phải quét cả file)")
    print(f"{'parquet columns=':28s} {t_pq_col:>9.1f} ms  -> nhanh hơn {t_csv_col/t_pq_col:.1f}x")
    print(f"   Parquet đọc 1 cột nhanh hơn đọc full {t_pq/t_pq_col:.1f}x; CSV gần như không đổi"
          f" ({t_csv/t_csv_col:.1f}x).")

    # --- Predicate pushdown: filter ngay khi đọc ---------------------
    print("\n== Predicate pushdown (filter discount > 0.1 khi đọc) ==")
    def pushdown():
        return pq.read_table(pq_path, columns=["line_total", "discount"],
                             filters=[("discount", ">", 0.1)]).num_rows
    n = pushdown()
    t_push = timeit(pushdown)
    print(f"đọc kèm filter -> {n:,} hàng khớp, {t_push:.1f} ms (bỏ qua row group không khớp)")

    # --- Metadata: row groups -----------------------------------------
    print("\n== Parquet metadata (row groups) ==")
    meta = pq.ParquetFile(pq_path).metadata
    print(f"row_groups={meta.num_row_groups}  rows={meta.num_rows:,}  cols={meta.num_columns}")

    print("\nDONE ✅ formats benchmark chạy xong.")


if __name__ == "__main__":
    main()
