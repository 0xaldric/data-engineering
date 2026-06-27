# AL02 — AI-DE Coding Exercises 1 (bài tập + lời giải)

> 5 bài coding-round AI-DE (RAG/embedding/eval) — **đề + lời giải đầy đủ + reasoning**. Tự code trước, rồi đối chiếu. Liên hệ [[ab02-rag-eval-harness]], [[g07-dsa-for-de]], [[ai03-chunking]].

---
## Bài 1 — recall@k & MRR từ kết quả retrieval
**Đề:** Cho `results` (list các list note trả về cho mỗi query) + `expected` (note đúng mỗi query). Tính recall@k và MRR.
```python
def recall_mrr(results, expected, k):
    rc, rr = [], []
    for got, exp in zip(results, expected):
        topk = got[:k]
        hit = exp in topk
        rc.append(1 if hit else 0)
        rr.append(1/(topk.index(exp)+1) if hit else 0)   # rank của exp (1-based)
    n = len(expected)
    return sum(rc)/n, sum(rr)/n
```
**Reasoning:** recall@k = có lọt top-k không (nhị phân). MRR = 1/rank của hit đầu tiên (thưởng hạng cao). `topk.index(exp)` cho vị trí 0-based → +1. Không hit → rr=0.

---
## Bài 2 — Chunk text giữ cấu trúc (theo heading)
**Đề:** Cắt markdown thành chunk theo heading `#`, mỗi chunk ≤ `size` ký tự, không cắt giữa dòng.
```python
def chunk_md(text, size=500):
    chunks, cur, cur_head = [], [], ""
    for line in text.split("\n"):
        if line.startswith("#"):                  # heading mới -> chốt chunk cũ
            if cur: chunks.append((cur_head, "\n".join(cur)))
            cur, cur_head = [], line.strip("# ")
        cur.append(line)
        if len("\n".join(cur)) >= size:           # quá size -> chốt, giữ heading
            chunks.append((cur_head, "\n".join(cur))); cur = []
    if cur: chunks.append((cur_head, "\n".join(cur)))
    return chunks
```
**Reasoning:** structure-aware ([[ai03-chunking]]): chốt chunk ở ranh giới heading (giữ ngữ nghĩa) + khi vượt size (giữ vừa context). Mỗi chunk mang heading làm metadata → retrieve tốt hơn. Không cắt giữa dòng (split theo `\n`).

---
## Bài 3 — Cosine similarity + ngưỡng
**Đề:** Viết `cosine(a,b)` và hàm trả True nếu 2 câu "tương đương" (cosine ≥ threshold). Không dùng numpy.
```python
import math
def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(y*y for y in b))
    return dot/(na*nb) if na and nb else 0.0

def equivalent(va, vb, threshold=0.85):
    return cosine(va, vb) >= threshold
```
**Reasoning:** cosine = dot/(|a||b|) → đo góc, bất biến độ dài. Ngưỡng phải **calibrate** trên data ([[ag04-drift-detection]]) — baseline tiếng Việt cao nên ngưỡng cao. ⚠️ cosine đo bề mặt, không đo sự thật ([[ag02-hallucination-detection]]).

---
## Bài 4 — Incremental index theo content-hash
**Đề:** Cho `files` (dict path→content) và `indexed` (dict path→hash đã index). Trả về (new, changed, deleted, unchanged).
```python
import hashlib
def diff_index(files, indexed):
    h = lambda c: hashlib.md5(c.encode()).hexdigest()
    cur = {p: h(c) for p, c in files.items()}
    new      = [p for p in cur if p not in indexed]
    changed  = [p for p in cur if p in indexed and cur[p] != indexed[p]]
    deleted  = [p for p in indexed if p not in cur]
    unchanged= [p for p in cur if p in indexed and cur[p] == indexed[p]]
    return new, changed, deleted, unchanged
```
**Reasoning:** incremental ([[ad01-streaming-rag]]): chỉ re-embed new+changed (so hash), xoá chunk của deleted (reconcile chống ghost [[ac06-kb-freshness]]), bỏ qua unchanged → chi phí ∝ thay đổi, không ∝ tổng corpus.

---
## Bài 5 — Near-duplicate bằng Jaccard
**Đề:** Cho list câu, tìm các cặp near-dup (Jaccard shingle ≥ thresh).
```python
def shingles(s, k=2):
    w = s.lower().split()
    return {" ".join(w[i:i+k]) for i in range(len(w)-k+1)} or {s.lower()}

def near_dups(sents, thresh=0.5):
    sh = [shingles(s) for s in sents]
    pairs = []
    for i in range(len(sents)):
        for j in range(i+1, len(sents)):
            j_sim = len(sh[i]&sh[j]) / len(sh[i]|sh[j]) if (sh[i]|sh[j]) else 0
            if j_sim >= thresh: pairs.append((i, j, round(j_sim, 2)))
    return pairs
```
**Reasoning:** Jaccard = |giao|/|hợp| trên shingle (k-gram) → đo trùng lặp văn bản. O(n²) brute-force OK cho nhỏ; scale lớn → MinHash+LSH ([[aa04-training-data-prep]]) đưa về ~O(n). Dùng để dedup training data / chống lặp context.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Code cả 5 bài KHÔNG nhìn lời giải, chạy thử.
- [ ] Giải thích reasoning mỗi bài (vì sao làm vậy).
- [ ] Nêu cách scale mỗi bài (vd Jaccard → MinHash).
- 🔭 Tự mò: ghép bài 1+4 — dùng `diff_index` quyết file nào re-embed, rồi `recall_mrr` đo trước/sau; thêm test case edge (query không có hit, file rỗng, chunk > size) cho mỗi hàm.

➡️ Tiếp [[al03-case-logistics-ai]] — case study logistics.
