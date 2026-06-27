# AG02 — Hallucination Detection & Mitigation ⭐ (có code chạy được)

> Phát hiện LLM "bịa" — vấn đề số 1 của LLM trong production. Nhiều phương pháp đo, mỗi cái bắt một kiểu. Bài học lớn: **đo bề mặt (cosine) ≠ đo sự thật**. Code: [`hallucination_detect.py`](../../projects/06-ai-data-engineering/hallucination_detect.py). Liên hệ [[aa02-guardrails]], [[ad02-llm-judge]], [[ai06-llm-output-governance]].

## Hallucination là gì & vì sao nguy hiểm
- LLM sinh thông tin **nghe hợp lý nhưng SAI** (bịa số, tên, sự kiện, trích dẫn không tồn tại).
- Nguy: người tin (giọng tự tin), sai trong support/y tế/pháp lý → hậu quả thật.
- Không thể loại 100% → phải **phát hiện + giảm thiểu + thừa nhận khi không chắc**.

## ⭐ Các phương pháp phát hiện
| Phương pháp | Ý tưởng | Bắt được |
|-------------|---------|----------|
| **Grounding** | câu trả lời có bám CONTEXT (RAG) không? | bịa ngoài nguồn |
| **Self-consistency** | hỏi N lần, lệch nhau nhiều = đoán/bịa | model không chắc |
| **NLI/entailment** | context có "kéo theo" (entail) câu trả lời? | mâu thuẫn logic |
| **Citation check** | mọi câu có nguồn dẫn thật không? | trích dẫn bịa |
| **LLM-judge** | model khác chấm "có grounded không" | tổng hợp ([[ad02-llm-judge]]) |

## ⭐⭐ Bài học cốt lõi (code chạy): cosine ≠ sự thật
Self-consistency bằng **cosine** giữa N câu trả lời — tưởng đơn giản nhưng **bị lừa**:
```
câu CHẮC CHẮN (paraphrase idempotency)  cosine=0.767
câu BỊA (DuckDB năm 2019/2015/2021)     cosine=0.838  <- CAO HƠN!
```
**NGHỊCH LÝ**: 3 câu bịa **cùng khuôn** ("DuckDB ra mắt năm X bởi Y"), chỉ khác năm → cosine cao **dù mâu thuẫn sự thật**. Câu đúng dùng từ ngữ đa dạng → cosine thấp hơn. → **Cosine đo bề mặt câu, KHÔNG đo đúng/sai** (cùng họ nghịch lý [[ad08-semantic-cache]]).

## ⭐ Đúng cách: so FACT, không so embedding
```
trích FACT (năm/số/entity) từ mỗi câu trả lời -> so có MÂU THUẪN không
câu CHẮC CHẮN: năm trích = {} -> không mâu thuẫn -> OK
câu BỊA:      năm trích = {2015, 2019, 2021} -> MÂU THUẪN -> ⚠️ bịa
```
→ Self-consistency phải ở mức **claim/fact** (NLI, trích entity, so số), không phải cosine surface. Code minh hoạ: trích năm 4 chữ số → mâu thuẫn = cờ bịa (bắt đúng cái cosine bỏ lỡ).

## ⭐ Grounding (phương pháp tin cậy hơn cho RAG)
```
trả lời ĐÚNG context (Parquet cột/nén)        grounding=0.870 -> OK
trả lời BỊA (Parquet dùng GPU/blockchain)     grounding=0.681 -> ⚠️ ngoài nguồn
```
→ Có context (RAG) → đo câu trả lời bám context (cosine/NLI) là tín hiệu tốt: ngoài nguồn = bịa. Calibrate ngưỡng ([[aa02-guardrails]]).

## Mitigation (giảm bịa)
- **RAG**: cho context thật → giảm bịa (model bám nguồn thay vì bộ nhớ).
- **"Tôi không chắc"**: confidence thấp → thừa nhận, không ép trả lời ([[ae01-self-correcting-rag]] escalate).
- **Citation bắt buộc**: mọi claim phải dẫn nguồn → kiểm được ([[af01-case-support-ai]]).
- **Validate output**: quarantine câu nghi bịa ([[ai06-llm-output-governance]]).
- **Temperature thấp** cho task factual; prompt "chỉ trả lời từ context".

## Cạm bẫy
- **Tin cosine self-consistency** → bị lừa bởi câu cùng khuôn khác fact → so fact/NLI.
- **Không có context mà đo grounding** → vô nghĩa → grounding chỉ cho RAG.
- **Ngưỡng grounding sai** → false-flag/bỏ lỡ → calibrate trên data thật.
- **Ép trả lời mọi câu** → bịa → cho phép "không chắc".
- **Chỉ 1 phương pháp** → mỗi cái bắt 1 kiểu → kết hợp (grounding + fact + judge).
- **Citation không kiểm** → trích dẫn bịa lọt → verify nguồn có thật.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 5 phương pháp phát hiện (grounding/self-consistency/NLI/citation/judge).
- [ ] ⭐ Cosine self-consistency bị lừa (cùng khuôn khác fact) → so FACT.
- [ ] Grounding cho RAG (bám context); calibrate ngưỡng.
- [ ] Mitigation: RAG, "không chắc", citation, validate, temp thấp.
- [ ] Kết hợp nhiều phương pháp (1 cái không đủ).
- 🔭 Tự mò: thêm vào `hallucination_detect.py` phương pháp **citation check**: bắt model "trả lời + trích chunk id"; verify chunk id có thật trong index `rag_over_notes` + câu trả lời cosine cao với chunk đó; cờ nếu trích chunk không tồn tại hoặc không liên quan.

➡️ Tiếp [[ag03-rlhf-preference-data]] — data cho RLHF.
