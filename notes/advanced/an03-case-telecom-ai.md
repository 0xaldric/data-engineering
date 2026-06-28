# AN03 — Case Study: Telecom AI

> AI viễn thông: tối ưu mạng, churn prediction, chăm sóc khách, gian lận cước. Nhấn: **scale data khổng lồ (CDR)**, real-time mạng, time-series. Khung 7 bước ([[af09-ai-review6]]). Liên hệ [[j02-case-telecom]], [[ak08-timeseries-tabular-fm]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: mạng ổn định (tối ưu/sửa nhanh), giữ khách (churn), chăm sóc tự động, chống gian lận.
- **Data**: **CDR** (Call Detail Record — tỉ bản ghi/ngày [[j02-case-telecom]]), sensor mạng, ticket, hành vi thuê bao.
- **Ràng buộc**: scale cực lớn, real-time (sự cố mạng báo ngay), nhiều thuê bao.

## 2. ⭐ Thành phần
| Thành phần | Kỹ thuật |
|-----------|----------|
| **Network optimization** | anomaly mạng + dự báo tải (time-series [[ak08-timeseries-tabular-fm]]) → tối ưu |
| **Churn prediction** | model rủi ro rời mạng → giữ khách chủ động |
| **Chăm sóc khách** | RAG (gói cước/chính sách) + chatbot + tool (tra cước) ([[ad05-structured-rag]]) |
| **Fraud cước** | anomaly (cuộc gọi bất thường, SIM box) real-time ([[ag04-drift-detection]]) |
| **RAG kỹ thuật mạng** | kỹ sư hỏi tài liệu thiết bị/sự cố ([[ak05-case-manufacturing-ai]]) |

## 3. ⭐ Scale CDR (đặc thù telecom)
```
CDR tỉ bản ghi/ngày -> không xử lý từng cái real-time tốn kém
   -> stream aggregate ([[ai09-streaming-ai]]) + lưu lakehouse ([[j02-case-telecom]])
   -> anomaly real-time trên stream (fraud/sự cố); analytics batch (churn/báo cáo)
   -> LLM cho CHĂM SÓC + giải thích, KHÔNG cho xử lý CDR thô (số khổng lồ)
```
→ Bài toán big-data streaming kinh điển; LLM ở lớp chăm sóc/giải thích, không lớp data thô.

## 4. ⭐ Network: LLM bổ trợ, không tự điều khiển
- Tối ưu/định tuyến mạng → thuật toán mạng chuyên (không LLM).
- LLM: giải thích sự cố ("vì sao trạm X quá tải"), RAG runbook sửa lỗi, copilot kỹ sư NOC.
- Hành động trên mạng thật (reroute/restart) → rule + người (hậu quả dịch vụ [[ak05-case-manufacturing-ai]]).

## 5. Đặc thù & eval
- **Real-time fraud**: SIM box/cước bất thường → cờ ngay (mất tiền nhanh).
- **Churn**: đo bằng giữ chân thật (không chỉ AUC) — A/B chiến dịch giữ khách.
- **Privacy CDR**: data liên lạc cực nhạy (ai gọi ai) → bảo vệ chặt ([[ad03-privacy-compliance]]).

## Cạm bẫy
- **LLM xử lý CDR thô** → số khổng lồ, LLM kém số → big-data tool, LLM ở lớp chăm sóc.
- **LLM tự điều khiển mạng** → sự cố dịch vụ → rule + người.
- **Fraud chậm** → mất tiền real-time → stream detection.
- **Churn model không đo giữ chân thật** → tối ưu AUC vô ích → A/B chiến dịch.
- **CDR privacy lỏng** → rò data liên lạc → bảo vệ nghiêm.
- **Chatbot bịa gói cước** → khách khiếu nại → grounding + tool tra cước thật.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: network-opt/churn/chăm-sóc/fraud/RAG-kỹ-thuật.
- [ ] Scale CDR: stream aggregate + lakehouse; LLM ở lớp chăm sóc.
- [ ] Network: LLM bổ trợ (giải thích/runbook), không tự điều khiển.
- [ ] Real-time fraud; churn đo giữ-chân-thật; CDR privacy.
- [ ] Cạm bẫy: LLM xử lý CDR thô, tự điều khiển mạng.
- 🔭 Tự mò: dựng "fraud detector" mini trên CDR giả — z-score số phút gọi/ngày mỗi thuê bao, cờ outlier; với mỗi cờ, mock-LLM "giải thích" (vd "gọi quốc tế tăng 10× — nghi SIM box") từ RAG runbook; LLM giải thích, rule quyết.

➡️ Tiếp [[an04-case-energy-ai]] — case study năng lượng.
