"""Hallucination Detection — phát hiện LLM "bịa" bằng 2 phương pháp đo được.

(1) SELF-CONSISTENCY: hỏi N lần, các câu trả lời LỆCH nhau nhiều (cosine thấp) =>
    model đang đoán/bịa (không có kiến thức ổn định). Nhất quán cao => tự tin.
(2) GROUNDING: câu trả lời có bám CONTEXT không (cosine với context). Thấp => bịa
    ngoài nguồn.

Chạy: python projects/06-ai-data-engineering/hallucination_detect.py
(Các "lần trả lời" được mock; cách ĐO bịa là thật.)
"""
from __future__ import annotations

import math
import re
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from rag_over_notes import embed


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def self_consistency(samples: list[str]) -> float:
    """Cosine trung bình giữa mọi cặp câu trả lời. (CẢNH BÁO: đo bề mặt, không đo sự thật.)"""
    vecs = embed(samples)
    pairs = list(combinations(range(len(vecs)), 2))
    return sum(cosine(vecs[i], vecs[j]) for i, j in pairs) / len(pairs)


def fact_consistency(samples: list[str]) -> tuple[bool, set]:
    """So FACT (ở đây: năm 4 chữ số). Các lần trả lời mâu thuẫn FACT = bịa.
    Mạnh hơn cosine vì bắt 'cùng khuôn câu nhưng khác sự thật'."""
    years = set()
    for s in samples:
        years |= set(re.findall(r"\b(?:19|20)\d{2}\b", s))   # năm 4 chữ số
    consistent = len(years) <= 1          # 0 hoặc 1 năm = không mâu thuẫn
    return consistent, years


# Câu CHẮC CHẮN: hỏi N lần -> paraphrase cùng 1 ý (nhất quán cao)
GROUNDED_Q = "Idempotency trong pipeline là gì?"
GROUNDED_SAMPLES = [
    "Idempotency nghĩa là chạy lại pipeline không tạo dữ liệu trùng lặp.",
    "Idempotent là chạy nhiều lần vẫn cho cùng kết quả, không nhân đôi bản ghi.",
    "Tính idempotent giúp retry an toàn, dữ liệu không bị trùng khi chạy lại.",
]

# Câu BỊA: model không biết -> mỗi lần đoán một kiểu (lệch nhau)
HALLUC_Q = "DuckDB phát hành phiên bản đầu tiên vào năm nào và do ai?"
HALLUC_SAMPLES = [
    "DuckDB ra mắt năm 2019 bởi nhóm nghiên cứu CWI ở Hà Lan.",
    "Phiên bản đầu của DuckDB xuất hiện khoảng 2015 từ một startup ở Mỹ.",
    "DuckDB được phát hành lần đầu năm 2021 trong một dự án đại học Đức.",
]

# Grounding: câu trả lời có bám context không
CONTEXT = "Parquet lưu dữ liệu theo cột, nén tốt, hỗ trợ predicate pushdown nên đọc nhanh."
ANSWER_GROUNDED = "Parquet nhanh vì lưu theo cột và nén, chỉ đọc cột cần."
ANSWER_HALLUC = "Parquet nhanh vì nó dùng GPU và chạy trên blockchain phân tán."


def main() -> None:
    print("== Hallucination Detection ==\n")

    print("  -- (1a) Self-consistency bằng COSINE (đo bề mặt) --")
    c_ok = self_consistency(GROUNDED_SAMPLES)
    c_bad = self_consistency(HALLUC_SAMPLES)
    print(f"  câu CHẮC CHẮN  cosine={c_ok:.3f}")
    print(f"  câu BỊA       cosine={c_bad:.3f}")
    print(f"  ⚠️ NGHỊCH LÝ: câu BỊA cosine CAO HƠN! Vì 3 câu bịa cùng KHUÔN ('...ra mắt năm X bởi Y'),")
    print("     chỉ khác năm -> cosine cao dù MÂU THUẪN sự thật. Cosine đo bề mặt, KHÔNG đo đúng/sai.")

    print("\n  -- (1b) Self-consistency bằng FACT (đo sự thật) — đúng cách --")
    ok_c, ok_y = fact_consistency(GROUNDED_SAMPLES)
    bad_c, bad_y = fact_consistency(HALLUC_SAMPLES)
    print(f"  câu CHẮC CHẮN  năm trích={ok_y or '{}'} -> {'OK (không mâu thuẫn)' if ok_c else '⚠️ mâu thuẫn'}")
    print(f"  câu BỊA       năm trích={bad_y} -> {'OK' if bad_c else '⚠️ NGHI BỊA (năm mâu thuẫn nhau!)'}")

    print("\n  -- (2) Grounding (câu trả lời bám context?) --")
    cv = embed([CONTEXT])[0]
    g_ok = cosine(cv, embed([ANSWER_GROUNDED])[0])
    g_bad = cosine(cv, embed([ANSWER_HALLUC])[0])
    GT = 0.70
    print(f"  trả lời ĐÚNG context  grounding={g_ok:.3f} -> {'OK bám nguồn' if g_ok >= GT else '⚠️ ngoài nguồn'}")
    print(f"  trả lời BỊA (GPU/blockchain) grounding={g_bad:.3f} -> {'OK' if g_bad >= GT else '⚠️ NGOÀI NGUỒN (bịa)'}")

    print("\n  Kết hợp: nhất quán THẤP hoặc grounding THẤP -> cờ 'có thể bịa' -> fallback/'tôi không chắc'.")
    print("  (Thực tế còn: NLI/entailment, citation check, LLM-judge — [[ad02-llm-judge]].)")
    print("\nDONE ✅ hallucination detection: self-consistency + grounding đo được.")


if __name__ == "__main__":
    main()
