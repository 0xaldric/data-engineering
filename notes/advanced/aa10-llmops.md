# AA10 — LLMOps + Vector DB at Scale (+ tổng kết AI-Advanced)

> Vận hành hệ LLM ở production (như MLOps/DataOps cho LLM) + vector DB quy mô lớn. Liên hệ [[f06-dataops]], [[k07-observability-tooling]].

## LLMOps là gì
DevOps/MLOps áp cho hệ LLM: deploy + monitor + version + cost + eval cho **model + prompt + RAG pipeline**. Khác MLOps truyền thống ở: prompt là artifact, output non-deterministic, cost theo token, đánh giá khó.

## Trụ cột LLMOps
| Trụ | Việc |
|-----|------|
| **Versioning** | model + **prompt** ([[aa07-prompt-management]]) + dataset + embedding model ([[ai04-embedding-versioning]]) + output (provenance — [[ai06-llm-output-governance]]) |
| **Deploy** | model serving (API/self-host), rollout (canary/blue-green — [[f06-dataops]]), rollback |
| **Eval/CI** | regression eval mỗi đổi prompt/model (golden set — [[aa06-llm-eval]]) → gate |
| **Monitor** | latency p99, cost/token, output quality (faithfulness), drift, % fallback, error |
| **Cost** | token spend dashboard, budget alert, cache hit rate ([[ai08-ai-cost-latency]]) |
| **Feedback** | thu user feedback → online eval + cải tiến |
| **Safety** | guardrail (PII/injection/grounding — [[aa02-guardrails]]) monitoring |

## ⭐ Monitor đặc thù LLM (khác monitor hệ thống)
- **Quality drift**: faithfulness/accuracy tụt theo thời gian (model API nâng cấp ngầm, tài liệu đổi).
- **Cost drift**: token/query tăng (prompt phình, retrieval nhiều chunk).
- **Output distribution**: phân phối nhãn/độ dài đổi → model behavior đổi.
- **Hallucination rate**, **% fallback**, **% quarantine** ([[ai06-llm-output-governance]]).
- = observability ([[k07-observability-tooling]] 5 trụ) áp cho output AI.

## ⭐ Vector DB at scale
Capstone dùng DuckDB (1454 vector) — production triệu/tỉ vector cần:
| Vấn đề | Khắc phục |
|--------|-----------|
| Brute-force O(n) sập | **ANN index** (HNSW/IVF — [[k05-vector-rag-deep]]) |
| RAM khổng lồ (vector to) | **quantization (PQ)**: nén vector → giảm RAM, giảm chính xác chút |
| 1 node không đủ | **sharding** (chia vector qua node) + replication |
| Filter + vector chậm | pre-filter vs post-filter; index hỗ trợ metadata filter |
| Write/rebuild index | incremental index, batch upsert |
| Re-embed khi đổi model | blue-green index ([[ai04-embedding-versioning]]) |
→ Vector DB chuyên (Qdrant/Milvus/Weaviate/pgvector) lo phần này; biết trade-off để chọn + tune (recall vs latency vs RAM vs cost).

## Model: API vs self-host
- **API** (OpenAI/Anthropic): nhanh có, chất lượng cao, không quản hạ tầng; nhưng cost/token, latency mạng, **gửi data ra ngoài** (PII!), version đổi ngầm.
- **Self-host** (Llama, local embedding như fastembed): kiểm soát, rẻ ở scale, data ở nhà; nhưng cần GPU/vận hành.
- Build vs buy ([[f03-modern-data-stack]]) áp cho LLM.

---
## 🏁 Tổng kết AI-Advanced (AA01–AA10)
| # | Chủ đề | Code chạy được |
|---|--------|----------------|
| AA01 | Text-to-SQL + guardrail | ✅ `text_to_sql.py` |
| AA02 | Guardrails (PII/injection/grounding) | ✅ `guardrails_demo.py` |
| AA03 | RAG production patterns | — |
| AA04 | Training data prep (MinHash/LSH) | ✅ `dedup_minhash.py` |
| AA05 | Agentic data pipelines | — |
| AA06 | LLM eval (RAGAS) | — |
| AA07 | Prompt management | — |
| AA08 | Multimodal pipelines | — |
| AA09 | GraphRAG | — |
| AA10 | LLMOps + vector DB at scale | — |

→ Cùng **6 script AI** (RAG/governance/test/text-to-SQL/guardrails/dedup) = bộ portfolio AI Data Engineering hoàn chỉnh.

## Thông điệp xuyên suốt Module AI
**Mọi nguyên tắc DE áp y nguyên cho AI**: idempotency, incremental, lineage/provenance, data quality (→ eval), data contract (→ output validation), cost (→ token), streaming (→ re-index), governance (→ guardrail/PII), versioning (→ model/prompt/embedding). "Danh từ đổi, tư duy không đổi" ([[ai10-summary]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] LLMOps trụ cột (version/deploy/eval/monitor/cost/safety).
- [ ] Monitor đặc thù LLM (quality/cost drift, hallucination rate).
- [ ] Vector DB at scale (ANN/PQ/sharding/filter).
- [ ] API vs self-host trade-off.
- 🔭 Tự kiểm: chạy lại cả 6 script trong `projects/06-ai-data-engineering/` — đó là "production AI-DE" thu nhỏ; nghĩ mỗi cái scale lên triệu doc thì đổi gì.

➡️ Hết AI-Advanced. Batch AI tiếp: synthetic data, context engineering, semantic layer cho LLM, RAG eval nâng cao.
