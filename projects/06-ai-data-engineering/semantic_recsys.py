"""Semantic Recommender — gợi ý bằng EMBEDDING (content-based) + giải thích.

Ý tưởng two-tower thu nhỏ: item-tower = embedding nội dung item; user-tower =
trung bình embedding các item user đã thích. Recommend = item gần user nhất (cosine)
mà user chưa xem. Cold-start OK: item mới vẫn có embedding nội dung (không cần lịch sử).

Chạy: python projects/06-ai-data-engineering/semantic_recsys.py
(Local fastembed, KHÔNG API. Vai trò DE: pipeline item/user embedding + serving.)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from rag_over_notes import embed

# "Catalog" — mỗi item: id + mô tả nội dung (LLM/metadata sinh được ở thực tế).
CATALOG = {
    "spark-shuffle":    "Tối ưu Spark: shuffle, partition, skew, broadcast join",
    "kafka-eos":        "Kafka exactly-once, idempotent producer, transaction",
    "scd2":             "Slowly changing dimension type 2, giữ lịch sử chiều",
    "star-schema":      "Mô hình sao: fact, dimension, grain, surrogate key",
    "dbt-incremental":  "dbt incremental model, snapshot, test, macro Jinja",
    "rag-chunking":     "RAG: chunk, embedding, vector database, hybrid search",
    "llm-guardrail":    "Guardrail LLM: PII redaction, prompt injection, grounding",
    "vector-ann":       "Vector search: HNSW, IVF, quantization, recall vs latency",
    "airflow-dag":      "Airflow DAG, scheduler, backfill, idempotent task",
    "parquet-format":   "Parquet cột, nén, đọc nhanh, predicate pushdown",
}


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def main() -> None:
    ids = list(CATALOG)
    vecs = dict(zip(ids, embed([CATALOG[i] for i in ids])))   # item-tower (1 lần, offline)

    # user "đã thích" vài item về AI/LLM + vector -> hồ sơ thiên về AI infra
    liked = ["rag-chunking", "llm-guardrail"]
    profile = [sum(c) / len(liked) for c in zip(*(vecs[i] for i in liked))]  # user-tower = mean

    print("== Semantic Recommender (content-based + cold-start) ==")
    print(f"  User đã thích: {liked}\n")

    # chấm điểm item CHƯA xem, kèm 'vì sao' = item đã thích gần nhất
    scored = []
    for i in ids:
        if i in liked:
            continue
        s = cosine(profile, vecs[i])
        why = max(liked, key=lambda L: cosine(vecs[L], vecs[i]))
        scored.append((s, i, why))
    scored.sort(reverse=True)

    print(f"  {'item':16s} {'score':>6s}  vì gần với (đã thích)")
    for s, i, why in scored[:5]:
        print(f"  {i:16s} {s:>6.3f}  ~ {why}")

    top = scored[0]
    print(f"\n  -> Gợi ý hàng đầu: '{top[1]}' (score {top[0]:.3f}), vì giống '{top[2]}' bạn đã thích.")
    print("  Cold-start: item mới chỉ cần MÔ TẢ là gợi ý được — không cần lịch sử click.")
    print("  (Thực tế: LLM có thể re-rank + sinh câu giải thích tự nhiên từ 'why' này.)")
    print("\nDONE ✅ recommender chạy xong (embedding item/user + cosine + giải thích).")


if __name__ == "__main__":
    main()
