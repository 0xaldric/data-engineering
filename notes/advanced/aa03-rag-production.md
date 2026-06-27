# AA03 — RAG Production Patterns

> RAG demo chạy được là một chuyện; RAG **production** (nhiều user, tin cậy, rẻ) cần thêm nhiều pattern. Sâu hơn [[k05-vector-rag-deep]], [[ai05-retrieval-eval]], [[ai02-rag-capstone-writeup]].

## ⭐ Semantic cache
Câu hỏi **tương tự** (không cần giống hệt) → trả lời từ cache, không gọi LLM lại (đắt nhất — [[ai08-ai-cost-latency]]).
```
query → embed → tìm trong cache câu cũ có cosine >= 0.95 → hit: trả cached answer
                                                          → miss: chạy RAG + lưu cache
```
Khác cache thường (exact key): dùng **vector similarity** làm key. Giảm cost/latency lớn cho FAQ lặp. ⚠️ Ngưỡng cao (0.95+) để tránh trả nhầm câu khác nghĩa; invalidate khi tài liệu đổi.

## Citations (nguồn)
Trả kèm **chunk nguồn** (file/section) cho mỗi câu trả lời → người dùng verify, tăng tin cậy, audit. LLM được yêu cầu "chỉ dùng context + trích nguồn". Chống hallucination (grounding — [[aa02-guardrails]]).

## Fallback (khi retrieval rỗng/kém)
- Retrieval không ra chunk nào > ngưỡng → **"không tìm thấy thông tin"** thay vì để LLM bịa.
- Confidence thấp → escalate (human / nói rõ không chắc).
- Tránh "luôn trả lời kể cả khi không biết" (nguồn hallucination).

## Query understanding
- **Query rewriting**: viết lại câu hỏi mơ hồ/đa ý thành rõ trước khi retrieve.
- **HyDE** (Hypothetical Document Embeddings): LLM sinh "câu trả lời giả định" → embed nó để retrieve (đôi khi khớp tài liệu tốt hơn câu hỏi).
- **Multi-query**: sinh nhiều biến thể câu hỏi → gộp kết quả (recall cao hơn).

## Reranking
Retrieve top-N rộng (bi-encoder, rẻ) → **cross-encoder rerank** top-N → top-k chính xác → đẩy chunk đúng lên đầu (tăng MRR/nDCG — [[ai05-retrieval-eval]]).

## Multi-tenancy
Nhiều khách/tổ chức dùng chung hệ → **filter theo tenant_id** (metadata filter + vector) để khách A không thấy tài liệu khách B. Bảo mật + đúng. Index riêng/namespace hoặc filter bắt buộc.

## Hybrid + metadata filter
Vector + keyword (BM25) + filter (ngày/nguồn/quyền) → recall tốt + an toàn + đúng phạm vi ([[k05-vector-rag-deep]]).

## Online eval & feedback
- Thu **feedback** (thumbs up/down, click) → đo chất lượng production thật.
- A/B test (chunk size/model/prompt) trên traffic thật.
- Monitor: latency p99, cost/query, retrieval score distribution, % fallback → observability ([[k07-observability-tooling]]).

## Kiến trúc RAG production
```
query → guardrail (PII/injection) → query rewrite → [semantic cache hit?]
  → retrieve (hybrid + tenant filter) → rerank → grounding check
  → LLM (với citations) → output filter → answer + sources + feedback log
```

## ⚠️ Cạm bẫy
- Không cache → cost/latency cao cho câu lặp.
- Không fallback → bịa khi không có tài liệu.
- Không citations → không verify/audit được.
- Multi-tenant không filter → rò rỉ chéo khách (nghiêm trọng).
- Không online eval → không biết chất lượng production (offline ≠ online).
- Cache không invalidate khi tài liệu đổi → trả lời cũ.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Semantic cache (vector làm key, ngưỡng cao, invalidate).
- [ ] Citations + fallback (chống hallucination).
- [ ] Query rewrite/HyDE/multi-query; reranking.
- [ ] Multi-tenancy filter; online eval/feedback.
- 🔭 Thêm semantic cache vào `rag_over_notes.py`: lưu (query_embedding, answer); query mới cosine >= 0.95 với cache → trả cached; đo hit rate.

➡️ Tiếp: [[aa04-training-data-prep]].
