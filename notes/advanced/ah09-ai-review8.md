# AH09 — AI Review 8 + Bản Đồ Hạ Tầng AI & Frontier

> Tổng kết **AI-Advanced 8** (AH01–AH08) + bản đồ hạ tầng AI (train→serve→eval→optimize) + xu hướng frontier + tổng kết **8 batch** Module AI. Nối [[ag09-ai-review7]], [[ai10-summary]].

## 🏁 Batch này (AH01–AH08)
| # | Chủ đề | Code | Ý chốt |
|---|--------|------|--------|
| AH01 | LLM serving | — | KV cache, continuous batching, prefill/decode |
| AH02 | Embedding benchmark | ✅ `embedding_benchmark.py` | prefix-OFF>ON: đo đừng tin mặc định |
| AH03 | AI red-teaming | — | tấn công chính mình; test suite an toàn |
| AH04 | Tokenization | — | token tax tiếng Việt 2-4× |
| AH05 | Multimodal training data | — | CLIP-score filter; image-text pairs |
| AH06 | RAG benchmarks | — | BEIR/MTEB; leaderboard caveat; golden riêng |
| AH07 | Inference optimization | — | speculative/PagedAttention/flash |
| AH08 | AI agents cho DE | — | self-healing; DE thành người giám sát |

→ Kho AI: **20 script chạy được** + ~82 note AI (8 batch).

## ⭐ Bản đồ HẠ TẦNG AI (vòng đời 1 hệ AI)
```
   DATA           TRAIN            SERVE            OPTIMIZE          OPERATE
training data ─> model/embedding ─> inference ──> tăng tốc ────> eval/monitor
[af05/ah05]      [ab08/ag03]        [ah01]         [ah07]          [af07/ag04]
dedup/quality    SFT/RLHF/CLIP      KV cache       speculative     continuous eval
synthetic        fine-tune          batching       PagedAttn       drift detect
[ab01/ae03]      [ab05]             [vLLM/TGI]     flash attn      observability
                                                                   [ab06/aa10]
   ↑ DE sở hữu DATA hai đầu (vào: training data; ra: eval/monitor data) ↑
```
→ DE không train model/viết kernel, nhưng **sở hữu data + eval + serving infra + cost** quanh mọi tầng.

## ⭐ Xu hướng Frontier (nói trong phỏng vấn)
| Xu hướng | Ý nghĩa cho DE |
|----------|----------------|
| **Agentic** | agent tự vận hành → cần data infra cho agent ([[ag05-agent-platform]]), self-healing ([[ah08-ai-agents-for-de]]) |
| **Multimodal** | ảnh/video/audio → pipeline nặng, cost ([[ag06-multimodal-production]], [[ah05-multimodal-training-data]]) |
| **On-device/edge** | model nhỏ chạy local → privacy, sync ([[ae05-edge-ai-data]]) |
| **Hiệu quả** | model nhỏ + quantize + speculative → rẻ hơn ([[ah07-inference-optimization]]) |
| **Reasoning models** | chain-of-thought dài → token nhiều → cost/context ([[ah04-tokenization]]) |
| **Long context** | nhồi nhiều hơn nhưng vẫn cần memory/RAG ([[ag07-conversational-memory]]) |
→ "Danh từ đổi (agent, multimodal, reasoning), **tư duy DE không đổi**": data quality, cost, eval, governance, infra.

## ⭐ Bài học "đo, đừng tin mặc định" (chủ đề lặp lại)
Batch này củng cố insight xuyên suốt qua code chạy thật:
- **AH02**: prefix "đúng chuẩn bge" lại HẠI corpus Việt (88% OFF > 75% ON) → đo trên data thật.
- Cùng họ với: semantic cache nghịch lý ([[ad08-semantic-cache]]), hallucination cosine ([[ag02-hallucination-detection]]), drift calibrate ([[ag04-drift-detection]]).
- → **Mọi "best practice"/ngưỡng/mặc định phải verify trên data của BẠN**. Đây là kỹ năng phân biệt junior (tin tài liệu) vs senior (đo).

## 🏆 Tổng kết 8 batch Module AI
| Batch | Trọng tâm |
|-------|-----------|
| Module AI | nền tảng RAG/governance/test |
| AA-AB | guardrails/text-to-SQL/synthetic/eval/fine-tune/obs |
| AC-AD | đa ngữ/recsys/streaming/judge/privacy/security/cache |
| AE | self-correct/GraphRAG/DQ/multimodal/rerank/code |
| AF | case studies + scale + internals + governance |
| AG | production: hallucination/drift/RLHF/agent/memory/contracts |
| AH | **infra: serving/benchmark/red-team/token/inference/agents-for-DE** |
→ **~82 note AI + 20 script** = khoá AI Data Engineering từ nền tảng → production → hạ tầng → frontier.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vẽ bản đồ hạ tầng AI (data→train→serve→optimize→operate) + DE sở hữu gì.
- [ ] 6 xu hướng frontier + ý nghĩa cho DE.
- [ ] Bài học "đo đừng tin mặc định" qua 4 ví dụ code.
- [ ] Tổng kết 8 batch — chủ đề nào còn yếu → ôn lại.
- 🔭 Tự mò: chạy lại 20 script một lượt (smoke test); với mỗi script tự hỏi "scale ×1000 đổi gì? mặc định nào cần đo lại?"; viết README cho `projects/06-ai-data-engineering/` liệt kê 20 script + 1 dòng mỗi cái (trang bìa portfolio).

➡️ Hết AI-Advanced 8. Batch tiếp: chủ đề mới (RLHF/DPO sâu, AI alignment, reasoning-model data, vector DB thế hệ mới) hoặc đào sâu trục yếu.
