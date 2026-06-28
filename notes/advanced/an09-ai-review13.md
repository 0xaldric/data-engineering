# AN09 — AI Review 13 + Trạng Thái Curriculum

> Tổng kết **AI-Advanced 13** (AN01–AN08): bảng "RAG pattern → vấn đề giải", danh mục ngành đã phủ, trạng thái curriculum (13 batch). Nối [[am09-ai-review12]], [[ak09-ai-review10]].

## 🏁 Batch này (AN01–AN08)
| # | Chủ đề | Code | Ý chốt |
|---|--------|------|--------|
| AN01 | RAG advanced patterns | ✅ `query_router.py` | routing + multi-vector + hypo + RAPTOR |
| AN02 | Agentic patterns | — | ReAct mặc định; tool>pattern |
| AN03 | Case telecom | — | CDR scale; LLM lớp chăm sóc |
| AN04 | Case energy | — | an toàn vật lý; không điều khiển lưới |
| AN05 | Case travel | — | đa ngữ + real-time inventory |
| AN06 | Case social media | — | engagement⇄safety; moderation scale |
| AN07 | Mock interview 3 | — | multimodal scale + frame sampling |
| AN08 | Coding exercises 4 | — | router/ReAct/provenance/budget/as-of (verify) |

→ Kho AI: **26 script chạy được** + ~122 note AI (13 batch).

## ⭐⭐ Bảng "RAG pattern → vấn đề giải" (tổng hợp)
| Vấn đề | Pattern |
|--------|---------|
| Câu không phải RAG (số/hành động) | query router ([[an01-rag-advanced-patterns]]) |
| Chunk lẻ thiếu ngữ cảnh | parent-child, RAPTOR ([[am03-advanced-chunking]]) |
| Lệch câu hỏi ↔ tài liệu | hypothetical questions, HyDE ([[ae01-self-correcting-rag]]) |
| 1 embedding/doc không đủ | multi-vector ([[an01-rag-advanced-patterns]]) |
| Vector vs keyword khác thang | RRF fusion ([[am04-hybrid-fusion]]) |
| Doc đúng rank thấp | rerank ([[ae07-reranking-deep]]) |
| Top-k trùng ý | MMR ([[am08-coding-exercises-3]]) |
| Retrieval yếu | self-correction ([[ae01-self-correcting-rag]]) |
| Không biết lỗi đâu | rag_debugger ([[am01-rag-debugging]]) |

## ⭐ Danh mục NGÀNH đã phủ (15 vertical)
```
e-commerce · legal · healthcare · finance · education · government ·
manufacturing/IoT · logistics · media/streaming · HR/recruiting ·
insurance · gaming · agritech · telecom · energy · travel · social media
```
→ Mỗi ngành áp khung 7 bước, làm nổi "nhấn" riêng + vị trí trên trục độ-gắt-an-toàn ([[ak09-ai-review10]]). Đủ để trả mọi đề system-design AI theo ngành.

## ⭐ Trạng thái Curriculum (cột mốc)
```
Track 1 (curriculum gốc Phase 0-9): hoàn thành
Track 2 nền tảng (SQL/system-design/modeling/ops): ~160 note
Module AI: 13 batch · ~122 note · 26 script chạy được
   = nền tảng + production + system-design + 15 vertical + luyện PV + kỹ thuật sâu + patterns
TỔNG: ~290 note + 26 script local (không API key)
```
→ Curriculum AI-DE **đã rất đầy đủ**. Batch tiếp: đào sâu hơn (kỹ thuật mới khi field tiến), ngành mới, hoặc luyện tập (mock/exercise) thêm.

## ⭐ 3 phát hiện code nổi bật (toàn hành trình)
1. **prefix-OFF > ON** ([[ah02-embedding-benchmark]]): mặc định model HẠI corpus Việt.
2. **RRF > weighted** ([[am04-hybrid-fusion]]): thêm keyword có thể TỤT, RRF robust.
3. **cosine ≠ sự thật** ([[ag02-hallucination-detection]], [[ad08-semantic-cache]]): bề mặt ≠ ngữ nghĩa.
→ Đều cùng thông điệp: **đo trên data của bạn, đừng tin mặc định**.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Bảng RAG pattern → vấn đề (nói được mỗi pattern giải gì).
- [ ] 15+ ngành đã phủ + nhấn riêng mỗi ngành.
- [ ] 3 phát hiện code + thông điệp "đo đừng tin mặc định".
- [ ] Tự chấm: phần nào curriculum còn yếu → ôn.
- 🔭 Tự mò: tự kiểm tra toàn diện — chạy lại 26 script một lượt (smoke test); với mỗi review note (ai10/ab09/.../an09) tự trả các checklist; chọn 1 ngành chưa có (vd bất động sản, bán lẻ vật lý) tự viết case study khung 7 bước.

➡️ Hết AI-Advanced 13. Curriculum AI-DE đã toàn diện; batch tiếp đào sâu/luyện tập thêm — vẫn ưu tiên AI/LLM.
