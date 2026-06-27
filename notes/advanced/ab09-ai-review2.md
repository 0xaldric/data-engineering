# AB09 — AI Data Engineering Review 2 + Checklist Phỏng vấn

> Tổng kết **AI-Advanced 2** (AB01–AB08) + checklist "AI Data Engineer sẵn sàng" đầy đủ + map mọi note/script → kỹ năng phỏng vấn + portfolio talking points. Nối tiếp [[ai10-summary]], [[aa10-llmops]].

## 🏁 Batch này có gì (AB01–AB08)
| # | Chủ đề | Code chạy được | Ý chốt |
|---|--------|----------------|--------|
| AB01 | Synthetic data generation | ✅ `synthetic_data.py` | 4 cổng chất lượng; mode collapse; 144→42 |
| AB02 | RAG eval harness | ✅ `rag_eval_harness.py` | chọn config bằng SỐ; hybrid 88%>vector 75%; nDCG/IDCG |
| AB03 | Context engineering & memory | — | token budget, lost-in-middle, memory=RAG pipeline |
| AB04 | Semantic layer cho LLM | — | NL→{metric,dim,filter} thay SQL thô; an toàn/nhất quán |
| AB05 | Embedding fine-tuning | — | contrastive+hard negative; DE=training pairs; re-embed |
| AB06 | LLM observability/tracing | — | trace/span; LLM logs=clickstream; provenance đầy đủ |
| AB07 | Vector search optimization | — | HNSW/IVF/quantization; recall⇄latency⇄RAM; tune SLA |
| AB08 | Fine-tuning data pipeline | — | 7 bước; decontaminate; version dataset; data>model |

→ Tổng kho AI giờ: **8 script chạy được** + ~27 note AI (Module AI 9 + AI-Advanced 10 + AI-Advanced 2: 8).

## ⭐ 8 script AI chạy được — bộ portfolio
| Script | Chứng minh kỹ năng | Câu phỏng vấn trả được |
|--------|--------------------|------------------------|
| `rag_over_notes.py` | RAG đầy đủ: chunk/embed/HNSW/hybrid/eval, incremental | "Xây RAG thế nào? đo ra sao?" |
| `rag_eval_harness.py` | chọn config bằng metric, sweep | "Biết RAG tốt lên nhờ đâu?" |
| `llm_output_pipeline.py` | governance: validate/repair/quarantine/provenance | "Output LLM không tin được, xử lý sao?" |
| `test_semantic.py` | test hệ phi-quyết-định (cosine) | "Test cái non-deterministic kiểu gì?" |
| `text_to_sql.py` | guardrail chặn SQL phá hoại + sandbox | "Text-to-SQL có nguy hiểm không?" |
| `guardrails_demo.py` | PII redact + injection + grounding | "Chống prompt injection / rò PII?" |
| `dedup_minhash.py` | MinHash+LSH near-dup ở scale | "Dedup triệu doc thế nào?" |
| `synthetic_data.py` | sinh data + 4 cổng chất lượng | "Thiếu data thì làm sao?" |

## ⭐⭐ Checklist "AI Data Engineer sẵn sàng" (tự chấm)
**RAG & Retrieval**
- [ ] Chunking (cố định/structure-aware/semantic) + trade-off ([[ai03-chunking]]).
- [ ] Embedding: model chọn sao, versioning, đổi model⇒re-embed ([[ai04-embedding-versioning]]).
- [ ] Vector store + ANN (HNSW/IVF), quantization, filter ([[ab07-vector-search-opt]], [[k05-vector-rag-deep]]).
- [ ] Hybrid + rerank ([[aa03-rag-production]]); đo recall@k/MRR/nDCG ([[ab02-rag-eval-harness]]).
- [ ] Production: cache, citation, fallback, multi-tenancy ([[aa03-rag-production]]).

**LLM output là dữ liệu không tin được**
- [ ] Validate/repair/quarantine + provenance ([[ai06-llm-output-governance]]).
- [ ] Guardrail: PII, prompt injection, grounding ([[aa02-guardrails]]).
- [ ] Test non-deterministic (semantic equivalence) ([[ai07-testing-nondeterministic]]).
- [ ] Text-to-SQL có guardrail / semantic layer ([[aa01-text-to-sql]], [[ab04-semantic-layer-llm]]).

**Data CHO AI (training/fine-tune)**
- [ ] Training data prep: clean/dedup/decontaminate ([[aa04-training-data-prep]]).
- [ ] Synthetic data + chất lượng ([[ab01-synthetic-data]]).
- [ ] Fine-tune pipeline + version dataset ([[ab08-finetune-pipeline]], [[ab05-embedding-finetune]]).

**Vận hành (LLMOps)**
- [ ] Eval framework + golden set + CI gate ([[aa06-llm-eval]], [[ab02-rag-eval-harness]]).
- [ ] Observability/tracing + cost/token ([[ab06-llm-observability]], [[ai08-ai-cost-latency]]).
- [ ] Prompt management/versioning ([[aa07-prompt-management]]).
- [ ] LLMOps tổng thể: deploy/monitor/drift ([[aa10-llmops]]).

**Kiến trúc & nâng cao**
- [ ] Streaming AI / re-index ([[ai09-streaming-ai]]).
- [ ] Agentic pipeline + giám sát ([[aa05-agentic-pipelines]]); context engineering ([[ab03-context-engineering]]).
- [ ] Multimodal ([[aa08-multimodal]]); GraphRAG ([[aa09-graphrag]]).

## ⭐ Thông điệp lớn (nói được trong phỏng vấn)
1. **"Danh từ đổi, tư duy DE không đổi"**: idempotency→re-index, lineage→provenance, data quality→eval, data contract→output validation, cost→token, governance→guardrail, versioning→model/prompt/embedding/dataset.
2. **"LLM output là dữ liệu KHÔNG TIN ĐƯỢC"** → áp data contract: validate/quarantine/provenance.
3. **"AI tốt lên nhờ ĐO"** → golden set + harness + metric, không "vibe".
4. **"Phần lớn AI là DATA, không phải model"** → RAG data, training data, eval data, synthetic data → đó là chỗ DE tạo giá trị.
5. **"An toàn không phải tuỳ chọn"** → guardrail, PII, injection, sandbox, decontamination.

## Portfolio talking points (kể chuyện 60 giây)
> "Mình xây một RAG end-to-end trên 200+ note: chunk structure-aware, embed local (fastembed, không API), HNSW trong DuckDB, hybrid search, **incremental theo content-hash**. Quan trọng hơn — mình viết **eval harness** đo recall@k/MRR/nDCG để chọn config bằng số (phát hiện hybrid k=5 đạt 88% vs vector-only 75%), một **governance pipeline** validate+quarantine output LLM như data contract, và **guardrail** chặn PII/injection/SQL phá hoại. Tất cả chạy được, không cần API key. Tư duy xuyên suốt: mọi nguyên tắc DE kinh điển áp y nguyên cho AI."

## ✅ "Tự kiểm tra & tự mò"
- [ ] Đọc lại checklist, chấm phần nào chưa vững → mở note tương ứng.
- [ ] Chạy lại cả 8 script, với mỗi cái nói được "scale lên triệu doc thì đổi gì".
- [ ] Tập kể portfolio 60 giây không nhìn note.
- 🔭 Tự mò lớn: ghép 3 script thành 1 mini-product — `guardrails_demo` (lọc input) → `rag_over_notes` (retrieve) → `llm_output_pipeline` (validate output) → `rag_eval_harness` (đo). Đó là "AI Data product" thu nhỏ có đủ: an toàn + retrieval + governance + eval.

➡️ Hết AI-Advanced 2. Batch tiếp: RAG đa ngôn ngữ, agentic sâu, data cho voice/recsys+LLM, evaluation-driven development.
