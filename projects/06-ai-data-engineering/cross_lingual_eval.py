"""Cross-lingual RAG eval — đo "khoảng cách đa ngữ" của embedding EN-centric.

Index (rag.duckdb) chứa note TIẾNG VIỆT, embed bằng bge-small (EN-centric).
Bắn cùng câu hỏi ở 2 ngôn ngữ (VI vs EN) -> đo recall@5 mỗi bên -> chênh lệch =
cái giá của việc dùng model EN cho corpus VI. Động lực: model đa ngữ (e5/bge-m3).

Chạy: python projects/06-ai-data-engineering/cross_lingual_eval.py
(Tái dùng index capstone, KHÔNG tải model mới.)
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, build_index, search

# (query_VI, query_EN, expected_note) — cùng ý, 2 ngôn ngữ, cùng doc đúng.
PAIRS = [
    ("vì sao shuffle đắt trong spark",          "why is shuffle expensive in spark",        "shuffle"),
    ("slowly changing dimension giữ lịch sử",   "slowly changing dimension keeping history","scd"),
    ("idempotency pipeline chạy lại không trùng","idempotent pipeline rerun no duplicates",  "pipeline-patterns"),
    ("exactly once trong kafka streaming",       "exactly once in kafka streaming",          "streaming-eos"),
    ("phân vùng và đánh chỉ mục để quét ít hơn", "partitioning and indexing to scan less",   "optimization"),
    ("nén cột parquet đọc nhanh hơn csv",        "parquet columnar reads faster than csv",   "file-formats"),
]


def recall(con, lang: str, k: int = 5) -> float:
    hits = 0
    for vi, en, expect in PAIRS:
        q = vi if lang == "vi" else en
        df = search(con, q, k=k, hybrid=True)
        rels = [1 for n in df["note"].tolist() if expect in n.lower()]
        hit = 1 if rels else 0
        hits += hit
        mark = "✓" if hit else "✗"
        print(f"    [{mark}] ({lang}) {q[:42]:42s} -> {df['note'].iloc[0] if len(df) else '-'}")
    return hits / len(PAIRS)


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    build_index(con)

    print("== Cross-lingual eval: query VI vs EN trên index note tiếng Việt ==\n")
    print("  -- Tiếng Việt (cùng ngôn ngữ với doc) --")
    rv = recall(con, "vi")
    print(f"\n  -- English (cross-lingual, model EN-centric) --")
    re_ = recall(con, "en")

    gap = rv - re_
    print(f"\n  recall@5  VI={rv:.0%}   EN={re_:.0%}   chênh={gap:+.0%}")
    if gap > 0:
        print("  -> EN rớt: model EN-centric map câu hỏi EN và doc VI vào vùng lệch nhau.")
    else:
        print("  -> Sát nhau ở các câu nhiều thuật ngữ chung (kafka/parquet) — token trùng giúp.")
    print("  Khắc phục: dùng embedding ĐA NGỮ (multilingual-e5/bge-m3) hoặc dịch query→ngôn ngữ doc.")
    print("\nDONE ✅ đo xong khoảng cách đa ngữ (định lượng động lực dùng model đa ngữ).")


if __name__ == "__main__":
    main()
