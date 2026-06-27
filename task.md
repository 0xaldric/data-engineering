# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 19 script).

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–4/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt trong `notes/advanced/` (khái niệm + "tại sao" + sơ đồ + snippet + cạm bẫy + checklist + "tự mò"). **Task có code: viết + CHẠY THỬ verify rồi mới tick.**
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch AI tiếp (vẫn AI/LLM — user ưu tiên). Cập nhật `00-INDEX.md`. Giữ PROTOCOL.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #31 — AI-Advanced 8: AI Infrastructure & Frontier ⭐
**Nguồn:** đào sâu AI/LLM — hạ tầng inference, benchmark, red-team, frontier

---

## BATCH HIỆN TẠI

### [x] AH01 — LLM Serving & Inference Infrastructure
- **Note:** `notes/advanced/ah01-llm-serving.md`. Phục vụ LLM ở production: continuous batching, **KV cache**, throughput vs latency, vLLM/TGI, quantization khi serve (GPTQ/AWQ), multi-GPU (tensor/pipeline parallel), autoscaling theo tải. Khác serving model thường (stateful KV, độ dài đổi). Vai trò DE: serving layer cho embedding/LLM. Liên hệ [[ac08-ai-cost-scale]], [[ae05-edge-ai-data]].

### [x] AH02 — Embedding Model Selection & Benchmark ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ah02-embedding-benchmark.md` + code `embedding_benchmark.py`. Chọn embedding model bằng SỐ: MTEB là gì, chiều đánh giá (recall/MRR, tốc độ, kích thước, đa ngữ, max-length), trade-off. Code: ablation trên capstone — bật/tắt query-prefix + L2-normalize + đổi top-k, đo recall@k mỗi cấu hình → thấy lựa chọn embedding ảnh hưởng thật. Liên hệ [[ab02-rag-eval-harness]], [[ai04-embedding-versioning]].

### [x] AH03 — AI Red-Teaming & Adversarial Testing
- **Note:** `notes/advanced/ah03-red-teaming.md`. Chủ động tấn công hệ AI để tìm lỗ hổng trước kẻ xấu: taxonomy jailbreak (role-play/mã hoá/injection [[ad04-llm-security]]), automated red-team (sinh adversarial prompt), safety eval, harm categories, red-team như test suite. Vai trò DE: data adversarial + eval harness an toàn. Liên hệ [[aa02-guardrails]], [[ag02-hallucination-detection]].

### [x] AH04 — Tokenization Deep-dive
- **Note:** `notes/advanced/ah04-tokenization.md`. BPE/WordPiece/SentencePiece, vocab size, **tokenizer đa ngữ kém hiệu quả** (tiếng Việt/Á tốn nhiều token hơn tiếng Anh → đắt hơn + context ngắn hơn), special token, ảnh hưởng tới cost ([[ac08-ai-cost-scale]]) + chunking ([[ai03-chunking]]). Vai trò DE: hiểu token để ước cost/context. Liên hệ [[af05-training-data-scale]].

### [ ] AH05 — Data cho Multimodal LLM Training
- **Note:** `notes/advanced/ah05-multimodal-training-data.md`. Data train model đa phương thức: image-text pairs ở scale (LAION-style), captioning (sinh/lọc caption), CLIP-score filtering (cặp ảnh-text khớp), dedup ảnh, alt-text, alignment. Sâu hơn [[af05-training-data-scale]] cho multimodal. Liên hệ [[ae04-multimodal-rag]], [[ag06-multimodal-production]].

### [ ] AH06 — RAG Benchmarks & Public Datasets
- **Note:** `notes/advanced/ah06-rag-benchmarks.md`. Benchmark công khai: BEIR (retrieval), MTEB (embedding), RAGAS/các bộ RAG eval, MS MARCO, Natural Questions. Cách dùng, leaderboard caveat (overfit benchmark, domain gap), vì sao golden RIÊNG vẫn cần ([[ab02-rag-eval-harness]]). Liên hệ [[ac03-eval-driven-dev]], [[ah02-embedding-benchmark]].

### [ ] AH07 — LLM Inference Optimization (sâu)
- **Note:** `notes/advanced/ah07-inference-optimization.md`. Tăng tốc inference: speculative decoding (model nhỏ đoán, lớn verify), continuous/dynamic batching, flash attention (khái niệm), KV cache management/paging (PagedAttention), prefill vs decode, prompt caching. Trade-off throughput/latency/cost. Sâu hơn [[ah01-llm-serving]], [[ac08-ai-cost-scale]].

### [ ] AH08 — AI Agents cho Data Engineering (meta)
- **Note:** `notes/advanced/ah08-ai-agents-for-de.md`. AI tự động hoá chính việc DE: text-to-pipeline (NL → dbt/SQL), self-healing pipeline (agent sửa lỗi job), data quality tự động (LLM phát hiện anomaly/viết test), doc/lineage tự sinh, copilot cho DE. Rủi ro (tin LLM sửa pipeline production) + guardrail. Liên hệ [[aa05-agentic-pipelines]], [[ag05-agent-platform]].

### [ ] AH09 — AI review 8 + định hướng frontier
- **Note:** `notes/advanced/ah09-ai-review8.md` + cập nhật `00-INDEX.md`. Tổng kết AI-Advanced 8; bản đồ hạ tầng AI (train→serve→eval→optimize); xu hướng frontier (agent, multimodal, on-device, hiệu quả); tổng kết 8 batch Module AI.

---
*Hết batch → sinh batch AI tiếp (RLHF/DPO sâu, AI safety alignment, data cho reasoning models, vector DB mới, case study mới...) — vẫn ưu tiên AI/LLM.*
