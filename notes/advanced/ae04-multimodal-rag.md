# AE04 — Multimodal RAG sâu (ảnh + text)

> RAG vượt khỏi text: tìm kiếm **xuyên phương thức** (text↔ảnh↔audio) nhờ **không gian embedding chung**. Hỏi bằng chữ tìm ra ảnh, và ngược lại. Sâu hơn [[aa08-multimodal]], [[ad06-doc-parsing]], [[ac05-voice-audio-pipeline]].

## Vì sao cần
- Dữ liệu thật **đa phương thức**: tài liệu có ảnh/biểu đồ, sản phẩm có hình, hỗ trợ có ảnh chụp lỗi, y tế có X-quang.
- Text-RAG **mù** với nội dung trong ảnh → bỏ sót thông tin → cần RAG hiểu cả ảnh.

## ⭐ Chìa khoá: Shared Embedding Space (CLIP)
```
"con mèo" ─(text encoder)─┐
                          ├─> CÙNG không gian vector ─> ảnh mèo & chữ "con mèo" GẦN nhau
🖼️ ảnh mèo ─(image encoder)┘
```
- **CLIP** (và họ): train text encoder + image encoder để ảnh và mô tả của nó **gần nhau** trong cùng không gian.
- → Cosine giữa **text vector** và **image vector** có nghĩa → cross-modal retrieval.

## ⭐ Cross-modal retrieval (4 hướng)
| Truy vấn → Kết quả | Ví dụ |
|--------------------|-------|
| text → ảnh | "biểu đồ doanh thu quý 3" → tìm ảnh chart |
| ảnh → text | upload ảnh lỗi → tìm doc mô tả/khắc phục |
| ảnh → ảnh | sản phẩm giống (recsys ảnh [[ac02-recsys-llm]]) |
| text → text | RAG thường |
→ Tất cả nhờ **một không gian chung** → một vector store, query bất kỳ phương thức.

## ⭐ OCR vs Visual embedding (chọn đúng)
| Cách | Khi nào | Bỏ lỡ gì |
|------|---------|----------|
| **OCR → text** ([[ad06-doc-parsing]]) | ảnh chứa **CHỮ** (scan, screenshot, hoá đơn) | bố cục, hình, biểu đồ phi-text |
| **Visual embedding** (CLIP) | nội dung **HÌNH ẢNH** (vật thể, cảnh, sơ đồ) | chữ chi tiết trong ảnh |
| **Cả hai** | tài liệu hỗn hợp (chữ + hình) | — |
→ Hoá đơn → OCR; ảnh sản phẩm → visual; trang tài liệu có cả → kết hợp.

## Multimodal chunking & indexing
```
tài liệu (text + ảnh)
 ─> tách: đoạn text -> embed text ; ảnh -> embed visual (+ caption nếu có)
 ─> ảnh kèm CAPTION/ngữ cảnh xung quanh -> embed cả hai -> truy được bằng chữ
 ─> lưu: vector + ref tới file gốc (object store) + metadata (trang, loại, nguồn)
 ─> retrieve: query -> tìm cả chunk text lẫn ảnh liên quan -> đưa LLM đa phương thức
```
- Ảnh **nên có caption/alt-text** (người viết hoặc model sinh) → tăng khả năng tìm bằng chữ.
- Lưu **ảnh ở object store** (S3...), vector store chỉ giữ embedding + ref (ảnh nặng [[ac05-voice-audio-pipeline]]).

## ⭐ Pipeline data ảnh (DE lo phần nặng)
- **Object store** cho file gốc (ảnh/video nặng) + tiering/retention (cost).
- **Incremental**: chỉ embed ảnh mới ([[ad01-streaming-rag]]); cache embedding (đắt hơn text).
- **Cost**: image embedding + multimodal LLM đắt hơn text nhiều → batch, sample, chỉ xử lý ảnh cần.
- **Chất lượng**: ảnh mờ/rác → embedding rác → lọc (như DQ [[ae03-training-data-quality]]).

## Cạm bẫy
- **Trộn 2 không gian** (CLIP cho ảnh, model khác cho text) vào 1 index → cosine vô nghĩa → phải **cùng họ model** (CLIP cho cả hai phía).
- **Dùng OCR cho ảnh phi-text** (sơ đồ, vật thể) → ra rác → visual embedding.
- **Quên caption ảnh** → không tìm được bằng chữ → sinh caption.
- **Nhồi ảnh nặng vào vector store** → phình → object store + ref.
- **Bỏ qua cost** → image/multimodal LLM đốt tiền → batch + chỉ xử lý cần thiết.
- **Đánh giá chỉ trên text** → không biết retrieval ảnh tốt không → golden đa phương thức ([[ab02-rag-eval-harness]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Shared embedding space (CLIP) — vì sao text↔ảnh so được.
- [ ] 4 hướng cross-modal retrieval.
- [ ] OCR vs visual embedding — chọn theo nội dung ảnh.
- [ ] Multimodal chunking: caption + object store + ref.
- [ ] Pipeline data ảnh: incremental, cost, chất lượng.
- [ ] Cạm bẫy: trộn không gian, quên caption, ảnh nặng vào vector store.
- 🔭 Tự mò: cài `fastembed` image model (vd CLIP qua onnx) hoặc dùng sentence-transformers CLIP; embed vài ảnh + mô tả của chúng; thử query bằng chữ tìm đúng ảnh (cross-modal); đo cosine text↔ảnh-đúng vs text↔ảnh-sai.

➡️ Tiếp [[ae05-edge-ai-data]] — AI trên thiết bị / edge.
