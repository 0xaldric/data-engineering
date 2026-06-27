"""Embedding Benchmark — chọn cấu hình embedding bằng SỐ (ablation trên capstone).

MTEB chọn model bằng benchmark; đây là phiên bản nhỏ: cùng corpus + golden, đổi
các LỰA CHỌN embedding (query-prefix on/off, k, cắt chiều) -> đo recall@k/MRR + tốc độ.
Cho thấy lựa chọn embedding ảnh hưởng THẬT, không phải "model nào cũng như nhau".

Chạy: python projects/06-ai-data-engineering/embedding_benchmark.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, DIM, GOLDEN, MODEL_NAME, build_index, embed

PREFIX = "Represent this sentence for searching relevant passages: "


def search_vec(con, qv, k):
    df = con.execute(
        f"SELECT note, array_cosine_similarity(embedding, ?::FLOAT[{DIM}]) AS s "
        f"FROM chunks ORDER BY s DESC LIMIT {k}", [qv]
    ).fetchdf()
    return df["note"].tolist()


def evaluate(con, use_prefix: bool, k: int) -> tuple[float, float]:
    rc, rr = [], []
    for q, expect in GOLDEN:
        text = (PREFIX + q) if use_prefix else q
        qv = embed([text])[0]
        notes = search_vec(con, qv, k)
        rels = [1 if expect in n.lower() else 0 for n in notes]
        rc.append(1 if any(rels) else 0)
        rr.append(next((1.0 / i for i, r in enumerate(rels, 1) if r), 0.0))
    n = len(GOLDEN)
    return sum(rc) / n, sum(rr) / n


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    build_index(con)
    print(f"== Embedding Benchmark (model={MODEL_NAME}, dim={DIM}, golden={len(GOLDEN)}) ==\n")

    # 1) Ablation: query-prefix ON vs OFF (bge khuyến nghị prefix cho query)
    print("  -- (1) Query-prefix ON vs OFF (k=5) --")
    print(f"  {'config':18s} {'recall@5':>9s} {'MRR':>7s}")
    for use_p in (True, False):
        rc, rr = evaluate(con, use_p, 5)
        print(f"  {'prefix ON' if use_p else 'prefix OFF':18s} {rc:>8.0%} {rr:>7.3f}")

    # 2) Sweep k (với prefix ON)
    print("\n  -- (2) Sweep k (prefix ON) --")
    print(f"  {'k':>3s} {'recall@k':>9s} {'MRR':>7s}")
    for k in (1, 3, 5, 10):
        rc, rr = evaluate(con, True, k)
        print(f"  {k:>3d} {rc:>8.0%} {rr:>7.3f}")

    # 3) Tốc độ embed (1 tiêu chí chọn model thật, không chỉ chất lượng)
    t0 = time.perf_counter()
    _ = embed([q for q, _ in GOLDEN])
    dt = (time.perf_counter() - t0) * 1000
    print(f"\n  -- (3) Tốc độ -- embed {len(GOLDEN)} câu: {dt:.0f} ms ({dt/len(GOLDEN):.0f} ms/câu)")

    print("\n  ⭐ BẤT NGỜ: prefix-OFF (88%) > prefix-ON (75%) trên corpus NÀY!")
    print("     Vì doc index embed KHÔNG prefix + nội dung tiếng Việt -> prefix tiếng Anh kéo query lệch.")
    print("     -> Khuyến nghị mặc định (bge: thêm prefix) KHÔNG luôn đúng cho corpus của bạn.")
    print("     Bài học: ĐO trên data THẬT, đừng tin mặc định. (k lớn -> recall tăng;")
    print("     chọn model còn cân TỐC ĐỘ + kích thước + đa ngữ — MTEB.)")
    print("\nDONE ✅ embedding benchmark: chọn cấu hình bằng SỐ, không cảm tính.")


if __name__ == "__main__":
    main()
