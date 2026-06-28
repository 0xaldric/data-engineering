# AN04 — Case Study: Energy/Utilities AI

> AI năng lượng: dự báo nhu cầu điện, tối ưu lưới, predictive maintenance, anomaly tiêu thụ. Nhấn: **time-series + real-time grid + an toàn vật lý** (không tự điều khiển lưới). Liên hệ [[ak08-timeseries-tabular-fm]], [[ak05-case-manufacturing-ai]], [[j03-case-energy]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: cân cung-cầu điện (dự báo), lưới ổn định (tối ưu/sửa), giảm tổn thất, phát hiện trộm điện.
- **Data**: smart meter (time-series tiêu thụ), sensor lưới, thời tiết, sản lượng tái tạo (gió/mặt trời biến động).
- **Ràng buộc**: real-time (lưới mất cân bằng → mất điện), an toàn vật lý cực cao, độ tin cậy (hạ tầng thiết yếu).

## 2. ⭐ Thành phần
| Thành phần | Kỹ thuật |
|-----------|----------|
| **Demand forecast** | time-series (mùa vụ/thời tiết — [[ak08-timeseries-tabular-fm]]) → cân cung cầu |
| **Grid optimization** | thuật toán tối ưu lưới (không LLM) + LLM giải thích |
| **Predictive maintenance** | sensor thiết bị → dự đoán hỏng ([[ak05-case-manufacturing-ai]]) |
| **Anomaly tiêu thụ** | phát hiện trộm điện/rò rỉ (bất thường meter) |
| **RAG vận hành** | kỹ sư hỏi quy trình/sự cố lưới |

## 3. ⭐ Demand forecast (cốt lõi — tái tạo làm khó)
```
nhu cầu điện: theo giờ/mùa/thời tiết (nóng -> điều hoà -> tải cao)
   + tái tạo (gió/mặt trời) BIẾN ĐỘNG khó dự báo -> cân cung-cầu khó hơn
-> time-series model + thời tiết feature ([[ac07-feature-store]] point-in-time)
-> dự báo sai -> thừa (lãng phí) / thiếu (mất điện) -> recall an toàn
```
→ Tái tạo tăng → forecast quan trọng + khó hơn (nguồn không ổn định).

## 4. ⭐ An toàn vật lý (hạ tầng thiết yếu — gắt nhất)
- Lưới điện = hạ tầng sống còn → sự cố = mất điện diện rộng/nguy hiểm.
- **LLM KHÔNG tự điều khiển lưới** (đóng/cắt) → thuật toán + người + hệ SCADA ([[ak05-case-manufacturing-ai]] an toàn vật lý).
- LLM: giải thích, RAG runbook, copilot điều độ viên — không tự hành động.
- Độ tin cậy + redundancy cao (không được hỏng).

## 5. Đặc thù
- **Trộm điện**: anomaly meter (tiêu thụ giảm bất thường/pattern lạ) → điều tra.
- **Privacy meter**: smart meter lộ thói quen sinh hoạt (ở nhà/đi vắng) → bảo vệ ([[ad03-privacy-compliance]]).
- **Regulatory**: ngành điện quản lý chặt → governance ([[af06-ai-data-governance]]).

## Cạm bẫy
- **LLM tự điều khiển lưới** → mất điện/nguy hiểm → thuật toán + người + SCADA.
- **Forecast bỏ thời tiết/tái tạo** → cân cung cầu sai → feature đầy đủ.
- **Point-in-time sai** (forecast) → leakage → as-of ([[ac07-feature-store]]).
- **Bỏ qua privacy meter** → lộ thói quen → bảo vệ.
- **Độ tin cậy thấp** → hạ tầng thiết yếu không chịu được → redundancy.
- **Anomaly false-positive** → điều tra oan → calibrate.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: forecast/grid-opt/maintenance/anomaly/RAG.
- [ ] Demand forecast: time-series + thời tiết; tái tạo làm khó.
- [ ] An toàn vật lý: LLM không tự điều khiển lưới (thiết yếu).
- [ ] Trộm điện anomaly; privacy meter; regulatory.
- [ ] Cạm bẫy: LLM điều khiển lưới, forecast thiếu feature.
- 🔭 Tự mò: chuỗi tiêu thụ điện giả (có chu kỳ ngày + tăng khi "nóng"); forecast bằng baseline (cùng giờ hôm qua + trung bình tuần); thêm "feature thời tiết" giả xem cải thiện không; cờ meter có tiêu thụ tụt đột ngột (nghi trộm điện) — LLM giải thích, rule quyết.

➡️ Tiếp [[an05-case-travel-ai]] — case study du lịch.
