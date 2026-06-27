# AM02 — Advanced Prompt Patterns

> Các mẫu prompt nâng cao — công cụ để LLM trả lời tốt hơn. Biết khi nào dùng cái nào. Liên hệ [[aj08-prompt-optimization]], [[aj01-reasoning-models]], [[aa05-agentic-pipelines]].

## ⭐ Bảng mẫu prompt (khi nào dùng)
| Mẫu | Ý tưởng | Dùng khi |
|-----|---------|----------|
| **Zero-shot** | chỉ instruction | task đơn giản, model đủ giỏi |
| **Few-shot** | kèm vài ví dụ (input→output) | cần format/style cụ thể; task lạ |
| **Chain-of-Thought** | "nghĩ từng bước trước khi trả lời" | suy luận, toán, logic ([[aj01-reasoning-models]]) |
| **ReAct** | reason → act (tool) → observe → lặp | agent dùng tool ([[aa05-agentic-pipelines]]) |
| **Self-consistency** | sinh N lần, vote đáp án phổ biến | tăng độ tin task có đáp án |
| **Structured output** | yêu cầu JSON theo schema | cần parse downstream ([[ai06-llm-output-governance]]) |
| **Role/Persona** | "Bạn là chuyên gia X..." | định hướng giọng/chuyên môn |
| **Step-back** | hỏi câu tổng quát trước → rồi cụ thể | cần bối cảnh/nguyên lý trước |

## ⭐ Chain-of-Thought (CoT)
```
THƯỜNG: "12×13 = ?" -> "156" (dễ sai nếu nhảy thẳng)
CoT:    "Tính từng bước: 12×13 = 12×10 + 12×3 = 120+36 = 156"
   -> model "nghĩ" ra giấy -> ít sai ở task nhiều bước
```
- Kích hoạt: "hãy suy luận từng bước" / few-shot có lời giải từng bước.
- Đổi lại: **token nhiều** ([[ah04-tokenization]]) → đắt/chậm; reasoning model làm sẵn ([[aj01-reasoning-models]]).

## ⭐ ReAct (Reason + Act) — nền của agent
```
Thought: cần biết doanh thu Q3 -> Action: query_db(...) -> Observation: 1.2 tỷ
Thought: so Q2 -> Action: query_db(...) -> Observation: 1.0 tỷ
Thought: đủ dữ liệu -> Answer: tăng 20%
```
→ Xen kẽ **nghĩ** và **hành động (tool)** → agent giải task nhiều bước ([[aa05-agentic-pipelines]]). Cần guardrail (max steps, tool an toàn [[ad04-llm-security]]).

## ⭐ Few-shot — chọn ví dụ quan trọng
- Ví dụ tốt > nhiều ví dụ. Chọn ví dụ **liên quan** câu hỏi (dynamic few-shot = RAG ví dụ [[aj08-prompt-optimization]]).
- Ví dụ đa dạng (cover nhiều case) + đúng format mong muốn.
- ⚠️ Nhiều ví dụ → token tăng → cân chất lượng vs cost.

## ⭐ Structured output (cho pipeline)
```
"Trả về JSON: {category: enum, confidence: float}"
   -> dễ parse + validate ([[ai06-llm-output-governance]]) downstream
   -> + schema/function-calling ép cấu trúc -> ít lỗi format
```
→ Bắt buộc cho output đưa vào code/DB (data contract [[ag08-ai-data-contracts]]).

## Nguyên tắc viết prompt tốt
- **Rõ ràng + cụ thể**: nói chính xác muốn gì, format gì.
- **Tách data/instruction**: đánh dấu rõ (chống injection [[ad04-llm-security]]).
- **Ràng buộc**: "chỉ trả lời từ context", "nếu không biết, nói không chắc" (chống bịa).
- **Ví dụ** khi cần format/style.
- **Đo bằng metric**, tối ưu prompt bằng data ([[aj08-prompt-optimization]]), không cảm tính.

## Cạm bẫy
- **CoT cho task đơn giản** → token thừa → chỉ khi cần suy luận.
- **Few-shot ví dụ tệ/không liên quan** → hại → chọn ví dụ đúng.
- **ReAct không giới hạn** → loop/cost ([[aa05-agentic-pipelines]]) → max steps + budget.
- **Structured output không validate** → tin format mù → validate ([[ai06-llm-output-governance]]).
- **Prompt phức tạp quá** → khó debug + token → giữ đơn giản nhất có thể.
- **Không tách data/instruction** → injection ([[ad04-llm-security]]).
- **Tối ưu prompt theo cảm giác** → metric + golden ([[aj08-prompt-optimization]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] 8 mẫu prompt + khi nào dùng.
- [ ] CoT (nghĩ từng bước, token nhiều); ReAct (reason+act, nền agent).
- [ ] Few-shot chọn ví dụ liên quan; structured output cho pipeline.
- [ ] Nguyên tắc: rõ ràng, tách data/instruction, ràng buộc, đo.
- [ ] Cạm bẫy: CoT thừa, ReAct loop, không validate structured.
- 🔭 Tự mò: với 1 task phân loại, viết 3 prompt (zero-shot, few-shot 3 ví dụ, CoT) cho mock-LLM (hoặc tự tay) → so chất lượng + đếm token mỗi cái → thấy trade-off chất lượng/cost; thêm structured output JSON + validate.

➡️ Tiếp [[am03-advanced-chunking]] — chiến lược chunking nâng cao.
