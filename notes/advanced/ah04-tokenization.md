# AH04 — Tokenization Deep-dive

> Token là **đơn vị tính tiền + đơn vị context** của LLM. Hiểu tokenization để ước cost, quản context, và biết vì sao **tiếng Việt đắt hơn tiếng Anh**. Liên hệ [[ac08-ai-cost-scale]], [[ai03-chunking]], [[af05-training-data-scale]].

## Token là gì & vì sao quan trọng
- LLM không đọc "từ" hay "ký tự" → đọc **token** (mảnh từ): "engineering" → ["engineer", "ing"].
- **Cost theo token** ([[ac08-ai-cost-scale]]): input + output token = tiền.
- **Context window theo token**: 8k/128k token, không phải ký tự → biết token mới ước được "nhồi được bao nhiêu".
- Chunking ([[ai03-chunking]]) đo bằng token (size 512 token), không phải ký tự.

## ⭐ Các thuật toán tokenize
| Thuật toán | Ý tưởng | Dùng ở |
|-----------|---------|--------|
| **BPE** (Byte-Pair Encoding) | gộp dần cặp ký tự/byte hay đi cùng → subword | GPT, nhiều LLM |
| **WordPiece** | tương tự BPE, chọn theo likelihood | BERT |
| **SentencePiece** | tokenize raw text (không cần tách từ trước), byte-level | đa ngữ (T5, Llama) |
- **Subword**: cân bằng giữa ký tự (vocab nhỏ, chuỗi dài) và từ (vocab to, OOV) → mảnh từ.
- **Vocab size** (vd 32k–256k): lớn → ít token/câu nhưng model nặng hơn; nhỏ → ngược lại.

## ⭐⭐ Tiếng Việt/Á ĐẮT hơn tiếng Anh (rất quan trọng)
Tokenizer chủ yếu train trên **tiếng Anh** → ngôn ngữ khác bị cắt vụn hơn:
```
"data engineering"        -> ~2-3 token (tiếng Anh, có sẵn trong vocab)
"kỹ thuật dữ liệu"        -> ~6-10 token (dấu + âm tiết bị tách nhỏ, byte-level)
cùng NGHĨA, tiếng Việt tốn 2-4× token!
```
**Hệ quả thực tế:**
- **Đắt hơn**: cùng nội dung, tiếng Việt tốn nhiều token → trả tiền nhiều hơn ([[ac08-ai-cost-scale]]).
- **Context ngắn hơn**: 8k token chứa ít chữ tiếng Việt hơn tiếng Anh → nhồi được ít hơn.
- **Chunking**: 512 token tiếng Việt = ít nội dung hơn 512 token tiếng Anh → điều chỉnh chunk.
- → Ngôn ngữ ít tài nguyên bị "thuế token" (token tax). Model/tokenizer đa ngữ tốt giảm thuế này.

## Special tokens
```
[BOS]/[EOS]  bắt đầu/kết thúc chuỗi
[PAD]        đệm cho batch
[SEP]/[CLS]  phân tách/đại diện (BERT)
chat template: <|system|>...<|user|>...<|assistant|>  (token đặc biệt định vai)
```
→ Format sai special token (chat template [[ab08-finetune-pipeline]]) → model hiểu sai cấu trúc.

## ⭐ Vai trò DE: ước cost & context bằng token
```
ước cost 1 request = (token_prompt + token_output) × giá/token
   token_prompt ≈ token(system) + token(context RAG) + token(câu hỏi)
context budget: tổng phải < context window
   -> tiếng Việt: nhân hệ số "token tax" khi ước (đừng dùng tỉ lệ tiếng Anh)
```
- Đếm token thật bằng tokenizer của model (tiktoken/HF), **không** đoán bằng số từ/ký tự.
- Prompt phình âm thầm → đo token/request theo thời gian (cost drift [[aa10-llmops]]).

## Cạm bẫy
- **Ước cost bằng số ký tự/từ** → sai (token ≠ từ); dùng tokenizer thật.
- **Quên token tax tiếng Việt** → ước cost/context thấp hơn thực → vượt budget/cắt cụt.
- **Chunk theo ký tự** → không khớp context budget token → chunk theo token.
- **Sai special token/chat template** → model hiểu sai vai → dùng đúng template model.
- **Vocab không phủ domain** (mã, ký hiệu hiếm) → cắt vụn → token tốn + nghĩa kém.
- **Bỏ qua output token** (thường đắt hơn input) → ước thiếu → giới hạn độ dài output.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Token = đơn vị cost + context; subword (BPE/WordPiece/SentencePiece).
- [ ] ⭐ Tiếng Việt tốn 2-4× token tiếng Anh (token tax) → đắt + context ngắn.
- [ ] Special token / chat template.
- [ ] Ước cost & context budget bằng token thật, không đoán.
- [ ] Cạm bẫy: ước bằng ký tự, quên token tax, chunk theo ký tự.
- 🔭 Tự mò: cài `tiktoken` (hoặc tokenizer HF của model bạn dùng), đếm token cho cùng 1 đoạn ở tiếng Việt vs bản dịch tiếng Anh → đo "token tax" thật (tỉ lệ); thử 1 note của bạn xem ~bao nhiêu token → ước nhồi được mấy note vào context 8k.

➡️ Tiếp [[ah05-multimodal-training-data]] — data train multimodal.
