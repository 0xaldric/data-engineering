"""Query Router — định tuyến câu hỏi tới đúng đường: SQL / RAG / ACTION / REJECT.

Routing là NGÃ BA quyết định: route sai -> hỏi số đi RAG (bịa), hỏi kiến thức đi SQL (lỗi).
Kết hợp HEURISTIC (từ khoá cho action/định lượng — chắc, rẻ) + EMBEDDING (RAG vs ngoài
phạm vi — ngữ nghĩa). In quyết định + lý do mỗi câu.

Chạy: python projects/06-ai-data-engineering/query_router.py
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from rag_over_notes import embed

# Exemplar mỗi nhóm -> centroid embedding (cho phần ngữ nghĩa RAG vs REJECT)
EXEMPLARS = {
    "RAG":    ["idempotency là gì", "giải thích shuffle trong spark",
               "cách hoạt động của scd type 2", "vì sao parquet nhanh hơn csv"],
    "REJECT": ["thời tiết hôm nay thế nào", "kể chuyện cười cho nghe",
               "bạn tên là gì", "công thức nấu phở bò"],
}
# Heuristic từ khoá (override — chắc chắn, ưu tiên)
ACTION = re.compile(r"\b(gửi|tạo|xoá|xóa|đặt|hủy|cập nhật|thêm|chuyển)\b", re.I)
QUANT = re.compile(r"\b(bao nhiêu|tổng|trung bình|đếm|top \d|mấy|số lượng|theo tháng|theo quý)\b", re.I)


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def centroid(vecs):
    n = len(vecs)
    return [sum(v[i] for v in vecs) / n for i in range(len(vecs[0]))]


def route(query: str, cents: dict) -> tuple[str, str]:
    # 1) heuristic override (action/định lượng — high-stakes, dễ nhận)
    if ACTION.search(query):
        return "ACTION", "heuristic: động từ hành động -> tool + human approve"
    if QUANT.search(query):
        return "SQL", "heuristic: từ định lượng -> text-to-SQL/semantic layer"
    # 2) embedding: RAG (kiến thức) vs REJECT (ngoài phạm vi)
    qv = embed([query])[0]
    sims = {k: cosine(qv, c) for k, c in cents.items()}
    pick = max(sims, key=sims.get)
    return pick, f"embedding: {pick} (cos RAG={sims['RAG']:.2f} vs REJECT={sims['REJECT']:.2f})"


def main() -> None:
    cents = {k: centroid(embed(v)) for k, v in EXEMPLARS.items()}
    print("== Query Router (heuristic + embedding) ==\n")
    tests = [
        "idempotency trong pipeline là gì",          # RAG
        "doanh thu quý 3 bao nhiêu",                 # SQL
        "gửi email báo giá cho khách hàng",          # ACTION
        "kể cho tôi một câu chuyện cười",            # REJECT
        "vì sao shuffle trong spark đắt",            # RAG
        "tạo ticket hỗ trợ cho lỗi này",             # ACTION
    ]
    dest = {"SQL": "→ text-to-SQL (sandbox) ", "RAG": "→ RAG retrieve     ",
            "ACTION": "→ tool + human approve", "REJECT": "→ từ chối lịch sự  "}
    for q in tests:
        r, why = route(q, cents)
        print(f"  '{q[:38]:38s}' [{r:6s}] {dest[r]}  ({why})")

    print("\n  Routing = ngã ba: route sai -> mọi tầng sau sai (hỏi số đi RAG -> bịa số).")
    print("  Heuristic cho action/định lượng (chắc, an toàn); embedding cho RAG vs ngoài-phạm-vi.")
    print("  Production: classifier/LLM nhỏ thay heuristic khi nhiều intent; LUÔN có fallback.")
    print("\nDONE ✅ query router: phân loại -> route đúng đường + lý do.")


if __name__ == "__main__":
    main()
