# AB05 — Embedding Fine-tuning & Domain Adaptation

> Khi embedding "general" (như bge-small) kém với **domain hẹp** (y tế, luật, tài chính, tiếng Việt) → fine-tune để vector "hiểu" domain. **Vai trò DE: chuẩn bị training pairs + eval cải thiện — không phải train model.** Liên hệ [[ai04-embedding-versioning]], [[ab02-rag-eval-harness]].

## Vì sao embedding general kém domain
- Model train trên web tổng quát → không phân biệt tốt thuật ngữ chuyên ngành.
  - VD y tế: "MI" (myocardial infarction) vs "MI" (Michigan); "cold" (cảm) vs "cold" (lạnh).
  - VD tiếng Việt: model EN-centric hiểu tiếng Việt yếu hơn (capstone vẫn 88% nhưng có thể tốt hơn với model đa ngữ/fine-tune).
- → retrieval trượt: câu hỏi domain không match đúng doc.

## ⭐ Quyết định: fine-tune hay KHÔNG? (rẻ trước, đắt sau)
Theo thứ tự thử (dừng khi đủ tốt — đo bằng [[ab02-rag-eval-harness]]):
```
1. Đổi model tốt hơn / đa ngữ (multilingual-e5, bge-m3)   ← rẻ nhất, thử trước
2. Hybrid search + rerank ([[aa03-rag-production]])         ← bù phần vector trượt
3. Chỉnh chunking / thêm metadata ([[ai03-chunking]])
4. Fine-tune embedding (domain adaptation)                  ← đắt nhất, làm cuối
```
**Đừng fine-tune vội** — thường (1)+(2) đã giải quyết phần lớn. Fine-tune khi domain *thật sự* lệch và đã đo thấy nghẽn ở retrieval.

## ⭐ Fine-tune embedding hoạt động sao — Contrastive Learning
Ý tưởng: **kéo gần** cặp liên quan, **đẩy xa** cặp không liên quan trong không gian vector.
```
        trước fine-tune                  sau fine-tune
   query •   • doc đúng            query •• doc đúng   (kéo gần)
         • doc sai (gần nhầm)                    • doc sai (đẩy xa)
```
- **Positive pair**: (query, doc đúng) — phải gần.
- **Negative pair**: (query, doc sai) — phải xa.
- **⭐ Hard negative**: doc *trông giống* nhưng *sai* — dạy model phân biệt tinh (quan trọng nhất; random negative quá dễ, học được ít).
- Loss: contrastive / triplet / MultipleNegativesRanking.

## ⭐ Vai trò DE: chuẩn bị TRAINING PAIRS (đây là phần của bạn)
Model có sẵn (sentence-transformers) — **data quyết định**. DE lấy pair từ đâu:
| Nguồn | Positive pair |
|-------|---------------|
| **Click/search log** | (query người dùng, doc họ click) ← vàng, có thật |
| **Feedback** 👍/👎 | 👍 = positive, 👎 = hard negative |
| **Q&A / ticket có nhãn** | (câu hỏi, câu trả lời đúng) |
| **Synthetic** ([[ab01-synthetic-data]]) | LLM sinh query cho mỗi doc (khi thiếu log) |
| **Hard negative mining** | retrieve top-k, lấy cái sai-nhưng-điểm-cao làm negative |

Rồi: **clean + dedup + decontaminate** ([[aa04-training-data-prep]]) — test set KHÔNG được rò vào train (nếu không, eval ảo đẹp). Split, version dataset ([[ai04-embedding-versioning]]).

## Vòng đời (DE sở hữu 2 đầu, train ở giữa)
```
[thu pair từ log/feedback] ─> [clean/dedup/decontaminate] ─> [split+version]
   ─> [train: contrastive]  ─> [EVAL: recall@k trước vs sau — ab02] ─> [blue-green deploy + RE-EMBED toàn corpus]
        (ML/bạn)                  (DE đo cải thiện THẬT)                  (ai04 — đổi model = re-index hết)
```
⚠️ **Đổi embedding model = phải re-embed TOÀN BỘ corpus** (vector cũ/mới không cùng không gian) → tốn, cần blue-green index ([[ai04-embedding-versioning]]).

## Cạm bẫy
- **Fine-tune mà không đo** → không biết có tốt hơn không (phải so recall@k trước/sau bằng [[ab02-rag-eval-harness]]).
- **Decontamination quên** → test rò vào train → recall ảo cao, thật thì fail.
- **Random negative** (không hard) → model học hời hợt, ít cải thiện.
- **Overfit domain hẹp** → mất khả năng tổng quát (đánh giá cả in-domain lẫn out).
- **Quên re-embed corpus** sau khi đổi model → query vector mới đập vào doc vector cũ → vô nghĩa.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao embedding general kém domain (thuật ngữ, ngôn ngữ).
- [ ] Thứ tự thử trước khi fine-tune (đổi model → hybrid → chunk → mới fine-tune).
- [ ] Contrastive learning + hard negative là gì.
- [ ] Vai trò DE = training pairs (nguồn) + decontaminate + eval, KHÔNG train.
- [ ] Đổi model ⇒ re-embed toàn corpus.
- 🔭 Tự mò: từ `rag_over_notes.py`, tạo "training pairs" giả: mỗi golden query là positive với note đúng; mine hard negative = note bị retrieve nhầm ở top-k; in ra file pairs (không cần train — chỉ hiểu data fine-tune trông thế nào).

➡️ Tiếp [[ab06-llm-observability]] — trace mọi request LLM.
