# AG06 — Multimodal AI in Production (video/ảnh scale)

> Đưa multimodal ([[ae04-multimodal-rag]]) lên **production scale**: video/ảnh nặng, GPU đắt, pipeline phức tạp. Bài toán DE khắc nghiệt nhất về cost/storage. Liên hệ [[ac05-voice-audio-pipeline]], [[af05-training-data-scale]], [[ad06-doc-parsing]].

## Vì sao video/ảnh ở scale là "ác mộng" data
- **Nặng**: 1 video = GB; triệu video = petabyte → storage + băng thông khổng lồ.
- **Đắt xử lý**: encode/decode + embed cần **GPU** → cost cực lớn so với text.
- **Phức tạp**: video = chuỗi frame + audio + thời gian → nhiều tầng trích xuất.
- → Mọi quyết định bị chi phối bởi **cost & storage**, không như text rẻ.

## ⭐ Pipeline video → searchable
```
video ─> [transcode] chuẩn hoá codec/độ phân giải (giảm dung lượng)
      ─> [frame sampling] KHÔNG xử lý mọi frame (30fps×giờ = quá nhiều)
                          -> lấy keyframe / 1 frame/giây / scene-change
      ─> [scene detection] cắt theo cảnh -> đơn vị có nghĩa
      ─> [trích đa tầng]: visual embed (CLIP) + audio→STT ([[ac05-voice-audio-pipeline]]) + OCR chữ trên màn
      ─> [index] vector (visual+text) + metadata (video_id, timestamp, scene)
      ─> object store video gốc (S3) + CDN phân phối
query (text/ảnh) ─> cross-modal retrieve ([[ae04-multimodal-rag]]) -> trả về CLIP đoạn (timestamp)
```

## ⭐ Frame sampling — chìa khoá cost
Xử lý mọi frame = bất khả thi (1 giờ × 30fps = 108k frame):
| Chiến lược | Lấy frame nào | Khi dùng |
|-----------|---------------|----------|
| **Uniform** | 1 frame/N giây | đơn giản, baseline |
| **Keyframe** | frame "đại diện" (I-frame) | rẻ, tận dụng codec |
| **Scene-change** | khi cảnh đổi (diff lớn) | giữ nội dung đổi, bỏ frame tĩnh lặp |
| **Adaptive** | dày ở đoạn động, thưa ở tĩnh | tối ưu nhất, phức tạp |
→ Bỏ frame trùng/tĩnh → giảm 100× chi phí embed mà giữ nội dung. Đây là **dedup theo thời gian**.

## ⭐ Cost & storage (DE đau đầu nhất)
- **Tiering**: video gốc nặng → cold storage/Glacier; embedding + thumbnail (nhẹ) → hot.
- **Incremental**: chỉ xử lý video mới ([[ad01-streaming-rag]]); cache embedding (đừng re-encode).
- **Batch GPU**: gom video xử lý theo lô giờ thấp điểm (GPU đắt).
- **Resolution phù hợp**: embed ở độ phân giải thấp đủ dùng (không cần 4K để hiểu nội dung).
- **CDN**: phân phối video tới người dùng (không serve từ origin).

## Ứng dụng & eval
| Case | Cần |
|------|-----|
| **Video search** | "tìm đoạn nói về X" → cross-modal + timestamp |
| **Kiểm duyệt nội dung** | phát hiện vi phạm (visual + audio + text) → cần recall cao, latency |
| **Recommendation** | embedding video → gợi ý tương tự ([[ac02-recsys-llm]]) |
- Eval: golden đa phương thức (query→đoạn đúng); đo recall + cost/giờ video.

## Cạm bẫy
- **Xử lý mọi frame** → đốt GPU vô ích → frame sampling.
- **Lưu mọi thứ ở hot tier** → cost storage nổ → tiering theo nhiệt.
- **Re-encode/re-embed toàn bộ** → tốn → incremental + cache.
- **Embed độ phân giải cao không cần** → chậm/đắt → resolution vừa đủ.
- **Bỏ qua audio/OCR** → mất nội dung (lời nói, chữ trên màn) → trích đa tầng.
- **Serve video từ origin** → quá tải → CDN.
- **Không đo cost/giờ video** → chi phí ngầm bùng → unit economics ([[ac08-ai-cost-scale]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao video/ảnh scale = bài toán cost/storage khắc nghiệt.
- [ ] Pipeline: transcode→sample→scene→trích đa tầng (visual/STT/OCR)→index.
- [ ] Frame sampling (uniform/keyframe/scene/adaptive) = dedup thời gian, giảm 100× cost.
- [ ] Cost: tiering, incremental, batch GPU, resolution vừa, CDN.
- [ ] Ứng dụng (search/kiểm duyệt/reco) + eval cross-modal + cost/giờ.
- 🔭 Tự mò: lấy 1 video ngắn, dùng `ffmpeg` trích 1 frame/giây (frame sampling) + scene-change (`ffmpeg select='gt(scene,0.4)'`); đếm frame giảm bao nhiêu so với mọi frame; (nếu có CLIP) embed các keyframe, query bằng text tìm đoạn — multimodal search mini.

➡️ Tiếp [[ag07-conversational-memory]] — memory hội thoại dài.
