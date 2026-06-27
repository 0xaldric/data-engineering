# AC05 — Voice/Audio AI Data Pipeline

> Biến **audio** (call center, voice note, họp, podcast) thành dữ liệu tìm kiếm/phân tích được: STT → diarization → align → chunk → index. **Audio là modality nặng — DE lo ingest/cost/PII.** Liên hệ [[aa08-multimodal]], [[ab06-llm-observability]], [[ai03-chunking]].

## Vì sao audio khó hơn text
- **Không cấu trúc + nặng**: 1 giờ audio ≈ vài chục MB, xử lý chậm/đắt hơn text nhiều.
- **Cần "phiên dịch"**: phải STT (speech-to-text) mới search/analytics được.
- **Nhiều người nói**: cần biết **ai** nói câu nào (diarization).
- **Thời gian thực**: call center cần gần real-time; có timestamp để tua.
- **PII kép**: nội dung (số thẻ, tên) **+ giọng nói** (biometric) đều nhạy cảm.

## ⭐ Pipeline audio → dữ liệu dùng được
```
audio file/stream
   ─> [1 STT: Whisper]        ─> transcript + timestamp mỗi từ/câu
   ─> [2 Diarization]         ─> "Speaker A/B/C" gán cho từng đoạn
   ─> [3 Alignment]           ─> ghép transcript + speaker + thời gian
   ─> [4 Chunk]               ─> cắt theo lượt nói/câu/thời lượng ([[ai03-chunking]])
   ─> [5 Embed + index]       ─> vector store (RAG trên audio — [[aa08-multimodal]])
   ─> [6 Analytics/Redact]    ─> sentiment, topic, PII redact ([[aa02-guardrails]])
```
| Bước | Công cụ | DE lo gì |
|------|---------|----------|
| STT | Whisper (local), Deepgram, AssemblyAI | batch lớn, GPU, retry, cost |
| Diarization | pyannote, NeMo | gán speaker, độ chính xác |
| Align | tự ghép theo timestamp | đồng bộ 2 nguồn (STT + diar) |
| Chunk | theo lượt/câu/30s | giữ ngữ cảnh hội thoại |
| Index | fastembed + vector DB | như RAG text |

## ⭐ Transcript = dữ liệu hạng nhất (mô hình hoá)
Sau STT, audio thành **bảng có cấu trúc** → analytics y như text:
```
fact_utterance:
  call_id | speaker | start_ms | end_ms | text | sentiment | pii_flag
```
- Search: "khách nào nhắc tới hoàn tiền?" → query transcript.
- Analytics: thời lượng nói/agent, % cuộc gọi tiêu cực, topic phổ biến.
- Compliance: agent có đọc disclaimer bắt buộc không? (kiểm transcript).
→ Đúng **dimensional modeling** ([[../18-scd.md|dimensional]]): cuộc gọi = fact, speaker/agent/time = dimension. "Danh từ đổi (audio), tư duy DE không đổi."

## ⭐ Chunking audio khác text
- Cắt theo **lượt nói (turn)** hoặc **khoảng lặng** (silence), không cắt giữa câu đang nói.
- Giữ **timestamp** trong metadata → click kết quả search tua đúng giây audio gốc (citation [[aa03-rag-production]]).
- Hội thoại dài → chunk theo cửa sổ thời gian + overlap (giữ mạch).

## PII & compliance (đặc thù audio)
- **Nội dung**: STT xong → redact số thẻ/CMND/tên trong **transcript** ([[aa02-guardrails]]).
- **Giọng nói = sinh trắc học**: bản thân audio là PII → mã hoá lưu trữ, kiểm soát truy cập, retention.
- **Đồng ý ghi âm**: pháp lý (GDPR/luật VN) — chỉ xử lý audio được phép.
- **Redact cả audio**: bíp đè đoạn nhạy cảm nếu cần lưu/chia sẻ.

## Cost & scale (DE đau đầu nhất)
- STT đắt (GPU/giây audio) → **batch giờ thấp điểm**, ưu tiên cuộc cần gấp.
- **Incremental**: chỉ xử lý file mới ([[ai09-streaming-ai]]); cache transcript (đừng STT lại).
- **Sampling** cho analytics: không cần STT 100% nếu chỉ lấy thống kê.
- Lưu transcript (rẻ, nhỏ) lâu dài; audio gốc (nặng) → tier rẻ/xoá theo retention.

## Cạm bẫy
- **STT lỗi domain** (thuật ngữ, tên riêng, tiếng Việt giọng vùng) → transcript sai → mọi thứ sau sai; cần đo WER (word error rate), fine-tune/từ điển domain.
- **Bỏ qua diarization** → không biết ai nói → phân tích agent vs khách bất khả.
- **Mất timestamp** → không tua được về audio gốc, citation vô dụng.
- **Quên PII trong audio gốc** (chỉ redact transcript) → vẫn rò qua file giọng.
- **STT lại từ đầu mỗi lần** → đốt tiền; phải cache/incremental.
- **Coi audio như text nhẹ** → bùng cost storage/compute.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 6 bước pipeline audio (STT→diar→align→chunk→embed→analytics/redact).
- [ ] Vì sao transcript = dữ liệu hạng nhất; mô hình hoá fact_utterance.
- [ ] Chunk audio khác text (turn/silence + timestamp).
- [ ] PII kép (nội dung + giọng = sinh trắc học) + đồng ý ghi âm.
- [ ] Cost: batch/incremental/cache/sampling/tiering.
- 🔭 Tự mò: cài `faster-whisper` (local, không API), STT 1 file audio ngắn → in transcript + timestamp; cắt theo câu thành "chunk", embed bằng `rag_over_notes.embed`, thử search 1 câu hỏi vào các chunk audio. Đó là RAG-trên-audio thu nhỏ.

➡️ Tiếp [[ac06-kb-freshness]] — giữ knowledge base tươi.
