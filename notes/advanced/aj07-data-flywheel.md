# AJ07 — LLM Data Flywheel (vòng cải tiến)

> Hệ AI tốt lên **theo thời gian** nhờ vòng lặp: dùng → thu signal → data tốt hơn → model tốt hơn → dùng nhiều hơn. **DE xây cái bánh đà này.** Đây là lợi thế cạnh tranh bền vững. Liên hệ [[ag03-rlhf-preference-data]], [[af07-continuous-eval]], [[ag04-drift-detection]].

## Flywheel là gì & vì sao mạnh
- **Bánh đà (flywheel)**: vòng tự củng cố — mỗi vòng làm vòng sau dễ hơn.
- AI: nhiều người dùng → nhiều data/feedback → model tốt hơn → hút thêm người dùng → ...
- → **Lợi thế cạnh tranh**: đối thủ khó đuổi vì bạn có data flywheel quay trước. "Data moat".

## ⭐ Vòng flywheel
```
        ┌──────────────────────────────────────────┐
        │                                          ↓
   [model phục vụ] → [usage + feedback 👍👎/sửa/click]
        ↑                                          │
        │                                          ↓
   [model tốt hơn] ← [eval/fine-tune] ← [data mới: lọc + nhãn]
        └──────────────────────────────────────────┘
   (DE sở hữu phần thu signal → lọc → đưa vào data → đo cải tiến)
```

## ⭐ DE xây flywheel — 4 mắt xích
| Mắt xích | Việc DE |
|----------|---------|
| **1. Thu signal** | log mọi tương tác + feedback (👍👎, sửa lại, click, escalate, quarantine) — [[ab06-llm-observability]] |
| **2. Lọc/nhãn** | signal nhiễu → lọc thành data sạch ([[ae03-training-data-quality]]); 👎 → ca khó; sửa-lại → preference ([[ag03-rlhf-preference-data]]) |
| **3. Đưa vào data** | bug → thêm golden ([[ac03-eval-driven-dev]]); preference → fine-tune; câu mới → mở rộng KB ([[ac06-kb-freshness]]) |
| **4. Đo cải tiến** | continuous eval ([[af07-continuous-eval]]) xác nhận vòng mới TỐT hơn (không xấu đi) |

## ⭐ Các loại signal (vàng từ production)
```
👍👎 explicit       -> preference trực tiếp
sửa lại câu trả lời -> "đúng phải là thế này" (gold label)
escalate/bỏ đi      -> AI thất bại -> ca cần cải thiện
click/chấp nhận     -> implicit positive ([[ac02-recsys-llm]])
quarantine/refuse   -> ca model không chắc -> thêm data
câu hỏi mới (drift) -> chủ đề thiếu KB ([[ag04-drift-detection]])
```
→ Mỗi tương tác = **một hạt data** nếu biết thu. DE biến "log" thành "nhiên liệu flywheel".

## ⭐ Vòng lặp lành mạnh vs độc hại
| Lành mạnh | Độc hại |
|-----------|---------|
| feedback → data sạch → model tốt hơn | feedback nhiễu/bias → model lệch hơn |
| đo cải tiến (gate) | không đo → trôi xuống ngầm |
| đa dạng signal | chỉ tối ưu 1 metric → Goodhart |
| human review điểm chốt | full-auto → model collapse ([[ab01-synthetic-data]]) |
→ Flywheel **khuếch đại** — cả tốt lẫn xấu. Phải có **gate + human + đo** để quay đúng hướng.

## Cạm bẫy
- **Không thu signal** → không có nhiên liệu → log feedback từ đầu.
- **Signal nhiễu vào thẳng training** → model lệch → lọc/QC trước.
- **Feedback bias** (chỉ người bực mới 👎) → lệch phân phối → cân nhắc.
- **Không đo cải tiến** → vòng mới tệ hơn mà không biết → continuous eval gate.
- **Full-auto flywheel** (model học output của chính nó) → collapse → human điểm chốt.
- **Privacy**: signal chứa PII → redact trước lưu/train ([[ad03-privacy-compliance]]).
- **Tối ưu 1 metric** (CTR) → Goodhart (clickbait) → đa metric.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Flywheel: usage→signal→data→model→usage (tự củng cố, data moat).
- [ ] 4 mắt xích DE: thu signal → lọc → đưa vào data → đo cải tiến.
- [ ] Loại signal (👍👎/sửa/escalate/click/drift).
- [ ] Lành mạnh vs độc hại (gate + human + đo, chống collapse).
- [ ] Cạm bẫy: signal nhiễu, không đo, full-auto, Goodhart.
- 🔭 Tự mò: thêm vào `ai_product.py` ([[aj03-capstone-integration]]) "feedback": mỗi câu trả lời gán 👍/👎 giả + lưu (q, answer, feedback) ra JSONL; viết script đọc JSONL: 👎 → thêm vào "golden cần cải thiện", sửa-lại → "preference pair". Đó là mắt xích thu→lọc của flywheel.

➡️ Tiếp [[aj08-prompt-optimization]] — tối ưu prompt tự động.
