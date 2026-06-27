# AM06 — Case Study: Gaming AI Data

> AI game: NPC thông minh, matchmaking, anti-cheat, player analytics, content gen. Nhấn: **real-time scale triệu player**, latency thấp, cost LLM cho NPC, an toàn chat. Khung 7 bước ([[af09-ai-review6]]). Liên hệ [[g04-case-gaming]], [[af08-case-personalization]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: game hấp dẫn hơn (NPC sống động, match cân bằng), công bằng (chống cheat), an toàn (chat).
- **Quy mô**: triệu player đồng thời, event/giây khổng lồ ([[g04-case-gaming]]), latency cực thấp (game real-time).
- **Ràng buộc**: cost (LLM cho NPC × triệu player = đắt), an toàn (chat toxic/grooming), chống gian lận.

## 2. ⭐ Thành phần
| Thành phần | Kỹ thuật |
|-----------|----------|
| **NPC dialogue** | LLM sinh hội thoại động (thay script cứng) + memory nhân vật ([[ag07-conversational-memory]]) |
| **Matchmaking** | model skill (Elo/TrueSkill) + cân bằng — KHÔNG LLM |
| **Anti-cheat** | anomaly detection hành vi (aimbot/speedhack) real-time ([[ag04-drift-detection]]) |
| **Player analytics** | clickstream game → churn/engagement ([[c06-case-clickstream]]) |
| **Content gen** | sinh quest/level/item (procedural + LLM) + validate |
| **Chat moderation** | lọc toxic real-time ([[al04-case-media-ai]]) |

## 3. ⭐ NPC LLM — cost & latency (thách thức lớn nhất)
```
LLM cho MỌI NPC × triệu player = cost KHỔNG LỒ + latency (game cần <100ms)
   -> model NHỎ/quantize cho NPC ([[ae05-edge-ai-data]]); cache hội thoại lặp ([[ad08-semantic-cache]])
   -> chỉ LLM cho NPC QUAN TRỌNG; NPC phụ dùng script/template
   -> pre-generate hội thoại offline khi có thể
```
→ Không thể LLM real-time mọi NPC → routing (LLM cho quan trọng, rule cho phụ) + cache + model nhỏ ([[ac08-ai-cost-scale]]).

## 4. ⭐ Anti-cheat (real-time anomaly + an toàn)
- Phát hiện hành vi bất thường (aim quá chuẩn, di chuyển bất khả) → cờ → review (không tự ban oan).
- Real-time + scale → stream processing ([[ai09-streaming-ai]]); model nhẹ ở server.
- False-positive ban oan player thật = mất khách → calibrate + human cho ban.

## 5. An toàn & data
- **Chat moderation**: toxic/grooming real-time, đặc biệt game trẻ em ([[ak03-case-education-ai]] an toàn).
- **Player data**: hành vi chơi (privacy, đặc biệt minor) → bảo vệ ([[ad03-privacy-compliance]]).
- **Anti-addiction**: không tối ưu gây nghiện mù (đạo đức [[aj02-ai-alignment]]).

## Cạm bẫy
- **LLM real-time mọi NPC** → cost/latency nổ → model nhỏ + cache + routing.
- **LLM cho matchmaking** → kém model skill chuyên → dùng Elo/TrueSkill.
- **Anti-cheat tự ban** → ban oan = mất khách → cờ + human review.
- **Chat moderation chậm** → toxic lọt real-time → model nhẹ real-time.
- **NPC LLM bịa lore** → phá thế giới game → grounding lore + validate.
- **Tối ưu engagement gây nghiện** → đạo đức → cân bằng.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thành phần: NPC/matchmaking/anti-cheat/analytics/content/moderation.
- [ ] NPC LLM cost/latency: model nhỏ + cache + routing + pre-gen.
- [ ] Anti-cheat: anomaly real-time + human cho ban (không tự ban).
- [ ] An toàn chat + privacy minor + anti-addiction.
- [ ] Cạm bẫy: LLM mọi NPC, tự ban, NPC bịa lore.
- 🔭 Tự mò: dùng `semantic_cache.py` ([[ad08-semantic-cache]]) cache hội thoại NPC — player hỏi NPC câu gần nghĩa câu cũ → trả cache (tiết kiệm LLM); đo hit-rate giả lập nhiều player hỏi tương tự → thấy cache cứu cost NPC thế nào.

➡️ Tiếp [[am07-case-agritech-ai]] — case study nông nghiệp.
