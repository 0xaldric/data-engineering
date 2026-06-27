# AK04 — Case Study: Government/Public Service AI

> AI dịch vụ công: trợ lý thủ tục hành chính, RAG văn bản pháp quy. Nhấn: **minh bạch + công bằng + privacy công dân + độ phủ ngôn ngữ/accessibility**. Liên hệ [[af06-ai-data-governance]], [[ak02-case-legal-ai]], [[ac01-multilingual-rag]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: giúp công dân tra cứu thủ tục, điền hồ sơ, hỏi chính sách — phục vụ MỌI người.
- **Đặc thù công**: phải **công bằng** (không thiên lệch nhóm), **minh bạch** (giải trình), **bao trùm** (đa ngôn ngữ/dân tộc, người khuyết tật), **trách nhiệm giải trình** (public accountability).
- **Quy mô**: toàn dân → đa dạng cực lớn về ngôn ngữ/trình độ/nhu cầu.

## 2. ⭐ Nguyên tắc đặc thù khu vực công
| Nguyên tắc | Vì sao |
|-----------|--------|
| **Minh bạch** | quyết định công phải giải trình được (vì sao từ chối hồ sơ?) ([[af06-ai-data-governance]]) |
| **Công bằng/fairness** | không thiên lệch nhóm (dân tộc/vùng/giới) → audit bias bắt buộc |
| **Accessibility** | người khiếm thị/khuyết tật, người ít học → đa kênh, ngôn ngữ đơn giản |
| **Đa ngôn ngữ** | nhiều dân tộc/ngôn ngữ → embedding đa ngữ ([[ac01-multilingual-rag]]) |
| **Privacy công dân** | data nhạy cảm toàn dân → bảo vệ cực chặt ([[ad03-privacy-compliance]]) |
| **Không bịa thủ tục** | sai thủ tục → công dân thiệt → grounding + citation văn bản ([[ak02-case-legal-ai]]) |

## 3. Kiến trúc
```
văn bản pháp quy (luật/nghị định/thủ tục) ─> RAG (citation văn bản thật)
   ─> đa ngôn ngữ (dịch + embedding đa ngữ) + ngôn ngữ ĐƠN GIẢN (plain language)
công dân hỏi (nhiều kênh: web/voice/chat) ─> [accessibility] STT/TTS ([[ac05-voice-audio-pipeline]])
   ─> retrieve thủ tục đúng ─> trả lời rõ ràng + nguồn + bước cụ thể
   ─> [minh bạch] giải trình + [audit] log + [fallback] chuyển cán bộ khi phức tạp
```

## 4. ⭐ Fairness & Transparency (cốt lõi khu vực công)
- **Fairness audit**: đo chất lượng dịch vụ ĐỀU giữa nhóm (ngôn ngữ ít người, vùng xa) → không để AI phục vụ kém nhóm yếu thế ([[af06-ai-data-governance]]).
- **Transparency**: quyết định ảnh hưởng quyền lợi (duyệt/từ chối) → giải trình rõ + quyền khiếu nại → **không để AI tự quyết** việc hệ trọng, human-in-loop.
- **Explainability**: "vì sao kết quả này" bằng ngôn ngữ công dân hiểu.
- EU AI Act: dịch vụ công nhiều phần là **high-risk** → governance chặt ([[af06-ai-data-governance]]).

## 5. Đặc thù
- **Độ phủ ngôn ngữ**: ngôn ngữ ít tài nguyên → model đa ngữ + tự xây data ([[ac01-multilingual-rag]], [[ah06-rag-benchmarks]]).
- **Plain language**: trả lời đơn giản (không thuật ngữ pháp lý) cho người ít học.
- **Tin cậy**: dịch vụ công phải đúng → grounding + cán bộ review việc hệ trọng.

## Cạm bẫy
- **AI tự quyết việc hệ trọng** (duyệt trợ cấp/phạt) → bất công + không khiếu nại được → human-in-loop + minh bạch.
- **Thiên lệch nhóm yếu thế** (phục vụ kém ngôn ngữ ít người) → fairness audit.
- **Ngôn ngữ phức tạp** → người ít học không hiểu → plain language.
- **Bịa thủ tục** → công dân làm sai/thiệt → grounding + citation văn bản.
- **Bỏ accessibility** → loại người khuyết tật → đa kênh + chuẩn accessibility.
- **Privacy lỏng** → rò data toàn dân → bảo vệ cực chặt + minimize.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Nguyên tắc công: minh bạch/công bằng/accessibility/đa ngữ/privacy/không bịa.
- [ ] Fairness audit (chất lượng đều giữa nhóm) + transparency (giải trình + khiếu nại).
- [ ] Không để AI tự quyết việc hệ trọng → human-in-loop.
- [ ] Độ phủ ngôn ngữ + plain language.
- [ ] Cạm bẫy: AI tự quyết, thiên lệch nhóm yếu, bỏ accessibility.
- 🔭 Tự mò: dùng `cross_lingual_eval.py` ([[ac01-multilingual-rag]]) đo recall cho 2 "nhóm ngôn ngữ" khác nhau trên cùng corpus thủ tục → nếu 1 nhóm rớt nhiều = bất công ngôn ngữ → đó là fairness audit thu nhỏ (chất lượng dịch vụ không đều).

➡️ Tiếp [[ak05-case-manufacturing-ai]] — case study sản xuất/IoT.
