# AH05 — Data cho Multimodal LLM Training

> Train model đa phương thức (CLIP, vision-LLM) cần **image-text pairs** ở scale web. Khác data text thuần: phải đảm bảo **ảnh khớp text**, lọc cặp rác. Sâu hơn [[af05-training-data-scale]] cho multimodal. Liên hệ [[ae04-multimodal-rag]], [[ag06-multimodal-production]].

## Đơn vị data: image-text PAIR
- Model đa ngữ học từ **cặp (ảnh, mô tả)**: ảnh con mèo + caption "con mèo đen" → học liên kết.
- Scale web: **LAION** (tỉ cặp lấy từ web: ảnh + alt-text), DataComp, COYO.
- Chất lượng **cặp** quyết định: ảnh-text **không khớp** → model học sai liên kết.

## ⭐ Pipeline data multimodal (web-scale)
```
crawl web ─> trích (ảnh src + alt-text/text xung quanh) = cặp thô (tỉ cặp, rất nhiễu)
   ─> [1 CLIP-score filter] ảnh-text có KHỚP không? (điểm thấp -> bỏ)
   ─> [2 lọc chất lượng ảnh] độ phân giải, NSFW, watermark, trùng
   ─> [3 dedup] ảnh trùng (perceptual hash) + text trùng ([[aa04-training-data-prep]])
   ─> [4 lọc text] độ dài, ngôn ngữ, rác, PII
   ─> [5 dedup vs test/benchmark] decontaminate ([[ab08-finetune-pipeline]])
   ─> cặp sạch -> train
```

## ⭐ CLIP-score filtering (đặc thù multimodal — quan trọng nhất)
```
alt-text web RẤT nhiễu: "IMG_2024.jpg", "click here", text không liên quan ảnh
-> dùng model CLIP có sẵn chấm: cosine(embed ảnh, embed text)
   cao = ảnh-text khớp (giữ) ; thấp = không khớp (bỏ)
```
→ Đây là **self-bootstrapping**: dùng model multimodal cũ lọc data train model mới. Lọc CLIP-score là bước **tăng chất lượng lớn nhất** (LAION-Aesthetics, DataComp đều dựa vào).

## ⭐ Captioning (sinh/cải thiện caption)
- Alt-text web nghèo/sai → **sinh caption** bằng model (BLIP/LLaVA) → caption giàu hơn.
- Re-caption: thay alt-text rác bằng mô tả model sinh (nhiều dataset hiện đại làm vậy).
- Lọc caption sinh (chất lượng, không hallucinate mô tả sai ảnh — [[ag02-hallucination-detection]]).

## Dedup ảnh (khác dedup text)
| Loại | Cách |
|------|------|
| **Exact** | hash file (md5) |
| **Near-dup** | **perceptual hash** (pHash) — ảnh giống dù resize/nén khác |
| **Semantic** | embedding ảnh (CLIP) gần nhau ([[aa04-training-data-prep]] MinHash cho text, pHash cho ảnh) |
→ Ảnh trùng → model memorize + lệch phân phối; web đầy ảnh lặp (logo, stock).

## Cạm bẫy
- **Không CLIP-filter** → cặp ảnh-text không khớp → model học sai liên kết (rác vào rác ra).
- **Alt-text web tin tưởng mù** → rất nhiễu → filter + re-caption.
- **Dedup text mà quên dedup ảnh** → ảnh trùng lọt → pHash.
- **Quên decontaminate** → benchmark ảnh rò → điểm ảo ([[ab08-finetune-pipeline]]).
- **NSFW/bản quyền/PII trong ảnh** → rủi ro pháp lý + an toàn → lọc ([[af06-ai-data-governance]]).
- **Caption sinh hallucinate** → mô tả sai ảnh → lọc caption.
- **Bias trong cặp** (alt-text web thiên lệch) → model học bias → audit ([[ab01-synthetic-data]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Đơn vị = image-text pair; chất lượng cặp quyết định.
- [ ] Pipeline: CLIP-filter → lọc ảnh → dedup → lọc text → decontaminate.
- [ ] ⭐ CLIP-score filter (ảnh-text khớp) = bước tăng chất lượng lớn nhất.
- [ ] Captioning/re-caption thay alt-text rác.
- [ ] Dedup ảnh = perceptual hash (khác MinHash text).
- [ ] Cạm bẫy: tin alt-text mù, quên dedup ảnh, NSFW/bản quyền.
- 🔭 Tự mò: (ý tưởng) nếu có CLIP, lấy 10 cặp (ảnh, caption) — vài cặp khớp, vài cặp ghép sai caption — tính CLIP-score mỗi cặp, đặt ngưỡng lọc cặp sai; so với dùng `data_quality_score.py` ([[ae03-training-data-quality]]) cho phần text caption (độ dài/dup/toxic).

➡️ Tiếp [[ah06-rag-benchmarks]] — benchmark RAG công khai.
