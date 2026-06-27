# AL08 — Case Study: Insurance AI

> AI bảo hiểm: xử lý claim, phát hiện gian lận, underwriting hỗ trợ, RAG hợp đồng. Nhấn: **compliance + explainability (giải trình từ chối) + point-in-time + LLM không tự quyết chi trả**. Tương tự finance ([[aj06-case-finance-ai]]). Liên hệ [[k02-case-insurance]], [[af06-ai-data-governance]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: xử lý claim nhanh, phát hiện gian lận, underwriting (định phí/duyệt) hỗ trợ.
- **Ràng buộc**: compliance nghiêm (luật bảo hiểm), **giải trình quyết định** (từ chối claim phải có lý do hợp lệ), công bằng (không phân biệt), point-in-time.
- **Sống còn**: LLM **không tự quyết chi trả/từ chối** — hỗ trợ, người quyết.

## 2. ⭐ Thành phần
| Thành phần | Kỹ thuật |
|-----------|----------|
| **Claim processing** | trích thông tin hồ sơ (structured extraction [[ak07-kg-construction]]) + validate ([[ai06-llm-output-governance]]) |
| **Fraud detection** | anomaly + pattern (như finance [[aj06-case-finance-ai]]) + LLM giải thích cờ |
| **Underwriting hỗ trợ** | RAG quy tắc + model rủi ro → gợi ý (người duyệt) |
| **RAG hợp đồng/điều khoản** | tra cứu điều khoản, quyền lợi (citation [[ak02-case-legal-ai]]) |
| **Chatbot khách** | hỏi đáp hợp đồng + trạng thái claim |

## 3. ⭐ Explainability — giải trình từ chối (cốt lõi pháp lý)
```
từ chối claim ─> PHẢI nêu lý do hợp lệ + điều khoản căn cứ
   ─> không phải "AI nói không" mà "Điều X khoản Y: trường hợp này không được bảo hiểm"
   ─> citation điều khoản THẬT ([[ak02-case-legal-ai]]) + người duyệt ký
   ─> khách có quyền khiếu nại -> audit trail đầy đủ
```
→ Quyết định ảnh hưởng quyền lợi tiền bạc → **giải trình được + người chịu trách nhiệm**, không black-box.

## 4. ⭐ Point-in-time & fraud (DE thuần)
- **Point-in-time**: định phí/duyệt dùng thông tin **tại thời điểm** ký hợp đồng, không "kết quả sau" → chống leakage ([[ac07-feature-store]], [[aj06-case-finance-ai]]).
- **Fraud**: phát hiện claim bất thường (nhiều claim, pattern lạ) → cờ + người điều tra; LLM giải thích cờ, không tự từ chối.
- **Bias/fairness**: định phí không phân biệt nhóm trái luật → audit ([[af06-ai-data-governance]]).

## Cạm bẫy
- **LLM tự quyết chi trả/từ chối** → sai = pháp lý + thiệt khách → người quyết.
- **Từ chối không giải trình** → vi phạm + khiếu nại → explainability + citation điều khoản.
- **Bịa điều khoản** → từ chối sai căn cứ → grounding + verify điều khoản có thật.
- **Point-in-time sai** → định phí dùng thông tin tương lai → as-of join.
- **Fraud false-positive cao** → từ chối oan khách thật → calibrate + người điều tra.
- **Bias định phí** → phân biệt trái luật → fairness audit.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: claim/fraud/underwriting/RAG-hợp-đồng.
- [ ] Explainability: giải trình từ chối + citation điều khoản + người ký.
- [ ] Point-in-time chống leakage; fraud cờ + người điều tra.
- [ ] LLM không tự quyết chi trả.
- [ ] Cạm bẫy: tự quyết, không giải trình, bịa điều khoản, bias.
- 🔭 Tự mò: dựng "claim validator" mini — trích field từ hồ sơ giả (số tiền, ngày, loại) → validate theo schema ([[ai06-llm-output-governance]]) → tra "điều khoản" (dict) xem có được bảo hiểm → nếu không, in lý do + điều khoản căn cứ (explainability). LLM chỉ diễn giải, rule quyết.

➡️ Tiếp [[al09-ai-review11]] — review 11 + lộ trình luyện phỏng vấn.
