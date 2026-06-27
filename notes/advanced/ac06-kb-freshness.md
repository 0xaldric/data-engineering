# AC06 — Knowledge Base Freshness & Maintenance

> RAG **không phải build một lần rồi quên**. Tài liệu đổi, cũ đi, mâu thuẫn nhau. Giữ corpus **tươi + nhất quán** là việc vận hành liên tục. Liên hệ [[ai09-streaming-ai]], [[ai04-embedding-versioning]], [[ab06-llm-observability]].

## Vấn đề: KB "thối" theo thời gian
- Tài liệu gốc cập nhật → vector store vẫn giữ **bản cũ** → RAG trả lời **sai/lỗi thời**.
- Doc bị xoá ở nguồn → vẫn còn trong index → "ma" (ghost doc).
- 2 tài liệu **mâu thuẫn** (policy v1 vs v2) → RAG lôi cả hai → LLM lúng túng/trả lời sai.
- → "Stale RAG" tệ hơn không RAG: trả lời **tự tin nhưng sai** (người dùng tin).

## ⭐ Vòng đời tài liệu trong KB (CRUD cho RAG)
```
nguồn (Confluence/DB/Drive...) ──┐
   CREATE  doc mới   ─> chunk ─> embed ─> upsert vào index
   UPDATE  doc đổi   ─> phát hiện (hash/mtime) ─> re-chunk ─> re-embed ─> THAY chunk cũ
   DELETE  doc xoá   ─> xoá chunk khỏi index (chống ghost)
   (định kỳ)         ─> reconcile: so nguồn ↔ index, dọn lệch
```
- **Phát hiện đổi**: content-hash (đã làm ở `rag_over_notes.py` — incremental theo hash) hoặc updated_at/CDC từ nguồn.
- **Idempotent upsert**: chạy lại không tạo trùng (đúng [[../11-idempotency.md|idempotency]] nếu có / [[i07-backfill-reprocessing]]).

## ⭐ Xử lý thông tin MÂU THUẪN (khó nhất)
Khi nhiều doc nói khác nhau về cùng việc:
| Cách | Làm |
|------|-----|
| **Versioning + recency** | gắn `version`/`effective_date`; ưu tiên bản mới nhất khi retrieve |
| **Authority/source rank** | doc chính thức > wiki cá nhân > comment; boost theo độ tin |
| **Supersede/tombstone** | đánh dấu doc cũ "đã thay thế" → loại khỏi retrieve (nhưng giữ để audit) |
| **Conflict surfaced** | nếu vẫn mâu thuẫn → LLM nói rõ "có 2 nguồn khác nhau" thay vì đoán |
→ Metadata (`effective_date`, `source`, `status`) là chìa khoá → filter/boost lúc retrieve ([[ab07-vector-search-opt]]).

## ⭐ Freshness SLA & monitor
- **Freshness SLA**: "KB trễ tối đa N phút/giờ so với nguồn" → thiết kế re-index theo đó ([[ai09-streaming-ai]]: event-driven cho gấp, batch cho chậm).
- **Monitor** ([[ab06-llm-observability]]): tuổi trung bình chunk, % doc quá hạn freshness, số ghost (index có-nguồn không), lần reconcile cuối.
- **Alert**: nguồn đổi mà re-index fail → KB lệch âm thầm.

## Right-to-be-forgotten / xoá có kiểm soát
- Người dùng yêu cầu xoá data (GDPR) → phải xoá **cả chunk trong vector store**, không chỉ nguồn.
- Re-embed khi đổi model ([[ai04-embedding-versioning]]) cũng là một dạng "làm mới" toàn corpus (blue-green index).

## Sơ đồ reconcile (chống lệch nguồn↔index)
```
       nguồn (set doc_id + hash)         index (set doc_id + hash)
              │  so sánh định kỳ  │
    chỉ ở nguồn → thiếu → ADD     chỉ ở index → ghost → DELETE
    hash khác → đổi → RE-EMBED            khớp → bỏ qua
```

## Cạm bẫy
- **Build 1 lần rồi quên** → KB thối, RAG sai tự tin (lỗi kinh điển nhất).
- **Update doc nhưng quên xoá chunk cũ** → cả cũ lẫn mới trong index → mâu thuẫn.
- **Không xoá ghost** → retrieve doc đã chết.
- **Không có effective_date** → không phân biệt bản mới/cũ → recency vô hiệu.
- **Re-index toàn bộ mỗi lần** (thay vì incremental) → tốn, chậm → dùng hash/CDC.
- **Quên right-to-be-forgotten ở vector store** → vi phạm compliance.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao stale RAG tệ hơn không RAG.
- [ ] CRUD cho KB: create/update/delete + reconcile; phát hiện đổi bằng hash/CDC.
- [ ] 4 cách xử lý mâu thuẫn (version/authority/supersede/surface).
- [ ] Freshness SLA + monitor (tuổi chunk, ghost, % quá hạn).
- [ ] Right-to-be-forgotten ở vector store.
- 🔭 Tự mò: trong `rag_over_notes.py`, thử **sửa nội dung 1 note** rồi chạy lại build_index → xác nhận incremental chỉ re-embed note đó (hash đổi); rồi **xoá 1 note** và viết đoạn code "reconcile" so file hệ thống ↔ bảng chunks, xoá chunk ghost. Đo trước/sau bằng `rag_eval_harness.py`.

➡️ Tiếp [[ac07-feature-store]] — feature store cho ML/LLM.
