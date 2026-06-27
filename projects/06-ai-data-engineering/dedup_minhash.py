"""Near-duplicate detection bằng MinHash + LSH — chuẩn bị dữ liệu train cho LLM.

Bài toán DE: corpus train có NHIỀU bản gần-trùng (cùng nội dung, sửa nhẹ) → model học lệch,
lãng phí, leakage. So từng cặp = O(n²) bất khả ở tỉ doc. → MinHash (ước lượng Jaccard rẻ)
+ LSH (chỉ so các cặp ỨNG VIÊN). Tự cài (không lib ngoài) để hiểu thuật toán.

Chạy: python projects/06-ai-data-engineering/dedup_minhash.py
"""
from __future__ import annotations

import hashlib
from itertools import combinations

NUM_HASHES = 64           # số hàm hash cho MinHash signature
BANDS, ROWS = 32, 2       # LSH: nhiều band × ít row = NHẠY hơn (bắt near-dup reword). BANDS*ROWS==NUM_HASHES
K = 2                     # shingle = k từ liên tiếp (nhỏ hơn -> near-dup có Jaccard cao hơn)

DOCS = {
    "d1": "spark shuffle is expensive because of network and disk io between stages",
    "d2": "spark shuffle is expensive due to network and disk io between the stages",   # near-dup d1
    "d3": "idempotency means running again gives the same result no duplicates",
    "d4": "running an operation again yields the same result idempotency no duplicates", # near-dup d3
    "d5": "kafka guarantees ordering only within a single partition",
    "d6": "spark shuffle is expensive because of network and disk io between stages",     # EXACT dup d1
    "d7": "data vault uses hubs links and satellites for auditable integration",
}


def shingles(text: str, k: int = K) -> set[str]:
    w = text.lower().split()
    return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)} or {text}


def _h(salt: int, s: str) -> int:
    return int(hashlib.md5(f"{salt}:{s}".encode()).hexdigest(), 16)


def minhash(sh: set[str]) -> list[int]:
    """Signature: với mỗi hàm hash, lấy MIN hash trên tập shingle."""
    return [min(_h(salt, s) for s in sh) for salt in range(NUM_HASHES)]


def lsh_candidates(sigs: dict[str, list[int]]) -> set[tuple[str, str]]:
    """LSH: chia signature thành band; doc cùng (band, bucket) -> cặp ứng viên."""
    buckets: dict[tuple, list[str]] = {}
    for doc, sig in sigs.items():
        for b in range(BANDS):
            band = tuple(sig[b * ROWS:(b + 1) * ROWS])
            buckets.setdefault((b, band), []).append(doc)
    cands = set()
    for docs in buckets.values():
        for a, b in combinations(sorted(docs), 2):
            cands.add((a, b))
    return cands


def est_jaccard(s1: list[int], s2: list[int]) -> float:
    return sum(x == y for x, y in zip(s1, s2)) / len(s1)


def main() -> None:
    sigs = {d: minhash(shingles(t)) for d, t in DOCS.items()}
    cands = lsh_candidates(sigs)

    print(f"== MinHash+LSH near-dup ({len(DOCS)} docs, {NUM_HASHES} hashes, {BANDS}x{ROWS} bands) ==")
    print(f"  Cặp ứng viên LSH: {len(cands)} (thay vì C({len(DOCS)},2)={len(DOCS)*(len(DOCS)-1)//2} cặp brute-force)\n")
    THRESH = 0.4          # ngưỡng Jaccard coi là near-dup (reword ~0.44; exact=1.0). Calibrate!
    dups = []
    for a, b in sorted(cands):
        j = est_jaccard(sigs[a], sigs[b])
        flag = "NEAR-DUP" if j >= THRESH else "candidate (dưới ngưỡng)"
        print(f"  {flag:24s} {a}~{b}  Jaccard≈{j:.2f}")
        if j >= THRESH:
            dups.append((a, b, j))

    # giữ 1 bản mỗi cụm trùng (union-find đơn giản)
    drop = set()
    for a, b, _ in dups:
        if a not in drop and b not in drop:
            drop.add(b)                     # giữ a, bỏ b
    kept = [d for d in DOCS if d not in drop]
    print(f"\n  -> phát hiện {len(dups)} cặp near-dup; BỎ {sorted(drop)}; GIỮ {len(kept)}/{len(DOCS)} docs")
    print("\nDONE ✅ MinHash dedup chạy xong.")
    assert "d2" in drop or "d6" in drop, "phải bắt được near-dup của d1"


if __name__ == "__main__":
    main()
