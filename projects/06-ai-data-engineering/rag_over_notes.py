"""RAG over your own DE notes — Capstone: Hạ tầng dữ liệu cho AI.

Pipeline DE cho RAG (cùng tư duy ETL, output là vector thay vì fact/dim):
    notes/*.md ──► CHUNK (structure-aware) ──► EMBED (fastembed, local)
              ──► VECTOR STORE (DuckDB FLOAT[384] + cosine) ──► SEARCH (semantic + hybrid)

Điểm DE quan trọng được minh hoạ:
  - INCREMENTAL & idempotent: chỉ re-embed file ĐỔI (theo content hash); xử lý update/delete.
  - PROVENANCE/lineage: lưu model + indexed_at cho mỗi chunk (governance dữ liệu LLM-era).
  - EVAL: recall@k trên golden set (chất lượng retrieval = data quality mặc áo mới).
  - HYBRID search: vector (semantic) + keyword (lexical) — bắt cả nghĩa lẫn từ khoá.

Chạy: python projects/06-ai-data-engineering/rag_over_notes.py            # index + demo + eval
      python projects/06-ai-data-engineering/rag_over_notes.py search "vì sao shuffle đắt"
Lib: fastembed (ONNX, không cần API key/torch/Java), duckdb.
"""
from __future__ import annotations

import hashlib
import re
import sys
import time
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
NOTES_DIRS = [ROOT / "notes", ROOT / "notes" / "advanced"]
DB_PATH = ROOT / "warehouse" / "rag.duckdb"
MODEL_NAME = "BAAI/bge-small-en-v1.5"   # multilingual: đổi 'intfloat/multilingual-e5-small'
DIM = 384
MAX_CHUNK_CHARS = 1200
OVERLAP_CHARS = 150

_embedder = None


def get_embedder():
    global _embedder
    if _embedder is None:
        from fastembed import TextEmbedding
        _embedder = TextEmbedding(MODEL_NAME)
    return _embedder


def embed(texts: list[str]) -> list[list[float]]:
    return [v.tolist() for v in get_embedder().embed(texts)]


def embed_query(q: str) -> list[float]:
    # bge khuyến nghị prefix cho câu truy vấn để retrieval tốt hơn
    prefix = "Represent this sentence for searching relevant passages: "
    return embed([prefix + q])[0]


# --------------------------- CHUNKING --------------------------------
def chunk_markdown(text: str, source: str) -> list[dict]:
    """Structure-aware: cắt theo heading (## / ###), section dài thì cắt theo size + overlap."""
    chunks: list[dict] = []
    # tách theo dòng heading, giữ heading làm ngữ cảnh
    parts = re.split(r"(?m)^(#{1,4}\s+.*)$", text)
    current_heading = source
    buf = parts[0]
    sections = []
    i = 1
    while i < len(parts):
        heading = parts[i].strip("# ").strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((heading, body))
        i += 2
    if not sections:
        sections = [(source, buf)]
    for heading, body in sections:
        body = body.strip()
        if not body:
            continue
        if len(body) <= MAX_CHUNK_CHARS:
            chunks.append({"heading": heading, "text": f"{heading}\n{body}"})
        else:  # section dài -> cắt size + overlap
            start = 0
            while start < len(body):
                piece = body[start:start + MAX_CHUNK_CHARS]
                chunks.append({"heading": heading, "text": f"{heading}\n{piece}"})
                start += MAX_CHUNK_CHARS - OVERLAP_CHARS
    return chunks


def iter_note_files() -> list[Path]:
    files = []
    for d in NOTES_DIRS:
        files += sorted(d.glob("*.md"))
    return files


def file_hash(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


# --------------------------- INDEX (incremental) ---------------------
def init_db(con):
    con.execute(f"""CREATE TABLE IF NOT EXISTS chunks (
        chunk_id VARCHAR, note VARCHAR, heading VARCHAR, text VARCHAR,
        embedding FLOAT[{DIM}], model VARCHAR, indexed_at VARCHAR)""")
    con.execute("""CREATE TABLE IF NOT EXISTS sources (
        note VARCHAR PRIMARY KEY, hash VARCHAR, n_chunks INT, indexed_at VARCHAR)""")


def build_index(con) -> dict:
    init_db(con)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    existing = dict(con.execute("SELECT note, hash FROM sources").fetchall())
    files = iter_note_files()
    present = {str(p.relative_to(ROOT)) for p in files}
    stats = {"new": 0, "changed": 0, "unchanged": 0, "deleted": 0, "chunks": 0}

    # xử lý file đã xoá (có trong sources nhưng không còn file) -> dọn chunk
    for note in list(existing):
        if note not in present:
            con.execute("DELETE FROM chunks WHERE note = ?", [note])
            con.execute("DELETE FROM sources WHERE note = ?", [note])
            stats["deleted"] += 1

    for p in files:
        note = str(p.relative_to(ROOT))
        h = file_hash(p)
        if existing.get(note) == h:
            stats["unchanged"] += 1
            continue
        stats["changed" if note in existing else "new"] += 1
        # idempotent: xoá chunk cũ của file này rồi ghi lại
        con.execute("DELETE FROM chunks WHERE note = ?", [note])
        cks = chunk_markdown(p.read_text(), p.stem)
        if not cks:
            continue
        vecs = embed([c["text"] for c in cks])
        rows = pd.DataFrame({
            "chunk_id": [f"{note}#{i}" for i in range(len(cks))],
            "note": note,
            "heading": [c["heading"] for c in cks],
            "text": [c["text"] for c in cks],
            "embedding": vecs,
            "model": MODEL_NAME,
            "indexed_at": now,
        })
        con.register("rows", rows)
        con.execute(f"INSERT INTO chunks SELECT chunk_id, note, heading, text, "
                    f"embedding::FLOAT[{DIM}], model, indexed_at FROM rows")
        con.unregister("rows")
        con.execute("INSERT OR REPLACE INTO sources VALUES (?,?,?,?)", [note, h, len(cks), now])
        stats["chunks"] += len(cks)

    # HNSW index (vss) — tăng tốc ANN khi scale; brute-force cosine vẫn chạy nếu bỏ qua
    try:
        con.execute("INSTALL vss; LOAD vss;")
        con.execute("SET hnsw_enable_experimental_persistence = true")
        con.execute("DROP INDEX IF EXISTS hnsw_idx")
        con.execute("CREATE INDEX hnsw_idx ON chunks USING HNSW (embedding) WITH (metric = 'cosine')")
        stats["hnsw"] = True
    except Exception:
        stats["hnsw"] = False
    return stats


# --------------------------- SEARCH ----------------------------------
def search(con, query: str, k: int = 5, hybrid: bool = True) -> pd.DataFrame:
    qv = embed_query(query)
    # vector score (cosine) + keyword bonus (lexical) -> hybrid
    terms = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]
    kw = " + ".join([f"(lower(text) LIKE '%{t}%')::INT" for t in terms]) or "0"
    sql = f"""
        SELECT note, heading,
               array_cosine_similarity(embedding, ?::FLOAT[{DIM}]) AS vec_score,
               ({kw}) AS kw_hits,
               substr(text, 1, 90) AS preview
        FROM chunks
        ORDER BY ({'vec_score + 0.03*' + '(' + kw + ')' if hybrid else 'vec_score'}) DESC
        LIMIT ?"""
    return con.execute(sql, [qv, k]).fetchdf()


# --------------------------- EVAL (recall@k) -------------------------
# golden set: query -> mảnh tên note ĐÚNG kỳ vọng (đặt nhãn theo tên file thật)
GOLDEN = [
    ("vì sao shuffle đắt trong spark", "shuffle"),
    ("slowly changing dimension giữ lịch sử", "scd"),
    ("idempotency pipeline chạy lại không trùng", "pipeline-patterns"),
    ("exactly once trong kafka streaming", "streaming-eos"),
    ("data vault hub link satellite", "data-vault"),
    ("chunking embedding vector database RAG", "rag"),
    ("star schema fact dimension grain", "dimensional"),
    ("parquet columnar đọc nhanh hơn csv", "file-formats"),
]


def evaluate(con, k: int = 5) -> float:
    hit = 0
    for q, expect in GOLDEN:
        df = search(con, q, k=k)
        notes = " ".join(df["note"].tolist()).lower()
        ok = expect in notes
        hit += int(ok)
        print(f"  recall@{k} [{'✓' if ok else '✗'}] {q[:42]:42s} -> {df['note'].iloc[0] if len(df) else '-'}")
    recall = hit / len(GOLDEN)
    print(f"\n  RECALL@{k} = {hit}/{len(GOLDEN)} = {recall:.0%}")
    return recall


# --------------------------- MAIN ------------------------------------
def main(argv: list[str]) -> int:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))

    if len(argv) >= 3 and argv[1] == "search":
        build_index(con)
        print(search(con, argv[2], k=6).to_string(index=False))
        return 0

    print("== INDEX (incremental) ==")
    t0 = time.time()
    s = build_index(con)
    total = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print(f"  files: new={s['new']} changed={s['changed']} unchanged={s['unchanged']} deleted={s['deleted']}")
    print(f"  embedded {s['chunks']} chunks mới; tổng {total} chunks trong vector store; "
          f"HNSW={s['hnsw']}; {time.time()-t0:.1f}s")

    print("\n== SEMANTIC SEARCH demo ==")
    for q in ["vì sao shuffle đắt", "giữ lịch sử khi khách đổi địa chỉ", "test dữ liệu do LLM sinh ra"]:
        df = search(con, q, k=3)
        print(f"\n  Q: {q}")
        for _, r in df.iterrows():
            print(f"    {r['vec_score']:.3f} | {r['note']} :: {r['heading'][:50]}")

    print("\n== EVAL recall@k (golden set) ==")
    evaluate(con, k=5)
    print("\nDONE ✅ RAG over notes chạy xong.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
