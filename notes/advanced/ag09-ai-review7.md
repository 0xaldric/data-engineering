# AG09 — AI Review 7 + Bản Đồ Năng Lực AI-DE Hoàn Chỉnh

> Tổng kết **AI-Advanced 7** (AG01–AG08) + **bản đồ năng lực AI Data Engineer** đầy đủ (7 batch, 19 script) + reflection cuối hành trình. Nối [[af09-ai-review6]], [[ae09-ai-review5]], [[ai10-summary]].

## 🏁 Batch này (AG01–AG08)
| # | Chủ đề | Code | Ý chốt |
|---|--------|------|--------|
| AG01 | RAG cho BI/Analytics | — | LLM không tự tính số; semantic layer + engine |
| AG02 | Hallucination detection | ✅ `hallucination_detect.py` | cosine≠sự thật → so FACT; grounding |
| AG03 | RLHF preference data | — | chosen/rejected; reward hacking |
| AG04 | Drift detection | ✅ `drift_detect.py` | im-lặng-hỏng; centroid; calibrate |
| AG05 | Agent platform | — | registry/state/run-store/coordination |
| AG06 | Multimodal production | — | frame sampling; cost/storage |
| AG07 | Conversational memory | — | working/episodic/semantic; entity memory |
| AG08 | Data contracts AI I/O | — | schema output; breaking change |

→ Kho AI: **19 script chạy được** + ~73 note AI (7 batch).

## ⭐⭐ BẢN ĐỒ NĂNG LỰC AI DATA ENGINEER (7 trục)
```
                    AI DATA ENGINEER
   ┌──────────────┬──────────────┬──────────────┐
1. RETRIEVAL      2. LLM OUTPUT   3. DATA CHO AI  4. EVAL & OPS
   RAG/chunk/embed  governance      training data    eval harness
   hybrid/rerank    guardrail       synthetic        LLM-judge
   GraphRAG         hallucination   RLHF pref        continuous gate
   đa ngữ/cross     test non-det    DQ/dedup         observability/drift
   ┌──────────────┬──────────────┬──────────────┐
5. SAFETY         6. SCALE/INFRA  7. SYSTEM DESIGN
   PII/injection    vector DB int    case studies
   privacy/compliance streaming      khung 7 bước
   security/agent   cache/cost       integration
```

## ⭐ 19 script — bản đồ portfolio
| Trục | Script |
|------|--------|
| **Retrieval** | rag_over_notes · streaming_rag · graphrag_links · cross_lingual_eval · self_correcting_rag |
| **LLM output** | llm_output_pipeline · guardrails_demo · test_semantic · hallucination_detect |
| **Data cho AI** | synthetic_data · dedup_minhash · data_quality_score |
| **Eval & Ops** | rag_eval_harness · llm_judge · continuous_eval · drift_detect |
| **Applied** | text_to_sql · semantic_recsys · semantic_cache |
→ Mỗi trục có code chạy được → portfolio "sờ được", không cần API key.

## ⭐ 7 thông điệp cốt lõi (toàn Module AI)
1. **"Danh từ đổi, tư duy DE không đổi"** — idempotency→re-index, lineage→provenance, DQ→eval, contract→output-validation, point-in-time→feature store, cost→token.
2. **"LLM output = dữ liệu KHÔNG tin được"** → data contract: validate/quarantine/provenance.
3. **"AI tốt lên nhờ ĐO"** → golden + harness + metric + continuous gate, không vibe.
4. **"Phần lớn AI là DATA"** → RAG/training/eval/synthetic/preference data.
5. **"An toàn không phải tuỳ chọn"** → guardrail/PII/injection/sandbox/decontamination.
6. **⭐ "Cosine đo bề mặt, KHÔNG đo sự thật"** → semantic cache nghịch lý ([[ad08-semantic-cache]]), hallucination self-consistency ([[ag02-hallucination-detection]]) → embedding similarity ≠ tương đương ngữ nghĩa → cần fact/NLI khi cần đúng-sai.
7. **"Hệ AI im lặng hỏng"** → phải chủ động đo drift/quality, không chờ exception ([[ag04-drift-detection]]).

## ⭐ Reflection: học được gì từ việc CHẠY code
Mỗi script chạy thật **phát hiện bài học** mà đọc lý thuyết không thấy:
- Self-correcting RAG: HyDE kéo confidence 0.656→0.814 (đo được).
- Semantic cache + hallucination: **nghịch lý cosine** (cùng khuôn khác nghĩa điểm cao) — lặp lại 2 lần → insight sâu nhất.
- Data quality: **hard gate** (toxic/dup loại ngay) vs trung bình để rác lọt.
- Drift/grounding: **calibrate ngưỡng** trên nhiễu nền, không hardcode mò.
- GraphRAG: hub in-degree **tự lộ** khái niệm nền tảng.
→ "Học xong tự mò" = chạy + quan sát + sửa khi kết quả bất ngờ. Đó là kỹ năng thật.

## ⭐ Định hướng tiếp (sau 7 batch)
- **Hands-on**: chạy lại 19 script, làm hết 🔭 "tự mò" → biến hiểu thành kỹ năng cơ bắp.
- **Tích hợp**: ghép thành 1 AI-data-product hoàn chỉnh ([[ad09-ai-review4]] capstone).
- **Scale thật**: corpus lớn + vector DB thật (Qdrant) + đo lại.
- **Portfolio**: viết README cho `projects/06-ai-data-engineering/` + blog → chứng minh năng lực.
- **Phỏng vấn**: ôn 45 Q&A ([[ac09-ai-review3]]) + khung system-design ([[af09-ai-review6]]) + 3 review tích hợp.

## 🏆 Tổng kết toàn Module AI (7 batch)
**~73 note AI + 19 script chạy được** = khoá "AI Data Engineering" tiếng Việt hoàn chỉnh: nền tảng → nâng cao → production → case study → vận hành. Cộng **Track 2 nền tảng** (~160 note DE/SQL/system-design) = bộ ôn DE + AI-DE đầy đủ nhất.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vẽ bản đồ 7 trục năng lực AI-DE từ trí nhớ.
- [ ] Map 19 script → trục → kỹ năng → câu phỏng vấn.
- [ ] Nói trôi 7 thông điệp cốt lõi.
- [ ] Chọn 1 trục yếu nhất → làm lại các 🔭 của trục đó.
- 🔭 Tự mò cuối hành trình: tự đánh giá 7 trục (1-5 điểm mỗi trục), trục thấp nhất → dành 1 tuần làm hands-on; viết 1 đoạn "career story" 90 giây dùng portfolio 19 script.

➡️ Hết AI-Advanced 7. Batch tiếp: chủ đề mới (LLM serving infra, AI red-teaming, RAG benchmark public, data cho multimodal LLM training) hoặc đào sâu trục yếu.
