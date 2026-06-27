"""RAG Debugger — chẩn đoán VÌ SAO một query không trả đúng doc.

RAG fail thầm lặng (trả doc sai mà không lỗi). Tool này soi từng bước:
  - doc đúng CÓ trong index không?
  - chunk tốt nhất của doc đúng điểm bao nhiêu?
  - doc đúng xếp hạng MẤY (note-level)?
  - note nào "cướp" top + khoảng cách điểm?
-> ra CHẨN ĐOÁN (not-indexed / điểm thấp / bị rank dưới k / note khác thắng).

Chạy: python projects/06-ai-data-engineering/rag_debugger.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, DIM, build_index, embed

K = 5


def diagnose(con, query: str, expect: str) -> None:
    qv = embed([query])[0]   # KHÔNG prefix (khớp doc — phát hiện ah02)
    df = con.execute(
        f"SELECT note, array_cosine_similarity(embedding, ?::FLOAT[{DIM}]) AS s "
        f"FROM chunks ORDER BY s DESC", [qv]
    ).fetchdf()
    df["short"] = df["note"].str.split("/").str[-1]

    # note-level: điểm tốt nhất mỗi note, xếp hạng
    note_best = (df.groupby("short", as_index=False)["s"].max()
                   .sort_values("s", ascending=False).reset_index(drop=True))
    in_index = df["note"].str.contains(expect, case=False).any()
    exp_rows = note_best[note_best["short"].str.contains(expect, case=False)]
    exp_score = float(exp_rows["s"].iloc[0]) if len(exp_rows) else None
    exp_rank = int(exp_rows.index[0]) + 1 if len(exp_rows) else None
    top_note = note_best["short"].iloc[0]
    top_score = float(note_best["s"].iloc[0])

    print(f"  Q: '{query}'  (mong: *{expect}*)")
    print(f"    top thực tế = {top_note} ({top_score:.3f})")
    if not in_index:
        print(f"    🔴 CHẨN ĐOÁN: doc '{expect}' KHÔNG có trong index -> ingest/chunk thiếu.")
        return
    print(f"    doc đúng: điểm tốt nhất={exp_score:.3f}, xếp hạng note-level=#{exp_rank}")
    if exp_rank <= K:
        print(f"    🟢 OK: doc đúng lọt top-{K} (#{exp_rank}).")
    elif exp_score < 0.5:
        print(f"    🔴 CHẨN ĐOÁN: điểm doc đúng THẤP ({exp_score:.3f}) -> embedding lệch "
              f"(đa ngữ? prefix? chunk tệ?) — xem [[ah02]],[[ac01]].")
    else:
        gap = top_score - exp_score
        print(f"    🟠 CHẨN ĐOÁN: doc đúng bị đẩy xuống #{exp_rank} (ngoài top-{K}); "
              f"'{top_note}' cướp top (gap {gap:.3f}).")
        print(f"       -> tăng k / rerank ([[ae07]]) / hybrid keyword ([[aa03]]) / reformulate ([[ae01]]).")
    print()


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    build_index(con)
    print(f"== RAG Debugger (k={K}) — chẩn đoán query fail ==\n")
    cases = [
        ("slowly changing dimension giữ lịch sử chiều", "scd"),    # nên OK
        ("EOS", "streaming-eos"),                                  # cộc lốc -> có thể fail
        ("zzz marker không tồn tại trong corpus", "khong-co-doc-nay"),  # not indexed
        ("tối ưu", "optimization"),                                # mơ hồ -> bị cướp top?
    ]
    for q, exp in cases:
        diagnose(con, q, exp)
    print("  Quy trình debug RAG: index? -> điểm doc đúng? -> xếp hạng? -> ai cướp top? -> fix đúng tầng.")
    print("\nDONE ✅ rag debugger: chẩn đoán fail theo TẦNG, không đoán mò.")


if __name__ == "__main__":
    main()
