# AL04 — Case Study: Media/Streaming AI

> AI media/streaming: content reco, kiểm duyệt, tóm tắt/tag, search video. Nhấn: **scale nội dung khổng lồ**, real-time personalization, moderation an toàn, cost GPU video. Liên hệ [[ac02-recsys-llm]], [[ag06-multimodal-production]], [[af08-case-personalization]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: giữ chân người xem (reco hợp gu), nội dung an toàn (moderation), dễ tìm (search/tag).
- **Data**: video/audio/ảnh nặng + hành vi xem (real-time, khổng lồ).
- **Ràng buộc**: scale cực lớn, latency thấp (reco/search), cost GPU (xử lý video [[ag06-multimodal-production]]), an toàn (nội dung độc/bản quyền).

## 2. ⭐ Thành phần
| Thành phần | Kỹ thuật |
|-----------|----------|
| **Content reco** | embedding video + hành vi, real-time profile ([[af08-case-personalization]]) |
| **Moderation** | multimodal (visual+audio+text) phát hiện vi phạm ([[ag06-multimodal-production]]) |
| **Tóm tắt/tag tự động** | LLM/multimodal sinh metadata từ nội dung |
| **Search video** | cross-modal (text→đoạn video [[ae04-multimodal-rag]]) + timestamp |
| **Subtitle/dịch** | STT + dịch ([[ac05-voice-audio-pipeline]]) |

## 3. ⭐ Content moderation (an toàn + scale)
```
nội dung upload (khổng lồ) ─> [tự động: model phát hiện vi phạm nhanh]
   ─> rõ ràng vi phạm -> chặn ; nghi ngờ -> [human review queue] ([[ag05-agent-platform]])
   ─> multimodal: visual (bạo lực/NSFW) + audio (lời) + text (caption/comment)
   ─> recall cao (bỏ sót vi phạm nguy hiểm) + human cho ranh giới
```
→ Không thể human duyệt mọi video (scale) → AI lọc + human cho ca khó. Recall an toàn cao (bỏ sót > false-positive ở nội dung nguy hiểm).

## 4. ⭐ Scale & cost (đặc thù media)
- **Video nặng**: frame sampling, transcode, tiering, CDN ([[ag06-multimodal-production]]) — cost GPU lớn nhất.
- **Reco real-time**: hành vi xem → profile cập nhật ngay ([[af08-case-personalization]]); pre-compute candidate.
- **Incremental**: chỉ xử lý nội dung mới ([[ad01-streaming-rag]]); cache embedding.
- **Cold-start nội dung mới**: content embedding gợi được ngay ([[ac02-recsys-llm]]).

## 5. Eval & vấn đề đặc thù
- **Eval engagement** (watch time, retention) nhưng coi chừng **filter bubble/echo chamber** → thêm đa dạng ([[ae07-reranking-deep]] MMR).
- **Bản quyền**: phát hiện nội dung vi phạm bản quyền (fingerprint).
- **Bias/an toàn**: reco không đẩy nội dung độc hại để tăng engagement (alignment [[aj02-ai-alignment]]).

## Cạm bẫy
- **Human duyệt mọi nội dung** → không scale → AI lọc + human ca khó.
- **Moderation recall thấp** → nội dung nguy hiểm lọt → recall an toàn cao.
- **Xử lý mọi frame video** → đốt GPU → frame sampling.
- **Reco tối ưu engagement mù** → filter bubble + đẩy nội dung độc → đa dạng + an toàn.
- **Cold-start nội dung mới vô hình** → content embedding.
- **Bỏ qua cost GPU** → chi phí video nổ → tiering + incremental + đo cost/giờ.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: reco/moderation/tóm-tắt/search/subtitle.
- [ ] Moderation: AI lọc + human ca khó; recall an toàn cao.
- [ ] Scale/cost video: frame sampling, CDN, incremental.
- [ ] Eval engagement nhưng chống filter bubble + an toàn.
- [ ] Cạm bẫy: human duyệt hết, recall thấp, engagement mù.
- 🔭 Tự mò: dùng `semantic_recsys.py` ([[ac02-recsys-llm]]) làm content reco, thêm **MMR** (phạt item giống cái đã gợi) để tăng đa dạng → so "thuần liên quan" vs "có đa dạng" → thấy chống filter bubble; thêm flag "đã xem" loại khỏi gợi ý.

➡️ Tiếp [[al05-case-hr-ai]] — case study HR/recruiting.
