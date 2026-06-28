# AN06 — Case Study: Social Media AI (Trust & Safety)

> AI mạng xã hội: feed ranking, **moderation ở scale tỉ post**, phát hiện misinformation/spam/bot. Nhấn: trust & safety + chống lan truyền độc hại + fairness. Liên hệ [[al04-case-media-ai]], [[af08-case-personalization]], [[h04-case-social-graph]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: feed hấp dẫn (giữ chân) NHƯNG an toàn (không lan truyền độc hại) + công bằng.
- **Quy mô**: TỈ post/ngày, tỉ user, real-time → moderation scale khủng khiếp.
- **Ràng buộc**: an toàn (harm/misinformation), fairness (không thiên lệch), tốc độ (lan truyền nhanh), pháp lý (nhiều nước).

## 2. ⭐ Feed ranking ⇄ Trust & Safety (căng thẳng trung tâm)
```
ENGAGEMENT (giữ chân): nội dung gây tương tác mạnh -> nhưng thường là CỰC ĐOAN/giật gân
SAFETY: nội dung cực đoan/sai sự thật lan nhanh -> hại xã hội
-> tối ưu engagement MÙ = khuếch đại độc hại (vòng xoáy)
-> phải cân: hấp dẫn MÀ an toàn; KHÔNG đẩy harm để tăng tương tác ([[aj02-ai-alignment]])
```
→ Đây là bài học lớn nhất của social AI: **engagement mù = khuếch đại độc hại**. Ranking phải tích hợp safety.

## 3. ⭐ Moderation ở scale tỉ post
```
post (tỉ/ngày) ─> [tier 1: model nhanh] lọc rõ ràng vi phạm (spam/NSFW/harm)
   ─> rõ vi phạm -> chặn ; nghi ngờ -> [tier 2: model kỹ / human queue]
   ─> multimodal (text+ảnh+video [[ag06-multimodal-production]]) + đa ngữ ([[ac01-multilingual-rag]])
   ─> ngữ cảnh: cùng câu, ngữ cảnh khác -> vi phạm khác (mỉa mai/trích dẫn)
```
→ Không human duyệt tỉ post → AI lọc tầng + human ca khó/ranh giới. **Recall an toàn cao** cho harm nguy hiểm (bỏ sót > false-positive).

## 4. ⭐ Misinformation / bot / coordinated (khó nhất)
| Vấn đề | Cách |
|--------|------|
| **Misinformation** | so claim với nguồn tin cậy (grounding [[ag02-hallucination-detection]]); fact-check; gắn nhãn |
| **Spam/bot** | anomaly hành vi (đăng hàng loạt, pattern giống nhau [[aa04-training-data-prep]] dedup) |
| **Coordinated/astroturfing** | graph phân tích (nhiều account hành động đồng bộ — [[h04-case-social-graph]]) |
| **Deepfake** | phát hiện nội dung tổng hợp |

## 5. ⭐ Fairness & minh bạch
- **Fairness**: moderation đều giữa nhóm/ngôn ngữ (không thiên lệch chính trị/dân tộc — [[ak04-case-govt-ai]]).
- **Minh bạch**: vì sao gỡ post → giải trình + khiếu nại (appeal).
- **Over-moderation**: gỡ nhầm nội dung hợp lệ → mất tự do ngôn luận → cân (false-positive cũng hại).

## Cạm bẫy (xã hội thật)
- **Tối ưu engagement mù** → khuếch đại cực đoan/misinformation → tích hợp safety vào ranking.
- **Human duyệt mọi post** → bất khả → AI lọc tầng + human ca khó.
- **Moderation recall thấp** → harm nguy hiểm lọt → recall an toàn cao.
- **Bỏ qua ngữ cảnh** (mỉa mai/trích dẫn) → gỡ nhầm → ngữ cảnh + human.
- **Thiên lệch moderation** → bất công nhóm → fairness audit + minh bạch.
- **Over-moderation** → kiểm duyệt quá → cân false-positive; appeal.
- **Bỏ coordinated behavior** → chiến dịch thao túng lọt → graph analysis.

## ✅ "Tự kiểm tra & tự mò"
- [ ] ⭐ Engagement ⇄ safety: tối ưu engagement mù = khuếch đại độc hại.
- [ ] Moderation tầng (AI lọc + human ca khó); recall an toàn cao.
- [ ] Misinformation/spam/bot/coordinated — cách phát hiện.
- [ ] Fairness + minh bạch + appeal + chống over-moderation.
- [ ] Cạm bẫy: engagement mù, recall thấp, bỏ ngữ cảnh, thiên lệch.
- 🔭 Tự mò: dùng `dedup_minhash.py` ([[aa04-training-data-prep]]) phát hiện "spam coordinated" — nhiều post gần trùng (bot đăng cùng nội dung nhẹ khác) → near-dup = nghi coordinated; thêm anomaly "1 account đăng N post/phút". Đó là spam/bot detection thu nhỏ.

➡️ Tiếp [[an07-mock-interview-3]] — mock phỏng vấn 3.
