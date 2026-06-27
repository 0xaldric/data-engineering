# AI08 — Cost & Latency cho AI Pipeline

> Chi phí thành **ràng buộc thiết kế** trong AI infra (khác analytics: tính theo token/call, không chỉ compute/scan). Sâu hơn [[59-cost-finops]].

## Vì sao cost/latency là ràng buộc thiết kế (không phải tối ưu sau)
- Mỗi embedding/LLM call **tốn tiền theo token** + **tốn thời gian** (API round-trip hoặc model inference).
- Pipeline triệu tài liệu × nhiều chunk × re-embed khi đổi model → tiền tăng tuyến tính/cấp số.
- Real-time serving có **latency budget cứng** (vd RAG trả lời < 2s, feature serving < 100ms).
→ Phải tính cost/latency **khi thiết kế** (chọn model, chunk size, cache), không để cuối.

## ⭐ Đòn bẩy giảm cost
| Đòn bẩy | Cách | Tác động |
|---------|------|----------|
| **Cache embedding** | hash(text+model) → vector; text không đổi → dùng lại | tránh re-embed (incremental — [[ai02-rag-capstone-writeup]]) |
| **Batch** | embed nhiều text/call thay từng cái | API/model hiệu quả hơn nhiều |
| **Chọn model đúng cỡ** | model nhỏ (bge-small 384) đủ thì đừng dùng lớn (1536) | rẻ + nhanh hơn |
| **Local vs API** | local (fastembed) rẻ/không gửi data; API chất lượng cao nhưng tốn $/token | cân theo scale + PII |
| **Giảm chunk dư** | dedup chunk, chunk size hợp lý | ít embedding hơn |
| **Semantic cache (LLM)** | câu hỏi tương tự → trả cache (không gọi LLM lại) | giảm LLM call (đắt nhất) |
| **Retrieval top-k nhỏ** | đưa ít chunk vào prompt LLM | ít token input → rẻ |

## Cost breakdown (RAG điển hình)
```
Embedding (index): 1 lần/tài liệu (+ re-embed khi đổi) — rẻ tương đối
Embedding (query): mỗi query 1 lần — rẻ
LLM generation:    mỗi query, token = prompt (chunk retrieved) + output — ĐẮT NHẤT
```
→ Đắt nhất thường là **LLM generation** (token nhiều, model lớn). Giảm: retrieval tốt (ít chunk hơn nhưng đúng — [[ai05-retrieval-eval]]), semantic cache, model nhỏ hơn cho task đơn giản.

## Đo thực tế (capstone)
Embed 1454 chunks (bge-small local, CPU) ~60s ≈ **24 chunks/s**. Re-embed incremental 30 chunks ~3.4s. → ở scale triệu chunk: 1M/24 ≈ 11 giờ trên 1 CPU → cần batch + nhiều worker/GPU. **Đo để biết scale nào cần gì.**

## Latency budget (real-time)
```
RAG trả lời = embed query (ms) + vector search (ms) + LLM generation (giây) 
            ── LLM thường là phần lâu nhất
```
- Feature/embedding serving cho inference: < 100ms → model nhỏ + cache + online store ([[c09-case-recsys]]).
- Streaming index < 1' ([[ai09-streaming-ai]]).
- Rate-limit/throughput của API embedding/LLM → backpressure + queue khi traffic cao.

## FinOps cho AI (khác analytics)
- **Unit economics**: cost per query/document/user (token × giá). Theo dõi.
- Tag/attribute cost theo feature/team.
- Budget alert khi token spend vượt ngưỡng.
- Đắt nhất: LLM generation > embedding > storage → tối ưu đúng chỗ (đo trước).

## ⚠️ Cạm bẫy
- Không cache → re-embed/re-call vô ích (tốn $).
- Embed từng text (không batch) → chậm + đắt.
- Model quá lớn cho task đơn giản.
- Gửi PII qua API embedding/LLM (rủi ro + có thể vi phạm) → local/redact ([[ai-advanced guardrails]]).
- Không đo token spend → bill sốc cuối tháng.
- Đưa quá nhiều chunk vào prompt (token input lớn) → đắt + nhiễu.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao cost là ràng buộc thiết kế (token/call); đắt nhất = LLM generation.
- [ ] Đòn bẩy: cache/batch/model-size/semantic-cache/top-k.
- [ ] Unit economics + latency budget real-time.
- 🔭 Trong capstone, thêm cache embedding (dict hash→vector) và đo thời gian re-index khi không có cache vs có.

➡️ Tiếp: [[ai09-streaming-ai]].
