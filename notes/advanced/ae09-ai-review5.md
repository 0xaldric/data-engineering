# AE09 — AI Review 5 + Final Portfolio & Career

> Tổng kết **AI-Advanced 5** (AE01–AE08) + **portfolio AI-DE hoàn chỉnh** (16 script) + lộ trình học tiếp + định vị career "AI Data Engineer" + tổng kết **5 batch** Module AI. Chốt hành trình AI. Nối [[ad09-ai-review4]], [[ac09-ai-review3]], [[ai10-summary]].

## 🏁 Batch này (AE01–AE08)
| # | Chủ đề | Code | Ý chốt |
|---|--------|------|--------|
| AE01 | Self-correcting RAG | ✅ `self_correcting_rag.py` | tự đo→reformulate→retry; conf 0.656→0.814 |
| AE02 | GraphRAG từ wikilinks | ✅ `graphrag_links.py` | graph thật 216 node; hub=khái niệm nền |
| AE03 | Data quality scoring | ✅ `data_quality_score.py` | hard gate vs trung bình; giữ 3/8 |
| AE04 | Multimodal RAG | — | CLIP shared space; cross-modal |
| AE05 | Edge/on-device AI | — | quantize/distill; federated + DP |
| AE06 | Query understanding | — | intent/rewrite/decompose/route |
| AE07 | Reranking sâu | — | bi vs cross-encoder; 2 tầng; MMR |
| AE08 | RAG cho code | — | AST chunk; repo-graph context |

## ⭐⭐ Portfolio AI-DE hoàn chỉnh — 16 script chạy được
| Script | Chủ đề | "Câu chuyện" phỏng vấn |
|--------|--------|------------------------|
| `rag_over_notes.py` | RAG end-to-end | chunk/embed/HNSW/hybrid/incremental |
| `rag_eval_harness.py` | eval sweep | chọn config bằng số (88%>75%) |
| `self_correcting_rag.py` | self-correction | RAG tự sửa, đo +0.158 |
| `streaming_rag.py` | real-time | doc mới searchable 191ms |
| `graphrag_links.py` | GraphRAG | graph thật từ liên kết, multi-hop |
| `cross_lingual_eval.py` | đa ngữ | đo thuế đa ngữ 83% vs 67% |
| `semantic_recsys.py` | recsys | two-tower + cold-start |
| `semantic_cache.py` | cache | cosine≠ngữ nghĩa (nghịch lý) |
| `llm_judge.py` | eval tự động | rubric + bias detection |
| `llm_output_pipeline.py` | governance | validate/quarantine/provenance |
| `test_semantic.py` | test non-det | semantic equivalence |
| `text_to_sql.py` | NL→SQL | guardrail chặn phá hoại |
| `guardrails_demo.py` | an toàn | PII/injection/grounding |
| `dedup_minhash.py` | dedup | MinHash/LSH scale |
| `synthetic_data.py` | sinh data | 4 cổng chất lượng |
| `data_quality_score.py` | DQ training | hard gate đa chiều |
→ **Không cái nào cần API key** (local fastembed/DuckDB) → ai cũng chạy lại được → portfolio "sờ được".

## ⭐ Định vị career: "AI Data Engineer" (trụ cột thứ 4)
```
DE truyền thống:  SQL + Modeling + Pipeline/Orchestration
DE 2025+:         + TRỤ CỘT AI/LLM  <- bạn đang xây ở đây
```
**Bạn KHÔNG cạnh tranh với ML Engineer** (train model) — bạn là người **kỹ-sư-hoá DỮ LIỆU quanh AI**:
- Data **cho** AI: training data, RAG corpus, eval data, synthetic, feature store.
- Data **từ** AI: output governance, LLM logs/observability, provenance.
- Hạ tầng AI-data: vector store, embedding pipeline, streaming re-index, cache, cost.
→ Đây là **ngách thiếu người**: nhiều người biết gọi LLM, ít người biết kỹ-sư-hoá data quanh nó ở chất lượng production.

## ⭐ 5 thông điệp định hình tư duy (nói trong phỏng vấn)
1. **"Danh từ đổi, tư duy DE không đổi"** — idempotency→re-index, lineage→provenance, DQ→eval, contract→output-validation, cost→token, point-in-time→feature store.
2. **"LLM output là dữ liệu KHÔNG tin được"** → data contract: validate/quarantine/provenance.
3. **"AI tốt lên nhờ ĐO"** → golden set + harness + metric, không vibe ([[ac03-eval-driven-dev]]).
4. **"Phần lớn AI là DATA"** → RAG/training/eval/synthetic data = chỗ DE tạo giá trị.
5. **"An toàn không phải tuỳ chọn"** → guardrail/PII/injection/sandbox/decontamination.

## ⭐ Lộ trình học tiếp (sau 5 batch)
- **Làm thật**: chạy lại 16 script, làm hết phần 🔭 "tự mò" → biến hiểu thành kỹ năng.
- **Tích hợp**: ghép thành 1 AI-data-product (capstone [[ad09-ai-review4]] mục 🔭).
- **Scale thật**: thử corpus lớn (10k+ doc), vector DB thật (Qdrant), đo lại.
- **Theo dõi**: vector DB internals, RAG benchmark mới, agent frameworks, LLMOps tools.
- **Đóng góp**: viết blog/repo công khai (đã có repo này!) → chứng minh năng lực.

## 🏆 Tổng kết 5 batch Module AI
| Batch | # note | # script mới | Trọng tâm |
|-------|--------|--------------|-----------|
| Module AI | 9 | 3 | nền tảng RAG/governance/test/cost |
| AA (Adv 1) | 10 | 3 | text-to-SQL/guardrails/dedup/agentic/eval/GraphRAG/LLMOps |
| AB (Adv 2) | 9 | 2 | synthetic/eval-harness/context/fine-tune/obs/vector-opt |
| AC (Adv 3) | 9 | 2 | đa ngữ/recsys/eval-driven/multi-agent/voice/freshness/feature-store/cost |
| AD (Adv 4) | 9 | 3 | streaming/judge/privacy/security/structured/parsing/agent-data/cache |
| AE (Adv 5) | 9 | 3 | self-correct/GraphRAG/DQ/multimodal/edge/query/rerank/code |
→ **~55 note AI + 16 script** = một khoá "AI Data Engineering" hoàn chỉnh, thực chiến, tiếng Việt.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Map 16 script → kỹ năng → câu phỏng vấn (che bảng, tự kể).
- [ ] Nói trôi 5 thông điệp + định vị "AI Data Engineer".
- [ ] Chọn 3 script, làm hết phần 🔭 của note tương ứng.
- 🔭 Tự mò cuối: viết `README` cho `projects/06-ai-data-engineering/` — bảng 16 script + 1 câu mỗi cái + cách chạy; đó là "trang bìa portfolio" khi gửi nhà tuyển dụng.

➡️ Hết AI-Advanced 5. Batch tiếp: RAG benchmark tự động, LLM data pipeline scale lớn, vector DB internals, AI data governance, case study AI-DE thực tế.
