# AJ09 — AI Review 9 + Grand Finale Module AI

> Tổng kết **AI-Advanced 9** (AJ01–AJ08) + **grand finale** toàn Module AI (9 batch, 22 script, ~91 note) + checklist "ngày 1 đi làm AI-DE" + lời kết. Nối [[ah09-ai-review8]], [[ai10-summary]].

## 🏁 Batch này (AJ01–AJ08)
| # | Chủ đề | Code | Ý chốt |
|---|--------|------|--------|
| AJ01 | Reasoning models | — | process vs outcome supervision |
| AJ02 | AI alignment | — | HHH; helpful↔harmless; refusal |
| AJ03 | Capstone integration | ✅ `ai_product.py` | luồng 7 tầng, 4 đường đi |
| AJ04 | Next-gen vector | ✅ `vector_compression.py` | binary giữ 88% ở /32 RAM |
| AJ05 | Case y tế | — | grounding tuyệt đối + PHI privacy |
| AJ06 | Case tài chính | — | real-time + point-in-time + LLM-không-tự-quyết |
| AJ07 | Data flywheel | — | usage→signal→data→model (data moat) |
| AJ08 | Prompt optimization | — | DSPy/few-shot bằng metric |

→ Kho AI: **22 script chạy được** + ~91 note AI (9 batch).

## 🏆 GRAND FINALE — Toàn cảnh Module AI (9 batch)
```
NỀN TẢNG    → RAG, governance, test non-det, cost, streaming           (Module AI)
NÂNG CAO    → text-to-SQL, guardrails, dedup, agentic, eval, GraphRAG   (AA)
DATA & EVAL → synthetic, harness, context, fine-tune, vector-opt        (AB)
ỨNG DỤNG    → đa ngữ, recsys, eval-driven, voice, feature-store         (AC)
PRODUCTION  → streaming, judge, privacy, security, structured, cache    (AD)
FRONTIER 1  → self-correct, GraphRAG-build, DQ, multimodal, rerank, code (AE)
SYSTEM      → case studies, vector-internals, scale, governance          (AF)
OPS         → hallucination, drift, RLHF, agent-platform, memory, contract (AG)
INFRA       → serving, embedding-benchmark, red-team, token, inference   (AH)
ĐỈNH        → reasoning, alignment, capstone-integration, flywheel       (AJ)
```
→ Từ "RAG là gì" → "thiết kế + vận hành + tối ưu hệ AI production hoàn chỉnh".

## ⭐ 22 script chạy được — tài sản portfolio
```
RAG core:   rag_over_notes, rag_eval_harness, embedding_benchmark, continuous_eval
retrieval+: self_correcting_rag, streaming_rag, graphrag_links, cross_lingual_eval
applied:    semantic_recsys, semantic_cache, text_to_sql
governance: llm_output_pipeline, guardrails_demo, test_semantic, hallucination_detect
data:       synthetic_data, dedup_minhash, data_quality_score
ops:        llm_judge, drift_detect
nextgen:    vector_compression
TÍCH HỢP:   ai_product (ghép tất cả thành 1 luồng) ⭐
```
→ Tất cả **local, không API key** → ai cũng chạy lại → portfolio "sờ được", chứng minh năng lực thật.

## ⭐⭐ Checklist "Ngày 1 đi làm AI Data Engineer"
**Hiểu & nói được:**
- [ ] RAG end-to-end + đo bằng số ([[ab02-rag-eval-harness]]); chọn embedding/chunk/config bằng benchmark.
- [ ] LLM output = dữ liệu không tin được → validate/quarantine/provenance ([[ai06-llm-output-governance]]).
- [ ] Guardrail (PII/injection/grounding) + red-team ([[aa02-guardrails]], [[ah03-red-teaming]]).
- [ ] Eval-driven + continuous gate + drift ([[ac03-eval-driven-dev]], [[af07-continuous-eval]], [[ag04-drift-detection]]).
- [ ] Data cho AI: training/synthetic/preference/DQ ([[ae03-training-data-quality]], [[ag03-rlhf-preference-data]]).
- [ ] System design AI theo khung 7 bước ([[af09-ai-review6]]).
- [ ] Vận hành: serving, cost, observability, governance ([[ah01-llm-serving]], [[ac08-ai-cost-scale]], [[af06-ai-data-governance]]).

**Làm được (hands-on):**
- [ ] Chạy + sửa cả 22 script; làm các phần 🔭 "tự mò".
- [ ] Ghép 1 AI data product ([[aj03-capstone-integration]]).
- [ ] Tự ra + giải 1 đề system-design AI.

## ⭐ Lời kết: 3 điều ghi nhớ nhất
1. **"Danh từ đổi, tư duy DE không đổi"** — mọi nguyên tắc DE (idempotency, lineage, contract, point-in-time, cost, governance, eval) áp y nguyên cho AI. Bạn ĐÃ là DE → học AI-DE là học **danh từ mới**, không phải nghề mới.
2. **"Đo, đừng tin mặc định"** — qua code chạy thật: prefix-OFF>ON ([[ah02-embedding-benchmark]]), binary giữ recall ([[aj04-nextgen-vector]]), cosine≠sự-thật ([[ag02-hallucination-detection]], [[ad08-semantic-cache]]), calibrate ngưỡng ([[ag04-drift-detection]]). Senior đo, junior tin tài liệu.
3. **"Phần lớn AI là DATA"** — không phải model. RAG data, training data, eval data, preference data, flywheel ([[aj07-data-flywheel]]) — đó là **sân nhà của DE**, là chỗ bạn tạo giá trị trong kỷ nguyên AI.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vẽ toàn cảnh 9 batch từ trí nhớ.
- [ ] Chấm checklist "ngày 1" — phần nào chưa vững → ôn.
- [ ] Nói trôi 3 điều ghi nhớ + map vào 22 script.
- 🔭 Tự mò GRAND: viết README cho repo (`projects/06-ai-data-engineering/`): bảng 22 script + cách chạy + 1 dòng mỗi cái + "phát hiện khi chạy" (prefix/binary/cosine); push lên GitHub làm trang bìa portfolio. Đó là sản phẩm cuối cùng để gửi nhà tuyển dụng.

➡️ Hết AI-Advanced 9. Hành trình Module AI: **9 batch · ~91 note · 22 script**. Batch tiếp: đào sâu trục yếu / case study mới / chủ đề frontier mới — vẫn ưu tiên AI/LLM.
