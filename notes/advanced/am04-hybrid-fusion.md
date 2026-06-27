# AM04 — Hybrid Search Tuning: RRF & Fusion ⭐ (có code chạy được)

> Cách **kết hợp** vector + keyword: gộp ĐIỂM (weighted) vs gộp THỨ HẠNG (RRF). RRF robust hơn vì không cần chuẩn hoá thang. Code: [`rrf_fusion.py`](../../projects/06-ai-data-engineering/rrf_fusion.py). Sâu hơn [[aa03-rag-production]], [[ae07-reranking-deep]].

## Vì sao "gộp" là vấn đề
- Vector (cosine ∈ [0,1]) và keyword (BM25 ∈ [0,∞)) **khác thang điểm** → cộng thẳng vô nghĩa.
- Gộp sai → 1 tín hiệu lấn át / nhiễu kéo nhầm.
- → Cần cách gộp **đúng**: chuẩn hoá thang (weighted) HOẶC bỏ điểm dùng thứ hạng (RRF).

## ⭐ Reciprocal Rank Fusion (RRF) — gộp THỨ HẠNG
```
mỗi hệ (vector, keyword) cho 1 BẢNG XẾP HẠNG
RRF score(doc) = Σ  1 / (C + rank_trong_hệ_đó)      (C ~ 60)
   doc xếp #1 ở vector + #3 ở keyword -> 1/61 + 1/63
-> KHÔNG dùng điểm thô -> không cần chuẩn hoá thang khác nhau!
```
- C (≈60) giảm ảnh hưởng hạng thấp (doc #1 vs #2 khác nhiều; #100 vs #101 gần như nhau).
- Doc xuất hiện cao ở **nhiều** hệ → score cao → lên top.

## ⭐⭐ Kết quả thật (đo trên capstone) — RRF robust hơn weighted
```
method                  recall@5
vector-only                100%      <- embedding tốt (no-prefix [[ah02]])
keyword-only                62%      <- chỉ trùng từ, yếu
RRF                        100%      <- giữ vững
weighted(vec+0.1kw)         88%      <- TỤT! keyword nhiễu kéo nhầm
```
**Phát hiện**:
- **weighted TỤT xuống 88%**: cộng `0.1×keyword` kéo note trùng-từ-nhưng-sai lên → hại (α chưa tune).
- **RRF giữ 100%**: gộp thứ hạng **không bị 1 tín hiệu nhiễu phá** → robust hơn.
- → ⭐ **Thêm keyword KHÔNG luôn tốt** + **RRF an toàn hơn weighted**. Lại bài học "đo, đừng tin mặc định" ([[ah02-embedding-benchmark]]).

## Weighted fusion (gộp ĐIỂM) — khi nào dùng
```
score = α·norm(vec) + (1-α)·norm(keyword)     (phải CHUẨN HOÁ về cùng thang)
   + tune α được (kiểm soát tỉ trọng) ; - cần chuẩn hoá + tune, nhạy nhiễu
```
- Dùng khi: muốn **kiểm soát tỉ trọng** + đã chuẩn hoá + tune α trên golden ([[ab02-rag-eval-harness]]).
- RRF dùng khi: muốn **đơn giản + robust** + không muốn lo chuẩn hoá thang.

## So sánh
| | RRF | Weighted |
|--|-----|----------|
| Gộp theo | thứ hạng | điểm |
| Chuẩn hoá thang | KHÔNG cần | CẦN |
| Tune | chỉ C (ít nhạy) | α (nhạy) |
| Robust nhiễu | cao | thấp hơn |
| Kiểm soát tỉ trọng | ít | nhiều |
→ **RRF mặc định tốt** (đơn giản, robust). Weighted khi cần kiểm soát + đã tune.

## Cạm bẫy
- **Cộng thẳng điểm khác thang** (cosine + BM25) → vô nghĩa → chuẩn hoá hoặc RRF.
- **Giả định "thêm keyword luôn tốt"** → SAI (đo: weighted tụt 88%) → đo trên data.
- **Weighted không tune α** → tỉ trọng sai → nhiễu lấn → tune trên golden.
- **RRF C quá nhỏ/lớn** → quá nhạy/phẳng hạng → C~60 chuẩn, thử.
- **Không đo fusion vs đơn lẻ** → tưởng fusion tốt mà tệ hơn → harness so sánh.
- **keyword-only cho ngữ nghĩa** → trượt ý (62%) → cần vector.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao gộp khó (vector vs keyword khác thang).
- [ ] RRF: gộp thứ hạng, 1/(C+rank), không cần chuẩn hoá.
- [ ] ⭐ Đo thật: weighted tụt 88%, RRF giữ 100% → RRF robust hơn.
- [ ] Weighted khi cần kiểm soát α (đã chuẩn hoá + tune).
- [ ] Cạm bẫy: cộng khác thang, thêm-keyword-luôn-tốt, không đo.
- 🔭 Tự mò: sửa `rrf_fusion.py` — thử C ∈ {10, 60, 200} xem recall RRF đổi không; tune α weighted (0.02, 0.1, 0.5) tìm mức không tụt; thêm "rerank" sau RRF (top-10 RRF → rerank cosine) đo MRR.

➡️ Tiếp [[am05-eval-metrics-deep]] — metric eval sâu.
