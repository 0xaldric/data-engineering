"""Hybrid Fusion — so cách KẾT HỢP vector + keyword: RRF vs weighted vs đơn lẻ.

RRF (Reciprocal Rank Fusion): gộp theo THỨ HẠNG, không gộp điểm -> không cần chuẩn hoá
thang điểm khác nhau (cosine vs BM25). score = sum 1/(C + rank) qua các bảng xếp hạng.
Đo recall@5 mỗi cách trên capstone -> thấy fusion ảnh hưởng thật.

Chạy: python projects/06-ai-data-engineering/rrf_fusion.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, DIM, GOLDEN, build_index, embed

K = 5
C = 60   # hằng số RRF (giảm ảnh hưởng hạng thấp)


def rankings(con, query: str):
    """Trả (rank_vec, rank_kw): dict note -> hạng (1-based) theo vector / keyword."""
    qv = embed([query])[0]
    terms = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]
    kw = " + ".join(f"(lower(text) LIKE '%{t}%')::INT" for t in terms) or "0"
    df = con.execute(
        f"SELECT note, max(array_cosine_similarity(embedding, ?::FLOAT[{DIM}])) AS vec, "
        f"max({kw}) AS kw FROM chunks GROUP BY note", [qv]
    ).fetchdf()
    df["note"] = df["note"].str.split("/").str[-1]
    vec_order = df.sort_values("vec", ascending=False)["note"].tolist()
    kw_df = df[df["kw"] > 0].sort_values("kw", ascending=False)
    kw_order = kw_df["note"].tolist()
    rank_vec = {n: i + 1 for i, n in enumerate(vec_order)}
    rank_kw = {n: i + 1 for i, n in enumerate(kw_order)}
    return rank_vec, rank_kw, df


def topk_recall(order, expect, k=K):
    return 1 if any(expect in n.lower() for n in order[:k]) else 0


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    build_index(con)
    print(f"== Hybrid Fusion (RRF C={C}, k={K}, golden={len(GOLDEN)}) ==\n")

    methods = {"vector-only": 0, "keyword-only": 0, "RRF": 0, "weighted(vec+0.1kw)": 0}
    for q, expect in GOLDEN:
        rv, rk, df = rankings(con, q)
        notes = df["note"].tolist()

        vec_order = sorted(notes, key=lambda n: rv.get(n, 1e9))
        kw_order = [n for n in sorted(notes, key=lambda n: rk.get(n, 1e9)) if n in rk]
        # RRF: gộp THỨ HẠNG
        rrf = sorted(notes, key=lambda n: -(1/(C+rv.get(n, 1e9)) + (1/(C+rk[n]) if n in rk else 0)))
        # weighted: gộp ĐIỂM (cần cùng thang — đây vec[0,1] + 0.1*kw)
        vmap = dict(zip(df["note"], df["vec"])); kmap = dict(zip(df["note"], df["kw"]))
        weighted = sorted(notes, key=lambda n: -(vmap[n] + 0.1*kmap[n]))

        methods["vector-only"] += topk_recall(vec_order, expect)
        methods["keyword-only"] += topk_recall(kw_order, expect)
        methods["RRF"] += topk_recall(rrf, expect)
        methods["weighted(vec+0.1kw)"] += topk_recall(weighted, expect)

    n = len(GOLDEN)
    print(f"  {'method':22s} {'recall@'+str(K):>9s}")
    for m, h in methods.items():
        print(f"  {m:22s} {h/n:>8.0%}")

    print("\n  ⭐ Nhận xét (đo thật trên corpus này):")
    print("   - vector-only đã 100% (embedding tốt, no-prefix); keyword-only yếu (62%, chỉ trùng từ).")
    print("   - weighted(vec+0.1kw) TỤT 88%! keyword nhiễu kéo nhầm note lên (chưa tune α).")
    print("   - RRF giữ 100% -> gộp THỨ HẠNG robust hơn gộp ĐIỂM (không bị 1 tín hiệu nhiễu phá).")
    print("   => RRF không cần chuẩn hoá thang (cosine vs BM25) + bền hơn weighted. Nhưng LUÔN đo:")
    print("      thêm keyword KHÔNG luôn tốt — đúng bài học 'đo, đừng tin mặc định'.")
    print("\nDONE ✅ hybrid fusion: so RRF vs weighted vs đơn lẻ bằng SỐ.")


if __name__ == "__main__":
    main()
