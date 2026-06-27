# AA08 — Multimodal Data Pipelines

> Dữ liệu không chỉ text: ảnh, audio, video, PDF scan. DE xây pipeline biến chúng thành **dạng query/embed được**. Liên hệ [[k05-vector-rag-deep]], [[c04-case-iot]] (imagery), [[i03-case-video-streaming]].

## Vì sao multimodal vào DE
LLM/AI giờ xử lý đa phương thức (vision, audio). DE phải **ingest + transform** ảnh/audio/video thành vector/feature/text để search & feed model. Cùng tư duy ETL, input đa dạng hơn.

## Pipeline theo loại dữ liệu
```
ẢNH ─────► image embedding (CLIP) ──► vector store (search ảnh theo text/ảnh)
       └─► OCR (tài liệu scan) ──► text ──► chunk/embed (RAG trên PDF scan)
AUDIO ───► transcription (Whisper) ──► text ──► chunk/embed/search
VIDEO ───► frame sampling + audio track ──► image/text embedding ──► search theo cảnh/lời
```

## Các transform chính (DE orchestrate model inference)
| Modality | Transform | Output |
|----------|-----------|--------|
| Ảnh | **CLIP** embedding | vector (search ảnh↔text cùng không gian) |
| Tài liệu scan/PDF | **OCR** (Tesseract, doc AI) | text → xử lý như tài liệu |
| Audio | **Whisper** transcription | text + timestamp |
| Video | frame sampling (1 frame/N giây) + audio | ảnh + transcript |
- DE không tự train model — **orchestrate inference** (gọi model) → biến media thành text/vector → lưu (object store + vector DB). Giống embedding pipeline ([[ai02-rag-capstone-writeup]]) nhưng thêm bước trích xuất.

## ⭐ CLIP & cross-modal search
CLIP embed **ảnh và text vào CÙNG không gian vector** → tìm ảnh bằng câu mô tả (text query → ảnh gần nhất) hoặc ảnh↔ảnh. Vector store giống RAG, chỉ vector là từ ảnh.

## Multimodal RAG
RAG trên tài liệu có cả text + ảnh + bảng: extract từng loại → embed → retrieve cross-modal → LLM đa phương thức trả lời (vd "biểu đồ trang 5 cho thấy gì"). Chunking phải xử lý layout (text/ảnh/bảng tách đúng).

## Đặc thù vận hành
- **Storage**: media nặng → object store (S3); vector + metadata riêng. Đừng nhét media vào DB ([[55-cloud-fundamentals]]).
- **Cost/latency**: inference ảnh/audio **đắt + chậm** hơn text → batch, GPU, cache ([[ai08-ai-cost-latency]]).
- **Incremental**: media đổi → re-process chỉ cái đó (idempotent theo media_id — [[ai02-rag-capstone-writeup]]).
- **Quality**: OCR/transcription có lỗi → DQ check (confidence, độ dài, ngôn ngữ).
- **Metadata**: timestamp (audio/video), trang (PDF), nguồn → cho filter + citation.

## ⚠️ Cạm bẫy
- Nhét media vào DB thay object store → phình, chậm.
- Quên cost: inference ảnh/audio đắt hơn text nhiều (đo + batch).
- OCR/transcription lỗi không validate → rác vào index.
- Re-process toàn bộ media khi 1 file đổi (phải incremental).
- Trộn không gian vector khác model (CLIP vs text embedding) → search sai ([[ai04-embedding-versioning]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Pipeline cho ảnh/audio/video → vector/text (CLIP/OCR/Whisper).
- [ ] CLIP cross-modal search (ảnh↔text cùng không gian).
- [ ] Multimodal RAG; lưu media ở object store + vector riêng.
- [ ] Cost/incremental/quality cho media.
- 🔭 (cần lib) `pip install pytesseract` OCR một ảnh chứa chữ → text → đưa vào `rag_over_notes.py` index; hoặc đọc CLIP docs, nghĩ search ảnh sản phẩm bằng mô tả.

➡️ Tiếp: [[aa09-graphrag]].
