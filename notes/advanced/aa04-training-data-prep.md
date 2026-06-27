# AA04 — Training / Fine-tuning Data Prep (vai trò DE) ⭐

> Train/fine-tune LLM cần **dữ liệu sạch quy mô lớn** — đó là việc DE (không phải data scientist). "Garbage in, garbage out" càng đúng với LLM. Code chạy được: [`dedup_minhash.py`](../../projects/06-ai-data-engineering/dedup_minhash.py).

## Vai trò DE trong training data
DE xây pipeline: thu thập → **dedup** → lọc chất lượng → format → decontaminate → mix → versioned dataset. Chất lượng dataset quyết định chất lượng model hơn cả kiến trúc.

## ⭐ Near-duplicate detection (MinHash + LSH)
Corpus có nhiều bản **gần-trùng** (cùng nội dung, reword/reformat) → model **học lệch** (overweight nội dung lặp), lãng phí, leakage. So từng cặp = **O(n²)** bất khả ở tỉ doc.
```
shingle (k-gram) → MinHash signature (ước lượng Jaccard rẻ) → LSH (chỉ so cặp ỨNG VIÊN) → Jaccard → dedup
```
- **MinHash**: nén tập shingle thành signature N số; agreement của signature ≈ Jaccard (xác suất min-hash bằng nhau = Jaccard). Đổi so-tập-lớn → so-N-số.
- **LSH** (Locality-Sensitive Hashing): chia signature thành **band**; doc cùng band-bucket = ứng viên → chỉ so các cặp này (không phải tất cả). Nhiều band × ít row = nhạy (recall cao); ít band × nhiều row = chặt (precision cao) — **tune** theo nhu cầu.
- Demo: 7 docs → LSH **3 cặp ứng viên** (vs 21 brute-force) → bắt exact-dup (J=1.0) + reword (J≈0.44) → bỏ trùng, giữ 5/7. LSH **xấp xỉ** (có thể miss — tune band để cân recall/precision).

(Liên hệ DS&A: hashing/sketch — [[g07-dsa-for-de]], [[g08-probabilistic-ds]].)

## Quality filtering
Loại dữ liệu rác trước khi train:
- **Heuristic**: độ dài, tỉ lệ ký tự lạ/số, ngôn ngữ (lang detect), boilerplate (header/footer lặp), perplexity (model nhỏ chấm "tự nhiên" không).
- **Toxicity/PII** filter ([[aa02-guardrails]], [[64-governance-pii]]).
- **Dedup** (trên) — quan trọng nhất.
- Classifier "chất lượng cao" (vd giống Wikipedia/sách).

## ⭐ Decontamination
Loại **dữ liệu test/benchmark** khỏi **train** (tránh model "học thuộc" bài test → đánh giá ảo). Tìm overlap train↔test (cũng bằng MinHash/n-gram match). Nghiêm túc với eval đáng tin. (Giống "data leakage" — [[c09-case-recsys]] point-in-time.)

## Instruction / RLHF data format
- **Instruction tuning**: cặp `(instruction, input, output)` chuẩn hoá format.
- **Preference/RLHF**: `(prompt, chosen, rejected)` — cặp so sánh.
- DE: thu thập, chuẩn hoá schema, validate ([[ai06-llm-output-governance]]), version.

## Data mixing & versioning
- **Mixing**: tỉ lệ các nguồn (code/web/sách/đa ngôn ngữ) ảnh hưởng model → thử nghiệm tỉ lệ.
- **Versioning dataset**: dataset có version (như code/model) → reproduce + so model train trên dataset nào (lineage — [[34-delta-lake]] time travel cho dataset).

## ⚠️ Cạm bẫy
- Không dedup → model overfit nội dung lặp, lãng phí compute.
- O(n²) so cặp trên dữ liệu lớn → phải MinHash+LSH.
- Quên decontamination → eval ảo (model thấy test khi train).
- LSH tune sai band → miss nhiều dup (recall thấp) hoặc quá nhiều candidate (chậm).
- Không version dataset → không reproduce model.
- PII/bản quyền trong train data (rủi ro pháp lý).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao dedup quan trọng; MinHash ước lượng Jaccard thế nào; LSH giảm so-cặp.
- [ ] Tune band: nhạy (recall) vs chặt (precision).
- [ ] Decontamination & vì sao (eval ảo).
- [ ] Quality filter + versioning dataset.
- 🔭 Chạy `dedup_minhash.py`; thêm 1 doc reword của d5/d7 xem có bị bắt; đổi `BANDS/ROWS` (8×8 vs 32×2) xem candidate/recall đổi.

➡️ Tiếp: [[aa05-agentic-pipelines]].
