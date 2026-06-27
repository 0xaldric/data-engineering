# AF01 — Case Study: Customer Support AI Platform (system design)

> Đề system-design tổng hợp: thiết kế hệ AI trả lời khách hàng (deflect ticket), an toàn, biết khi nào chuyển người. Vận dụng toàn bộ Module AI. Liên hệ [[aa03-rag-production]], [[ad02-llm-judge]], [[ae01-self-correcting-rag]].

## 1. Làm rõ yêu cầu (clarify trước khi vẽ)
- **Mục tiêu**: giảm ticket tới người (deflection) mà giữ chất lượng + an toàn.
- **Nguồn**: tài liệu help center, lịch sử ticket, FAQ, chính sách.
- **Ràng buộc**: không bịa (sai → mất khách/pháp lý), trả lời <vài giây, đa kênh (chat/email), có PII.
- **Quy mô**: vd 100k câu hỏi/ngày, tài liệu cập nhật hàng ngày.
- **Thước đo**: deflection rate, CSAT, % escalation đúng, hallucination rate ~0.

## 2. ⭐ Kiến trúc tổng thể
```
       INGEST (offline/streaming)                    SERVE (online, mỗi câu hỏi)
help docs/ticket/FAQ                          user hỏi
  ─> parse ([[ad06-doc-parsing]])               ─> [guardrail input] PII/injection ([[aa02-guardrails]])
  ─> chunk + embed                              ─> [semantic cache] ([[ad08-semantic-cache]]) hit? trả luôn
  ─> vector store (incremental [[ad01]])        ─> [query understanding] ([[ae06-query-understanding]])
  ─> freshness: docs đổi -> re-index            ─> [retrieve hybrid + rerank] ([[ae07-reranking-deep]])
                                                ─> [confidence check] đủ tự tin? ([[ae01-self-correcting-rag]])
                                                     ├─ có ─> LLM trả lời + TRÍCH DẪN
                                                     │        ─> [validate output] ([[ai06-llm-output-governance]])
                                                     └─ không ─> ESCALATE sang người
                                                ─> [log + feedback] ([[ab06-llm-observability]])
```

## 3. ⭐ Quyết định thiết kế then chốt
| Vấn đề | Quyết định |
|--------|-----------|
| Chống bịa | **bắt buộc trích dẫn** nguồn; grounding check; không đủ context → "tôi chuyển bạn cho nhân viên" |
| Khi nào escalate | confidence thấp ([[ae01-self-correcting-rag]]) / chủ đề nhạy cảm / khách yêu cầu / sau N lần không giải quyết |
| An toàn | guardrail input+output, PII redact trước khi log ([[ad03-privacy-compliance]]) |
| Tươi | help docs đổi → re-index trong phút ([[ad01-streaming-rag]]); cache invalidation ([[ac06-kb-freshness]]) |
| Rẻ | semantic cache (câu lặp nhiều!) + model routing ([[ac08-ai-cost-scale]]) |
| Đa kênh | voice → STT ([[ac05-voice-audio-pipeline]]) → cùng pipeline text |

## 4. ⭐ Escalation — "biết khi nào KHÔNG trả lời"
Đặc trưng quan trọng nhất của support AI tốt: **thừa nhận không biết** thay vì bịa.
```
trả lời tự động khi: confidence cao + có nguồn + không nhạy cảm
chuyển NGƯỜI khi: confidence thấp / không có doc / khách bực / vấn đề tiền-pháp lý / yêu cầu hành động
-> chuyển kèm TÓM TẮT hội thoại + doc đã tìm (người không phải đọc lại từ đầu)
```
→ Sai cách (cố trả mọi câu) = hallucinate = mất niềm tin. Escalation đúng = AI + người bổ sung nhau.

## 5. Eval & feedback loop
- **Offline**: golden set câu hỏi thật → recall + faithfulness ([[ab02-rag-eval-harness]], [[aa06-llm-eval]]); gate CI.
- **Online**: deflection rate, CSAT 👍/👎, % escalation, câu bị 👎 → bổ sung KB/golden ([[ac03-eval-driven-dev]]).
- 👎 + escalation → **tín hiệu cải thiện**: thiếu doc? chunk tệ? cần FAQ mới? → vòng lặp.

## 6. Data flow & lưu trữ
- Vector store (chunk + embedding), object store (doc gốc), warehouse (log/ticket/feedback → analytics).
- Log mỗi tương tác (provenance [[ai06-llm-output-governance]]) → debug + eval + audit + train FAQ mới.
- LLM logs = nguồn lớn ([[ab06-llm-observability]], [[c06-case-clickstream]]).

## Cạm bẫy (nói trong phỏng vấn)
- **Cố trả mọi câu** (không escalate) → bịa → mất khách; phải có ngưỡng "không biết".
- **Không trích dẫn** → không kiểm chứng được + khách không tin.
- **Quên freshness** → trả chính sách cũ (sai pháp lý) → re-index + cache invalidation.
- **Log cả PII** → rò → redact trước khi log.
- **Không feedback loop** → không cải thiện; 👎 phải thành golden/doc mới.
- **Bỏ qua cache** → đốt tiền (support nhiều câu lặp) → semantic cache.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vẽ kiến trúc ingest + serve từ trí nhớ.
- [ ] Quyết định: chống bịa (trích dẫn), khi nào escalate, an toàn, tươi, rẻ.
- [ ] Escalation = "biết khi nào không trả lời" + chuyển kèm tóm tắt.
- [ ] Eval offline (golden) + online (deflection/CSAT) + feedback loop.
- 🔭 Tự mò: ghép `guardrails_demo` + `rag_over_notes` + `self_correcting_rag` + `llm_output_pipeline` thành 1 luồng support mini: câu hỏi → guardrail → retrieve → nếu confidence < ngưỡng "escalate" (in ra), else trả lời + validate. Log mỗi câu ra JSON.

➡️ Tiếp [[af02-case-enterprise-kb]] — enterprise knowledge assistant.
