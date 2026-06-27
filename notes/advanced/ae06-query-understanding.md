# AE06 — Query Understanding & Routing

> Trước khi retrieve, phải **hiểu câu hỏi**: ý định gì, viết lại cho rõ, tách câu phức, định tuyến đúng nguồn. "Hỏi đúng mới tìm đúng" — khâu này quyết định 50% chất lượng RAG. Liên hệ [[ad05-structured-rag]], [[ae01-self-correcting-rag]], [[ab04-semantic-layer-llm]].

## Vì sao retrieval tốt vẫn fail nếu không hiểu query
- Câu hỏi thật **mơ hồ, sai chính tả, viết tắt, đa ý, phụ thuộc ngữ cảnh** ("cái đó so với hôm qua thế nào?").
- Ném thẳng câu thô vào vector search → embed lệch → kéo sai doc (đã thấy ở [[ae01-self-correcting-rag]]: "EOS" 0.643).
- → Một **tầng hiểu query** trước retrieval: phân loại + viết lại + tách + định tuyến.

## ⭐ 4 việc của tầng query understanding
```
câu hỏi thô
 ─> [1 INTENT] phân loại ý định: tra cứu / tính toán / hành động / chitchat
 ─> [2 REWRITE] sửa chính tả, mở rộng đồng nghĩa, giải ngữ cảnh (resolve "nó/cái đó")
 ─> [3 DECOMPOSE] câu phức -> nhiều câu con đơn giản
 ─> [4 ROUTE] gửi tới nguồn đúng: RAG / SQL / cache / tool / từ chối
```

## ⭐ 1. Intent classification
Phân loại để xử lý đúng đường:
| Intent | Đường đi |
|--------|----------|
| Tra cứu kiến thức ("X là gì") | vector RAG ([[ai02-rag-capstone-writeup]]) |
| Định lượng ("doanh thu bao nhiêu") | text-to-SQL / semantic layer ([[ad05-structured-rag]]) |
| Hành động ("gửi email", "tạo ticket") | tool/agent ([[ac04-multi-agent]]) + human approve |
| Chitchat / ngoài phạm vi | trả lời thẳng / từ chối lịch sự |

## ⭐ 2. Query rewriting
| Kỹ thuật | Ví dụ |
|----------|-------|
| Sửa chính tả | "kafka exacly once" → "exactly once" |
| Mở rộng đồng nghĩa/viết tắt | "EOS" → "exactly once semantics" |
| Giải ngữ cảnh (coreference) | "nó chạy chậm" + lịch sử → "Spark job chạy chậm" |
| HyDE (giả thuyết trả lời) | câu hỏi → đoạn trả lời giả → embed ([[ae01-self-correcting-rag]]) |
→ Rewrite dùng **lịch sử hội thoại** ([[ab03-context-engineering]]) để câu standalone (đủ nghĩa độc lập).

## ⭐ 3. Query decomposition (câu phức)
```
"So sánh chi phí Spark và Kafka, cái nào hợp streaming?"
 ─> Q1: chi phí Spark?      ─> retrieve
 ─> Q2: chi phí Kafka?      ─> retrieve
 ─> Q3: cái nào hợp streaming? ─> retrieve
 ─> tổng hợp 3 kết quả -> câu trả lời
```
- Câu hỏi nhiều ý → retrieve từng ý → đủ context hơn là 1 lần cho cả câu (mỗi ý cần doc khác nhau).
- Liên hệ multi-hop ([[ae02-graphrag-build]]) và self-correction ([[ae01-self-correcting-rag]]).

## ⭐ 4. Routing (đắt nhất nếu sai)
```
query ─> router (heuristic / classifier / LLM nhỏ)
   ├─ cache hit? ─> trả ngay ([[ad08-semantic-cache]])
   ├─ định lượng ─> SQL/semantic layer ([[ad05-structured-rag]])
   ├─ kiến thức ─> RAG
   ├─ hành động ─> tool (guardrail + approve [[ad04-llm-security]])
   └─ ngoài phạm vi ─> từ chối ("tôi không hỗ trợ việc này")
```
→ Route sai = mọi thứ sau sai (hỏi số mà đi RAG → bịa số). Router là **ngã ba quyết định**.

## Snippet (router heuristic đơn giản)
```python
def route(q: str) -> str:
    ql = q.lower()
    if any(w in ql for w in ["bao nhiêu", "tổng", "trung bình", "top "]):
        return "sql"          # định lượng -> truy bảng
    if any(w in ql for w in ["gửi", "tạo", "xoá", "đặt"]):
        return "tool"         # hành động -> tool + approve
    return "rag"              # mặc định -> kiến thức
```
(Thực tế: classifier/LLM nhỏ thay heuristic khi nhiều intent.)

## Cạm bẫy
- **Bỏ qua tầng hiểu query** → embed câu thô mơ hồ → retrieve sai (lỗi gốc thường ở đây, không phải retriever).
- **Route sai** → hỏi số đi RAG (bịa), hỏi kiến thức đi SQL (lỗi) → router phải chắc + có fallback.
- **Rewrite làm méo ý** → mở rộng quá tay đổi nghĩa → giữ sát ý gốc.
- **Decompose câu đơn** (không cần) → tốn call thừa → chỉ tách khi thật sự đa ý.
- **Không giải coreference** → "nó/cái đó" không rõ → retrieve vô nghĩa → dùng lịch sử hội thoại.
- **Không có "từ chối"** → cố trả mọi câu kể cả ngoài phạm vi → hallucinate.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 4 việc: intent / rewrite / decompose / route.
- [ ] Intent → đường đi (RAG/SQL/tool/từ chối).
- [ ] Rewrite: chính tả/đồng nghĩa/coreference/HyDE; dùng lịch sử.
- [ ] Decompose câu phức → câu con → tổng hợp.
- [ ] Routing là ngã ba quyết định; route sai = sai hết.
- 🔭 Tự mò: viết `query_router.py` — heuristic route 6 câu hỏi (số/kiến thức/hành động/ngoài-phạm-vi) in ra đường đi; ghép với `text_to_sql.py` (SQL path) + `rag_over_notes.py` (RAG path) thành 1 entry point; thêm rewrite mở rộng viết tắt trước khi retrieve.

➡️ Tiếp [[ae07-reranking-deep]] — rerank sâu.
