# AB07 — Vector Search Optimization (sâu)

> Tune tìm kiếm vector ở scale: ANN index (HNSW/IVF) + **quantization** + filter strategy. Bài toán cân **recall ⇄ latency ⇄ RAM ⇄ cost** — không có "tốt nhất", chỉ có "đúng cho ràng buộc của bạn". Sâu hơn [[k05-vector-rag-deep]], [[aa10-llmops]].

## Vì sao cần (nhắc nhanh)
Brute-force so cosine với **mọi** vector = O(n·d). 1454 vector (capstone) thì OK; **triệu/tỉ** vector thì sập → cần **ANN** (Approximate NN): nhanh hơn nhiều, đổi lại **bỏ sót đôi chút** (recall < 100%). Cả trò chơi là **chỉnh để recall đủ cao mà vẫn nhanh/rẻ**.

## ⭐ HNSW — tham số & trade-off
Graph nhiều tầng, "nhảy" gần dần tới NN (đa số vector DB dùng).
| Param | Tăng lên thì | Trade-off |
|-------|--------------|-----------|
| **M** (số liên kết/node) | recall ↑, graph dày | RAM ↑, build chậm ↑ |
| **ef_construction** (lúc build) | chất lượng graph ↑ → recall ↑ | build chậm ↑ |
| **ef_search** (lúc query) | recall ↑ | latency ↑ (**chỉnh runtime được!**) |
→ **ef_search là nút vặn lúc chạy**: cần recall cao hơn → tăng ef_search (chậm hơn); cần nhanh → giảm. Tune theo SLA.

## ⭐ IVF — tham số & trade-off
Chia vector thành `nlist` cụm (k-means); query chỉ xét `nprobe` cụm gần nhất.
| Param | Ý nghĩa | Trade-off |
|-------|---------|-----------|
| **nlist** | số cụm | nhiều cụm → mỗi cụm nhỏ, nhanh nhưng dễ trượt biên |
| **nprobe** | số cụm xét lúc query | ↑ → recall ↑, latency ↑ (nút vặn runtime) |
→ IVF hợp dataset **rất lớn, tĩnh**; HNSW hợp **recall cao + update động** nhưng tốn RAM hơn.

## ⭐⭐ Quantization — giảm RAM (chìa khoá ở scale tỉ vector)
Vector gốc FLOAT32 384-chiều = 1536 byte/vector. 1 tỉ vector ≈ **1.5 TB RAM** → không khả thi. Nén:
| Cách | Ý tưởng | Giảm RAM | Mất chính xác |
|------|---------|----------|---------------|
| **SQ** (scalar) | float32 → int8 mỗi chiều | ~4× | ít |
| **PQ** (product) | chia vector thành sub-vector, mã hoá bằng codebook | ~8–32× | vừa |
| **Binary** | mỗi chiều → 1 bit, so bằng Hamming | ~32× | nhiều (cần rerank lại bằng vector gốc) |
→ Mẫu hình phổ biến: **quantize để lọc nhanh (coarse) → rerank top-N bằng vector gốc (chính xác)**. Cân RAM↓ vs recall↓.

## ⭐ Filter + vector: pre vs post
Truy vấn thật hay kèm lọc metadata ("doc tiếng Việt, sau 2024, của tenant X"):
```
PRE-filter:  lọc metadata TRƯỚC → ANN trên tập con
   + chính xác (đúng số k sau lọc)   - lọc xong tập nhỏ làm ANN index kém hiệu lực
POST-filter: ANN top-k TRƯỚC → bỏ cái không khớp filter
   + tận dụng index   - lọc xong có thể còn < k kết quả (phải lấy dư k rồi lọc)
```
→ Vector DB tốt cho **filtered ANN** (index hỗ trợ metadata). Multi-tenancy ([[aa03-rag-production]]) = filter theo tenant; pre-filter thường an toàn hơn cho cách ly.

## Hybrid weight & rerank (nhắc)
- **Hybrid** (vector + keyword [[aa03-rag-production]]): trọng số α cân hai điểm — tune bằng harness ([[ab02-rag-eval-harness]], đã thấy hybrid 88% > vector 75%).
- **Rerank**: ANN lấy top-50 (recall cao, thô) → cross-encoder rerank xuống top-5 (chính xác). Cải thiện **thứ hạng** (MRR/nDCG) mà tăng k không làm được.

## ⭐ Quy trình tune (đừng vặn mù)
```
1. Đặt SLA: recall ≥ ?, p99 latency ≤ ?, RAM/cost budget ≤ ?
2. Đo baseline bằng harness ([[ab02-rag-eval-harness]]) — recall@k + latency
3. Vặn 1 nút/lần (ef_search, nprobe, quantize) → đo lại → giữ nếu trong SLA
4. Recall thấp? ↑ef_search/nprobe, bỏ/giảm quantize, thêm rerank
   Latency cao? ↓ef_search/nprobe, thêm quantize, shard
   RAM cao? quantize (PQ), shard qua node
```

## Cạm bẫy
- **Vặn mù không đo** → tưởng nhanh hơn nhưng recall tụt thầm lặng (ANN giấu lỗi: vẫn trả kết quả, chỉ là sai). Luôn đo recall.
- **Quá tin ANN = exact** → ANN là *xấp xỉ*; bài toán cần chính xác tuyệt đối (vd dedup pháp lý) phải rerank/verify.
- **Quantize quá tay** → recall sập; nhớ rerank bằng vector gốc.
- **Build index lại từ đầu mỗi update** → dùng incremental/upsert; rebuild định kỳ.
- **Bỏ qua filter selectivity** → filter rất chọn lọc thì pre-filter; filter rộng thì post-filter.

## ✅ "Tự kiểm tra & tự mò"
- [ ] HNSW: M / ef_construction / ef_search — cái nào vặn runtime, đổi gì.
- [ ] IVF: nlist / nprobe; khi nào IVF vs HNSW.
- [ ] Quantization (SQ/PQ/binary): giảm RAM bao nhiêu, mất gì, vì sao cần rerank.
- [ ] Pre vs post filter — ưu nhược.
- [ ] Tune bằng SLA + harness, vặn 1 nút/lần, luôn đo recall.
- 🔭 Tự mò: trong `rag_over_notes.py`, DuckDB HNSW có `ef_search` — thử đặt 2 mức (thấp/cao), chạy `rag_eval_harness.py` đo recall + thời gian, xem trade-off thật. Thử cắt vector xuống 8-bit (giả quantize) rồi đo recall tụt bao nhiêu.

➡️ Tiếp [[ab08-finetune-pipeline]] — pipeline data cho fine-tuning.
