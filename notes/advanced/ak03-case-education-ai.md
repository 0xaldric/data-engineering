# AK03 — Case Study: Education AI Platform

> AI giáo dục: gia sư cá nhân hoá, sinh nội dung/câu hỏi, chấm bài + feedback. Nhấn: **personalization theo trình độ**, an toàn trẻ em, eval sư phạm, data flywheel. Liên hệ [[af08-case-personalization]], [[aj02-ai-alignment]], [[aj07-data-flywheel]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: học hiệu quả hơn (cá nhân hoá theo trình độ/tốc độ), giảm tải giáo viên (chấm/sinh đề).
- **Người dùng**: học sinh (nhiều lứa tuổi/trình độ), giáo viên.
- **Ràng buộc**: an toàn trẻ em (nội dung phù hợp), chính xác (dạy sai kiến thức = hại), chống gian lận (làm hộ).

## 2. ⭐ Thành phần & kỹ thuật
| Thành phần | Kỹ thuật |
|-----------|----------|
| **Gia sư cá nhân hoá** | RAG kiến thức + memory tiến độ ([[ag07-conversational-memory]]) + adapt độ khó |
| **Sinh câu hỏi/nội dung** | LLM sinh + validate đúng kiến thức ([[ai06-llm-output-governance]]) |
| **Chấm bài tự động** | so đáp án + LLM-judge cho tự luận ([[ad02-llm-judge]]) + feedback |
| **Theo dõi tiến độ** | profile học (điểm yếu/mạnh) → đề xuất ([[af08-case-personalization]]) |

## 3. ⭐ Personalization sư phạm (khác reco thường)
```
profile học sinh: trình độ, điểm yếu (chủ đề sai nhiều), tốc độ, phong cách
   ─> chọn nội dung ĐÚNG ĐỘ KHÓ (không quá dễ chán, không quá khó nản — "vùng phát triển gần")
   ─> ôn lại chủ đề yếu (spaced repetition)
   ─> feedback xây dựng (chỉ chỗ sai + cách sửa, không chỉ đúng/sai)
```
→ Khác recsys bán hàng: mục tiêu **học được**, không phải "thích/mua". Cá nhân hoá theo **sư phạm**.

## 4. ⭐ An toàn & chính xác (gắt cho trẻ em)
- **An toàn nội dung**: lọc nội dung không phù hợp lứa tuổi ([[aj02-ai-alignment]] harmless); guardrail ([[aa02-guardrails]]).
- **Chính xác kiến thức**: dạy sai = hại lâu dài → grounding + giáo viên review nội dung sinh.
- **Chống gian lận**: phát hiện "làm hộ bài" → giới hạn (gợi ý hướng, không cho đáp án thẳng).
- **Privacy trẻ em**: data học sinh nhạy cảm (COPPA/luật) → bảo vệ chặt ([[ad03-privacy-compliance]]).

## 5. ⭐ Data flywheel giáo dục
```
học sinh tương tác (làm bài, hỏi, sai) ─> signal (chủ đề sai, câu hỏi khó)
   ─> cải thiện: nội dung yếu, câu hỏi sinh kém, cá nhân hoá tốt hơn ([[aj07-data-flywheel]])
   ─> eval: học sinh có TIẾN BỘ không (không chỉ "thích app")
```
→ Đo bằng **kết quả học** (tiến bộ điểm, thành thạo), không chỉ engagement.

## Cạm bẫy
- **Dạy sai kiến thức** → hại lâu dài → grounding + giáo viên review.
- **Cho đáp án thẳng** → học sinh không học, gian lận → gợi ý hướng dẫn.
- **Độ khó sai** (quá dễ/khó) → chán/nản → adapt theo trình độ.
- **Nội dung không phù hợp lứa tuổi** → an toàn trẻ em → lọc nghiêm.
- **Đo engagement thay học tập** → tối ưu gây nghiện, không dạy → đo tiến bộ thật.
- **Privacy trẻ em lỏng** → vi phạm luật → bảo vệ data học sinh.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: gia sư/sinh đề/chấm bài/theo dõi.
- [ ] Personalization sư phạm (đúng độ khó, ôn chỗ yếu) khác recsys bán hàng.
- [ ] An toàn trẻ em + chính xác kiến thức + chống gian lận + privacy.
- [ ] Data flywheel đo bằng tiến bộ học, không engagement.
- [ ] Cạm bẫy: dạy sai, cho đáp án thẳng, đo engagement.
- 🔭 Tự mò: dựng "gia sư mini" — pool câu hỏi gắn độ khó (1-5); "học sinh" giả có trình độ; chọn câu hỏi quanh trình độ (±1); nếu sai → giảm độ khó + ôn chủ đề đó; theo dõi "thành thạo" mỗi chủ đề. Đó là personalization sư phạm thu nhỏ.

➡️ Tiếp [[ak04-case-govt-ai]] — case study dịch vụ công.
