"""GraphRAG từ wikilinks — dựng KNOWLEDGE GRAPH THẬT từ [[links]] giữa các note.

Vector RAG tìm theo "giống nghĩa"; GraphRAG đi theo "quan hệ" (note A -> B -> C).
Câu hỏi multi-hop ("X liên quan gì, rồi cái đó liên quan gì nữa") cần đi graph, không
chỉ similarity. Đây là GraphRAG thu nhỏ: graph = [[links]], hybrid vector + traversal.

Chạy: python projects/06-ai-data-engineering/graphrag_links.py
"""
from __future__ import annotations

import re
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import duckdb
from rag_over_notes import DB_PATH, ROOT, build_index, search

NOTE_DIRS = [ROOT / "notes", ROOT / "notes" / "advanced"]
LINK = re.compile(r"\[\[([^\]]+)\]\]")


def norm(target: str) -> str:
    """[[../18-scd.md|dimensional]] -> '18-scd' ; [[ai03-chunking]] -> 'ai03-chunking'."""
    t = target.split("|")[0].split("/")[-1]
    return t.replace(".md", "").strip()


def build_graph():
    nodes = set()
    for d in NOTE_DIRS:
        nodes |= {p.stem for p in d.glob("*.md")}
    out, inc = {n: set() for n in nodes}, {n: set() for n in nodes}
    for d in NOTE_DIRS:
        for p in d.glob("*.md"):
            src = p.stem
            for m in LINK.findall(p.read_text()):
                tgt = norm(m)
                if tgt in nodes and tgt != src:
                    out[src].add(tgt); inc[tgt].add(src)
    return nodes, out, inc


def bfs(out, start, hops=2):
    """Trả các node trong <= hops bước từ start (multi-hop neighborhood)."""
    seen, frontier, layers = {start}, {start}, {}
    for h in range(1, hops + 1):
        nxt = set()
        for u in frontier:
            nxt |= (out.get(u, set()) - seen)
        layers[h] = nxt
        seen |= nxt; frontier = nxt
    return layers


def main() -> None:
    nodes, out, inc = build_graph()
    n_edges = sum(len(v) for v in out.values())
    print("== GraphRAG từ wikilinks ==")
    print(f"  graph: {len(nodes)} node (note), {n_edges} cạnh ([[link]] có hướng)\n")

    # hub = note được TRỎ TỚI nhiều nhất (in-degree) -> khái niệm trung tâm
    hubs = sorted(nodes, key=lambda n: len(inc[n]), reverse=True)[:6]
    print("  Hub (được trỏ tới nhiều nhất = khái niệm nền tảng):")
    for h in hubs:
        print(f"    {h:32s} in={len(inc[h]):2d}  out={len(out[h]):2d}")

    # --- Hybrid: vector tìm SEED, graph mở rộng multi-hop ---
    con = duckdb.connect(str(DB_PATH)); build_index(con)
    query = "đánh giá chất lượng RAG"
    seed_note = search(con, query, k=1, hybrid=True)["note"].iloc[0].split("/")[-1].replace(".md", "")
    print(f"\n  Query: '{query}'  -> vector SEED = {seed_note}")
    layers = bfs(out, seed_note, hops=2)
    print(f"  Graph mở rộng từ seed (multi-hop):")
    print(f"    1-hop (liên quan trực tiếp): {sorted(layers.get(1, []))[:8]}")
    print(f"    2-hop (liên quan gián tiếp): {sorted(layers.get(2, []))[:8]}")
    reach = len(layers.get(1, set())) + len(layers.get(2, set()))
    print(f"  -> từ 1 seed, graph kéo thêm {reach} note liên quan mà vector top-k có thể BỎ SÓT.")

    # --- multi-hop path: nối 2 khái niệm xa nhau ---
    print(f"\n  Multi-hop: từ '{seed_note}' đi 2 bước tới đâu? (chuỗi quan hệ)")
    for nb in sorted(layers.get(1, []))[:3]:
        for nb2 in sorted(out.get(nb, []))[:1]:
            print(f"    {seed_note} -> {nb} -> {nb2}")
    print("\n  Ý: GraphRAG trả lời câu cần ĐI QUA quan hệ; bổ sung vector (giống nghĩa) bằng cấu trúc (liên kết).")
    print("\nDONE ✅ GraphRAG: graph thật từ [[links]] + hybrid vector-seed × graph-expand.")


if __name__ == "__main__":
    main()
