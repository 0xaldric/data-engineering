# AM01 — RAG Failure Modes & Debugging ⭐ (có code chạy được)

> RAG **fail thầm lặng** (trả doc sai mà không lỗi). Biết các kiểu hỏng + cách **debug theo tầng** để fix đúng chỗ. Code: [`rag_debugger.py`](../../projects/06-ai-data-engineering/rag_debugger.py). Liên hệ [[ab02-rag-eval-harness]], [[ae01-self-correcting-rag]].

## Vì sao cần debug có hệ thống
- RAG trả lời sai → lỗi ở đâu? **retrieval** (lấy sai doc) hay **generation** (có doc đúng mà trả sai)?
- Đoán mò → sửa nhầm tầng (chỉnh prompt khi lỗi ở chunk). Phải **chẩn đoán theo tầng**.

## ⭐ Catalog failure modes (RAG hỏng ở đâu)
| Tầng | Kiểu hỏng | Triệu chứng |
|------|-----------|-------------|
| **Ingest** | doc không vào index | doc đúng KHÔNG có trong store |
| **Chunk** | chunk quá nhỏ (mất ngữ cảnh) / quá to (loãng) | chunk đúng điểm thấp |
| **Embed** | embedding lệch (đa ngữ/prefix [[ah02-embedding-benchmark]]) | doc đúng điểm thấp dù có |
| **Retrieve** | doc đúng có nhưng **rank dưới k** | doc đúng #20, lấy top-5 |
| **Rank** | note khác "cướp" top (giống bề mặt) | top là doc sai điểm cao hơn |
| **Generate** | có doc đúng trong context mà LLM bỏ qua/bịa | answer sai dù context đúng |
| **Query** | câu hỏi mơ hồ/cộc lốc | embed lệch, không match ([[ae06-query-understanding]]) |

## ⭐ Debug theo TẦNG (code chạy)
Quy trình chẩn đoán: **index? → điểm doc đúng? → xếp hạng? → ai cướp top?**
```
Q 'scd...'  -> top=18-scd #1                    🟢 OK
Q 'EOS'     -> doc đúng điểm 0.580, hạng #147   🟠 bị cướp top -> reformulate/rerank/hybrid
Q 'zzz...'  -> doc không có trong index         🔴 ingest/chunk thiếu
Q 'tối ưu'  -> doc đúng #4                       🟢 OK (sát rìa top-5)
```
→ Mỗi triệu chứng → **fix đúng tầng**:
- không trong index → kiểm ingest/chunk pipeline.
- điểm thấp → embedding (đổi model đa ngữ / bỏ prefix / chunk lại).
- rank dưới k → tăng k / **rerank** ([[ae07-reranking-deep]]) / hybrid keyword ([[aa03-rag-production]]).
- note khác cướp top → rerank / hybrid / reformulate ([[ae01-self-correcting-rag]]).
- context đúng mà answer sai → generation (prompt / grounding / model).

## ⭐ Retrieval vs Generation (chia đôi để debug)
```
answer sai
 ├─ doc đúng CÓ trong context? 
 │    KHÔNG -> lỗi RETRIEVAL (debug như trên)
 │    CÓ    -> lỗi GENERATION (LLM bỏ qua context / bịa)
 │            -> grounding check ([[ag02-hallucination-detection]]), prompt "chỉ từ context", đổi model
```
→ Bước đầu tiên LUÔN: kiểm doc đúng có trong context không → khoanh vùng retrieval vs generation.

## Snippet (note-level rank của doc đúng)
```python
df = cosine_search_all(query)              # mọi chunk + điểm
note_best = df.groupby("note")["s"].max().sort_values(ascending=False)
rank = list(note_best.index).index(expected) + 1    # doc đúng xếp #?
# rank <= k: OK ; rank > k: bị đẩy xuống ; không thấy: không trong index
```

## Cạm bẫy
- **Sửa mò không chẩn đoán** → chỉnh prompt khi lỗi ở chunk → debug theo tầng trước.
- **Quên kiểm index** → tưởng retrieval kém mà doc chưa vào index → kiểm ingest đầu tiên.
- **Không chia retrieval/generation** → fix nhầm nửa → kiểm context có doc đúng không.
- **Đổ tại model** → thường lỗi ở data/retrieval, không phải LLM → đo trước khi đổ.
- **Một query fail kết luận cả hệ** → đo trên golden ([[ab02-rag-eval-harness]]), không 1 ca.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Catalog failure modes theo tầng (ingest/chunk/embed/retrieve/rank/generate/query).
- [ ] Debug theo tầng: index? → điểm? → rank? → ai cướp top?
- [ ] Chia retrieval vs generation (doc đúng có trong context?).
- [ ] Fix đúng tầng (điểm thấp→embed, rank dưới k→rerank...).
- [ ] Cạm bẫy: sửa mò, quên kiểm index, đổ tại model.
- 🔭 Tự mò: chạy `rag_debugger.py`, thêm case query của bạn; với case "EOS" #147, thử reformulate (HyDE [[ae01-self-correcting-rag]]) rồi chạy lại debugger xem hạng cải thiện không — đó là vòng debug→fix→verify.

➡️ Tiếp [[am02-prompt-patterns]] — mẫu prompt nâng cao.
