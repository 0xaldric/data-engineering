"""Drift Detection — phát hiện phân phối INPUT đổi (câu hỏi người dùng dịch chuyển).

Hệ AI "im lặng hỏng" khi input drift: câu hỏi production khác dần lúc build -> RAG/model
gặp phân phối lạ -> chất lượng tụt mà không lỗi rõ. Đo bằng embedding: so CENTROID
batch tham chiếu vs batch mới; lệch nhiều = drift -> cảnh báo (re-eval/re-index/mở rộng KB).

Chạy: python projects/06-ai-data-engineering/drift_detect.py
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


def centroid(vecs):
    n = len(vecs)
    return [sum(v[i] for v in vecs) / n for i in range(len(vecs[0]))]


# Batch THAM CHIẾU (lúc build hệ) — câu hỏi về Data Engineering (đủ lớn để centroid ổn định)
REFERENCE = [
    "tối ưu shuffle trong spark", "kafka exactly once là gì",
    "star schema fact dimension", "parquet cột nén đọc nhanh",
    "idempotency trong pipeline", "partition và bucketing trong hive",
    "window function tính running total", "dbt test và snapshot",
]
# Batch mới A: VẪN về DE (không drift)
CURRENT_SAME = [
    "dbt incremental model hoạt động sao", "airflow dag scheduler backfill",
    "slowly changing dimension type 2", "vector embedding cho RAG",
    "delta lake time travel", "spark broadcast join khi nào",
    "data warehouse vs data lake", "cdc change data capture là gì",
]
# Batch mới B: chủ đề LẠ hẳn (drift mạnh)
CURRENT_DRIFT = [
    "công thức nấu phở bò ngon", "kết quả bóng đá tối qua",
    "thời tiết Hà Nội ngày mai", "cách trồng rau sạch tại nhà",
    "mua điện thoại nào tốt", "bài tập giảm cân tại nhà",
    "phim chiếu rạp tuần này", "giá vàng hôm nay bao nhiêu",
]


def drift_score(ref_centroid, batch) -> tuple[float, float]:
    """Trả (cosine centroid, drift=1-cosine). Cao drift = phân phối dịch xa."""
    c = centroid(embed(batch))
    cs = cosine(ref_centroid, c)
    return cs, 1 - cs


def main() -> None:
    ref_c = centroid(embed(REFERENCE))
    # Ngưỡng CALIBRATE: đặt giữa "drift nội-phân-phối" (cùng chủ đề, ~0.08) và drift thật.
    # Production: calibrate từ LỊCH SỬ batch-to-batch (đủ mẫu) — KHÔNG hardcode mò.
    TH = 0.15

    print("== Drift Detection (so centroid batch mới vs tham chiếu) ==")
    print(f"  tham chiếu: {len(REFERENCE)} câu hỏi về Data Engineering | ngưỡng drift = {TH}\n")

    for name, batch in [("CÙNG chủ đề (DE)", CURRENT_SAME), ("LẠ chủ đề (nấu ăn/bóng đá)", CURRENT_DRIFT)]:
        cs, drift = drift_score(ref_c, batch)
        flag = "⚠️ DRIFT!" if drift > TH else "OK (ổn định)"
        print(f"  batch '{name:28s}' cosine={cs:.3f}  drift={drift:.3f}  -> {flag}")

    print(f"\n  (ngưỡng drift {TH:.3f}: vượt = phân phối câu hỏi đã dịch chuyển)")
    print("  Khi DRIFT -> hành động: re-eval golden, mở rộng KB/golden theo chủ đề mới,")
    print("              kiểm chất lượng (recall có tụt? — chạy continuous_eval), cân nhắc re-index/đổi model.")
    print("  Drift là 'im lặng hỏng': không có exception, chỉ chất lượng tụt dần -> phải CHỦ ĐỘNG đo.")
    print("\nDONE ✅ drift detection: so centroid embedding -> cảnh báo phân phối đổi.")


if __name__ == "__main__":
    main()
