# AF09 — AI Review 6 + System-Design Interview Drill

> Tổng kết **AI-Advanced 6** (AF01–AF08) + **khung trả lời system-design AI** + 3 đề có lời giải + tổng kết 6 batch Module AI. Nối [[ae09-ai-review5]], [[c01-system-design-framework]].

## 🏁 Batch này (AF01–AF08)
| # | Loại | Ý chốt |
|---|------|--------|
| AF01 | Case: Support AI | escalation "biết khi nào không trả lời"; deflection |
| AF02 | Case: Enterprise KB | permission-aware retrieval (pre-filter ACL) |
| AF03 | Case: Coding Assistant | incremental theo commit; repo-context graph |
| AF04 | Internals | HNSW/IVF-PQ/DiskANN/filtered search |
| AF05 | Scale | training data petabyte; dedup phân tán |
| AF06 | Governance | lineage AI; model card; EU AI Act |
| AF07 | ✅ `continuous_eval.py` | regression gate exit-code; baseline |
| AF08 | Case: Personalization | streaming features + point-in-time + LLM re-rank |

## ⭐⭐ KHUNG trả lời system-design AI (7 bước — học thuộc)
```
1. CLARIFY   mục tiêu, nguồn data, ràng buộc (latency/PII/scale), thước đo thành công
2. DATA FLOW ingest (parse/chunk/embed/index) + freshness (stream vs batch)
3. RETRIEVE  hybrid + rerank + filter (permission/tenant) + query understanding
4. SAFETY    guardrail (PII/injection), grounding/citation, escalation, output validate
5. EVAL      golden set, recall/faithfulness, continuous gate, online feedback
6. SCALE     vector DB (ANN/quantize/shard), incremental, cache, streaming
7. COST      routing/cascade, cache, $/query, budget cap
```
→ Mọi đề AI-DE đi qua khung này. Khác đề chỉ là **nhấn** bước nào (support→safety/escalation; enterprise→permission; personalization→streaming/point-in-time).

## ⭐ Đề 1: "Thiết kế RAG hỏi-đáp tài liệu nội bộ 1 triệu doc, có phân quyền"
> **Clarify**: ai dùng, quyền thế nào, freshness cần, PII? **Data flow**: connector đa nguồn giữ ACL → parse → chunk → embed → vector DB (chunk + ACL + version). **Retrieve**: ⭐ **pre-filter ACL** (user chỉ thấy doc được phép [[af02-case-enterprise-kb]]) + hybrid + rerank. **Safety**: chỉ đưa doc được phép vào context; citation; PII redact. **Eval**: golden có cả test quyền (user X không thấy doc Y); recall + faithfulness. **Scale**: Qdrant filtered search ([[af04-vector-db-internals]]), incremental. **Cost**: cache theo user. → Nhấn: **permission + freshness**.

## ⭐ Đề 2: "Thiết kế hệ phát hiện gian lận dùng LLM trên giao dịch real-time"
> **Clarify**: latency (real-time!), volume, định nghĩa fraud, hậu quả false-pos/neg. **Data flow**: stream giao dịch (Kafka) → feature real-time ([[ac07-feature-store]]) + LLM phân tích pattern bất thường/giải thích. **Retrieve**: RAG luật/case fraud tương tự (vector). **Safety**: LLM **bổ trợ** không tự quyết khoá tiền → human/rule cho hành động ([[ad04-llm-security]] excessive agency); output validate ([[ai06-llm-output-governance]]). **Eval**: precision/recall fraud, point-in-time chống leakage ([[af08-case-personalization]]). **Scale**: streaming, LLM chỉ cho ca nghi ngờ (cascade [[ac08-ai-cost-scale]]). **Cost**: đa số giao dịch qua rule rẻ, LLM cho ca khó. → Nhấn: **real-time + LLM-bổ-trợ-không-tự-quyết + point-in-time**.

## ⭐ Đề 3: "Thiết kế nền data cho AI agent tự động xử lý email khách hàng"
> **Clarify**: agent làm gì (đọc/phân loại/trả lời/tạo ticket?), quyền hành động, rủi ro. **Data flow**: email → parse → phân loại intent ([[ae06-query-understanding]]) → RAG context. **Retrieve + agent**: tool data-access có governance ([[ad07-agent-data]]); memory ([[ab03-context-engineering]]). **Safety**: ⭐ indirect injection (email = nguồn không tin — [[ad04-llm-security]]); hành động nguy hiểm (gửi tiền/xoá) → human approve; least-privilege tool. **Eval**: task success rate; LLM-judge ([[ad02-llm-judge]]). **Scale**: checkpoint/resume ([[ad07-agent-data]]), audit mọi action. **Cost**: budget cap chống loop. → Nhấn: **agent safety + indirect injection + audit**.

## 🏆 Tổng kết 6 batch Module AI
| Batch | Trọng tâm | Script |
|-------|-----------|--------|
| Module AI | nền tảng RAG/governance/test | 3 |
| AA | text-to-SQL/guardrails/dedup/agentic/eval | 3 |
| AB | synthetic/harness/context/fine-tune/obs | 2 |
| AC | đa ngữ/recsys/eval-driven/voice/feature-store | 2 |
| AD | streaming/judge/privacy/security/cache | 3 |
| AE | self-correct/GraphRAG/DQ/multimodal/rerank/code | 3 |
| AF | **case studies + scale + internals + governance** | 1 |
→ **6 batch · ~64 note AI · 17 script chạy được** = khoá "AI Data Engineering" đầy đủ từ nền tảng → nâng cao → **system design thực chiến**.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Thuộc khung 7 bước system-design AI (clarify→flow→retrieve→safety→eval→scale→cost).
- [ ] Giải 3 đề, nhận ra mỗi đề "nhấn" bước nào.
- [ ] Map case study → kỹ năng nền tảng đã học.
- 🔭 Tự mò cuối: tự ra 1 đề system-design AI (vd "AI tóm tắt cuộc họp", "AI search ảnh sản phẩm") rồi viết lời giải theo khung 7 bước, vẽ kiến trúc, chỉ rõ nhấn bước nào — như phỏng vấn thật.

➡️ Hết AI-Advanced 6. Batch tiếp: agent platform data, RAG cho BI/analytics, AI observability sâu, RLHF data, multimodal production.
