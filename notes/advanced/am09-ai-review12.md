# AM09 — AI Review 12 + Tổng Kết Kỹ Thuật Sâu

> Tổng kết **AI-Advanced 12** (AM01–AM08): bảng "kỹ thuật sâu → khi nào dùng", **checklist debug RAG**, tổng kết **12 batch** Module AI. Nối [[al09-ai-review11]], [[am01-rag-debugging]].

## 🏁 Batch này (AM01–AM08)
| # | Chủ đề | Code | Ý chốt |
|---|--------|------|--------|
| AM01 | RAG debugging | ✅ `rag_debugger.py` | chẩn đoán theo tầng |
| AM02 | Prompt patterns | — | CoT/ReAct/few-shot/structured |
| AM03 | Advanced chunking | — | parent-child, semantic, late |
| AM04 | Hybrid fusion | ✅ `rrf_fusion.py` | RRF robust hơn weighted |
| AM05 | Eval metrics deep | — | nDCG/MAP/percentiles |
| AM06 | Case gaming | — | NPC LLM cost, anti-cheat |
| AM07 | Case agritech | — | edge-first + multimodal + đa ngữ |
| AM08 | Coding exercises 3 | — | RRF/nDCG/MMR (verify) |

→ Kho AI: **25 script chạy được** + ~113 note AI (12 batch).

## ⭐⭐ Bảng "Kỹ thuật sâu → khi nào dùng"
| Vấn đề | Kỹ thuật |
|--------|----------|
| Retrieve trượt, chunk vô nghĩa | chunk strategy đúng ([[am03-advanced-chunking]]): parent-child mặc định tốt |
| Cosine vs keyword khác thang | RRF fusion ([[am04-hybrid-fusion]]) — robust hơn weighted |
| Doc đúng có nhưng rank thấp | rerank ([[ae07-reranking-deep]]) / tăng k |
| Top-k trùng ý | MMR ([[am08-coding-exercises-3]]) |
| Câu hỏi mơ hồ/cộc lốc | query understanding + reformulate ([[ae06-query-understanding]], [[ae01-self-correcting-rag]]) |
| LLM suy luận sai | CoT / reasoning model ([[am02-prompt-patterns]], [[aj01-reasoning-models]]) |
| Output cần parse | structured output + validate ([[ai06-llm-output-governance]]) |
| Không biết lỗi ở đâu | rag_debugger theo tầng ([[am01-rag-debugging]]) |
| Chọn metric | theo hậu quả FP/FN ([[am05-eval-metrics-deep]]) |

## ⭐⭐ CHECKLIST DEBUG RAG (in ra dán bàn)
```
answer SAI -> debug theo thứ tự:
[1] doc đúng CÓ trong context không?
     KHÔNG -> lỗi RETRIEVAL (xuống [2]) | CÓ -> lỗi GENERATION (xuống [6])
[2] doc đúng có trong INDEX không?       -> không: fix ingest/chunk
[3] điểm embedding doc đúng cao không?    -> thấp: đổi model/bỏ prefix/chunk lại ([[ah02]])
[4] doc đúng xếp hạng <= k không?         -> không: rerank/tăng k/hybrid
[5] note nào CƯỚP top? vì sao?           -> hybrid keyword/reformulate
[6] (generation) prompt "chỉ từ context"? grounding check? đổi model?
[7] ĐO trên golden (không 1 ca) + continuous gate ([[af07]])
```

## ⭐ 3 phát hiện code lượt này (đo, đừng tin mặc định)
1. **RAG debug**: EOS cộc lốc → doc đúng rank #147 (không phải "model ngu" mà query lệch) → reformulate.
2. **RRF vs weighted**: thêm keyword (weighted) **TỤT** 88%, RRF giữ 100% → RRF robust hơn ([[am04-hybrid-fusion]]).
3. → Củng cố: **mọi "best practice" phải verify trên data của bạn**.

## 🏆 Tổng kết 12 batch Module AI
nền tảng (Module AI) → production (AA-AD) → frontier/system (AE-AF) → ops/infra (AG-AH) → đỉnh (AJ) → vertical (AK) → mock/exercise (AL) → **deep techniques (AM)**.
→ **12 batch · ~113 note AI · 25 script** = khoá AI-DE toàn diện: lý thuyết + thực hành + system design + vertical + luyện phỏng vấn + kỹ thuật sâu.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Bảng kỹ thuật sâu → khi nào dùng (nói được mỗi cái giải vấn đề gì).
- [ ] Thuộc checklist debug RAG (7 bước).
- [ ] 3 phát hiện code (RAG debug, RRF, đo-đừng-tin-mặc-định).
- 🔭 Tự mò: chạy `rag_debugger.py` + `rrf_fusion.py` cùng nhau — với query fail, debug ra tầng lỗi, thử RRF/reformulate fix, đo lại. Đó là vòng debug→hypothesize→fix→verify hoàn chỉnh.

➡️ Hết AI-Advanced 12. Batch tiếp: kỹ thuật mới / ngành mới / mock-exercise mới — vẫn ưu tiên AI/LLM.
