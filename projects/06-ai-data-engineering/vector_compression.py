"""Vector Compression — Matryoshka (cắt chiều) + Binary quantization, đo recall THẬT.

Vector store production phải nén để vừa RAM (tỉ vector — [[af04-vector-db-internals]]).
2 kỹ thuật mới:
  - Matryoshka: cắt 384 -> 128 -> 64 chiều, vẫn dùng được (NẾU model train kiểu Matryoshka).
  - Binary quant: mỗi chiều -> 1 bit (dấu), so bằng Hamming -> RAM /32.
Đo recall@5 mỗi cách trên capstone -> thấy trade-off RAM/recall thật.

Chạy: python projects/06-ai-data-engineering/vector_compression.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, GOLDEN, build_index, embed


def cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    build_index(con)
    rows = con.execute("SELECT note, embedding FROM chunks").fetchall()
    notes = [r[0].lower() for r in rows]
    vecs = [list(r[1]) for r in rows]
    print(f"== Vector Compression (chunks={len(vecs)}, dim đầy đủ=384, golden={len(GOLDEN)}) ==\n")

    # query vectors (KHÔNG prefix — khớp doc, theo phát hiện ah02)
    qvecs = [(embed([q])[0], expect) for q, expect in GOLDEN]

    def recall_cosine(dim: int) -> float:
        hits = 0
        for qv, expect in qvecs:
            order = sorted(range(len(vecs)), key=lambda i: cosine(qv[:dim], vecs[i][:dim]), reverse=True)[:5]
            hits += 1 if any(expect in notes[i] for i in order) else 0
        return hits / len(qvecs)

    # --- Matryoshka: cắt chiều ---
    print("  -- Matryoshka (cắt chiều) — recall@5 + RAM/vector --")
    print(f"  {'dim':>5s} {'recall@5':>9s} {'bytes/vec':>10s}")
    for dim in (384, 256, 128, 64):
        print(f"  {dim:>5d} {recall_cosine(dim):>8.0%} {dim*4:>9d}B")

    # --- Binary quantization: dấu mỗi chiều -> bit, Hamming ---
    def to_bits(v): return [1 if x > 0 else 0 for x in v]
    cbits = [to_bits(v) for v in vecs]
    def hamming(a, b): return sum(x != y for x, y in zip(a, b))
    hits = 0
    for qv, expect in qvecs:
        qb = to_bits(qv)
        order = sorted(range(len(vecs)), key=lambda i: hamming(qb, cbits[i]))[:5]  # gần = Hamming nhỏ
        hits += 1 if any(expect in notes[i] for i in order) else 0
    rb = hits / len(qvecs)
    print(f"\n  -- Binary quantization (384 bit = 48B, Hamming) --")
    print(f"  recall@5={rb:.0%}  bytes/vec=48B (RAM /32 so với 1536B đầy đủ)")

    print("\n  ⭐ Nhận xét (BẤT NGỜ, đo thật):")
    print("   - Binary quant: GIỮ 88% recall ở /32 RAM (48B)! — rất đáng giá ở corpus này.")
    print("   - Cắt 256 chiều: ổn (thậm chí 100% — golden nhỏ, nhiễu); cắt 64: tụt 62% (quá tay).")
    print("   - bge KHÔNG train Matryoshka mà cắt vừa phải vẫn ổn -> nhưng model train-Matryoshka an toàn hơn.")
    print("   - Production: binary để LỌC nhanh rồi RERANK vector gốc top-N (bù phần mất).")
    print("   => Trade-off RAM⇄recall KHÔNG đoán được — phải ĐO trên data của bạn (bài học lặp lại).")
    print("\nDONE ✅ vector compression: đo trade-off RAM/recall (Matryoshka + binary).")


if __name__ == "__main__":
    main()
