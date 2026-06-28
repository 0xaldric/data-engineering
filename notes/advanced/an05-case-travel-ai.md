# AN05 — Case Study: Travel/Hospitality AI

> AI du lịch: trợ lý đặt phòng/vé, reco điểm đến, dynamic pricing, tóm tắt review. Nhấn: **đa ngữ (khách quốc tế)**, real-time giá/tồn phòng, personalization. Khung 7 bước ([[af09-ai-review6]]). Liên hệ [[ac01-multilingual-rag]], [[ak01-case-ecommerce-ai]], [[ac02-recsys-llm]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: khách tìm/đặt dễ (trợ lý), gợi đúng gu (reco), giá tối ưu (pricing), tin tưởng (review).
- **Đặc thù**: khách **đa quốc gia/ngôn ngữ**, hành trình phức tạp (bay+phòng+tour), giá/tồn phòng đổi liên tục.
- **Ràng buộc**: đa ngữ, real-time inventory, mùa vụ mạnh (lễ/hè).

## 2. ⭐ Thành phần
| Thành phần | Kỹ thuật |
|-----------|----------|
| **Trợ lý đặt phòng/vé** | RAG (chính sách/điểm đến) + tool (tra giá/tồn real-time) ([[ad05-structured-rag]]) |
| **Reco điểm đến** | embedding sở thích + nội dung ([[ac02-recsys-llm]]) |
| **Dynamic pricing** | model giá theo cầu/mùa — KHÔNG LLM (tối ưu số) |
| **Tóm tắt review** | LLM tóm + sentiment, lọc review giả ([[ak01-case-ecommerce-ai]]) |
| **Chatbot đa ngữ** | đa ngôn ngữ ([[ac01-multilingual-rag]]) + voice ([[ac05-voice-audio-pipeline]]) |

## 3. ⭐ Đa ngữ (cốt lõi — khách quốc tế)
```
khách hỏi bằng tiếng mẹ đẻ (Anh/Trung/Nhật/Việt...) -> hiểu + trả lời đúng ngôn ngữ
   -> embedding ĐA NGỮ ([[ac01-multilingual-rag]]) cho search/RAG
   -> dịch nội dung (review/mô tả) hoặc model đa ngữ native
   -> ⚠️ đa ngữ FAIR: chất lượng đều giữa ngôn ngữ ([[ak04-case-govt-ai]] fairness)
```
→ Du lịch = đa ngữ bản chất; chất lượng kém ở 1 ngôn ngữ = mất khách thị trường đó.

## 4. ⭐ Real-time inventory + dynamic pricing
- **Giá/tồn phòng đổi từng phút** → filter "còn phòng" lúc tìm (đừng gợi hết phòng — [[ak01-case-ecommerce-ai]]).
- **Dynamic pricing**: model số (cầu/mùa/đối thủ) — không LLM; LLM giải thích giá nếu cần.
- Tool tra giá/tồn **real-time** (không cache cũ → giá sai).

## 5. Personalization & trust
- **Reco theo gu**: gia đình vs phượt vs công tác → khác hẳn → profile + content ([[af08-case-personalization]]).
- **Cold-start**: khách mới → hỏi sở thích / popular theo mùa.
- **Review thật**: lọc review giả (bot/trả tiền) trước tóm tắt → tin tưởng.

## Cạm bẫy
- **Gợi phòng/vé hết chỗ hoặc giá cũ** → filter real-time, tool tra giá ngay.
- **Đa ngữ kém ở 1 ngôn ngữ** → mất thị trường → model đa ngữ + đo fairness ngôn ngữ.
- **LLM tự định giá** → kém model số → dynamic pricing chuyên.
- **Tóm tắt review giả** → mất tin → lọc giả trước.
- **Bịa chính sách** (hủy/hoàn) → khiếu nại → RAG chính sách thật + citation.
- **Bỏ cold-start** → khách mới gợi rác → content + popular.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: trợ lý/reco/pricing/review/chatbot đa ngữ.
- [ ] Đa ngữ: embedding đa ngữ + fairness chất lượng đều.
- [ ] Real-time inventory + dynamic pricing (số, không LLM).
- [ ] Personalization theo gu + cold-start + review thật.
- [ ] Cạm bẫy: gợi hết phòng, đa ngữ lệch, LLM định giá, bịa chính sách.
- 🔭 Tự mò: dùng `cross_lingual_eval.py` ([[ac01-multilingual-rag]]) đo recall RAG chính sách du lịch cho 2 ngôn ngữ → nếu lệch = bất công ngôn ngữ (mất khách thị trường yếu); thêm filter `available` + `price<=budget` vào `semantic_recsys.py` cho reco phòng.

➡️ Tiếp [[an06-case-social-ai]] — case study mạng xã hội.
