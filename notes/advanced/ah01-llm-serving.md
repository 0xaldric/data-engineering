# AH01 — LLM Serving & Inference Infrastructure

> Phục vụ LLM ở production khác hẳn serving model thường: **stateful KV cache**, độ dài output đổi, GPU đắt. Hiểu để tối ưu throughput/latency/cost. Liên hệ [[ac08-ai-cost-scale]], [[ah07-inference-optimization]], [[ae05-edge-ai-data]].

## Vì sao serving LLM khó hơn model thường
- Model thường (classifier): input → 1 forward → output. Đơn giản, stateless.
- LLM: sinh **từng token một** (autoregressive), output **độ dài đổi**, giữ **KV cache** giữa các token → stateful, khó batch.
- GPU đắt + RAM hạn → tối ưu **throughput** (phục vụ nhiều) mà giữ **latency** (nhanh) là bài toán trung tâm.

## ⭐ KV Cache (chìa khoá hiểu serving LLM)
```
sinh token: "Data" -> "engineering" -> "là" -> ...
mỗi token mới attention tới MỌI token trước -> tính lại K,V của tất cả = lãng phí
KV cache: LƯU K,V của token đã sinh -> token mới chỉ tính K,V của CHÍNH NÓ
```
- → Tăng tốc lớn, nhưng **tốn RAM**: KV cache ∝ (độ dài × layer × heads) → context dài = RAM nhiều.
- Quản KV cache = bài toán bộ nhớ chính của LLM serving (PagedAttention [[ah07-inference-optimization]]).

## ⭐ Continuous batching (throughput)
```
STATIC batch: chờ đủ N request -> chạy cùng -> chờ TẤT CẢ xong (request ngắn chờ request dài)
CONTINUOUS batch: request xong thì THOÁT, request mới CHÈN vào chỗ trống ngay
   -> GPU không idle, throughput cao hơn nhiều
```
→ Vì output LLM độ dài khác nhau, static batch lãng phí (chờ cái dài nhất). Continuous batching (vLLM/TGI) là chuẩn production.

## ⭐ Prefill vs Decode (2 pha khác nhau)
```
PREFILL: xử lý CẢ prompt 1 lần (song song mọi token) -> tính, compute-bound
DECODE:  sinh từng token (tuần tự) -> memory-bound (đọc KV cache + weights)
```
- Prompt dài → prefill nặng (compute); output dài → decode nhiều bước (memory).
- Hiểu để tối ưu: prompt dài tốn prefill; cache prefix dùng lại được ([[ad08-semantic-cache]] prompt cache).

## Throughput vs Latency (tam giác serving)
| Mục tiêu | Cách | Đánh đổi |
|----------|------|----------|
| **Throughput cao** | batch lớn, continuous batching | latency từng request tăng |
| **Latency thấp** | batch nhỏ, ưu tiên 1 request | throughput giảm, GPU phí |
| **TTFT** (time-to-first-token) | tối ưu prefill | — |
| **TPOT** (time-per-output-token) | tối ưu decode | — |
→ Đo cả TTFT (chờ token đầu) + TPOT (tốc độ stream) + throughput tổng.

## Multi-GPU & quantization (model lớn)
- **Tensor parallel**: chia 1 layer qua nhiều GPU (model không vừa 1 GPU).
- **Pipeline parallel**: chia layer theo tầng qua GPU.
- **Quantization khi serve** (GPTQ/AWQ/INT8): nén weight → vừa GPU nhỏ hơn + nhanh hơn, mất chính xác chút ([[ae05-edge-ai-data]], [[af04-vector-db-internals]] PQ cùng ý).

## Công cụ & vai trò DE
- **vLLM / TGI / TensorRT-LLM**: serving engine (continuous batching, PagedAttention).
- **Autoscaling**: scale replica theo tải (queue depth) — đắt nên scale-to-zero khi rảnh.
- **DE**: serving layer cho **embedding** (fastembed local!) + LLM; đo cost/throughput ([[ab06-llm-observability]]); routing model ([[ac08-ai-cost-scale]]).

## Cạm bẫy
- **Static batch cho LLM** → lãng phí (chờ output dài nhất) → continuous batching.
- **Bỏ qua KV cache RAM** → OOM khi context dài/nhiều request → giới hạn context + paging.
- **Chỉ đo latency trung bình** → bỏ p99 + TTFT/TPOT → đo đủ.
- **1 GPU cho model quá lớn** → OOM → tensor/pipeline parallel hoặc quantize.
- **Không autoscale** → trả tiền GPU idle / quá tải lúc cao điểm.
- **Quên prompt cache** → re-prefill prompt lặp (system prompt dài) → cache prefix.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao serving LLM khó (autoregressive, KV cache stateful, độ dài đổi).
- [ ] KV cache: tăng tốc nhưng tốn RAM ∝ độ dài.
- [ ] Continuous batching > static (output độ dài khác nhau).
- [ ] Prefill (compute) vs decode (memory); TTFT vs TPOT.
- [ ] Multi-GPU (tensor/pipeline) + quantization serve.
- 🔭 Tự mò: đo `fastembed` (embedding serving local) — embed 1 câu vs batch 100 câu, tính throughput (câu/giây) mỗi cách → thấy batching tăng throughput; nghĩ tại sao LLM autoregressive không batch đơn giản như embedding.

➡️ Tiếp [[ah02-embedding-benchmark]] — chọn embedding bằng số (chạy được).
