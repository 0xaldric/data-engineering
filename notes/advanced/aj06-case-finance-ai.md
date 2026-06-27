# AJ06 — Case Study: Financial/Trading AI Data

> Thiết kế AI cho tài chính — **real-time**, **compliance nghiêm**, **giải trình được**, và tuyệt đối **không để LLM tự quyết tiền**. Đề system-design nhấn real-time + audit + explainability. Liên hệ [[ac07-feature-store]], [[ad04-llm-security]], [[c07-case-fintech]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: hỗ trợ phân tích (rủi ro, gian lận, báo cáo), trợ lý hỏi-đáp dữ liệu tài chính, tóm tắt tin.
- **Ràng buộc**: real-time (giá/giao dịch đổi từng giây), compliance + audit nghiêm (luật tài chính), point-in-time (chống leakage), giải trình mọi quyết định.
- **Sống còn**: LLM **KHÔNG tự quyết tiền** (đặt lệnh/chuyển khoản) — chỉ phân tích/gợi ý.

## 2. ⭐ Nguyên tắc thiết kế
| Nguyên tắc | Vì sao |
|-----------|--------|
| **LLM bổ trợ, không tự quyết** | đặt lệnh/chuyển tiền → rule + human ([[ad04-llm-security]] excessive agency) |
| **Real-time** | giá/giao dịch streaming ([[ai09-streaming-ai]], [[c07-case-fintech]]) |
| **Point-in-time** | feature as-of lúc đó, không nhìn tương lai ([[ac07-feature-store]], [[af08-case-personalization]]) |
| **Explainability** | giải trình "vì sao gắn cờ gian lận" (luật + tin cậy) |
| **Audit bất biến** | mọi phân tích/quyết định log (thanh tra) |

## 3. Kiến trúc (lambda: real-time + batch)
```
giao dịch/giá ─stream─> [feature real-time] ([[ac07-feature-store]]) ─┐
tin tức/báo cáo ─> RAG (vector) ─────────────────────────────────────┤
                                                                      ├─> LLM phân tích
   ─> phát hiện bất thường (rule + model) + giải thích                │   (bổ trợ)
   ─> [gắn cờ] -> human/rule QUYẾT (LLM không tự hành động)           │
   ─> audit log bất biến + explainability ──────────────────────────-┘
batch (đêm): re-train, báo cáo, reconcile, point-in-time training data
```

## 4. ⭐ Point-in-time & leakage (DE thuần, gắt ở tài chính)
- Train model gian lận/rủi ro: feature phải **as-of lúc giao dịch**, không dùng "kết quả sau" → leakage ([[ac07-feature-store]]).
- Backtest chiến lược: chỉ dùng data **biết tại thời điểm đó** (không nhìn tương lai) → kết quả thật.
- Bitemporal ([[e04-bitemporal]]): phân biệt "thời điểm xảy ra" vs "thời điểm biết" — quan trọng cho tài chính.

## 5. ⭐ Compliance & Explainability
- **Audit trail bất biến**: ai làm gì, AI gợi gì, dựa data nào (provenance [[af06-ai-data-governance]]) → thanh tra.
- **Explainability**: "vì sao cờ gian lận" → SHAP/feature importance + LLM giải thích bằng tiếng người (nhưng phải đúng, không bịa lý do).
- **Model risk management**: model card, validation, monitoring (luật ngân hàng yêu cầu).
- **Data residency**: data tài chính nhạy cảm → self-host/vùng ([[ad03-privacy-compliance]]).

## Cạm bẫy (tốn tiền thật)
- **Để LLM tự đặt lệnh/chuyển tiền** → 1 lỗi = mất tiền → rule + human cho hành động.
- **Point-in-time sai** → leakage → backtest đẹp, thật lỗ → as-of join.
- **Bịa lý do explainability** → giải thích sai → giải thích từ feature THẬT, không LLM tưởng tượng.
- **Không audit bất biến** → không qua thanh tra → log immutable.
- **Real-time mà dùng feature batch cũ** → quyết định trên data lỗi thời → streaming feature.
- **Tin LLM phân tích số** → LLM tính sai ([[ag01-rag-bi-analytics]]) → số từ engine, LLM chỉ diễn giải.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Nguyên tắc: LLM bổ trợ không tự quyết tiền; real-time; point-in-time; explainability; audit.
- [ ] Kiến trúc lambda (stream real-time + batch).
- [ ] Point-in-time/bitemporal chống leakage (backtest thật).
- [ ] Compliance: audit bất biến, explainability đúng, model risk.
- [ ] Cạm bẫy: LLM tự quyết tiền, leakage, bịa lý do.
- 🔭 Tự mò: bằng DuckDB, dựng `transactions(user, ts, amount)`; tính feature "tổng giao dịch 1h trước mỗi giao dịch" bằng **as-of/window** (point-in-time đúng) vs phiên bản dùng tổng-cả-ngày (leakage) → thấy leakage làm feature "biết tương lai"; gắn cờ giao dịch > 3×trung-bình-trước-đó (rule), LLM chỉ "giải thích" cờ.

➡️ Tiếp [[aj07-data-flywheel]] — LLM data flywheel.
