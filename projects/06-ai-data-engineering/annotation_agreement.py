"""Annotation Agreement — đo độ ĐỒNG THUẬN giữa người gán nhãn (Cohen's kappa).

Data nhãn (preference/category) chỉ tốt khi annotator NHẤT QUÁN. Kappa đo đồng thuận
ĐÃ TRỪ may rủi (khác accuracy thô). Kappa thấp = guideline mơ hồ / annotator ẩu/lệch.
Code: 3 annotator gán nhãn 12 mẫu, tính kappa từng cặp + vs gold -> phát hiện annotator lệch.

Chạy: python projects/06-ai-data-engineering/annotation_agreement.py
(Heuristic thuần, deterministic. Tư duy QC nhãn là thật.)
"""
from __future__ import annotations

from collections import Counter

# 12 mẫu, nhãn ∈ {bil, tec, acc}. gold = nhãn "đúng" (tham chiếu).
GOLD = ["bil", "tec", "acc", "bil", "tec", "acc", "bil", "tec", "acc", "bil", "tec", "acc"]
# A: cẩn thận (lệch gold 1/12)
A    = ["bil", "tec", "acc", "bil", "tec", "acc", "bil", "tec", "tec", "bil", "tec", "acc"]
# B: ổn (lệch gold 2/12)
B    = ["bil", "tec", "acc", "bil", "acc", "acc", "bil", "tec", "acc", "bil", "tec", "bil"]
# C: LƯỜI/LỆCH — gán "bil" mọi mẫu (label bias)
C    = ["bil"] * 12


def cohen_kappa(x: list[str], y: list[str]) -> float:
    n = len(x)
    po = sum(1 for a, b in zip(x, y) if a == b) / n        # đồng thuận quan sát
    cx, cy = Counter(x), Counter(y)
    cats = set(x) | set(y)
    pe = sum((cx[c] / n) * (cy[c] / n) for c in cats)       # đồng thuận do MAY RỦI
    return (po - pe) / (1 - pe) if pe < 1 else 1.0          # trừ may rủi


def label(k: float) -> str:
    # thang Landis-Koch
    if k < 0.2: return "kém (poor)"
    if k < 0.4: return "tạm (fair)"
    if k < 0.6: return "khá (moderate)"
    if k < 0.8: return "tốt (substantial)"
    return "rất tốt (almost perfect)"


def main() -> None:
    print("== Annotation Agreement (Cohen's kappa, 12 mẫu, 3 annotator) ==\n")
    anns = {"A": A, "B": B, "C": C}

    print("  -- Đồng thuận từng cặp (kappa) --")
    for i, j in [("A", "B"), ("A", "C"), ("B", "C")]:
        k = cohen_kappa(anns[i], anns[j])
        print(f"  {i} ↔ {j}: kappa={k:+.2f}  ({label(k)})")

    print("\n  -- So với GOLD (annotator nào đáng tin) --")
    for name, ann in anns.items():
        k = cohen_kappa(GOLD, ann)
        acc = sum(1 for g, a in zip(GOLD, ann) if g == a) / len(GOLD)
        print(f"  {name} vs gold: kappa={k:+.2f} ({label(k)}) | accuracy thô={acc:.0%}")

    # phát hiện annotator lệch: kappa trung bình với người khác thấp
    avg = {}
    for name in anns:
        ks = [cohen_kappa(anns[name], anns[o]) for o in anns if o != name]
        avg[name] = sum(ks) / len(ks)
    worst = min(avg, key=avg.get)
    print(f"\n  ⚠️ Annotator LỆCH nhất: '{worst}' (kappa TB với người khác={avg[worst]:+.2f})")
    print(f"     -> C gán 'bil' mọi mẫu (label bias): accuracy thô 33% nhưng kappa ~0 (= may rủi).")
    print("  ⭐ Bài học: accuracy THÔ đánh lừa (C 'đúng' 33% nhờ đoán bừa); kappa TRỪ may rủi -> lộ ẩu.")
    print("  Hành động: loại/đào tạo lại C, làm rõ guideline, thêm gold question.")
    print("\nDONE ✅ annotation agreement: kappa lộ annotator ẩu/lệch mà accuracy thô giấu.")


if __name__ == "__main__":
    main()
