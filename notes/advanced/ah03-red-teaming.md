# AH03 — AI Red-Teaming & Adversarial Testing

> Chủ động **tấn công hệ AI của chính mình** để tìm lỗ hổng trước kẻ xấu. Như pentest cho LLM. Biến safety thành **test suite tự động**. Liên hệ [[ad04-llm-security]], [[aa02-guardrails]], [[ag02-hallucination-detection]].

## Vì sao red-team (không chờ bị tấn công)
- Hệ AI có bề mặt tấn công mới (injection, jailbreak, leak — [[ad04-llm-security]]) → không thể chỉ "hy vọng an toàn".
- Red-team = **tìm cách phá trước** → vá trước khi kẻ xấu/người dùng vô tình kích hoạt.
- Biến thành **eval an toàn tự động**: mỗi đổi prompt/model → chạy bộ tấn công → đo % bị phá.

## ⭐ Taxonomy tấn công (biết để test)
| Loại | Mô tả | Test |
|------|-------|------|
| **Jailbreak** | lừa bỏ qua safety (role-play "DAN", giả định, mã hoá) | bộ prompt jailbreak |
| **Prompt injection** | direct + indirect ([[ad04-llm-security]]) | inject lệnh trong input/doc |
| **Data exfiltration** | moi PII/system prompt/data train | hỏi lộ system prompt, PII |
| **Harmful content** | sinh nội dung độc/nguy hiểm | prompt yêu cầu harm |
| **Bias/fairness** | output phân biệt đối xử | prompt nhóm nhạy cảm ([[af06-ai-data-governance]]) |
| **Hallucination bait** | dụ bịa (câu hỏi không có đáp án) | câu bẫy ([[ag02-hallucination-detection]]) |

## ⭐ Manual vs Automated red-team
```
MANUAL: chuyên gia nghĩ cách phá sáng tạo -> sâu, bắt lỗi tinh vi -> chậm, không scale
AUTOMATED: LLM/script SINH adversarial prompt hàng loạt -> scale, regression -> nông hơn
   vd: "viết lại yêu cầu độc này thành 50 biến thể né guardrail"
   vd: dùng LLM tấn công LLM (attacker model vs target)
```
→ Kết hợp: manual tìm lỗ hổng mới → tự động hoá thành test suite chạy mỗi release.

## ⭐ Red-team như test suite (vai trò DE/MLOps)
```
bộ adversarial prompts (versioned, lớn dần theo lỗ hổng tìm được)
   ─> chạy qua hệ AI ─> đo: % bị jailbreak, % rò PII, % sinh harm
   ─> gate: vượt ngưỡng -> CHẶN release ([[af07-continuous-eval]] style)
   ─> lỗ hổng mới -> thêm vào bộ test (như regression [[ac03-eval-driven-dev]])
```
→ Đúng tinh thần eval-driven: an toàn **đo được + gác cổng**, không "cảm thấy an toàn".

## Vai trò DE
- **Adversarial dataset**: thu thập/sinh/version bộ prompt tấn công (như golden set cho an toàn).
- **Safety eval harness**: chạy bộ tấn công, chấm tự động (LLM-judge "có vi phạm không" [[ad02-llm-judge]]).
- **Logging**: lưu mọi tấn công + kết quả (provenance [[ab06-llm-observability]]) → phân tích pattern.
- **Defense-in-depth** ([[ad04-llm-security]]): red-team kiểm mọi tầng (input/output/tool).

## Cạm bẫy
- **Không red-team** → kẻ xấu/user tìm ra trước → sự cố thật.
- **Chỉ test 1 lần** → model/prompt đổi → lỗ hổng mới → red-team liên tục (regression).
- **Chỉ manual** → không scale/regression → tự động hoá bộ test.
- **Bộ test tĩnh** → kẻ tấn công sáng tạo hơn → cập nhật theo kỹ thuật mới.
- **Đo chủ quan** → "có vẻ ổn" → metric rõ (% bị phá) + judge.
- **Red-team mà không vá** → biết lỗ hổng mà để đó → gate + fix.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao red-team (tìm lỗ hổng trước kẻ xấu).
- [ ] Taxonomy: jailbreak/injection/exfiltration/harm/bias/hallucination.
- [ ] Manual (sâu) vs automated (scale) — kết hợp.
- [ ] Red-team = test suite an toàn + gate + regression.
- [ ] Vai trò DE: adversarial dataset + safety harness + logging.
- 🔭 Tự mò: mở rộng `guardrails_demo.py` thành "red-team harness": tạo bộ 10 prompt tấn công (injection EN/VN, jailbreak role-play, hỏi lộ PII), chạy qua guardrail, đếm % bị chặn vs lọt; thêm 1 prompt né được → cho thấy cần cập nhật pattern (regression an toàn).

➡️ Tiếp [[ah04-tokenization]] — tokenization deep-dive.
