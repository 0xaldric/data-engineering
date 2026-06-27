# AH07 — LLM Inference Optimization (sâu)

> Kỹ thuật tăng tốc inference LLM: speculative decoding, PagedAttention, flash attention, continuous batching. Hiểu để chọn engine + ước throughput/cost. Sâu hơn [[ah01-llm-serving]], [[ac08-ai-cost-scale]].

## Nhắc: nút thắt ở đâu
- LLM sinh **tuần tự** từng token (decode) → chậm + memory-bound (đọc weight + KV cache mỗi bước).
- Prefill (xử lý prompt) compute-bound; decode (sinh) memory-bound ([[ah01-llm-serving]]).
- → Tối ưu nhắm: **giảm bước decode**, **dùng GPU hiệu quả hơn**, **quản KV cache tốt**.

## ⭐ Speculative Decoding (giảm bước decode)
```
model NHỎ (draft) đoán nhanh K token tiếp -> model LỚN verify CÙNG LÚC (1 forward)
   token nào draft đúng -> chấp nhận (free!) ; sai -> lớn sửa
-> nếu draft đoán đúng nhiều -> sinh K token với ~1 forward của model lớn -> nhanh 2-3×
```
- Ý: model lớn **verify song song** rẻ hơn **sinh tuần tự**. Draft tốt → tăng tốc lớn, chất lượng **không đổi** (lớn vẫn quyết).
- Biến thể: Medusa (nhiều đầu đoán), n-gram/prompt lookup (đoán từ context).

## ⭐ PagedAttention (quản KV cache — vLLM)
```
KV cache cũ: cấp 1 khối LIÊN TỤC tối đa cho mỗi request -> phí RAM (output ngắn vẫn giữ chỗ dài)
PagedAttention: chia KV cache thành "trang" nhỏ (như virtual memory OS)
   -> cấp trang theo nhu cầu, chia sẻ trang (prefix chung) -> ít phí, nhiều request hơn
```
→ Tăng throughput lớn (vLLM) nhờ **không phí RAM KV cache**. Cho phép batch nhiều request hơn trên cùng GPU.

## ⭐ Flash Attention (khái niệm)
```
attention thường: tạo ma trận N×N (độ dài²) trong RAM GPU -> chậm + tốn bộ nhớ
flash attention: tính theo KHỐI, không vật chất hoá ma trận N×N đầy đủ
   -> ít đọc/ghi HBM (bottleneck thật) -> nhanh hơn + tiết kiệm RAM, KẾT QUẢ y hệt
```
→ Tối ưu **memory I/O** (không phải FLOPs) — vì attention bị nghẽn ở băng thông bộ nhớ, không phải tính toán.

## ⭐ Continuous batching + prompt caching (nhắc + sâu)
- **Continuous batching** ([[ah01-llm-serving]]): request xong thoát, request mới chèn → GPU không idle.
- **Prompt/prefix caching**: system prompt/context lặp → cache KV của prefix → không re-prefill ([[ad08-semantic-cache]] ở mức KV).
- **Chunked prefill**: chia prefill prompt dài thành khối → xen kẽ với decode → latency mượt.

## Bảng tổng kỹ thuật
| Kỹ thuật | Tối ưu | Tăng tốc |
|----------|--------|----------|
| Speculative decoding | giảm bước decode | 2-3× latency |
| PagedAttention | KV cache RAM | throughput (nhiều request) |
| Flash attention | memory I/O attention | nhanh + ít RAM |
| Continuous batching | GPU utilization | throughput |
| Prompt caching | bỏ re-prefill | TTFT cho prompt lặp |
| Quantization | kích thước/băng thông | nhanh + vừa GPU nhỏ ([[ah01-llm-serving]]) |

## Vai trò DE
- **Chọn engine** (vLLM/TGI/TensorRT-LLM) theo kỹ thuật hỗ trợ + workload.
- **Ước throughput/cost** ([[ac08-ai-cost-scale]]): tokens/giây/GPU → $/triệu token.
- **Benchmark serving**: đo TTFT/TPOT/throughput dưới tải thật ([[ab06-llm-observability]]).
- Đa số DE **dùng** (không tự viết kernel) → biết để chọn + tune + ước cost.

## Cạm bẫy
- **Tự viết tối ưu** thay dùng engine có sẵn → tốn công, thua vLLM/TGI.
- **Speculative với draft kém** → đoán sai nhiều → chậm hơn (verify phí) → draft phải đủ tốt.
- **Bỏ qua KV cache RAM** → OOM → PagedAttention/giới hạn context.
- **Đo throughput không đo p99 latency** → tối ưu throughput hại trải nghiệm → đo cả hai.
- **Quantize quá tay** → chất lượng tụt → đo eval sau quantize.
- **Tưởng flash attention đổi kết quả** → không, chỉ nhanh hơn (kết quả y hệt).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Speculative decoding: draft đoán + lớn verify song song → nhanh, chất lượng giữ.
- [ ] PagedAttention: KV cache như virtual memory → ít phí, nhiều request.
- [ ] Flash attention: tối ưu memory I/O, kết quả y hệt.
- [ ] Continuous batching + prompt caching + chunked prefill.
- [ ] Vai trò DE: chọn engine + ước throughput/cost, không tự viết kernel.
- 🔭 Tự mò: đọc doc vLLM về PagedAttention + continuous batching; với `fastembed` (embedding), đo throughput batch 1 vs 32 vs 128 câu (câu/giây) → thấy batching tăng GPU/CPU utilization thế nào (ý tưởng giống continuous batching cho LLM).

➡️ Tiếp [[ah08-ai-agents-for-de]] — AI agent tự động hoá DE.
