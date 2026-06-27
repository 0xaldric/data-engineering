# AD01 — Real-time / Streaming RAG ⭐ (có code chạy được)

> RAG **tươi gần real-time**: tài liệu mới/đổi phải tìm được trong vài giây, không chờ batch đêm. Incremental theo hash/CDC + freshness SLA. Code: [`streaming_rag.py`](../../projects/06-ai-data-engineering/streaming_rag.py). Sâu hơn [[ai09-streaming-ai]], [[ac06-kb-freshness]].

## Vì sao cần
- Nhiều ca **không chịu được trễ**: doc support vừa cập nhật, giá vừa đổi, tin tức mới, chính sách mới → RAG phải biết **ngay**.
- Batch re-index hàng đêm → câu trả lời "lỗi thời" cả ngày → người dùng mất tin.
- → RAG là **hệ thống sống**, ingest liên tục, không phải build-1-lần ([[ac06-kb-freshness]]).

## ⭐ Luồng streaming RAG
```
nguồn đổi (webhook/CDC/queue)
   ─> [phát hiện] doc mới/đổi (event hoặc hash)
   ─> [chunk + embed] CHỈ doc đó ([[ai03-chunking]])
   ─> [upsert] vào vector store (idempotent: xoá chunk cũ -> ghi mới)
   ─> searchable trong vài giây  ✅ freshness
   (song song: doc xoá -> xoá chunk -> chống ghost — reconcile [[ac06-kb-freshness]])
```

## ⭐ Đo thật (code chạy)
Thêm 1 doc mới vào corpus 206 note, đo "ingest → searchable":
```
[TRƯỚC ] top = ai09-streaming-ai.md (0.749) — chưa có doc chứa 'zorvex'
[re-index] new=1 changed=0 unchanged=206 -> chỉ embed doc MỚI (không rebuild corpus)
[SAU   ] top = _streaming_demo_tmp.md (0.842) — THẤY NGAY
freshness latency: 191 ms
[cleanup] reconcile deleted=1 (chống ghost)
```
→ **Incremental là chìa khoá**: chỉ embed 1/207 doc, không đụng 206 cái cũ. Doc mới lên top **191ms** sau khi xuất hiện. Đây là "freshness" định lượng được.

## ⭐ Incremental — vì sao bắt buộc (không full rebuild)
| | Full re-index | Incremental (streaming) |
|--|--------------|-------------------------|
| Phạm vi | embed lại TẤT CẢ | chỉ doc mới/đổi |
| Chi phí | O(toàn corpus) mỗi lần | O(thay đổi) |
| Độ trễ | hàng giờ | giây |
| Cách phát hiện | — | **content-hash** / updated_at / CDC |
→ `rag_over_notes.py` so **md5 hash** mỗi file: trùng→bỏ qua, khác→re-embed, mất→xoá chunk. Đó là incremental + reconcile.

## ⚠️ Cái gì incremental, cái gì KHÔNG
- **Embed**: incremental (chỉ doc mới) — rẻ.
- **HNSW index**: ở DuckDB demo phải **rebuild toàn bộ** sau mỗi đổi (DROP+CREATE) → ở scale lớn đây là **điểm nghẽn**. Vector DB production hỗ trợ **incremental index** (thêm node vào HNSW không rebuild) → đó là lý do dùng Qdrant/Milvus thay vì tự build ([[aa10-llmops]]).
- Bài học: "incremental embed" ≠ "incremental index"; phải tối ưu cả hai ở scale.

## ⭐ Streaming vs Batch — khi nào dùng cái nào (đừng over-stream)
| Tươi cỡ nào | Cách | Ví dụ |
|-------------|------|-------|
| Giây–phút (gấp) | event-driven (webhook/CDC/queue) | giá, tồn kho, tin nóng, support đang mở |
| Giờ | micro-batch định kỳ | wiki nội bộ, FAQ |
| Ngày | batch đêm | tài liệu pháp lý ít đổi |
→ Streaming **đắt + phức tạp** hơn ([[ai09-streaming-ai]] "đừng over-stream"). Chỉ stream cái **thật sự cần tươi**; phần còn lại batch.

## Kiến trúc production
```
CDC/Debezium / webhook / Kafka ─> consumer ─> chunk+embed ─> vector DB (upsert)
   ─> (idempotent theo doc_id) ─> dedup ─> freshness metric ([[ab06-llm-observability]])
   tách "hot" (cần tươi) vs "cold" (batch) để tiết kiệm
```

## Cạm bẫy
- **Full rebuild mỗi lần** → không scale; phải incremental theo hash/CDC.
- **Quên xoá chunk doc đã xoá** → ghost, retrieve doc chết ([[ac06-kb-freshness]]).
- **Upsert không idempotent** → chunk trùng khi re-stream cùng doc.
- **HNSW rebuild là nghẽn ẩn** → dùng vector DB hỗ trợ incremental index.
- **Over-stream mọi thứ** → đốt tiền cho data không cần tươi.
- **Không đo freshness** → tưởng tươi mà trễ ngầm → cần freshness SLA + alert.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao RAG = hệ sống, cần freshness (đo 191ms).
- [ ] Incremental theo hash/CDC vs full rebuild.
- [ ] "Incremental embed" ≠ "incremental index" (HNSW rebuild là nghẽn).
- [ ] Streaming vs batch theo nhu cầu tươi; đừng over-stream.
- [ ] Idempotent upsert + reconcile chống ghost.
- 🔭 Tự mò: sửa `streaming_rag.py` — thêm 5 doc liên tiếp (vòng lặp), đo freshness latency mỗi lần; thử **đổi** 1 doc cũ (hash đổi) xem có re-embed đúng 1 cái không; in tổng thời gian rebuild HNSW để thấy nó tăng theo corpus (nghẽn).

➡️ Tiếp [[ad02-llm-judge]] — eval tự động bằng LLM-judge.
