"""Data Quality Score cho LLM training data — chấm CHẤT LƯỢNG từng mẫu đa chiều.

Train tốt cần data sạch. Chấm mỗi mẫu theo nhiều CHIỀU (length/dup/diversity/clean/format),
gộp thành quality score, lọc theo ngưỡng. "Garbage in, garbage out" -> cổng chất lượng.

Chạy: python projects/06-ai-data-engineering/data_quality_score.py
(Heuristic thuần, deterministic, không cần model. Tư duy DQ là thật.)
"""
from __future__ import annotations

# Tập mẫu trộn: tốt + xấu (ngắn/trùng/lặp/bẩn/sai-format) để thấy cổng lọc hoạt động.
SAMPLES = [
    "Idempotency giúp pipeline chạy lại không tạo dữ liệu trùng hay sai lệch.",   # tốt
    "Parquet lưu theo cột nên đọc nhanh hơn CSV nhờ chỉ quét cột cần thiết.",     # tốt
    "ok",                                                                          # quá ngắn
    "Idempotency giúp pipeline chạy lại không tạo dữ liệu trùng hay sai lệch.",   # TRÙNG y hệt
    "data data data data data data data data data data data data data data",      # lặp, diversity thấp
    "Thằng kia ngu vãi đồ rác rưởi câm mồm đi.",                                  # toxic
    "Spark shuffle move data across network between executors causing IO cost.",  # OK nhưng khác ngôn ngữ
    "",                                                                            # rỗng, sai format
]

TOXIC = {"ngu", "rác rưởi", "câm mồm", "đồ rác"}


def shingles(text, k=2):
    w = text.lower().split()
    return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)} or {text.lower()}


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0


def score_record(text, seen_shingles):
    """HARD gate (rớt 1 -> loại ngay) + SOFT score (trung bình các chiều mềm)."""
    w = text.split()
    n = len(w)
    sh = shingles(text)
    gates = {                                          # nghiêm trọng -> loại tuyệt đối
        "fmt": bool(text.strip()),                     # không rỗng
        "dup": not any(jaccard(sh, s) >= 0.8 for s in seen_shingles),  # không trùng
        "cln": not any(t in text.lower() for t in TOXIC),              # không toxic
    }
    soft = {                                           # chất lượng mềm -> tính điểm
        "len": 1.0 if 5 <= n <= 60 else 0.0,           # độ dài hợp lý
        "div": (len(set(w)) / n) if n else 0.0,        # đa dạng từ (lặp -> thấp)
    }
    soft_score = sum(soft.values()) / len(soft)
    return gates, soft, soft_score, sh


def main() -> None:
    THRESH = 0.8
    print(f"== Data Quality Score (HARD gate + SOFT score ≥ {THRESH}) ==\n")
    print(f"  {'#':2s} {'fmt':>4s} {'dup':>4s} {'cln':>4s} | {'len':>4s} {'div':>5s} {'soft':>5s}  decision  lý do bỏ")
    seen, kept, dropped = [], 0, 0
    for i, text in enumerate(SAMPLES, 1):
        gates, soft, ss, sh = score_record(text, seen)
        gate_ok = all(gates.values())
        keep = gate_ok and ss >= THRESH
        if keep:
            kept += 1; seen.append(sh)                 # chỉ mẫu GIỮ vào seen (bắt dup sau)
        else:
            dropped += 1
        reason = ""
        if not gates["fmt"]: reason = "rỗng"
        elif not gates["dup"]: reason = "TRÙNG"
        elif not gates["cln"]: reason = "TOXIC"
        elif ss < THRESH: reason = f"soft thấp ({ss:.2f})"
        g = gates
        print(f"  {i:<2d} {g['fmt']:>4d} {g['dup']:>4d} {g['cln']:>4d} | "
              f"{soft['len']:>4.0f} {soft['div']:>5.2f} {ss:>5.2f}  "
              f"{'GIỮ ✓ ' if keep else 'BỎ ✗  '}  {reason:14s} {text[:32]!r}")

    print(f"\n  Kết quả: giữ {kept}/{len(SAMPLES)}, bỏ {dropped}.")
    print("  ⭐ HARD gate (rỗng/trùng/toxic) loại NGAY — không cho trung bình 'cứu' mẫu độc/trùng.")
    print("  SOFT (length/diversity) tính điểm; cả hai phải đạt mới giữ.")
    print("  Mở rộng: thêm chiều ngôn ngữ, PII, decontamination (trùng test set — [[aa04]]).")
    print("\nDONE ✅ data quality scoring: chấm đa chiều -> lọc rác trước khi train.")


if __name__ == "__main__":
    main()
