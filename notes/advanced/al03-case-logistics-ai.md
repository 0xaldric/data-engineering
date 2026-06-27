# AL03 — Case Study: Logistics/Supply-chain AI

> AI logistics: tối ưu tuyến, dự báo nhu cầu, tracking, anomaly giao hàng. Nhấn: **real-time + tối ưu + dự báo time-series**; LLM bổ trợ không tự điều phối. Khung 7 bước ([[af09-ai-review6]]). Liên hệ [[ak08-timeseries-tabular-fm]], [[i02-case-logistics]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: giao nhanh/rẻ (tối ưu tuyến), không thiếu/thừa hàng (dự báo), minh bạch (tracking).
- **Data chính**: vị trí (GPS real-time), đơn hàng, tồn kho, time-series nhu cầu.
- **Ràng buộc**: real-time (xe/đơn đổi liên tục), quy mô lớn (nghìn xe/triệu đơn), tối ưu (bài toán NP-hard).

## 2. ⭐ Thành phần (AI + tối ưu cổ điển)
| Thành phần | Kỹ thuật |
|-----------|----------|
| **Route optimization** | thuật toán tối ưu (VRP) — KHÔNG phải LLM; LLM giải thích/điều chỉnh |
| **Demand forecast** | time-series FM/model ([[ak08-timeseries-tabular-fm]]) → đặt hàng/phân bổ |
| **Tracking chatbot** | RAG trạng thái đơn + tool query ([[ad05-structured-rag]]) |
| **Anomaly giao hàng** | phát hiện chậm/lệch bất thường real-time ([[ag04-drift-detection]]) |
| **RAG tài liệu vận hành** | SOP, quy trình kho ([[ae08-rag-for-code]] kiểu cho doc) |

## 3. ⭐ Ranh giới: AI tối ưu vs LLM (quan trọng)
```
TỐI ƯU TUYẾN: bài toán toán học (VRP, constraint) -> SOLVER chuyên, KHÔNG LLM
   LLM kém tính toán/tối ưu số ([[ag01-rag-bi-analytics]])
LLM Ở ĐÂU: giải thích kế hoạch ("vì sao tuyến này"), chatbot tracking, đọc/tóm tài liệu,
           xử lý ngoại lệ ngôn ngữ ("khách báo đổi địa chỉ")
```
→ **Đừng dùng LLM cho việc solver làm tốt hơn**. LLM cho ngôn ngữ + giải thích + RAG, không cho tối ưu số.

## 4. Kiến trúc (real-time + batch)
```
GPS/đơn/tồn kho ─stream─> [real-time: vị trí, trạng thái, anomaly] ([[ai09-streaming-ai]])
   ─> route solver (tối ưu) + demand forecast (time-series) [batch + cập nhật]
   ─> tracking: khách hỏi -> RAG trạng thái + tool ETA
   ─> điều phối: gợi ý cho người điều phối -> NGƯỜI quyết (không LLM tự điều xe)
```

## Cạm bẫy
- **Dùng LLM tối ưu tuyến** → kém solver → dùng solver, LLM giải thích.
- **LLM tự điều phối xe/đơn** → sai = tốn kém vật lý → người quyết ([[ad04-llm-security]]).
- **Forecast bỏ mùa vụ/sự kiện** → đặt hàng sai → time-series có mùa vụ ([[ak08-timeseries-tabular-fm]]).
- **Tracking bịa ETA** → khách mất tin → số từ hệ thống, LLM diễn giải.
- **Real-time dùng data cũ** → điều phối sai → streaming.
- **Anomaly false-alarm** → bỏ qua → calibrate ngưỡng.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: route/forecast/tracking/anomaly/RAG-SOP.
- [ ] ⭐ Ranh giới: solver tối ưu (không LLM), LLM giải thích/RAG/ngôn ngữ.
- [ ] LLM không tự điều phối (hậu quả vật lý).
- [ ] Real-time + batch; forecast có mùa vụ.
- [ ] Cạm bẫy: LLM tối ưu, bịa ETA, data cũ.
- 🔭 Tự mò: viết chatbot tracking mini — "đơn #123 đâu rồi?" → tra dict trạng thái (tool) → LLM diễn giải ETA bằng câu tự nhiên; thử câu "tối ưu tuyến cho 5 điểm" → nhận ra nên gọi solver (nearest-neighbor heuristic) không phải LLM bịa thứ tự.

➡️ Tiếp [[al04-case-media-ai]] — case study media/streaming.
