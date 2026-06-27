"""RAG Eval Harness — so sánh nhiều CẤU HÌNH retrieval bằng số (không "vibe check").

Chọn chunk size / hybrid on-off / k bằng METRIC, không cảm tính. Tái dùng capstone
(rag_over_notes): cùng golden set, sweep config, in bảng recall@k / MRR / nDCG.

Chạy: python projects/06-ai-data-engineering/rag_eval_harness.py
(Cần index đã build: chạy rag_over_notes.py trước, hoặc harness tự build.)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, GOLDEN, build_index, search


def dcg(rels: list[int]) -> float:
    return sum(r / math.log2(i + 1) for i, r in enumerate(rels, 1))


def metrics(con, k: int, hybrid: bool) -> dict:
    rc, rr, nd = [], [], []
    for q, expect in GOLDEN:
        df = search(con, q, k=k, hybrid=hybrid)
        rels = [1 if expect in n.lower() else 0 for n in df["note"].tolist()]
        rc.append(1 if any(rels) else 0)
        rr.append(next((1.0 / i for i, r in enumerate(rels, 1) if r), 0.0))
        idcg = dcg(sorted(rels, reverse=True))   # ideal: mọi relevant dồn lên đầu
        nd.append(dcg(rels) / idcg if idcg else 0.0)   # nDCG chuẩn hoá ∈ [0,1]
    n = len(GOLDEN)
    return {"recall": sum(rc) / n, "mrr": sum(rr) / n, "ndcg": sum(nd) / n}


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    build_index(con)                       # đảm bảo index sẵn sàng + load vss

    print("== RAG Eval Harness — sweep cấu hình trên golden set ==")
    print(f"  golden: {len(GOLDEN)} câu hỏi\n")
    print(f"  {'config':28s} {'recall@k':>9s} {'MRR':>7s} {'nDCG':>7s}")
    configs = [
        ("hybrid, k=3", 3, True),
        ("hybrid, k=5", 5, True),
        ("hybrid, k=10", 10, True),
        ("vector-only, k=5", 5, False),
    ]
    rows = []
    for name, k, hyb in configs:
        m = metrics(con, k, hyb)
        rows.append((name, m))
        print(f"  {name:28s} {m['recall']:>8.0%} {m['mrr']:>7.3f} {m['ndcg']:>7.3f}")

    # chọn cấu hình tốt nhất theo nDCG (cân cả hit lẫn thứ hạng)
    best = max(rows, key=lambda r: r[1]["ndcg"])
    print(f"\n  -> Tốt nhất theo nDCG: '{best[0]}' (nDCG={best[1]['ndcg']:.3f})")
    print("  Nhận xét: k lớn -> recall tăng nhưng MRR/nDCG có thể giảm (đúng tụt hạng);")
    print("            hybrid thường >= vector-only nhờ bắt cả từ khoá.")
    print("\nDONE ✅ eval harness chạy xong — chọn config bằng SỐ.")


if __name__ == "__main__":
    main()
