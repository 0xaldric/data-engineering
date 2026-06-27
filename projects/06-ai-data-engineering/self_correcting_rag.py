"""Self-Correcting RAG — RAG tự đánh giá retrieval, yếu thì TỰ VIẾT LẠI query rồi thử lại.

Vòng: retrieve -> đo confidence (điểm top) -> nếu thấp: reformulate (mock-HyDE: sinh
"giả thuyết câu trả lời" rồi embed nó thay vì câu hỏi cộc lốc) -> retry -> giữ kết quả
TỐT HƠN. Bắt chước agent tự sửa ([[aa05-agentic-pipelines]]).

Chạy: python projects/06-ai-data-engineering/self_correcting_rag.py
(Logic self-correction là THẬT; phần "LLM viết lại" được mock bằng reformulation soạn sẵn.)
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, build_index, search

THRESHOLD = 0.75   # dưới ngưỡng = "không tự tin" -> kích hoạt self-correction

# (query cộc lốc, mock-HyDE reformulation = "giả thuyết câu trả lời" LLM sẽ sinh)
QUERIES = [
    ("EOS", "exactly once semantics trong kafka streaming với idempotent producer và transaction"),
    ("SCD", "slowly changing dimension type 2 giữ lịch sử thay đổi của chiều trong data warehouse"),
    ("RAG đánh giá", "đánh giá retrieval RAG bằng recall@k MRR nDCG trên golden set"),
]


def confidence(con, q):
    df = search(con, q, k=3, hybrid=True)
    if len(df) == 0:
        return 0.0, "-"
    return float(df["vec_score"].iloc[0]), df["note"].iloc[0].split("/")[-1]


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    build_index(con)

    print(f"== Self-Correcting RAG (ngưỡng tự tin = {THRESHOLD}) ==\n")
    before, after = [], []
    for weak, hyde in QUERIES:
        s0, n0 = confidence(con, weak)
        before.append(s0)
        print(f"  Q: '{weak}'")
        print(f"    [thử 1] score={s0:.3f} top={n0}", end="")
        if s0 >= THRESHOLD:
            print("  -> tự tin, GIỮ")
            after.append(s0)
            continue
        print("  -> THẤP, tự sửa...")
        # self-correction: reformulate + retry
        s1, n1 = confidence(con, hyde)
        if s1 > s0:
            print(f"    [reformulate -> HyDE] score={s1:.3f} top={n1}  -> TỐT HƠN (+{s1-s0:.3f}), giữ bản mới ✓")
            after.append(s1)
        else:
            print(f"    [reformulate -> HyDE] score={s1:.3f} top={n1}  -> không hơn, giữ bản gốc")
            after.append(s0)
        print()

    avg_b, avg_a = sum(before) / len(before), sum(after) / len(after)
    print(f"  Trung bình confidence: TRƯỚC {avg_b:.3f} -> SAU self-correct {avg_a:.3f} (+{avg_a-avg_b:.3f})")
    print("  Ý: câu hỏi cộc lốc -> retrieve note chung chung; viết lại thành 'giả thuyết trả lời'")
    print("     (HyDE) khớp chunk khai báo tốt hơn -> kéo đúng note cụ thể lên top.")
    print("  ⚠️ Phải có ĐIỀU KIỆN DỪNG (max retries) + chỉ giữ khi THỰC SỰ tốt hơn (đo, không đoán).")
    print("\nDONE ✅ self-correcting RAG: tự đánh giá -> reformulate -> retry -> giữ tốt hơn.")


if __name__ == "__main__":
    main()
