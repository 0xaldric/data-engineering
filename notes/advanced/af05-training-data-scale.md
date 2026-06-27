# AF05 — LLM Training Data Pipeline ở Scale (petabyte)

> Pipeline chuẩn bị data train LLM ở **web-scale** (petabyte): thu thập → clean → dedup phân tán → quality filter → tokenize → shard → stream tới trainer. Đây là DE thuần ở quy mô cực lớn. Liên hệ [[aa04-training-data-prep]], [[ae03-training-data-quality]], [[ab08-finetune-pipeline]].

## Vì sao khác fine-tune nhỏ
- Fine-tune: nghìn-triệu mẫu, chạy 1 máy ([[ab08-finetune-pipeline]]).
- Pretrain LLM: **tỉ-nghìn tỉ token**, petabyte text → mọi bước phải **phân tán** (Spark/Ray) + streaming.
- Chất lượng data ở scale này = yếu tố #1 quyết định model (hơn cả kiến trúc).

## ⭐ Pipeline web-scale
```
[1 Thu thập] Common Crawl / web / sách / code (petabyte thô)
[2 Trích text] bỏ HTML/boilerplate ([[ad06-doc-parsing]]) -> text sạch
[3 Lọc ngôn ngữ/chất lượng] heuristic + classifier ([[ae03-training-data-quality]])
[4 DEDUP phân tán] exact + near-dup (MinHash/LSH) qua TỈ document ([[aa04-training-data-prep]])
[5 Lọc độc/PII] toxic, PII redact ([[ad03-privacy-compliance]])
[6 DECONTAMINATE] bỏ trùng benchmark/test ([[ab08-finetune-pipeline]])
[7 Tokenize] text -> token id (BPE/SentencePiece)
[8 Shard + mix] chia file + trộn nguồn theo tỉ lệ -> stream tới trainer
```

## ⭐ Dedup ở scale (khó nhất kỹ thuật)
Dedup tỉ document không thể so từng cặp (O(n²)):
```
MinHash mỗi doc (signature nhỏ) -> LSH band -> gom CANDIDATE cùng band
   -> chỉ so trong band (không so toàn bộ) -> O(n) thực tế
chạy PHÂN TÁN: Spark/Ray, shuffle theo band key
```
- Đúng thuật toán `dedup_minhash.py` (capstone) nhưng **phân tán** qua cluster.
- Dedup quan trọng: data trùng → model **memorize** + lãng phí compute + lệch phân phối.
- Cả **fuzzy dedup** (near-dup) lẫn exact; cross-document và intra-document.

## ⭐ Tokenization & sharding
- **Tokenize**: text → token id (BPE). Tokenizer cũng phải train (trên data đại diện). Lưu dạng nén.
- **Shard**: chia thành nghìn file (WebDataset/.tar, Parquet, Mosaic MDS) → trainer đọc song song.
- **Streaming tới trainer**: không load hết vào RAM → stream shard, prefetch, shuffle buffer (đọc tuần tự đĩa nhưng trộn đủ để không bias thứ tự).

## ⭐ Data mixing & weighting (quyết định chất lượng model)
```
nguồn: web 60% + sách 15% + code 15% + wiki 10%  (tỉ lệ là HYPERPARAMETER)
   -> data tốt (wiki/sách) weight cao hơn web nhiễu
   -> curriculum: dễ -> khó, hoặc upsample domain mục tiêu
```
→ Trộn **đúng tỉ lệ** ảnh hưởng lớn tới năng lực model. Đây là quyết định data, không phải model.

## Hạ tầng & công cụ
- **Compute phân tán**: Spark / Ray / Dask / Beam (cho dedup/filter petabyte).
- **Lưu trữ**: object store (S3/GCS), định dạng cột/shard (Parquet/WebDataset/MDS).
- **Orchestration**: pipeline nhiều bước, idempotent, resumable ([[i07-backfill-reprocessing]]).
- **Lineage**: dataset version → biết model train từ data nào ([[af06-ai-data-governance]]).

## Cạm bẫy
- **Dedup O(n²)** → bất khả thi → MinHash+LSH phân tán.
- **Bỏ qua quality filter** → web rác vào → model kém (rác vào rác ra ở scale lớn).
- **Quên decontamination** → benchmark rò → điểm ảo ([[ab08-finetune-pipeline]]).
- **Mixing sai tỉ lệ** → model lệch (quá nhiều code → kém văn xuôi).
- **Không idempotent/resumable** → job petabyte fail giữa chừng = thảm hoạ → checkpoint từng shard.
- **PII/bản quyền** → rủi ro pháp lý ở scale → lọc + provenance + consent.
- **Shuffle kém** → trainer thấy data theo thứ tự bias → shuffle buffer đủ lớn.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao web-scale khác fine-tune (phân tán + streaming).
- [ ] 8 bước pipeline; dedup phân tán (MinHash+LSH) là khó nhất.
- [ ] Tokenize + shard + streaming tới trainer (shuffle buffer).
- [ ] Data mixing/weighting = quyết định chất lượng model.
- [ ] Cạm bẫy: dedup O(n²), quên decontaminate, mixing sai, không resumable.
- 🔭 Tự mò: lấy `dedup_minhash.py`, nghĩ cách biến nó **phân tán**: nhóm theo band key (như shuffle Spark) → chỉ so trong nhóm; ước lượng nếu có 1 tỉ doc, mỗi band trung bình bao nhiêu candidate → thấy vì sao LSH làm dedup khả thi.

➡️ Tiếp [[af06-ai-data-governance]] — governance cho AI.
