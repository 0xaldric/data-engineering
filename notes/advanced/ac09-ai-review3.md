# AC09 — AI Review 3 + Ngân Hàng Câu Hỏi Phỏng Vấn AI-DE

> Tổng kết **AI-Advanced 3** (AC01–AC08) + **ngân hàng 45 câu hỏi phỏng vấn** AI Data Engineering (trả lời ngắn) + final portfolio pitch. Nối tiếp [[ai10-summary]], [[ab09-ai-review2]].

## 🏁 Batch này có gì (AC01–AC08)
| # | Chủ đề | Code | Ý chốt |
|---|--------|------|--------|
| AC01 | Cross-lingual RAG | ✅ `cross_lingual_eval.py` | thuế đa ngữ VI 83% vs EN 67%; model đa ngữ |
| AC02 | Semantic recsys | ✅ `semantic_recsys.py` | two-tower; cold-start; point-in-time |
| AC03 | Eval-driven development | — | eval-first/TDD cho LLM; golden=spec; CI gate |
| AC04 | Multi-agent & tool design | — | 1 agent đủ; tool tốt > nhiều agent |
| AC05 | Voice/audio pipeline | — | STT→diar→align→chunk; transcript=fact |
| AC06 | KB freshness | — | RAG không build-1-lần; reconcile; mâu thuẫn |
| AC07 | Feature store | — | parity + point-in-time; embedding=feature |
| AC08 | Cost ở scale | — | routing/cascade/cache nhiều tầng; $/query |

→ Kho AI: **10 script chạy được** + ~36 note AI (Module AI 9 + AA 10 + AB 9 + AC 9).

## ⭐⭐ NGÂN HÀNG CÂU HỎI PHỎNG VẤN (45 câu, trả lời ngắn)

### A. RAG & Retrieval
1. **RAG là gì, khi nào dùng thay fine-tune?** Retrieval-Augmented Gen: lấy context liên quan rồi đưa vào prompt. Dùng khi cần *kiến thức mới/đổi nhanh*; fine-tune khi cần *đổi hành vi/phong cách*. ([[ab08-finetune-pipeline]])
2. **Chunk thế nào cho tốt?** Structure-aware (theo heading) + size hợp lý + overlap; giữ ngữ nghĩa trọn. ([[ai03-chunking]])
3. **Đo retrieval ra sao?** recall@k (có lọt không), MRR/nDCG (xếp hạng). nDCG chia IDCG ∈[0,1]. ([[ab02-rag-eval-harness]])
4. **Hybrid search là gì, vì sao hơn vector-only?** Lai vector + keyword; bắt cả từ khoá/tên riêng vector trượt. Đo được: 88% vs 75%. ([[aa03-rag-production]])
5. **Vì sao cần rerank?** Tăng k chỉ tăng recall, không sửa hạng; cross-encoder rerank top-N cải thiện MRR/nDCG. ([[ab07-vector-search-opt]])
6. **Đổi embedding model phải làm gì?** Re-embed TOÀN corpus (không cùng không gian) + blue-green index. ([[ai04-embedding-versioning]])
7. **RAG đa ngôn ngữ?** Model EN-centric rớt cross-lingual (đo +17%); dùng embedding đa ngữ (e5/bge-m3). ([[ac01-multilingual-rag]])
8. **Stale RAG xử lý sao?** Reconcile nguồn↔index; phát hiện đổi bằng hash/CDC; xoá ghost; effective_date cho mâu thuẫn. ([[ac06-kb-freshness]])

### B. LLM output = dữ liệu không tin được
9. **Vì sao không tin output LLM?** Non-deterministic, hay hallucinate, sai format → coi như data contract: validate. ([[ai06-llm-output-governance]])
10. **Pipeline governance output?** extract→validate(schema)→repair→quarantine→provenance log. ([[ai06-llm-output-governance]])
11. **Test cái non-deterministic kiểu gì?** Semantic equivalence (cosine ≥ ngưỡng) + schema validation, không so chuỗi. ([[ai07-testing-nondeterministic]])
12. **Prompt injection là gì, chống sao?** Input lừa LLM bỏ qua lệnh; chống: tách data/instruction, lọc pattern, guardrail, least privilege. ([[aa02-guardrails]])
13. **Grounding/faithfulness check?** Đo câu trả lời có bám context (cosine/LLM-judge); ngưỡng phải calibrate. ([[aa02-guardrails]])
14. **Text-to-SQL có nguy hiểm không?** Có: SQL phá hoại + sai metric. Chống: guardrail (chỉ SELECT, chặn DROP), EXPLAIN, sandbox read-only; tốt hơn → semantic layer. ([[aa01-text-to-sql]], [[ab04-semantic-layer-llm]])

### C. Data CHO AI
15. **Chuẩn bị training data?** Clean → dedup (MinHash/LSH) → **decontaminate** (bỏ trùng test) → format → split → version. ([[aa04-training-data-prep]])
16. **Decontamination là gì, vì sao quan trọng?** Loại mẫu trùng test khỏi train; quên → eval ảo cao, thật thì kém. ([[ab08-finetune-pipeline]])
17. **Synthetic data — kiểm soát chất lượng?** 4 cổng: quality/dedup/diversity/balance; coi chừng mode collapse. ([[ab01-synthetic-data]])
18. **Embedding fine-tune khi nào?** Khi domain lệch & đã thử model đa ngữ/hybrid/chunk không đủ; contrastive + hard negative. ([[ab05-embedding-finetune]])
19. **Version dataset để làm gì?** Reproducibility: model checkpoint ↔ dataset version → tái lập/debug. ([[ab08-finetune-pipeline]])
20. **Vai trò DE trong fine-tune?** Sở hữu DATA (thu/sạch/dedup/decontaminate/format/version/eval), không train. "Data > model".

### D. Eval & LLMOps
21. **Eval-driven development?** Eval trước, code sau (TDD cho LLM); golden=spec; mọi đổi qua gate; CI chống regression. ([[ac03-eval-driven-dev]])
22. **Golden set tốt?** Đại diện, đa dạng, có nhãn, lớn dần theo bug, versioned.
23. **RAGAS đo gì?** faithfulness, answer relevance, context precision/recall. ([[aa06-llm-eval]])
24. **LLM-as-judge rủi ro?** Thiên vị (vị trí, độ dài, tự khen); cần calibrate + human spot-check. ([[aa06-llm-eval]])
25. **Offline vs online eval?** Offline (golden, trước deploy) + online (feedback/A-B thật). ([[aa06-llm-eval]])
26. **LLM observability log gì?** Trace input→retrieval→prompt→output, token/cost/latency, status, faithfulness; = provenance đầy đủ. ([[ab06-llm-observability]])
27. **Prompt management?** Prompt as code: registry, version (SemVer), regression eval, A/B, lineage prompt→output. ([[aa07-prompt-management]])
28. **LLMOps trụ cột?** version (model/prompt/data/embedding) + deploy + eval/CI + monitor + cost + safety. ([[aa10-llmops]])
29. **Monitor đặc thù LLM?** Quality drift, cost drift, hallucination rate, % fallback/quarantine. ([[aa10-llmops]])

### E. Kiến trúc & nâng cao
30. **Vector DB ở scale cần gì?** ANN (HNSW/IVF), quantization (PQ giảm RAM), sharding, filtered search. ([[ab07-vector-search-opt]])
31. **HNSW tune gì?** M, ef_construction (build), ef_search (runtime: recall↑/latency↑). ([[ab07-vector-search-opt]])
32. **Quantization?** Nén vector (SQ/PQ/binary) giảm RAM; coarse filter → rerank vector gốc. ([[ab07-vector-search-opt]])
33. **Pre vs post filter?** Pre: lọc metadata trước ANN (chính xác); post: ANN rồi lọc (tận dụng index). ([[ab07-vector-search-opt]])
34. **Streaming AI / real-time RAG?** Event-driven re-index <1'; đừng over-stream cái không cần tươi. ([[ai09-streaming-ai]])
35. **Agentic pipeline rủi ro?** Loop vô tận, cost phình, hành động nguy hiểm; chống: max-steps, budget cap, human approve, guardrail. ([[aa05-agentic-pipelines]])
36. **Multi-agent khi nào?** Hiếm — đa số 1 agent + tool tốt đủ; multi khi tách vai trò rõ. ([[ac04-multi-agent]])
37. **Tool tốt thiết kế sao?** Tên/mô tả rõ, schema chặt, output gọn, lỗi rõ, idempotent, ít-mà-tinh. ([[ac04-multi-agent]])
38. **Context engineering?** Quản token budget; lost-in-the-middle; short-term (summary) + long-term (RAG) memory. ([[ab03-context-engineering]])
39. **GraphRAG khi nào hơn vector RAG?** Câu hỏi multi-hop/quan hệ; trích entity/relation → graph + vector. ([[aa09-graphrag]])
40. **Multimodal pipeline?** CLIP/OCR/Whisper → embed cross-modal → multimodal RAG; object store + cost. ([[aa08-multimodal]])
41. **Voice/audio data?** STT→diarization→align→chunk; transcript=fact table; PII kép (nội dung+giọng). ([[ac05-voice-audio-pipeline]])

### F. ML/Cost
42. **Feature store giải gì?** Train/serve parity + point-in-time (chống leakage) + reuse + online low-latency. ([[ac07-feature-store]])
43. **Point-in-time correctness?** Train dùng feature as-of thời điểm sự kiện, không nhìn tương lai → as-of join. ([[ac07-feature-store]])
44. **Tối ưu cost LLM ở scale?** Routing/cascade (model nhỏ trước), cache nhiều tầng, nén prompt, batch, distill; đo $/query. ([[ac08-ai-cost-scale]])
45. **Recsys + embedding?** Two-tower (item/user vector), cosine recommend, cold-start nhờ content embedding, LLM re-rank/giải thích. ([[ac02-recsys-llm]])

## ⭐ Final Portfolio Pitch (90 giây)
> "Mình build một bộ **AI Data Engineering** chạy được, không cần API key (local fastembed/DuckDB): RAG end-to-end trên 200+ note (chunk structure-aware, HNSW, hybrid, incremental theo content-hash), **eval harness** chọn config bằng số, **governance pipeline** validate/quarantine output LLM như data contract, **guardrails** chặn PII/injection/SQL phá hoại, **MinHash dedup**, **synthetic data** có kiểm soát chất lượng, **cross-lingual eval** định lượng thuế đa ngữ, và **semantic recsys**. Xuyên suốt một niềm tin: *mọi nguyên tắc DE kinh điển — idempotency, lineage, data contract, point-in-time, cost, governance — áp y nguyên cho AI; danh từ đổi, tư duy không đổi*. Mình không chỉ gọi LLM — mình kỹ-sư-hoá dữ liệu quanh nó."

## ✅ "Tự kiểm tra & tự mò"
- [ ] Trả trôi 45 câu (che đáp án, tự nói).
- [ ] Chạy lại 10 script, mỗi cái nói "scale triệu doc đổi gì".
- [ ] Kể pitch 90 giây không nhìn note.
- 🔭 Tự mò lớn: chọn 10 câu khó nhất, viết câu trả lời 5 phút (whiteboard) kèm sơ đồ — như phỏng vấn thật.

➡️ Hết AI-Advanced 3. Batch tiếp: real-time RAG, LLM-judge tự động, privacy/compliance cho LLM, data cho AI agents production.
