# AG03 — RLHF & Preference Data Pipeline

> Data để "dạy model theo ý người" (RLHF/DPO): cặp **preference** (câu nào tốt hơn). Vai trò DE: thu thập, đảm bảo chất lượng annotation, version preference data. "Model thông minh nhờ data preference tốt". Liên hệ [[ab08-finetune-pipeline]], [[ae03-training-data-quality]], [[ad02-llm-judge]].

## RLHF/DPO cần data gì
| Giai đoạn | Data |
|-----------|------|
| **SFT** (nền) | (prompt, câu trả lời tốt) — instruction tuning ([[ab08-finetune-pipeline]]) |
| **Reward model / DPO** | (prompt, **chosen**, **rejected**) — cặp so sánh "A tốt hơn B" |
| **RL (PPO)** | reward model chấm output → tinh chỉnh policy |
→ Trọng tâm DE ở đây: **preference pairs** (cặp so sánh) — khác data thường (không phải nhãn đúng/sai, mà **thứ tự ưu tiên**).

## ⭐ Thu preference data — nguồn
```
1 prompt -> model sinh 2+ câu trả lời (A, B) -> NGƯỜI chọn cái tốt hơn -> (chosen, rejected)
```
| Nguồn | Mô tả | Đánh đổi |
|-------|-------|----------|
| **Human annotation** | người chấm A vs B theo guideline | chất lượng cao, đắt/chậm |
| **RLAIF** (AI feedback) | LLM mạnh chấm thay người ([[ad02-llm-judge]]) | rẻ/nhanh, nhưng kế thừa bias model-judge |
| **Implicit** (production) | 👍/👎, click, sửa lại của user | nhiều, miễn phí, nhưng nhiễu |
→ Thực tế trộn: human cho phần khó/an toàn, AI/implicit cho scale.

## ⭐⭐ Chất lượng annotation (DE chịu trách nhiệm)
Preference data **rác → model học sai sở thích**. Phải kiểm:
| Vấn đề | Cách |
|--------|------|
| **Inter-annotator agreement** | nhiều người chấm cùng cặp → đo đồng thuận (Cohen's kappa); thấp = guideline mơ hồ |
| **Guideline rõ** | tiêu chí "tốt" cụ thể (đúng/an toàn/hữu ích) → giảm chủ quan |
| **Annotator bias** | người thích câu DÀI/tự tin (như LLM-judge [[ad02-llm-judge]]) → kiểm + cân bằng |
| **Calibration** | annotator chấm nhất quán theo thời gian không |
| **Gold questions** | chèn câu có đáp án biết trước → bắt annotator ẩu |
→ Đây là **data quality** ([[ae03-training-data-quality]]) cho preference: agreement + gold + guideline.

## ⭐ Reward hacking (cạm bẫy đặc thù RLHF)
Model học **tối ưu reward, không phải ý thật**:
```
reward model thích câu DÀI -> policy sinh câu dài lê thê (dù không tốt hơn)
reward model thích "tự tin" -> policy tự tin cả khi sai (hallucinate tự tin!)
```
→ Preference data lệch → reward model lệch → policy "lách luật". Chống: data đa dạng, kiểm bias độ dài/giọng, eval trên ý THẬT không chỉ reward score.

## Pipeline preference data (DE sở hữu)
```
prompt set ─> sinh nhiều câu trả lời ─> [annotation: human/AI/implicit]
   ─> [QC: agreement, gold check, dedup] ([[ae03-training-data-quality]])
   ─> [cân bằng: đa dạng prompt, chống bias độ dài]
   ─> [format: (prompt, chosen, rejected)] + [version dataset] ([[ab08-finetune-pipeline]])
   ─> reward model / DPO train ─> eval trên ý thật (không chỉ reward)
```

## Cạm bẫy
- **Annotation ẩu/mơ hồ guideline** → agreement thấp → data nhiễu → gold + guideline rõ.
- **Annotator bias** (thích dài/tự tin) → model học bias → kiểm + cân bằng.
- **Reward hacking** → policy lách reward → eval ý thật + data đa dạng.
- **Chỉ RLAIF** (AI chấm hết) → kế thừa bias model-judge + thiếu góc người → trộn human.
- **Implicit nhiễu** (click ≠ tốt) → lọc/khử nhiễu trước dùng.
- **Không version** → không tái lập "model học từ preference nào" ([[af06-ai-data-governance]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] RLHF/DPO cần preference pairs (chosen/rejected), khác nhãn đúng/sai.
- [ ] Nguồn: human / RLAIF / implicit — đánh đổi.
- [ ] Chất lượng annotation: agreement (kappa), gold, guideline, bias.
- [ ] Reward hacking: tối ưu reward ≠ ý thật (bias dài/tự tin).
- [ ] Pipeline: thu → QC → cân bằng → format → version → eval ý thật.
- 🔭 Tự mò: tạo 20 cặp preference giả (prompt + 2 câu trả lời, gán "chosen") trộn vài cặp "annotator bias" (chọn câu dài hơn dù tệ); viết check phát hiện bias: tỉ lệ "chosen dài hơn rejected" — nếu quá cao → cảnh báo length bias trong annotation.

➡️ Tiếp [[ag04-drift-detection]] — phát hiện drift (chạy được).
