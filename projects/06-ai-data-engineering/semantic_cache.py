"""Semantic Cache — cache câu trả lời theo NGỮ NGHĨA, không chỉ exact match.

Câu hỏi mới gần nghĩa câu đã hỏi (cosine >= ngưỡng) -> trả cache, KHỎI gọi LLM
(tiết kiệm tiền/độ trễ — [[ac08-ai-cost-scale]]). Demo: exact hit, semantic hit
(diễn đạt khác), miss, và FALSE-HIT (gần chữ khác ý) -> vì sao ngưỡng phải cao + calibrate.

Chạy: python projects/06-ai-data-engineering/semantic_cache.py
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


class SemanticCache:
    def __init__(self, threshold: float = 0.93):
        self.threshold = threshold
        self.q, self.v, self.a = [], [], []
        self.hits = self.miss = 0

    def put(self, question: str, answer: str):
        self.q.append(question); self.v.append(embed([question])[0]); self.a.append(answer)

    def get(self, question: str):
        qv = embed([question])[0]
        best, bi = 0.0, -1
        for i, cv in enumerate(self.v):
            s = cosine(qv, cv)
            if s > best:
                best, bi = s, i
        if best >= self.threshold:
            self.hits += 1
            return self.a[bi], best, self.q[bi]
        self.miss += 1
        return None, best, (self.q[bi] if bi >= 0 else "-")


def main() -> None:
    cache = SemanticCache(threshold=0.93)
    # seed: câu đã hỏi -> câu trả lời (đã gọi LLM lần đầu)
    cache.put("idempotency trong data pipeline là gì",
              "Chạy lại pipeline không tạo dữ liệu trùng/sai; cùng input ra cùng kết quả.")
    cache.put("vì sao parquet nhanh hơn csv",
              "Parquet lưu theo cột + nén + predicate pushdown nên đọc ít dữ liệu hơn.")

    print("== Semantic Cache (threshold=0.93) ==\n")
    # (label, query, có nên hit không)
    tests = [
        ("EXACT   ", "idempotency trong data pipeline là gì", True),
        ("REWORD  ", "idempotent nghĩa là gì trong pipeline dữ liệu", True),
        ("MISS    ", "cách tối ưu shuffle trong spark", False),
        ("TRICKY  ", "vì sao csv nhanh hơn parquet", False),   # gần chữ, NGƯỢC ý -> không nên hit
    ]
    scores = {}
    for label, q, should_hit in tests:
        ans, score, near = cache.get(q)
        scores[label.strip()] = score
        hit = ans is not None
        flag = "HIT " if hit else "MISS"
        warn = ""
        if hit and not should_hit:
            warn = "  ⚠️ FALSE-HIT (gần chữ khác ý!)"
        if not hit and should_hit:
            warn = "  ⚠️ FALSE-MISS (nên hit mà trượt)"
        print(f"  [{flag}] {label} cos={score:.3f} ~ '{near[:34]}'{warn}")

    total = cache.hits + cache.miss
    print(f"\n  hit rate = {cache.hits}/{total} = {cache.hits/total:.0%} (mỗi hit = 1 lần KHỎI gọi LLM)")
    # ⭐ punchline: cùng-nghĩa lại điểm THẤP hơn ngược-nghĩa -> không ngưỡng nào tách được
    if scores.get("REWORD", 1) < scores.get("TRICKY", 0):
        print(f"  ⭐ NGHỊCH LÝ: REWORD cùng nghĩa ({scores['REWORD']:.3f}) < TRICKY ngược nghĩa ({scores['TRICKY']:.3f})!")
        print("     -> embedding gần bất biến thứ tự từ; cosine ≠ tương đương ngữ nghĩa.")
        print("     -> KHÔNG ngưỡng đơn nào vừa bắt reword vừa loại negation. Đây là GIỚI HẠN THẬT.")
    print("  Lưu ý: ngưỡng THẤP -> nhiều hit nhưng FALSE-HIT (trả sai); CAO -> an toàn mà ít tiết kiệm.")
    print("  -> calibrate ngưỡng trên tập câu thật; nhớ INVALIDATE cache khi KB đổi ([[ac06-kb-freshness]]).")
    print("\nDONE ✅ semantic cache: tiết kiệm LLM call + soi false-hit/ngưỡng.")


if __name__ == "__main__":
    main()
