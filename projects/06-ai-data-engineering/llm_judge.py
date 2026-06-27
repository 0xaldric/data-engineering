"""LLM-as-Judge — chấm điểm câu trả lời TỰ ĐỘNG bằng rubric (thay người).

Mock-judge (không API): grounding = cosine với reference; coverage = từ khoá bắt buộc;
penalty độ dài. Demo: pointwise (chấm 1 câu), pairwise (so 2 câu), và 2 BIAS kinh điển
của judge — length bias (dài hơn ăn điểm oan) + position bias (đổi chỗ phải bất biến).

Chạy: python projects/06-ai-data-engineering/llm_judge.py
(Cosine local thay cho 'LLM rubric'. Tư duy eval là thật; bias là thật.)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from rag_over_notes import embed


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


QUESTION = "Vì sao cần idempotency trong data pipeline?"
REFERENCE = ("Idempotency để chạy lại pipeline (retry/backfill) không tạo dữ liệu trùng "
             "hay sai; cùng input cho cùng kết quả, an toàn khi lỗi giữa chừng.")
MUST_HAVE = ["chạy lại", "trùng", "retry", "backfill"]

# 2 câu trả lời ứng viên
ANS_GOOD = ("Vì pipeline hay phải chạy lại khi lỗi hoặc backfill; idempotency đảm bảo "
            "retry không tạo bản ghi trùng, cùng input ra cùng kết quả.")
ANS_VERBOSE = ("Nói chung trong thế giới dữ liệu hiện đại ngày nay thì có rất nhiều điều "
               "quan trọng và idempotency cũng là một trong những điều mà chúng ta nên "
               "quan tâm bởi vì nó liên quan đến việc chạy lại và nhiều thứ khác nữa.")


def score(answer: str, reference: str, must_have: list[str]) -> dict:
    av, rv = embed([answer, reference])
    grounding = cosine(av, rv)                                  # bám ý reference
    coverage = sum(1 for k in must_have if k.lower() in answer.lower()) / len(must_have)
    raw = 0.6 * grounding + 0.4 * coverage                      # rubric tổng hợp
    return {"grounding": grounding, "coverage": coverage, "score": raw, "len": len(answer.split())}


def main() -> None:
    print("== LLM-as-Judge (mock, rubric) ==")
    print(f"  Q: {QUESTION}\n")

    g = score(ANS_GOOD, REFERENCE, MUST_HAVE)
    v = score(ANS_VERBOSE, REFERENCE, MUST_HAVE)
    print("  -- Pointwise --")
    print(f"  GOOD    grounding={g['grounding']:.3f} coverage={g['coverage']:.0%} -> score {g['score']:.3f} ({g['len']} từ)")
    print(f"  VERBOSE grounding={v['grounding']:.3f} coverage={v['coverage']:.0%} -> score {v['score']:.3f} ({v['len']} từ)")

    # -- Pairwise: ai thắng --
    winner = "GOOD" if g["score"] >= v["score"] else "VERBOSE"
    print(f"\n  -- Pairwise --  Winner = {winner} "
          f"(GOOD {g['score']:.3f} vs VERBOSE {v['score']:.3f})")

    # -- BIAS 1: length bias --  câu dài lê thê KHÔNG được thắng nhờ dài
    print("\n  -- Bias check --")
    if v["len"] > g["len"] and v["score"] < g["score"]:
        print(f"  [length] VERBOSE dài hơn ({v['len']}>{g['len']} từ) nhưng điểm THẤP hơn -> rubric không thiên vị độ dài ✓")
    else:
        print(f"  [length] ⚠️ cảnh báo: câu dài đang ăn điểm oan -> cần length-control")

    # -- BIAS 2: position bias --  đổi thứ tự A/B điểm phải bất biến
    g2 = score(ANS_GOOD, REFERENCE, MUST_HAVE)
    consistent = abs(g2["score"] - g["score"]) < 1e-9
    print(f"  [position] đổi chỗ A/B -> điểm GOOD bất biến ({consistent}) "
          f"-> mock-judge ổn định; LLM-judge THẬT phải test swap (hay thiên vị vị trí đầu)")

    print("\n  Lưu ý: judge THẬT (LLM) còn self-preference (thích văn của chính model),")
    print("  -> luôn CALIBRATE với nhãn người + test swap + kiểm soát độ dài ([[aa06-llm-eval]]).")
    print("\nDONE ✅ LLM-as-judge: chấm tự động + soi bias (length/position).")


if __name__ == "__main__":
    main()
