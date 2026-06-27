# AD09 — AI Review 4 + Capstone Integration + Drill Cuối

> Tổng kết **AI-Advanced 4** (AD01–AD08) + **mini-product tích hợp** (guardrail→retrieve→judge→cache) + drill phỏng vấn cuối + tổng kết toàn Module AI (4 batch, 13 script). Nối [[ac09-ai-review3]], [[ai10-summary]].

## 🏁 Batch này (AD01–AD08)
| # | Chủ đề | Code | Ý chốt |
|---|--------|------|--------|
| AD01 | Streaming/real-time RAG | ✅ `streaming_rag.py` | doc mới searchable 191ms; incremental≠incremental-index |
| AD02 | LLM-as-judge | ✅ `llm_judge.py` | rubric + bias (length/position); calibrate |
| AD03 | Privacy & compliance | — | residency, RTBF khó với fine-tune, DP, audit |
| AD04 | LLM security | — | indirect injection; 7 tầng defense-in-depth |
| AD05 | RAG dữ liệu có cấu trúc | — | router định lượng/tính; schema retrieval |
| AD06 | Document parsing | — | rác-vào-rác-ra; giữ cấu trúc cho chunk |
| AD07 | Data cho agent prod | — | memory/tool-layer/checkpoint/audit |
| AD08 | Semantic caching | ✅ `semantic_cache.py` | cosine≠ngữ nghĩa; false-hit > false-miss |

→ Kho AI: **13 script chạy được** + ~45 note AI (Module AI + AA + AB + AC + AD).

## ⭐⭐ Capstone Integration — "AI Data Product" thu nhỏ
Ghép các script đã có thành **một luồng production AI hoàn chỉnh**:
```
câu hỏi người dùng
  ─> [1 GUARDRAIL]  guardrails_demo: chặn PII/injection, redact ([[aa02-guardrails]], [[ad04-llm-security]])
  ─> [2 CACHE]      semantic_cache: gần nghĩa câu cũ? -> trả ngay (ngưỡng cao) ([[ad08-semantic-cache]])
  ─> [3 RETRIEVE]   rag_over_notes: hybrid search + incremental index ([[ai02-rag-capstone-writeup]])
  ─> [4 GENERATE]   (LLM sinh câu trả lời từ context — mock)
  ─> [5 VALIDATE]   llm_output_pipeline: schema + grounding, quarantine nếu lỗi ([[ai06-llm-output-governance]])
  ─> [6 JUDGE]      llm_judge: chấm chất lượng, log điểm (online eval) ([[ad02-llm-judge]])
  ─> [7 OBSERVE]    trace + cost + provenance ([[ab06-llm-observability]])
  (định kỳ: rag_eval_harness đo regression; streaming_rag giữ KB tươi)
```
→ **7 tầng** = một hệ AI-DE thật: an toàn + rẻ + đúng + đo được. Mỗi tầng là 1 script đã chạy verify. **Đây là portfolio mạnh nhất**: không phải "gọi API", mà kỹ-sư-hoá toàn pipeline.

## ⭐ Drill phỏng vấn cuối (5 câu KHÓ — tự trả whiteboard)

**Q1. Thiết kế RAG cho 10 triệu tài liệu, cập nhật liên tục, đa ngôn ngữ, có PII. Vẽ kiến trúc.**
> Ingest (CDC/queue) → parse layout-aware ([[ad06-doc-parsing]]) → PII redact + phân loại ([[ad03-privacy-compliance]]) → chunk structure-aware → embed **đa ngữ** ([[ac01-multilingual-rag]]) → vector DB chuyên (Qdrant: HNSW+quantization+sharding [[ab07-vector-search-opt]]) incremental index → serve: guardrail → semantic cache → hybrid retrieve + rerank + filter tenant/lang → LLM → validate output → judge/observe. Freshness SLA: hot=streaming, cold=batch ([[ad01-streaming-rag]]). Eval harness gate ([[ab02-rag-eval-harness]]).

**Q2. Output LLM của bạn thỉnh thoảng sai/độc. Làm sao tin được để đưa vào hệ downstream?**
> Coi output LLM = **dữ liệu không tin được** → data contract: schema validate (pydantic) → repair → quarantine → provenance ([[ai06-llm-output-governance]]); guardrail input+output ([[aa02-guardrails]]); grounding check; test non-deterministic bằng semantic equivalence ([[ai07-testing-nondeterministic]]); hành động nguy hiểm → sandbox + human approve ([[ad04-llm-security]]).

**Q3. Chi phí LLM tháng này gấp 5 lần dự tính. Điều tra & giảm thế nào?**
> Observability ([[ab06-llm-observability]]): dashboard token/cost theo feature/model/user → tìm chỗ đốt. Giảm: semantic cache ([[ad08-semantic-cache]]), model routing/cascade (nhỏ trước [[ac08-ai-cost-scale]]), nén prompt/ít chunk, batch embedding, giới hạn output token, budget cap cho agent. Đo $/query; cảnh báo cost drift.

**Q4. Làm sao biết RAG của bạn "tốt"? Chứng minh bằng số.**
> Eval-driven ([[ac03-eval-driven-dev]]): golden set đại diện → harness đo recall@k/MRR/nDCG ([[ab02-rag-eval-harness]]) + faithfulness (RAGAS [[aa06-llm-eval]]) + LLM-judge có calibrate ([[ad02-llm-judge]]); offline gate CI + online feedback. Đã đo thật: hybrid k=5 = 88% > vector-only 75%.

**Q5. Agent của bạn có quyền chạy SQL và gửi email. Một tài liệu trong KB chứa lệnh độc. Chuyện gì xảy ra, chặn sao?**
> **Indirect prompt injection** ([[ad04-llm-security]]): doc độc bị RAG kéo vào context → LLM coi như lệnh → lạm dụng tool. Chặn: quét nguồn trước index, tách data/instruction, **least-privilege tool** (SQL read-only sandbox [[aa01-text-to-sql]], email cần human approve), output filter, audit mọi tool-call ([[ad07-agent-data]]), defense-in-depth.

## 🏆 Tổng kết toàn Module AI (4 batch)
| Batch | Chủ đề | Script mới |
|-------|--------|-----------|
| Module AI | RAG/governance/test/cost/streaming nền tảng | rag_over_notes, llm_output_pipeline, test_semantic |
| AA (Adv 1) | text-to-SQL, guardrails, dedup, agentic, eval, multimodal, GraphRAG, LLMOps | text_to_sql, guardrails_demo, dedup_minhash |
| AB (Adv 2) | synthetic data, eval harness, context, semantic layer, fine-tune, obs, vector-opt | synthetic_data, rag_eval_harness |
| AC (Adv 3) | đa ngữ, recsys, eval-driven, multi-agent, voice, freshness, feature store, cost | cross_lingual_eval, semantic_recsys |
| AD (Adv 4) | streaming RAG, judge, privacy, security, structured-RAG, parsing, agent-data, cache | streaming_rag, llm_judge, semantic_cache |
→ **13 script chạy được + ~45 note**, không cần API key. Thông điệp xuyên suốt: *mọi nguyên tắc DE áp y nguyên cho AI — danh từ đổi, tư duy không đổi* ([[ai10-summary]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vẽ được luồng tích hợp 7 tầng từ trí nhớ.
- [ ] Trả trôi 5 câu drill (che đáp án).
- [ ] Map mỗi script → tầng nào trong AI data product.
- 🔭 Tự mò LỚN (capstone thật): viết `ai_product.py` ghép tuần tự guardrail → cache → retrieve → (mock generate) → validate → judge, log mỗi tầng; chạy 5 câu hỏi, in ra hành trình mỗi câu (cache hit? quarantine? điểm judge?). Đó là demo phỏng vấn ấn tượng nhất.

➡️ Hết AI-Advanced 4. Batch tiếp: GraphRAG production, RAG agent tự cải thiện, multimodal sâu, data quality cho LLM training, on-device AI.
