# AI09 — Streaming cho AI Infra (re-index < 1 phút)

> "Streaming bị thổi phồng" cho analytics — nhưng **AI infra là cái 10% streaming thực sự cần**. Sâu hơn [[45-streaming-intro]], [[52-lambda-kappa]].

## Vì sao AI infra cần streaming (lý do thật)
Câu phỏng vấn mới: *"Thiết kế hệ thống mà khi tài liệu cập nhật, nó tự chạy qua embedding rồi vào vector index trong **dưới 1 phút**. Cái gì vỡ khi traffic ×2?"*
- **Freshness có yêu cầu thật**: tài liệu/chính sách đổi → RAG phải trả lời theo bản mới ngay (không chờ batch đêm). SLA freshness < 1' là yêu cầu nghiệp vụ, không "stream cho oai".
- **Feature real-time cho inference**: model cần feature mới nhất lúc serve ([[c09-case-recsys]], [[c03-case-fraud]]).
- **Kiểm dữ liệu LLM trước khi vào production**: validate streaming ([[ai06-llm-output-governance]]).

## Kiến trúc event-driven re-index
```
Tài liệu đổi (CDC/webhook/file-watch) ──► event "doc_changed" ──► Kafka/queue
                                                                    │
                                                                    ▼
                                          Stream processor:
                                          1. fetch doc        2. CHUNK (chỉ doc đó)
                                          3. EMBED chunks     4. UPSERT vector store (idempotent theo doc_id)
                                          5. xoá chunk cũ của doc
                                                                    │
                                                                    ▼
                                          vector index cập nhật < 1' ──► RAG query thấy bản mới
```
= incremental re-index ([[ai02-rag-capstone-writeup]]) nhưng **event-driven** thay vì batch. Cùng nguyên tắc idempotent upsert theo doc_id.

## ⭐ "Cái gì vỡ khi traffic ×2?" (câu hỏi cốt lõi — trả lời thế nào)
Phân tích bottleneck theo từng tầng (tư duy hệ phân tán — [[c01-system-design-framework]]):
| Tầng | Vỡ thế nào khi ×2 | Khắc phục |
|------|-------------------|-----------|
| **Embedding throughput** | model inference là nút cổ chai (vd 24 chunk/s — [[ai08-ai-cost-latency]]) → hàng đợi dồn | nhiều worker/GPU, batch, autoscale consumer |
| **Vector DB write** | upsert + rebuild index (HNSW) tốn → write amplification | batch upsert, index incremental, sharding |
| **API rate limit** | embedding/LLM API giới hạn req/s → 429 | backpressure, queue, retry/backoff, cache |
| **Kafka/queue** | partition không đủ → lag | tăng partition, scale consumer ([[46-kafka-core]]) |
| **Freshness SLA** | lag tăng → vượt 1' | monitor lag, ưu tiên doc nóng |
→ Trả lời "X vỡ vì Y, khắc phục bằng Z" cho mỗi tầng = thể hiện tư duy hệ thống (cái phỏng vấn tìm).

## Stateful streaming features cho AI
- Feature real-time (vd "user vừa xem N sản phẩm") → windowed aggregation → online feature store cho inference ([[49-stream-processing]], [[c09-case-recsys]]).
- Watermark/late data áp y nguyên.

## Batch vs Streaming cho embedding — khi nào
- **Batch/micro-batch**: index ban đầu, tài liệu đổi không gấp (đêm) — đa số trường hợp, rẻ & đơn giản.
- **Streaming (<1')**: chỉ khi freshness là yêu cầu thật (tài liệu đổi liên tục cần phản ánh ngay). **Đừng over-stream** — nhiều RAG batch/micro-batch là đủ.

## Validate dữ liệu LLM trong stream
LLM output streaming vào production → validate **trước khi** vào bảng (governance — [[ai06-llm-output-governance]]): schema check + quarantine trong stream processor, không để rác vào real-time.

## ⚠️ Cạm bẫy
- Stream hoá mọi thứ khi batch đủ (over-engineer — anh senior nói đúng cho analytics).
- Re-embed toàn bộ mỗi event (phải incremental theo doc_id).
- Không idempotent upsert → trùng chunk khi event replay (at-least-once).
- Quên rate-limit API embedding → 429 khi traffic cao.
- Không monitor lag/freshness → vượt SLA âm thầm.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao AI infra là "10% streaming thực sự cần".
- [ ] Kiến trúc event-driven re-index (<1', idempotent theo doc_id).
- [ ] Trả lời "vỡ gì khi ×2" theo từng tầng (embedding/vector-write/rate-limit/queue).
- 🔭 Mô phỏng: watch `notes/` (file thay đổi) → gọi `build_index` của capstone → đo thời gian từ "sửa note" tới "search thấy bản mới" (incremental đã có sẵn).

➡️ Tiếp: [[ai10-summary]].
