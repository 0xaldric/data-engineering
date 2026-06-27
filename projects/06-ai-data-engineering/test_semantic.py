"""Testing dữ liệu Non-deterministic — semantic equivalence test cho output LLM.

Vấn đề: output LLM cùng input có thể KHÁC CHỮ mỗi lần → exact-match test (như ETL) vô dụng.
Giải: so TƯƠNG ĐƯƠNG NGỮ NGHĨA bằng cosine của embedding (khác chữ cùng nghĩa -> pass;
khác nghĩa -> fail). Cộng với schema/format validation.

Chạy: python projects/06-ai-data-engineering/test_semantic.py
(Dùng fastembed local — không cần API key.)
"""
from __future__ import annotations

import json

_embedder = None
THRESHOLD = 0.80   # cosine >= ngưỡng -> coi là tương đương ngữ nghĩa


def get_embedder():
    global _embedder
    if _embedder is None:
        from fastembed import TextEmbedding
        _embedder = TextEmbedding("BAAI/bge-small-en-v1.5")
    return _embedder


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def embed_all(texts: list[str]) -> list[list[float]]:
    return [v.tolist() for v in get_embedder().embed(texts)]


# --------------------------- Test 1: semantic equivalence ------------
# (reference đúng, candidate output của LLM, có nên coi là tương đương?)
SEMANTIC_CASES = [
    ("Shuffle đắt vì tốn network I/O và ghi đĩa giữa các stage",
     "Shuffle tốn kém do phải truyền dữ liệu qua mạng và ghi tạm ra đĩa", True),
    ("Idempotency nghĩa là chạy lại nhiều lần vẫn ra cùng kết quả",
     "Một thao tác idempotent thì thực thi lặp lại không làm thay đổi kết quả", True),
    ("SCD Type 2 giữ lịch sử bằng cách thêm dòng phiên bản mới",
     "Spark dùng lazy evaluation, transformation không chạy ngay", False),   # khác nghĩa
    ("Partition pruning giúp đọc ít dữ liệu hơn",
     "Nhờ partition pruning, query chỉ quét các partition cần thiết", True),
    ("Kafka đảm bảo thứ tự trong một partition",
     "Exactly-once cần idempotent producer và transaction", False),          # khác nghĩa
]


def test_semantic_equivalence() -> tuple[int, int]:
    refs = [c[0] for c in SEMANTIC_CASES]
    cands = [c[1] for c in SEMANTIC_CASES]
    rv, cv = embed_all(refs), embed_all(cands)
    print("== Test 1: Semantic equivalence (cosine >= %.2f) ==" % THRESHOLD)
    passed = 0
    for (ref, cand, expect), a, b in zip(SEMANTIC_CASES, rv, cv):
        sim = cosine(a, b)
        is_equal = sim >= THRESHOLD
        ok = (is_equal == expect)
        passed += ok
        exact = (ref.strip() == cand.strip())   # exact-match để so sánh
        print(f"  [{'PASS' if ok else 'FAIL'}] cos={sim:.3f} equal={is_equal} expect={expect} "
              f"(exact-match={'T' if exact else 'F'}) :: {cand[:38]}")
    print(f"  -> {passed}/{len(SEMANTIC_CASES)} đúng. (Lưu ý: exact-match=F hết -> ETL test thường THẤT BẠI)")
    return passed, len(SEMANTIC_CASES)


# --------------------------- Test 2: structured output validation ----
def test_schema_validation() -> tuple[int, int]:
    """Output LLM dạng JSON: kiểm format/schema (deterministic phần này)."""
    from pydantic import BaseModel, ValidationError

    class Label(BaseModel):
        category: str
        confidence: float

    cases = [
        ('{"category":"billing","confidence":0.9}', True),
        ('{"category":"billing","confidence":1.5}', False),   # confidence > 1
        ('{"category":"billing"}', False),                    # thiếu field
        ('not a json', False),
    ]
    print("\n== Test 2: Schema/format validation (output có cấu trúc) ==")
    passed = 0
    for raw, expect_valid in cases:
        try:
            d = json.loads(raw)
            Label(**d)
            if not (0 <= d.get("confidence", -1) <= 1):
                raise ValueError("confidence out of range")
            valid = True
        except (json.JSONDecodeError, ValidationError, ValueError):
            valid = False
        ok = (valid == expect_valid)
        passed += ok
        print(f"  [{'PASS' if ok else 'FAIL'}] valid={valid} expect={expect_valid} :: {raw[:40]}")
    print(f"  -> {passed}/{len(cases)} đúng.")
    return passed, len(cases)


def main() -> None:
    p1, t1 = test_semantic_equivalence()
    p2, t2 = test_schema_validation()
    total_p, total_t = p1 + p2, t1 + t2
    print(f"\n== TỔNG: {total_p}/{total_t} test PASS ==")
    print("Bài học: dữ liệu LLM cần test NGỮ NGHĨA (cosine) + SCHEMA, không exact-match.")
    print("\nDONE ✅ semantic/non-deterministic testing chạy xong.")
    assert total_p == total_t, "có test FAIL!"


if __name__ == "__main__":
    main()
