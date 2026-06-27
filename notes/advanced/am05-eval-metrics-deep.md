# AM05 — Evaluation Metrics Deep

> Hiểu SÂU metric eval: công thức + khi nào dùng. Chọn sai metric → tối ưu sai thứ. Liên hệ [[ab02-rag-eval-harness]], [[aa06-llm-eval]], [[am04-hybrid-fusion]].

## ⭐ Bản đồ metric (nhóm theo cái đo)
```
RETRIEVAL (lấy đúng doc?)        GENERATION (trả lời tốt?)      HỆ THỐNG
  recall@k, precision@k            faithfulness                   latency p50/p95/p99
  MRR, MAP, nDCG, hit-rate         answer relevance               throughput, $/query
                                   context precision/recall
```

## ⭐ Retrieval metrics — công thức
| Metric | Hỏi | Công thức |
|--------|-----|-----------|
| **recall@k** | doc đúng lọt top-k? | #query có hit / #query (binary) |
| **precision@k** | top-k bao nhiêu đúng? | #relevant trong k / k |
| **hit-rate@k** | = recall@k (binary, 1 doc đúng) | có hit không |
| **MRR** | doc đúng hạng mấy? | mean(1/rank_hit_đầu) |
| **MAP** | precision trung bình mọi vị trí hit | mean(AveP) qua query |
| **nDCG** | xếp hạng tốt cỡ nào (graded) | DCG / IDCG |

## ⭐ nDCG đầy đủ (hay hỏi)
```
DCG@k = Σ (rel_i / log2(i+1))      rel = độ liên quan (0/1 hoặc graded 0-3)
IDCG@k = DCG của thứ tự LÝ TƯỞNG (mọi rel cao dồn lên đầu)
nDCG@k = DCG / IDCG    ∈ [0,1]
```
- **Graded relevance**: rel không chỉ 0/1 mà 0-3 (rất liên quan=3) → nDCG phân biệt "đúng nhất" vs "tạm đúng".
- ⚠️ Quên chia IDCG → ra >1 = sai (lỗi đã mắc ở [[ab02-rag-eval-harness]]).

## ⭐ MAP (Mean Average Precision)
```
AveP cho 1 query = trung bình precision@k TẠI MỖI vị trí có doc đúng
   vd hit ở rank 1,3 -> (P@1 + P@3)/2 = (1/1 + 2/3)/2
MAP = mean(AveP) qua mọi query
```
→ Thưởng doc đúng ở hạng cao + nhiều doc đúng. Dùng khi **nhiều doc đúng/query** (recall@k chỉ binary).

## ⭐ recall vs precision trade-off (chọn theo bài toán)
```
RECALL cao (lấy nhiều, ít bỏ sót)   <-> PRECISION cao (lấy ít, ít rác)
RAG cho LLM đọc -> ưu RECALL (doc đúng lọt context, LLM tự lọc)
Search trả người -> ưu PRECISION/nDCG (top-3 phải sạch)
Y tế/an toàn -> RECALL (không bỏ sót cảnh báo [[aj05-case-healthcare-ai]])
Spam filter -> PRECISION (đừng chặn nhầm thư thật)
```
→ Không có metric "đúng" — chọn theo **hậu quả false-positive vs false-negative**.

## ⭐ Latency percentiles (đừng dùng trung bình)
```
p50 (median): nửa request nhanh hơn   p95/p99: đuôi chậm (trải nghiệm tệ nhất)
trung bình ĐÁNH LỪA: vài request 10s kéo mean lên dù p50 ổn
-> đo p95/p99 ([[ah01-llm-serving]] TTFT/TPOT) -> SLA theo p99
```
→ User cảm nhận **đuôi** (p99), không phải trung bình. 1% chậm = nhiều user bực.

## RAGAS internals (generation)
- **Faithfulness**: câu trả lời có bám context? (claim có trong context không) — chống bịa.
- **Answer relevance**: trả lời đúng câu hỏi?
- **Context precision**: context lấy về có liên quan (không rác)?
- **Context recall**: context đủ để trả lời?
→ Cần LLM-judge ([[ad02-llm-judge]]) — nhớ bias + calibrate.

## Cạm bẫy
- **Chọn 1 metric cho mọi bài** → recall cho search-người (cần precision) → chọn theo hậu quả.
- **nDCG quên IDCG** → >1 sai.
- **Dùng latency trung bình** → giấu đuôi chậm → p95/p99.
- **recall@k cho nhiều-doc-đúng** → mất thông tin → MAP/nDCG.
- **Chỉ retrieval metric, quên generation** → retrieve tốt answer tệ → faithfulness.
- **Tối ưu metric ≠ mục tiêu** (Goodhart) → metric kinh doanh thật (conversion/deflection).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Bản đồ metric (retrieval/generation/hệ thống).
- [ ] nDCG = DCG/IDCG, graded relevance; MAP = mean AveP.
- [ ] recall vs precision theo hậu quả FP/FN.
- [ ] Latency p95/p99 không trung bình.
- [ ] RAGAS: faithfulness/relevance/context-precision-recall.
- 🔭 Tự mò: viết hàm tính nDCG@k với **graded relevance** (rel 0-3) + MAP cho golden có nhiều-doc-đúng; thêm vào `rag_eval_harness.py` in p50/p95 latency mỗi config (đo time.perf_counter mỗi query).

➡️ Tiếp [[am06-case-gaming-ai]] — case study gaming.
