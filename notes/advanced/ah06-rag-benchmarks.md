# AH06 — RAG Benchmarks & Public Datasets

> Benchmark công khai (BEIR, MTEB, RAGAS) để so model/phương pháp với cộng đồng. Nhưng leaderboard cao **≠** tốt cho bạn → vẫn cần golden RIÊNG. Liên hệ [[ab02-rag-eval-harness]], [[ah02-embedding-benchmark]], [[ac03-eval-driven-dev]].

## Vì sao có benchmark công khai
- So sánh **khách quan** giữa model/phương pháp (cùng data, cùng metric).
- Tiết kiệm: không phải tự tạo data eval khổng lồ.
- Theo dõi tiến bộ field (SOTA mới).

## ⭐ Các benchmark chính (biết để nói)
| Benchmark | Đo gì | Dùng khi |
|-----------|-------|----------|
| **MTEB** | embedding qua nhiều task (retrieval/classification/clustering/STS) | chọn embedding model ([[ah02-embedding-benchmark]]) |
| **BEIR** | retrieval zero-shot trên 18 dataset đa domain | đánh giá retriever tổng quát |
| **MS MARCO** | passage ranking (web search) | train/eval retriever, reranker |
| **Natural Questions / TriviaQA** | open-domain QA | RAG end-to-end |
| **RAGAS** (+ datasets) | RAG: faithfulness, answer/context relevance | eval generation RAG ([[aa06-llm-eval]]) |
| **MMLU / GSM8K / HumanEval** | kiến thức/suy luận/code của LLM | chọn LLM (không phải retrieval) |

## ⭐ Metric & cách dùng
- Retrieval: nDCG@10, recall@k, MRR ([[ab02-rag-eval-harness]]) — BEIR chuẩn nDCG@10.
- Embedding: MTEB trung bình nhiều task → số tổng hợp.
- RAG generation: faithfulness/relevance (RAGAS, cần LLM-judge [[ad02-llm-judge]]).
```
chọn model: lọc theo MTEB/BEIR -> shortlist -> đo trên GOLDEN RIÊNG -> chọn (ah02 quy trình)
```

## ⭐⭐ Leaderboard caveat (đừng tin mù — bài học AH02)
| Caveat | Vì sao |
|--------|--------|
| **Domain gap** | benchmark = Wikipedia/web EN; corpus bạn = nội bộ/tiếng Việt → khác xa ([[ac01-multilingual-rag]]) |
| **Overfit benchmark** | model tune để cao trên benchmark, kém ngoài đời (Goodhart) |
| **Contamination** | model train trúng data benchmark → điểm ảo ([[ab08-finetune-pipeline]] decontaminate) |
| **Metric ≠ mục tiêu** | nDCG cao nhưng app cần recall/latency khác |
| **Cấu hình khác** | AH02 đã thấy: prefix "đúng chuẩn" lại HẠI corpus Việt → cấu hình mặc định ≠ tối ưu cho bạn |
→ **Benchmark để SHORTLIST, golden riêng để CHỌN**. Leaderboard #1 có thể thua model #10 trên data của bạn.

## Vai trò DE
- Hiểu benchmark để **đọc** so sánh model (chọn shortlist).
- Xây **golden riêng** ([[ab02-rag-eval-harness]]) — benchmark thật sự quan trọng là **của bạn**.
- Decontaminate: đảm bảo không lẫn benchmark vào train nếu fine-tune.
- (Cho tiếng Việt: ít benchmark → càng phải tự xây golden.)

## Cạm bẫy
- **Chọn model chỉ theo leaderboard** → domain gap → kém trên data thật → golden riêng.
- **Tin điểm cao = tốt mọi mặt** → bỏ tốc độ/kích thước/đa ngữ ([[ah02-embedding-benchmark]] trade-off).
- **Bỏ qua contamination** → điểm ảo.
- **Không có benchmark tiếng Việt** → dùng EN rồi ngạc nhiên khi rớt → tự xây + model đa ngữ.
- **So benchmark khác cấu hình** (prefix/chunk khác) → không công bằng → kiểm cấu hình.

## ✅ "Tự kiểm tra & tự mò"
- [ ] MTEB/BEIR/MS-MARCO/RAGAS đo gì, dùng khi nào.
- [ ] Metric: nDCG@10/recall/MRR + faithfulness.
- [ ] ⭐ Leaderboard caveat: domain gap, overfit, contamination, cấu hình.
- [ ] Benchmark = shortlist; golden riêng = chọn cuối.
- [ ] Tiếng Việt thiếu benchmark → tự xây golden.
- 🔭 Tự mò: coi `rag_eval_harness.py` + golden 8 câu của bạn như "benchmark mini" cho corpus này; thêm 10 câu nữa cho đa dạng; nghĩ nếu submit corpus này thành "benchmark BEIR-style" thì cần gì (qrels: câu hỏi → doc đúng, format chuẩn).

➡️ Tiếp [[ah07-inference-optimization]] — tối ưu inference sâu.
