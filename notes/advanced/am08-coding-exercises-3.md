# AM08 — AI-DE Coding Exercises 3 (bài tập + lời giải)

> 5 bài coding-round nâng cao (retrieval/fusion/eval) — **đề + lời giải + reasoning**. Tự code trước. Liên hệ [[am04-hybrid-fusion]], [[am05-eval-metrics-deep]], [[ae07-reranking-deep]].

---
## Bài 1 — Reciprocal Rank Fusion (RRF)
**Đề:** Gộp 2 bảng xếp hạng (list doc theo thứ tự) bằng RRF, trả top theo điểm RRF.
```python
def rrf(rank_lists, C=60):
    score = {}
    for lst in rank_lists:
        for rank, doc in enumerate(lst, 1):     # rank 1-based
            score[doc] = score.get(doc, 0) + 1/(C + rank)
    return sorted(score, key=score.get, reverse=True)
```
**Reasoning:** RRF gộp **thứ hạng** không gộp điểm → không cần chuẩn hoá thang (cosine vs BM25) ([[am04-hybrid-fusion]]). Doc cao ở nhiều list → điểm cộng dồn. C giảm ảnh hưởng hạng thấp.

---
## Bài 2 — nDCG@k với graded relevance
**Đề:** Cho `rels` (độ liên quan 0-3 theo thứ tự retrieve), tính nDCG@k.
```python
import math
def dcg(rels):
    return sum(r/math.log2(i+1) for i, r in enumerate(rels, 1))
def ndcg(rels, k):
    rels = rels[:k]
    ideal = sorted(rels, reverse=True)          # thứ tự lý tưởng
    idcg = dcg(ideal)
    return dcg(rels)/idcg if idcg else 0.0
```
**Reasoning:** DCG thưởng relevant ở hạng cao (chia log rank). IDCG = DCG của thứ tự lý tưởng (rel cao dồn đầu). nDCG = DCG/IDCG ∈ [0,1] ([[am05-eval-metrics-deep]]). Graded (0-3) phân biệt "đúng nhất" vs "tạm đúng". ⚠️ quên IDCG → >1 sai.

---
## Bài 3 — MMR (Maximal Marginal Relevance) chống trùng
**Đề:** Chọn k doc vừa liên quan vừa đa dạng. Cho `rel` (dict doc→điểm liên quan) và `sim(a,b)`.
```python
def mmr(docs, rel, sim, k, lam=0.5):
    selected = []
    cand = list(docs)
    while cand and len(selected) < k:
        def score(d):
            div = max((sim(d, s) for s in selected), default=0)   # giống cái đã chọn nhất
            return lam*rel[d] - (1-lam)*div
        best = max(cand, key=score)
        selected.append(best); cand.remove(best)
    return selected
```
**Reasoning:** MMR ([[ae07-reranking-deep]]) chọn lần lượt: cân **liên quan** (lam·rel) trừ **trùng** ((1-lam)·giống-cái-đã-chọn). lam cao→ưu liên quan; thấp→ưu đa dạng. Chống top-k cùng 1 ý (filter bubble [[al04-case-media-ai]]).

---
## Bài 4 — Sliding-window chunk với overlap
**Đề:** Cắt list token thành chunk size W, overlap O.
```python
def sliding_chunks(tokens, W=100, O=20):
    chunks, i = [], 0
    step = W - O                                # bước nhảy = size - overlap
    while i < len(tokens):
        chunks.append(tokens[i:i+W])
        if i + W >= len(tokens): break
        i += step
    return chunks
```
**Reasoning:** overlap giữ liên tục giữa chunk (câu ở ranh giới không mất [[am03-advanced-chunking]]). step = W-O (không O=0 thì lặp vô hạn nếu... thực ra step>0 luôn nếu O<W). `break` khi chunk cuối chạm hết tránh chunk thừa.

---
## Bài 5 — Semantic cache lookup
**Đề:** Cache (câu hỏi-vector, answer). Câu mới: nếu cosine với câu cũ ≥ thresh → trả cache.
```python
def cache_get(qv, cache, sim, thresh=0.95):
    best, ans = 0, None
    for cv, cached_ans in cache:
        s = sim(qv, cv)
        if s > best: best, ans = s, cached_ans
    return (ans, best) if best >= thresh else (None, best)
```
**Reasoning:** semantic cache ([[ad08-semantic-cache]]): tìm câu cũ gần nhất, hit nếu ≥ thresh. ⚠️ thresh CAO (0.95) vì false-hit (trả sai) nguy hiểm hơn false-miss; cosine ≠ ngữ nghĩa (negation bẫy) → ngưỡng cao + cẩn thận.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Code 5 bài, chạy với edge case.
- [ ] Reasoning: RRF gộp hạng, nDCG/IDCG, MMR đa dạng, overlap, cache thresh cao.
- [ ] Giới hạn mỗi bài (RRF C, MMR lam, cache false-hit).
- 🔭 Tự mò: ghép bài 1+2 — 2 hệ retrieve → RRF gộp → tính nDCG kết quả gộp vs từng hệ; ghép bài 3 — thêm MMR sau RRF để đa dạng top-5; so nDCG trước/sau MMR (MMR có thể giảm nDCG nhưng tăng đa dạng — trade-off).

➡️ Tiếp [[am09-ai-review12]] — review 12 + tổng kết kỹ thuật sâu.
