# AI04 — Embedding Models & Versioning ⭐

> Chọn embedding model và xử lý khi **đổi model** — nỗi đau riêng của RAG, không có tương đương trong ETL truyền thống. Sâu hơn [[k05-vector-rag-deep]].

## Embedding model là gì (góc DE)
Model biến text → vector (dimension cố định, vd 384/768/1536). Với DE, nó là **một transform gọi model** — không tự train, nhưng phải chọn đúng + quản lý vận hành.

## Chọn model — tiêu chí
| Tiêu chí | Ảnh hưởng |
|----------|-----------|
| **Dimension** (384/768/1536) | cao hơn → chính xác hơn nhưng tốn RAM/storage/tốc độ |
| **Chất lượng** (MTEB benchmark) | recall retrieval |
| **Ngôn ngữ** | EN-only vs **multilingual** (tiếng Việt cần multilingual!) |
| **Cost/latency** | API (OpenAI text-embedding-3) vs **local** (fastembed/sentence-transformers) |
| **Context length** | chunk tối đa embed được |
| **Domain** | model general vs fine-tuned cho domain (code/legal/medical) |

VD: capstone dùng `bge-small-en` (local, 384, nhanh, nhưng EN → cross-lingual VI yếu) → đổi `multilingual-e5-small` cho tiếng Việt. API model chất lượng cao nhưng tốn tiền/latency + gửi data ra ngoài (PII!).

## ⭐ Vấn đề cốt lõi: đổi model = re-embed TOÀN BỘ
Vector của model A **không tương thích** vector model B (không gian khác, có thể khác dimension). → Đổi/nâng cấp embedding model → **phải embed lại 100% dữ liệu**.
- Khác ETL: thêm cột mới chỉ backfill cột đó; đổi embedding model → **rebuild cả vector store**.
- Đắt (compute/token cost) + có thể downtime (index cũ vs mới).
- Đây là lý do **version hoá embedding model** là bắt buộc.

## Chiến lược migration (đổi model an toàn)
Giống lakehouse migration ([[j06-lakehouse-migration]]) + blue-green ([[f06-dataops]]):
```
1. Build index MỚI (model B) SONG SONG với index cũ (model A) — không đụng live
2. Re-embed toàn bộ tài liệu bằng model B → vector store mới
3. VALIDATE: so recall@k cũ vs mới (model B có tốt hơn không?)
4. CUTOVER: chuyển query sang index B (atomic/blue-green)
5. Giữ index A một thời gian để rollback
```
⚠️ **Query phải dùng CÙNG model với index** — query embed bằng A nhưng search index B = rác.

## Versioning trong vector store
Lưu **model name + version** mỗi chunk (capstone có cột `model`):
```sql
-- biết chunk nào embed bằng model nào -> phát hiện index "lẫn lộn" model
SELECT model, count(*) FROM chunks GROUP BY model;
-- khi đổi model: re-embed những chunk model cũ
```
→ Provenance + cho phép migration từng phần + audit.

## Cache & batch (giảm cost re-embed)
- **Cache embedding** theo hash(text + model): text không đổi + cùng model → dùng lại vector, không gọi lại model.
- **Batch**: embed nhiều text/lần (model/API hiệu quả hơn per-call).
- **Incremental** ([[ai02-rag-capstone-writeup]]): chỉ re-embed file đổi — nhưng đổi MODEL thì incremental không cứu (phải toàn bộ).

## Snippet
```python
# version-aware: re-embed chỉ chunk dùng model cũ khi nâng cấp
con.execute("SELECT chunk_id, text FROM chunks WHERE model != ?", [NEW_MODEL])
# ... embed bằng NEW_MODEL, update embedding + model
```

## ⚠️ Cạm bẫy
- Query embed bằng model khác index → kết quả rác (phải cùng model).
- Đổi model mà không re-embed toàn bộ → index lẫn lộn không gian vector.
- Không version model → không biết khi nào cần rebuild.
- Dùng API embedding cho PII (gửi data nhạy cảm ra ngoài) — cân nhắc local.
- Quên cost re-embed khi quyết định nâng cấp model.

## ✅ "Tự mò"
🔭 Đổi `MODEL_NAME` trong capstone sang `intfloat/multilingual-e5-small`, xoá `warehouse/rag.duckdb`, re-index, so recall@k với bge-small trên query tiếng Việt → thấy multilingual tốt hơn cho VI.

➡️ Tiếp: [[ai05-retrieval-eval]].
