"""Continuous RAG Eval & Regression Gate — eval như CI, chặn merge khi chất lượng tụt.

Chạy harness -> so với BASELINE đã lưu (JSON) -> PASS/FAIL theo ngưỡng -> exit code.
Đây là cách biến eval thành "test tự động" cho RAG: mỗi đổi prompt/chunk/model phải
qua gate, không cho regression lọt ([[ac03-eval-driven-dev]], [[ad02-llm-judge]]).

Chạy: python projects/06-ai-data-engineering/continuous_eval.py
  (lần đầu: tạo baseline + PASS; lần sau: so baseline, FAIL nếu recall tụt > TOL)
  UPDATE_BASELINE=1 python ... -> cập nhật baseline (sau cải tiến CÓ CHỦ ĐÍCH)
Exit code: 0 = PASS, 1 = FAIL (dùng cho CI gate).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, ROOT, build_index
from rag_eval_harness import metrics

BASELINE = ROOT / "warehouse" / "eval_baseline.json"
TOL = 0.05          # cho phép dao động 5% (noise); tụt quá mức này = regression
GATE_KEY = "recall" # metric gate (RAG: recall quan trọng nhất — doc đúng có lọt context)


def main() -> int:
    con = duckdb.connect(str(DB_PATH))
    build_index(con)
    cur = metrics(con, k=5, hybrid=True)   # {recall, mrr, ndcg}
    print("== Continuous RAG Eval (config: hybrid k=5) ==")
    print(f"  hiện tại: recall={cur['recall']:.3f}  MRR={cur['mrr']:.3f}  nDCG={cur['ndcg']:.3f}")

    # lần đầu hoặc yêu cầu cập nhật -> ghi baseline
    if not BASELINE.exists() or os.environ.get("UPDATE_BASELINE") == "1":
        BASELINE.write_text(json.dumps(cur, indent=2))
        print(f"  -> đã lưu BASELINE ({BASELINE.name}). PASS (chưa có mốc so).")
        print("\nDONE ✅ (baseline saved)")
        return 0

    base = json.loads(BASELINE.read_text())
    print(f"  baseline: recall={base['recall']:.3f}  MRR={base['mrr']:.3f}  nDCG={base['ndcg']:.3f}")
    print(f"\n  {'metric':8s} {'baseline':>9s} {'hiện tại':>9s} {'delta':>8s}")
    for k in ("recall", "mrr", "ndcg"):
        d = cur[k] - base[k]
        flag = " ⬇️" if d < -TOL else (" ⬆️" if d > TOL else "")
        print(f"  {k:8s} {base[k]:>9.3f} {cur[k]:>9.3f} {d:>+8.3f}{flag}")

    # GATE: recall tụt quá TOL = regression -> FAIL
    regressed = cur[GATE_KEY] < base[GATE_KEY] - TOL
    print()
    if regressed:
        print(f"  ❌ FAIL: {GATE_KEY} tụt {base[GATE_KEY]-cur[GATE_KEY]:.3f} > TOL {TOL} -> CHẶN merge (regression).")
        print("DONE (exit 1)")
        return 1
    print(f"  ✅ PASS: {GATE_KEY} trong ngưỡng (>= baseline - {TOL}).")
    print("DONE ✅ (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
