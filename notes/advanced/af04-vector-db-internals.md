# AF04 — Vector DB Internals sâu

> Bên trong vector DB: HNSW build, IVF-PQ, **DiskANN** (khi vector vượt RAM), filtered search, sharding. Hiểu internals để **chọn + tune** đúng, không dùng như hộp đen. Sâu hơn [[ab07-vector-search-opt]], [[aa10-llmops]].

## Vì sao hiểu internals
- Chọn vector DB (Qdrant/Milvus/pgvector/Weaviate) = chọn **trade-off internals** (recall/latency/RAM/cost/filter).
- Tune (ef_search/nprobe/quantize) cần biết nó làm gì bên dưới ([[ab07-vector-search-opt]]).
- Debug "recall tụt/latency cao" = hiểu thuật toán.

## ⭐ HNSW — bên trong (graph nhiều tầng)
```
Tầng cao (thưa, "đường cao tốc")  • ──────── •
Tầng giữa                          • ── • ── • ── •
Tầng 0 (dày, mọi điểm)            •-•-•-•-•-•-•-•-•
Search: vào tầng cao -> greedy tới gần -> tụt tầng -> tinh dần ở tầng 0
```
- **M**: số liên kết/node (đồ thị dày) → recall↑, RAM↑, build chậm.
- **ef_construction**: độ rộng tìm khi BUILD → chất lượng graph.
- **ef_search**: độ rộng tìm khi QUERY → recall↑/latency↑ (chỉnh runtime).
- Build = chèn từng điểm, nối tới M hàng xóm gần nhất qua các tầng. **Insert được** (incremental) nhưng xoá khó (thường tombstone + rebuild định kỳ).

## ⭐ IVF-PQ — cụm + nén (tiết kiệm RAM)
```
IVF: k-means chia vector thành nlist cụm -> query chỉ xét nprobe cụm gần nhất
PQ:  chia vector thành m sub-vector, mỗi sub mã hoá bằng codebook 256 tâm
     -> 1 vector 384-float (1536B) -> m byte (vd 48B) -> giảm RAM ~32x
```
- **IVF** giảm số phép so (chỉ nprobe cụm); **PQ** giảm RAM mỗi vector.
- Kết hợp **IVF-PQ**: cụm để lọc nhanh + nén để vừa RAM → cho tỉ vector.
- Đổi lại: PQ **mất chính xác** → thường **rerank bằng vector gốc** top-N ([[ae07-reranking-deep]]).

## ⭐ DiskANN — khi vector vượt RAM
RAM không chứa nổi tỉ vector → để **trên đĩa SSD**:
```
graph (như HNSW) + vector NÉN ở RAM (PQ, để duyệt nhanh)
   + vector GỐC trên SSD (đọc khi cần chấm chính xác)
-> duyệt graph bằng vector nén (RAM) -> chấm cuối bằng vector gốc (SSD)
```
→ Cho phép ANN trên dataset **lớn hơn RAM** với latency chấp nhận được (SSD nhanh). Đây là cách scale tới tỉ-vector mà không cần RAM khổng lồ.

## ⭐ Filtered search internals (vector + metadata)
"tìm vector gần NHƯNG chỉ trong tenant X, sau 2024":
| Chiến lược | Cách | Vấn đề |
|-----------|------|--------|
| Pre-filter | lọc tập con trước rồi ANN | tập con nhỏ → HNSW graph rời rạc, kém hiệu lực |
| Post-filter | ANN rồi lọc | lọc xong < k → phải lấy dư |
| Filter trong lúc duyệt | bỏ qua node không khớp khi traverse graph | tốt nhất; Qdrant/Weaviate hỗ trợ |
→ Vector DB tốt làm **filter trong lúc duyệt** (không pre/post thuần). Filter chọn lọc cao → khó cho ANN.

## Sharding & replication (scale ngang)
- **Shard**: chia vector qua nhiều node (theo hash/tenant) → query fan-out → gộp top-k.
- **Replica**: nhân bản để chịu tải đọc + HA.
- **Consistency**: index mới ghi → khi nào searchable (eventual vs strong) → ảnh hưởng freshness ([[ad01-streaming-rag]]).

## Chọn vector DB (trade-off internals)
| DB | Điểm |
|----|------|
| **pgvector** | đơn giản, trong Postgres; tốt khi data nhỏ-vừa + đã có PG |
| **Qdrant** | filter mạnh, Rust nhanh, payload index |
| **Milvus** | scale lớn, nhiều index type (IVF/HNSW/DiskANN) |
| **Weaviate** | hybrid + module hoá |
| **DuckDB vss** (capstone) | nhúng, không server; tốt prototype/analytics |
→ Chọn theo: quy mô, nhu cầu filter, có sẵn hạ tầng, self-host/cloud.

## Cạm bẫy
- **Dùng như hộp đen** → tune sai (vd ef_search thấp → recall tụt ngầm).
- **PQ không rerank** → recall sập vì nén mất mát → rerank vector gốc.
- **Pre-filter chọn lọc cao** → HNSW kém → dùng filter-trong-duyệt.
- **Quên xoá/tombstone tích tụ** → graph phình, recall giảm → rebuild định kỳ.
- **1 node cho tỉ vector** → OOM → DiskANN/sharding.
- **Eventual consistency** mà cần freshness ngay → hiểu mô hình nhất quán của DB.

## ✅ "Tự kiểm tra & tự mò"
- [ ] HNSW: tầng, M/ef_construction/ef_search; insert được, xoá khó.
- [ ] IVF (cụm/nprobe) + PQ (nén/codebook) → IVF-PQ cho tỉ vector + rerank.
- [ ] DiskANN: graph + PQ ở RAM, vector gốc ở SSD → vượt RAM.
- [ ] Filtered search: pre/post/trong-duyệt; chọn lọc cao là khó.
- [ ] Sharding/replication/consistency; chọn DB theo trade-off.
- 🔭 Tự mò: trong DuckDB vss (capstone), tạo HNSW index với `ef_search` 2 mức (thấp/cao), chạy `rag_eval_harness.py` đo recall + thời gian → thấy ef_search ảnh hưởng thật; thử cắt vector về 8-bit (giả PQ) đo recall tụt + RAM giảm.

➡️ Tiếp [[af05-training-data-scale]] — pipeline training data ở scale.
