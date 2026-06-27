# AK05 — Case Study: Manufacturing/IoT AI

> AI sản xuất/IoT: predictive maintenance, anomaly detection, RAG tài liệu kỹ thuật, edge AI. Nhấn: **time-series sensor scale lớn**, real-time edge, LLM bổ trợ chẩn đoán (không tự dừng máy). Liên hệ [[c04-case-iot]], [[ae05-edge-ai-data]], [[ak08-timeseries-tabular-fm]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: giảm downtime (bảo trì dự đoán), phát hiện lỗi sớm, hỗ trợ kỹ thuật viên.
- **Data chính**: **time-series sensor** (nhiệt độ/rung/áp suất) — tần suất cao, nhiều thiết bị → scale khổng lồ ([[c04-case-iot]]).
- **Ràng buộc**: real-time (lỗi máy phải báo ngay), edge (nhà máy mạng yếu), an toàn (dừng máy sai = tốn kém/nguy hiểm).

## 2. ⭐ Thành phần (time-series + LLM kết hợp)
| Thành phần | Kỹ thuật |
|-----------|----------|
| **Predictive maintenance** | model time-series dự đoán hỏng ([[ak08-timeseries-tabular-fm]]) + LLM giải thích |
| **Anomaly detection** | phát hiện bất thường sensor real-time ([[g08-probabilistic-ds]]) |
| **RAG tài liệu kỹ thuật** | kỹ thuật viên hỏi manual/sửa chữa ([[ae08-rag-for-code]] kiểu cho tài liệu máy) |
| **Digital twin** | mô phỏng máy + AI dự đoán kịch bản |
| **Copilot kỹ thuật viên** | "máy báo lỗi E27, sửa sao?" → RAG manual + lịch sử |

## 3. ⭐ Kiến trúc (edge + cloud)
```
sensor (IoT, tần suất cao) ─> [EDGE: lọc/aggregate/anomaly nhanh] ([[ae05-edge-ai-data]])
   ─> chỉ gửi bất thường/tóm tắt lên cloud (không gửi raw khổng lồ — băng thông)
cloud ─> time-series model (predictive) + RAG manual + lịch sử bảo trì
   ─> lỗi dự đoán -> [LLM giải thích + RAG cách sửa] -> kỹ thuật viên
   ─> hành động (dừng máy/đặt phụ tùng) -> RULE + người, KHÔNG để LLM tự dừng ([[ad04-llm-security]])
```

## 4. ⭐ Thách thức time-series scale (đặc thù IoT)
- **Volume khổng lồ**: nghìn sensor × tần suất cao = tỉ điểm/ngày → downsampling, aggregate ở edge ([[c04-case-iot]]).
- **Real-time**: anomaly phải phát hiện ngay → stream processing ([[ai09-streaming-ai]]).
- **Edge constraint**: nhà máy mạng yếu/offline → model nhỏ chạy local ([[ae05-edge-ai-data]]).
- **LLM cho time-series**: serialize chuỗi số → text, hoặc time-series FM ([[ak08-timeseries-tabular-fm]]); LLM mạnh ở **giải thích** + RAG, không phải dự báo số thô.

## 5. ⭐ LLM bổ trợ, KHÔNG tự quyết (an toàn vật lý)
- LLM **giải thích** chẩn đoán + **gợi ý** cách sửa (RAG manual) → kỹ thuật viên làm.
- Hành động vật lý (dừng dây chuyền, đặt phụ tùng) → **rule + người duyệt**, không LLM tự quyết ([[ad04-llm-security]] excessive agency — ở đây hậu quả vật lý).
- Sai → tốn kém/nguy hiểm vật lý → conservative.

## Cạm bẫy
- **Gửi raw sensor lên cloud** → băng thông/cost nổ → aggregate/lọc ở edge.
- **LLM tự dừng máy** → dừng sai = tốn kém/nguy hiểm → rule + người.
- **Dùng LLM dự báo số thô** → LLM kém số → time-series model chuyên ([[ak08-timeseries-tabular-fm]]), LLM giải thích.
- **Bỏ qua edge offline** → mất giám sát khi mất mạng → model local.
- **Anomaly nhiều false-alarm** → kỹ thuật viên bỏ qua → calibrate ngưỡng ([[ag04-drift-detection]]).
- **Manual lỗi thời** → gợi ý sửa sai → freshness tài liệu kỹ thuật ([[ac06-kb-freshness]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: predictive maintenance/anomaly/RAG-manual/digital-twin/copilot.
- [ ] Kiến trúc edge (lọc/anomaly) + cloud (model + RAG); gửi bất thường không gửi raw.
- [ ] Time-series scale: volume, real-time, edge; LLM giải thích không dự báo số.
- [ ] LLM bổ trợ không tự quyết hành động vật lý.
- [ ] Cạm bẫy: gửi raw, LLM dừng máy, false-alarm.
- 🔭 Tự mò: tạo chuỗi sensor giả (bình thường + vài spike), viết anomaly detector đơn giản (z-score/ngưỡng) phát hiện spike; với mỗi anomaly, mock-RAG tra "mã lỗi → cách sửa" từ một "manual" nhỏ; LLM chỉ "giải thích" cờ — không tự dừng. Edge-style: chỉ gửi anomaly, không gửi cả chuỗi.

➡️ Tiếp [[ak06-data-labeling]] — hạ tầng gán nhãn (chạy được).
