# AC01 — RAG Đa Ngôn Ngữ / Cross-lingual ⭐ (có code chạy được)

> Khi corpus + người dùng **đa ngôn ngữ** (VN dùng tiếng Việt lẫn tài liệu tiếng Anh), embedding EN-centric retrieve kém. Đo bằng số rồi chọn cách khắc phục. Code: [`cross_lingual_eval.py`](../../projects/06-ai-data-engineering/cross_lingual_eval.py). Liên hệ [[ai04-embedding-versioning]], [[ab02-rag-eval-harness]].

## Vấn đề
- Tài liệu công ty VN thường **trộn**: doc tiếng Việt + tài liệu/kỹ thuật tiếng Anh.
- Người dùng hỏi khi tiếng Việt, khi tiếng Anh, khi **trộn cả hai** ("làm sao optimize cái pipeline này").
- Embedding **EN-centric** (bge-small) map ngôn ngữ khác vào không gian **lệch** → câu hỏi và doc cùng nghĩa nhưng khác ngôn ngữ **không nằm gần nhau** → retrieve trượt.

## ⭐ Đo thật (code chạy trên capstone)
Index chứa note **tiếng Việt** (embed bge-small EN-centric). Bắn cùng câu hỏi ở 2 ngôn ngữ:
```
recall@5   VI = 83%    EN = 67%    chênh = +17%
```
→ Query **tiếng Anh** rớt 17% so với tiếng Việt (cùng ngôn ngữ với doc). Có câu EN vẫn trúng (nhiều token chung như "parquet/kafka") nhưng tổng thể tệ hơn. **Đây là "thuế đa ngữ" định lượng được** — lý do để nâng cấp model, không phải "cảm thấy".

## ⭐ 3 cách khắc phục (chọn theo ràng buộc)
| Cách | Làm gì | Ưu | Nhược |
|------|--------|----|-------|
| **1. Embedding đa ngữ** | đổi sang **multilingual-e5 / bge-m3 / LaBSE** | 1 không gian chung mọi ngôn ngữ; query bất kỳ match doc bất kỳ | model to hơn, phải **re-embed toàn corpus** ([[ai04-embedding-versioning]]) |
| **2. Dịch rồi embed** | dịch query (hoặc doc) về 1 ngôn ngữ chung trước khi embed | dùng được model mạnh 1 ngôn ngữ | thêm bước dịch (cost/latency/lỗi dịch); mất sắc thái |
| **3. Per-language index** | mỗi ngôn ngữ 1 index + route theo ngôn ngữ phát hiện | tối ưu từng ngôn ngữ | không cross-lingual (EN hỏi không thấy doc VI); phức tạp |
→ **Mặc định nên: (1) embedding đa ngữ** — đơn giản, đúng bản chất "1 không gian ngữ nghĩa chung". (2) khi buộc giữ model cũ. (3) khi mỗi ngôn ngữ tách bạch rõ.

## ⭐ Cross-lingual retrieval là gì
Mục tiêu: query ngôn ngữ A **tìm được** doc ngôn ngữ B nếu **cùng nghĩa**. Model đa ngữ tốt đặt "ngân hàng" (VI) và "bank" (EN) gần nhau → hỏi tiếng Việt vẫn lôi được doc tiếng Anh. Đây là siêu năng lực thật sự cho corpus trộn.

## Pipeline DE cho RAG đa ngữ
```
ingest doc (nhiều ngôn ngữ) ─> [detect language] (lưu metadata lang)
   ─> embed bằng model ĐA NGỮ ─> 1 vector store chung
query (bất kỳ ngôn ngữ) ─> cùng model ─> search ─> (tuỳ chọn) filter/boost theo lang ưa thích
   ─> rerank ─> LLM trả lời (chỉ định ngôn ngữ output theo người dùng)
```
- Lưu `language` làm **metadata** → filter/boost được ([[ab07-vector-search-opt]] pre/post filter).
- Eval phải có golden **đa ngữ** (query mỗi ngôn ngữ) — không chỉ test 1 thứ tiếng ([[ab02-rag-eval-harness]]).

## Cạm bẫy
- **Giả định "model nào cũng đa ngữ"** → sai; bge-small EN-centric (đã đo rớt 17%). Phải chọn model **được train đa ngữ**.
- **Chỉ eval 1 ngôn ngữ** → mù với phần rớt ở ngôn ngữ kia → golden phải đa ngữ.
- **Trộn 2 model (EN cho doc EN, model khác cho doc VI)** vào **1 index** → 2 không gian khác nhau, cosine vô nghĩa. Phải **một model** cho cả index.
- **Dịch sai** (cách 2) → kéo theo retrieve sai; tên riêng/thuật ngữ dễ hỏng.
- **Quên output ngôn ngữ**: retrieve đúng nhưng LLM trả lời sai ngôn ngữ người dùng → chỉ định rõ trong prompt.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao embedding EN-centric rớt với corpus/query ngôn ngữ khác (đo 83% vs 67%).
- [ ] 3 cách khắc phục + khi nào chọn cái nào.
- [ ] Cross-lingual retrieval = query A tìm doc B cùng nghĩa.
- [ ] Vì sao 1 index phải dùng **một** model; golden phải đa ngữ.
- 🔭 Tự mò: cài `fastembed` model đa ngữ (vd `intfloat/multilingual-e5-small`) trong `rag_over_notes.py`, re-embed, chạy lại `cross_lingual_eval.py` — xem recall EN có **đuổi kịp** VI không (kỳ vọng gap thu hẹp). Đó là bằng chứng số cho việc nâng cấp model.

➡️ Tiếp [[ac02-recsys-llm]] — recommendation bằng embedding + LLM.
