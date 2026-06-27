"""Synthetic Data Generation — sinh dữ liệu giả (cho train/test khi thiếu data).

Vai trò DE: không chỉ "gọi LLM sinh data" — mà đảm bảo CHẤT LƯỢNG: đa dạng (diversity),
khử trùng (dedup), cân bằng nhãn (balance), lọc rác (quality). Synthetic data tệ → model lệch.

Chạy: python projects/06-ai-data-engineering/synthetic_data.py
(Mock-LLM sinh bằng template-combination — KHÔNG cần API. Logic kiểm soát chất lượng là thật.)
"""
from __future__ import annotations

from collections import Counter
from itertools import product

# Mock-LLM "sinh" ticket bằng tổ hợp template (LLM thật: gọi model với prompt đa dạng).
SUBJECTS = ["Tôi", "Khách hàng", "Bên mình", "Tài khoản của tôi"]
ISSUES = {
    "billing":   ["bị tính phí hai lần", "hóa đơn sai số tiền", "không hoàn tiền"],
    "technical": ["app bị crash", "không export được", "trang load mãi không xong"],
    "account":   ["quên mật khẩu", "không đổi được email", "bị khóa tài khoản"],
}
TAILS = [", mong hỗ trợ.", " rất bực.", ", cần xem gấp.", "."]


def generate() -> list[dict]:
    """Sinh mọi tổ hợp (mô phỏng LLM). Cố ý tạo TRÙNG (nhiều tail giống) để demo dedup."""
    rows = []
    for cat, issues in ISSUES.items():
        for subj, issue, tail in product(SUBJECTS, issues, TAILS):
            rows.append({"text": f"{subj} {issue}{tail}", "category": cat})
    return rows


# ---------------------------- Quality controls -----------------------
def shingles(text: str, k: int = 2) -> set:
    w = text.lower().split()
    return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)} or {text}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if (a | b) else 0.0


def dedup(rows: list[dict], thresh: float = 0.5) -> list[dict]:
    """Khử near-duplicate (Jaccard >= thresh). (Scale lớn dùng MinHash+LSH — [[aa04]].)"""
    kept, kept_sh = [], []
    for r in rows:
        sh = shingles(r["text"])
        if all(jaccard(sh, s) < thresh for s in kept_sh):
            kept.append(r); kept_sh.append(sh)
    return kept


def quality_filter(rows: list[dict]) -> list[dict]:
    """Lọc rác: độ dài hợp lý (không quá ngắn/dài)."""
    return [r for r in rows if 4 <= len(r["text"].split()) <= 30]


def diversity(rows: list[dict]) -> float:
    """Đa dạng = tỉ lệ bigram unique / tổng bigram (thấp = mode collapse, lặp khuôn)."""
    all_sh, uniq = 0, set()
    for r in rows:
        sh = shingles(r["text"])
        all_sh += len(sh); uniq |= sh
    return len(uniq) / all_sh if all_sh else 0.0


def balance(rows: list[dict], per_class: int) -> list[dict]:
    """Cân bằng nhãn: lấy tối đa per_class mỗi category (tránh model lệch về lớp đông)."""
    seen: Counter = Counter()
    out = []
    for r in rows:
        if seen[r["category"]] < per_class:
            out.append(r); seen[r["category"]] += 1
    return out


def main() -> None:
    raw = generate()
    print(f"== Synthetic data generation (mock-LLM) ==")
    print(f"  1. Sinh thô: {len(raw)} records | nhãn: {dict(Counter(r['category'] for r in raw))}")

    q = quality_filter(raw)
    print(f"  2. Quality filter (độ dài): {len(q)} (-{len(raw)-len(q)} rác)")

    d = dedup(q)
    print(f"  3. Dedup (Jaccard>=0.5): {len(d)} (-{len(q)-len(d)} near-dup) | diversity={diversity(d):.2f}")

    per = min(Counter(r["category"] for r in d).values())
    b = balance(d, per)
    print(f"  4. Balance (≤{per}/lớp): {len(b)} | nhãn: {dict(Counter(r['category'] for r in b))}")

    print(f"\n  -> Dataset cuối: {len(b)} records sạch, đa dạng, cân bằng (từ {len(raw)} thô)")
    print("  Mẫu:")
    for r in b[:4]:
        print(f"    [{r['category']:9s}] {r['text']}")
    print("\nDONE ✅ synthetic data pipeline chạy xong (diversity/dedup/balance/quality).")


if __name__ == "__main__":
    main()
