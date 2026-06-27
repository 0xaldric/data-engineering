# AJ02 — AI Alignment & Safety (sâu)

> Căn chỉnh model theo **giá trị con người**: hữu ích + trung thực + vô hại. Sâu hơn [[ag03-rlhf-preference-data]]: RLHF → Constitutional AI, refusal training, helpful↔harmless trade-off. Liên hệ [[ad04-llm-security]], [[ah03-red-teaming]].

## Alignment là gì & vì sao khó
- Model train trên web → học cả tốt lẫn xấu → cần **căn chỉnh** để hữu ích + an toàn.
- "Đúng ý người" mơ hồ: hữu ích cho ai? an toàn theo chuẩn nào? → giá trị khó định nghĩa + xung đột.
- 3 trụ (HHH): **Helpful** (giúp được việc), **Honest** (không bịa [[ag02-hallucination-detection]]), **Harmless** (không gây hại).

## ⭐ Phổ kỹ thuật alignment
```
SFT (instruction) ─> RLHF (preference người [[ag03]]) ─> Constitutional AI / RLAIF
   dạy làm theo       dạy "tốt hơn" theo người          AI tự phê theo "hiến pháp"
```
| Kỹ thuật | Ý tưởng |
|----------|---------|
| **RLHF** | người chấm preference → reward model → tinh chỉnh ([[ag03-rlhf-preference-data]]) |
| **DPO** | tối ưu trực tiếp từ preference (không cần reward model riêng) |
| **Constitutional AI** | model tự phê output theo bộ nguyên tắc ("hiến pháp") → tự sửa → giảm cần người |
| **RLAIF** | AI feedback thay người (rẻ/scale, kế thừa bias model) |

## ⭐ Helpful ↔ Harmless trade-off (căng thẳng trung tâm)
```
quá HARMLESS: từ chối cả câu vô hại ("tôi không thể...") -> vô dụng, khó chịu
quá HELPFUL:  trả lời cả câu nguy hiểm -> có hại
-> alignment = cân bằng: giúp tối đa MÀ an toàn; từ chối ĐÚNG cái cần từ chối
```
- **Refusal training**: dạy model từ chối yêu cầu có hại — nhưng không over-refuse (false refusal).
- Data alignment phải có **cả hai**: ví dụ nên-giúp + ví dụ nên-từ-chối, ranh giới rõ.

## ⭐ Jailbreak resistance (alignment gặp security)
- Alignment dạy từ chối harm; jailbreak ([[ah03-red-teaming]]) tìm cách lách → cuộc đua.
- Data: thêm **adversarial examples** (jailbreak đã biết → từ chối đúng) vào training.
- Defense-in-depth ([[ad04-llm-security]]): alignment (model) + guardrail (hệ thống) — không chỉ dựa model.

## Vai trò DE (data cho alignment)
- **Preference data** HHH ([[ag03-rlhf-preference-data]]): chosen/rejected theo helpful + honest + harmless.
- **Refusal data**: (yêu cầu có hại, câu từ chối tốt) + (yêu cầu vô hại, không từ chối).
- **Adversarial data**: jailbreak → nhãn từ chối ([[ah03-red-teaming]] red-team feed alignment).
- **Constitution**: bộ nguyên tắc (text) để AI tự phê — versioned ([[aa07-prompt-management]]).
- **Eval alignment**: đo helpful (task success) + harmless (% từ chối harm) + over-refusal — gate ([[af07-continuous-eval]]).

## Cạm bẫy
- **Chỉ tối ưu helpful** → model nguy hiểm; **chỉ harmless** → vô dụng (over-refuse) → cân bằng + đo cả hai.
- **Alignment chỉ ở model** → jailbreak lách → thêm guardrail hệ thống.
- **Preference data thiên lệch** (annotator [[ag03-rlhf-preference-data]]) → model lệch giá trị → đa dạng annotator + guideline.
- **RLAIF thuần** → kế thừa + khuếch đại bias model-judge → trộn người.
- **Reward hacking** → model "có vẻ aligned" mà lách → eval đối kháng ([[ah03-red-teaming]]).
- **Value lock-in**: "hiến pháp" của ai? → minh bạch + governance ([[af06-ai-data-governance]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] 3 trụ HHH (helpful/honest/harmless).
- [ ] Phổ: SFT → RLHF/DPO → Constitutional AI/RLAIF.
- [ ] Helpful↔harmless trade-off; refusal training (không over-refuse).
- [ ] Jailbreak resistance = alignment + guardrail (defense-in-depth).
- [ ] DE: preference HHH + refusal + adversarial data + eval alignment.
- 🔭 Tự mò: tạo 10 cặp (yêu cầu, có-nên-trả-lời?) — 5 vô hại nên giúp, 5 có hại nên từ chối; viết "constitution" 3 dòng; với mỗi yêu cầu, tự phê theo constitution → quyết định giúp/từ chối. Đo over-refusal (từ chối nhầm câu vô hại) — chính là tín hiệu alignment lệch.

➡️ Tiếp [[aj03-capstone-integration]] — AI data product (chạy được).
