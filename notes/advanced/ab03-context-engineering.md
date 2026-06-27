# AB03 — Context Engineering & Memory cho Agent

> Quản "cửa sổ context" (token budget) của LLM/agent: chọn — cắt — nén — nhớ. **DE là người xây kho memory + retrieval cho agent.** Liên hệ [[aa05-agentic-pipelines]], [[ai08-ai-cost-latency]].

## Vì sao quan trọng
Context window có **hạn** (token) và **đắt** ([[ai08-ai-cost-latency]]). Nhồi tất cả vào = tốn tiền, chậm, và tệ hơn: **"lost in the middle"** — LLM chú ý kém ở GIỮA context dài, dễ bỏ sót thông tin ở giữa. → Phải *kỹ thuật hoá* việc đưa gì vào context. "Context engineering" = thế hệ sau của "prompt engineering": không chỉ viết prompt hay, mà **dàn dựng đúng thông tin, đúng lượng, đúng vị trí**.

## ⭐ Ngân sách context (token budget)
```
[ system + instructions ]  cố định, ngắn, rõ
[ tools / schema ]         chỉ tool cần cho task
[ retrieved context ]      top-k từ RAG (đã rerank) — KHÔNG nhồi 50 chunk
[ memory ]                 tóm tắt hội thoại + fact dài hạn liên quan
[ user query ]            đặt CUỐI (gần nơi sinh, ít bị "lost in middle")
```
Mỗi phần cạnh tranh cùng 1 ngân sách → phải ưu tiên. **Đặt thông tin quan trọng ở ĐẦU hoặc CUỐI**, không vùi giữa.

## ⭐ Memory cho agent — 2 loại (DE xây cả hai)
| Loại | Là gì | Lưu ở đâu | DE làm gì |
|------|-------|-----------|-----------|
| **Short-term** (working) | hội thoại hiện tại, kết quả tool vừa gọi | trong context / cache phiên | cắt cửa sổ, **tóm tắt** lượt cũ khi đầy |
| **Long-term** | fact bền (hồ sơ user, tài liệu, lịch sử) | **vector store** + DB ([[ai02-rag-capstone-writeup]]) | ingest, embed, index, **retrieve đúng lúc** |

→ "Memory" của agent thực chất là **một pipeline RAG**: ghi (write) fact → embed → lưu; đọc (read) = semantic search khi cần. Mọi nguyên tắc DE (idempotency, versioning, dedup) áp y nguyên.

## Kỹ thuật quản context
| Kỹ thuật | Ý tưởng | Khi dùng |
|----------|---------|----------|
| **Truncation** | cắt bớt lượt cũ nhất | đơn giản, mất thông tin |
| **Summarization** | nén hội thoại cũ thành tóm tắt ngắn | giữ ý, giảm token (rolling summary) |
| **Retrieval (RAG)** | chỉ kéo phần liên quan query | kho lớn, chọn lọc |
| **Compression** | bỏ token thừa, gộp, trích yếu | tiết kiệm thêm |
| **Tool-result caching** | cache kết quả tool/truy vấn lặp | tránh gọi lại tốn kém ([[ai08-ai-cost-latency]]) |
| **Structured memory** | lưu fact dạng key-value/graph, không text thô | fact chính xác (tên, số) |

## Sơ đồ vòng đời 1 lượt agent
```
query ─> [retrieve long-term memory] ─┐
         [load short-term summary]  ──┼─> build context (budget) ─> LLM ─> answer + (write new facts back to memory)
         [pick tools]               ──┘                                         └─> cập nhật memory (vòng sau dùng)
```

## Cạm bẫy
- **Nhồi nhiều = tốt? SAI.** Context dài → "lost in middle", nhiễu, đắt, chậm. **Ít mà đúng** thắng.
- **Memory không dọn** → phình, lẫn fact cũ/mâu thuẫn → cần versioning + TTL + dedup.
- **Tóm tắt mất fact quan trọng** (số tiền, ID) → giữ structured memory cho fact chính xác.
- **Không tách phiên** → memory user A rò sang user B (rủi ro privacy [[aa02-guardrails]]).
- **Cache không key đúng** → trả kết quả cũ sai ngữ cảnh.

## Liên hệ DE kinh điển
- Memory store = **feature store / serving layer** cho agent.
- Rolling summary = **incremental aggregation** ([[ai09-streaming-ai]]) áp cho hội thoại.
- Tool-cache = **materialized view** áp cho lời gọi LLM.

## ✅ "Tự kiểm tra & tự mò"
- [ ] "Lost in the middle" là gì → vì sao đặt info quan trọng ở đầu/cuối.
- [ ] Short-term vs long-term memory; vì sao long-term = RAG pipeline.
- [ ] 6 kỹ thuật quản context (truncate/summarize/retrieve/compress/cache/structured).
- [ ] Vì sao "nhồi nhiều" không tốt.
- 🔭 Tự mò: lấy `rag_over_notes.py`, viết vòng hội thoại nhiều lượt với **rolling summary** (mỗi 3 lượt nén thành 1 tóm tắt) + **token budget** (đếm xấp xỉ bằng số từ) cắt context khi vượt ngưỡng.

➡️ Tiếp [[ab04-semantic-layer-llm]] — NL→metric an toàn thay text-to-SQL thô.
