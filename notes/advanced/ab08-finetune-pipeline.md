# AB08 — Data Pipeline cho Fine-tuning Workflow

> Pipeline **end-to-end chuẩn bị data** để fine-tune LLM (instruction/preference tuning). **DE sở hữu phần DATA (thu thập → sạch → format → version → eval-set), không train model.** Reproducibility là vua. Liên hệ [[aa04-training-data-prep]], [[ai04-embedding-versioning]], [[ab05-embedding-finetune]].

## Fine-tune cái gì? (DE chuẩn bị data cho mỗi loại)
| Loại | Data cần | Mục tiêu |
|------|----------|----------|
| **SFT** (instruction tuning) | (instruction, response) đúng | model làm theo lệnh |
| **Preference** (DPO/RLHF) | (prompt, chosen, rejected) | model "thích" câu tốt hơn |
| **Domain continued pretrain** | text domain thô (lượng lớn) | model ngấm domain |
| **Embedding** ([[ab05-embedding-finetune]]) | (query, positive, negative) | vector hiểu domain |

## ⭐ Pipeline end-to-end (DE làm các ô không phải "train")
```
[1 thu thập] → [2 clean/dedup] → [3 decontaminate] → [4 format] → [5 split] → [6 version]
     │                                                                                   │
     └─ nguồn: log thật, feedback 👍👎, expert label, synthetic (ab01)        train ──────┘→ [7 EVAL] → deploy
```

### 1. Thu thập (collection)
- Nguồn: production log (input/output thật), human label (expert), feedback 👍/👎 (→ preference pair), synthetic ([[ab01-synthetic-data]] khi thiếu).
- Ghi **nguồn gốc** mỗi mẫu (provenance) → audit "model học từ đâu".

### 2. Clean & Dedup ([[aa04-training-data-prep]])
- Bỏ rác, PII redact ([[aa02-guardrails]]), lọc chất lượng (độ dài, ngôn ngữ, toxic).
- **Dedup near-dup** (MinHash/LSH) → trùng lặp làm model overfit + phí compute.

### 3. ⭐ Decontamination (CỰC QUAN TRỌNG — hay bị quên)
Loại mọi mẫu **trùng/giống test/benchmark** khỏi train. Quên → model "thuộc bài thi" → điểm eval ảo cao, thực tế kém. Đây là lỗi nghiêm trọng & âm thầm nhất.

### 4. Format (chuẩn hoá)
- Đưa về **chat template** đúng của model (system/user/assistant turns).
- Schema thống nhất (JSONL: `{"messages":[...]}` hoặc `{"prompt","chosen","rejected"}`).
- Validate schema từng dòng ([[ai06-llm-output-governance]] — như data contract).

### 5. Split
- train / validation / **test giữ riêng** (test KHÔNG đụng vào tuning, để eval cuối khách quan).
- Cẩn thận **leakage** giữa các split (cùng user/cùng doc rơi 2 bên).

### 6. ⭐ Version dataset (reproducibility)
- Version data như version code ([[ai04-embedding-versioning]]): hash nội dung, tag `v1.2`, lineage.
- "Model checkpoint X train từ dataset version Y" → **tái lập được** + debug khi model lỗi.
- Công cụ: DVC / lakeFS / data version trong registry.

### 7. Eval (đo, không "cảm thấy tốt")
- Chạy golden set ([[aa06-llm-eval]]) **trước vs sau** fine-tune → có cải thiện thật?
- Regression: không được tệ đi ở năng lực cũ (catastrophic forgetting).
- Embedding thì đo recall@k ([[ab02-rag-eval-harness]]).

## ⭐ Thông điệp: fine-tune là bài toán DATA, không phải bài toán model
> "Garbage in, garbage out" — model có sẵn, **chất lượng data quyết định** kết quả fine-tune. 80% công sức là pipeline data (thu/sạch/dedup/decontaminate/format/version), 20% là chạy train. Đây đúng là **chỗ DE tạo giá trị**.

## Khi nào KHÔNG nên fine-tune (cân nhắc trước)
- **RAG đủ chưa?** Cần *kiến thức mới* → RAG ([[aa03-rag-production]]) thường rẻ/nhanh hơn fine-tune.
- **Prompt engineering đủ chưa?** Cần *đổi hành vi nhẹ* → prompt ([[aa07-prompt-management]]).
- Fine-tune khi: cần *phong cách/format ổn định*, *giảm token prompt*, *domain rất hẹp* — và đã đo RAG/prompt không đủ.
- (Cùng tinh thần thứ-tự-rẻ-trước ở [[ab05-embedding-finetune]].)

## Cạm bẫy
- **Quên decontaminate** → eval ảo, thật thì kém (lỗi #1).
- **Data bẩn/trùng** → overfit, lãng phí compute.
- **Không version dataset** → không tái lập, không debug được "vì sao model v3 tệ".
- **Test rò vào train** (leakage) → mọi con số eval vô nghĩa.
- **Fine-tune khi RAG/prompt đã đủ** → tốn tiền vô ích.
- **Catastrophic forgetting** → giỏi task mới, quên task cũ; phải eval cả hai.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 4 loại fine-tune (SFT/preference/continued/embedding) cần data gì.
- [ ] 7 bước pipeline; DE sở hữu bước nào.
- [ ] Decontamination là gì, vì sao quên nó là thảm hoạ.
- [ ] Vì sao version dataset = reproducibility.
- [ ] Khi nào KHÔNG fine-tune (RAG/prompt trước).
- 🔭 Tự mò: dùng `synthetic_data.py` ([[ab01-synthetic-data]]) sinh data → format thành JSONL chat template `{"messages":[{"role":"user",...},{"role":"assistant",...}]}` → dedup ([[aa04-training-data-prep]]) → split 80/10/10 → in stats mỗi split (số mẫu, phân phối nhãn, độ trùng giữa train/test = decontamination check).

➡️ Tiếp [[ab09-ai-review2]] — tổng kết AI-Advanced 2 + checklist phỏng vấn.
