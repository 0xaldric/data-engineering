# AM07 — Case Study: Agriculture/AgriTech AI

> AI nông nghiệp: phân tích ảnh cây/sâu bệnh, dự báo mùa vụ, RAG kiến thức canh tác. Nhấn: **multimodal + edge (đồng ruộng mạng yếu) + đa ngữ nông dân**. Khung 7 bước. Liên hệ [[ae04-multimodal-rag]], [[ae05-edge-ai-data]], [[k04-case-agritech]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: tăng năng suất (phát hiện bệnh sớm, tưới/bón đúng), hỗ trợ nông dân (tư vấn canh tác).
- **Người dùng**: nông dân (nhiều trình độ, đa ngôn ngữ/dân tộc, ít công nghệ).
- **Ràng buộc**: edge (đồng ruộng mạng yếu/offline), multimodal (ảnh cây + sensor), chi phí thấp (nông dân nhỏ).

## 2. ⭐ Thành phần
| Thành phần | Kỹ thuật |
|-----------|----------|
| **Chẩn đoán sâu bệnh** | ảnh lá/cây → model phân loại bệnh (multimodal [[ae04-multimodal-rag]]) |
| **Dự báo mùa vụ/thời tiết** | time-series (thời tiết/độ ẩm/sản lượng — [[ak08-timeseries-tabular-fm]]) |
| **RAG kiến thức canh tác** | hỏi "lúa vàng lá làm sao" → tài liệu nông nghiệp, plain language |
| **Tối ưu tưới/bón** | sensor đất + model → khuyến nghị |
| **Edge** | chạy trên điện thoại/thiết bị đồng ruộng ([[ae05-edge-ai-data]]) |

## 3. ⭐ Edge-first (đặc thù nông nghiệp)
```
đồng ruộng: mạng yếu/không có -> KHÔNG dựa cloud real-time
   -> model nhỏ chẩn đoán bệnh CHẠY TRÊN ĐIỆN THOẠI (offline [[ae05-edge-ai-data]])
   -> chụp ảnh lá -> phân loại bệnh ngay (không cần mạng)
   -> sync kết quả/data khi có mạng (về cloud tổng hợp)
```
→ Privacy/latency/offline → edge bắt buộc. Cloud cho tổng hợp + model update OTA.

## 4. ⭐ Accessibility nông dân (như government)
- **Đa ngôn ngữ/dân tộc**: nông dân nói nhiều thứ tiếng → model đa ngữ + voice ([[ac01-multilingual-rag]], [[ac05-voice-audio-pipeline]]).
- **Plain language + voice**: nhiều nông dân ít đọc → giao tiếp giọng nói, đơn giản ([[ak04-case-govt-ai]]).
- **Chi phí thấp**: nông dân nhỏ → model local rẻ, không API đắt.

## 5. Multimodal + dữ liệu đặc thù
- **Ảnh cây/lá**: chất lượng ảnh đồng ruộng kém (ánh sáng/góc) → robust + chỉ dẫn chụp.
- **Sensor đất/thời tiết**: time-series ([[ak05-case-manufacturing-ai]] IoT) → dự báo.
- **Vệ tinh/drone**: ảnh diện rộng (NDVI sức khoẻ cây) → phân tích vùng.

## Cạm bẫy
- **Dựa cloud real-time** → đồng ruộng mất mạng → edge offline.
- **Giao diện phức tạp/ngôn ngữ khó** → nông dân không dùng → plain language + voice.
- **Model ảnh train phòng lab** → ảnh đồng ruộng thật kém → train/eval data thực địa.
- **API đắt** → nông dân nhỏ không kham → model local rẻ.
- **Bỏ đa ngôn ngữ** → loại nông dân dân tộc → đa ngữ.
- **Chẩn đoán bịa bệnh** → nông dân phun thuốc sai → grounding + độ tin + chuyên gia.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: chẩn đoán bệnh/dự báo/RAG-canh-tác/tưới-bón/edge.
- [ ] Edge-first: model trên điện thoại offline, sync khi có mạng.
- [ ] Accessibility: đa ngữ + voice + plain language + chi phí thấp.
- [ ] Multimodal: ảnh đồng ruộng robust + sensor time-series.
- [ ] Cạm bẫy: dựa cloud, giao diện khó, model lab, chẩn đoán bịa.
- 🔭 Tự mò: phác pipeline chẩn đoán bệnh edge — (ý tưởng) model nhỏ phân loại ảnh lá → nếu không chắc (confidence thấp [[ae01-self-correcting-rag]]) → "chụp lại rõ hơn" hoặc RAG "triệu chứng X có thể là bệnh Y"; voice trả lời tiếng địa phương. Edge + multimodal + accessibility ghép lại.

➡️ Tiếp [[am08-coding-exercises-3]] — bài tập retrieval/fusion/eval.
