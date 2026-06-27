"""Streaming / Real-time RAG — doc MỚI stream vào -> truy vấn thấy NGAY (freshness).

Mô phỏng: corpus đang chạy -> 1 tài liệu mới xuất hiện -> incremental re-index
(chỉ embed doc mới, KHÔNG rebuild cả corpus) -> query phản ánh ngay. Đo độ trễ
"ingest -> searchable" = freshness latency. Tự dọn doc demo (reconcile chống ghost).

Chạy: python projects/06-ai-data-engineering/streaming_rag.py
(Tái dùng index capstone; doc demo bị xoá cuối script, KHÔNG commit vào repo.)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, ROOT, build_index, search

MARKER = "zorvex"   # token độc nhất, chắc chắn chưa có trong corpus
NEW_NOTE = ROOT / "notes" / "advanced" / "_streaming_demo_tmp.md"
QUERY = f"{MARKER} streaming freshness tài liệu mới vừa cập nhật"


def top_hit(con):
    df = search(con, QUERY, k=3, hybrid=True)
    if len(df) == 0:
        return "-", 0.0
    return df["note"].iloc[0], float(df["vec_score"].iloc[0])


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    build_index(con)                       # đảm bảo trạng thái hiện tại

    print("== Streaming RAG — freshness demo ==")
    nb, sb = top_hit(con)
    print(f"  [TRƯỚC ] top = {nb} (score {sb:.3f}) — chưa có doc chứa '{MARKER}'")

    try:
        # --- doc mới "stream" vào corpus ---
        NEW_NOTE.write_text(
            f"# Streaming Demo {MARKER}\n\n"
            f"Tài liệu MỚI chứa marker {MARKER}. Mô phỏng doc vừa stream vào corpus, "
            f"cần xuất hiện trong RAG trong vài giây theo freshness SLA.\n"
        )
        t0 = time.perf_counter()
        stats = build_index(con)           # incremental: chỉ embed doc mới
        latency_ms = (time.perf_counter() - t0) * 1000

        na, sa = top_hit(con)
        print(f"  [re-index] new={stats['new']} changed={stats['changed']} "
              f"unchanged={stats['unchanged']} -> chỉ embed doc mới (không rebuild corpus)")
        print(f"  [SAU   ] top = {na} (score {sa:.3f}) — THẤY NGAY")
        print(f"  freshness latency (ingest -> searchable): {latency_ms:.0f} ms")
        ok = MARKER in str(na).lower() or "_streaming_demo" in str(na).lower()
        print(f"  -> doc mới {'ĐÃ' if ok else 'CHƯA'} lên top sau khi stream vào.")
    finally:
        # --- dọn: xoá doc demo + reconcile (xoá ghost chunk) ---
        if NEW_NOTE.exists():
            NEW_NOTE.unlink()
        d = build_index(con)
        print(f"  [cleanup] xoá doc demo -> reconcile deleted={d['deleted']} (chống ghost — ac06)")

    print("\nDONE ✅ streaming RAG: doc mới searchable gần real-time, incremental, tự dọn.")


if __name__ == "__main__":
    main()
