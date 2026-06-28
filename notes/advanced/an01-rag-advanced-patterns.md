# AN01 — RAG Advanced Patterns + Query Router ⭐ (có code chạy được)

> Mẫu RAG nâng cao vượt "chunk-embed-retrieve" cơ bản: query routing, multi-vector, hypothetical questions, RAPTOR. Code: [`query_router.py`](../../projects/06-ai-data-engineering/query_router.py). Liên hệ [[ae06-query-understanding]], [[ad05-structured-rag]], [[am03-advanced-chunking]].

## ⭐ 1. Query Routing (định tuyến — đã code)
Không phải câu nào cũng đi RAG. Route tới đúng nguồn:
```
câu hỏi ─> [router]
   định lượng ("doanh thu bao nhiêu") -> text-to-SQL/semantic layer ([[ad05-structured-rag]])
   kiến thức ("X là gì")              -> RAG retrieve
   hành động ("gửi email")           -> tool + human approve ([[ad04-llm-security]])
   ngoài phạm vi ("kể chuyện cười")  -> từ chối lịch sự
```
**Code chạy** (heuristic + embedding): 6/6 câu route đúng — heuristic cho action/định lượng (từ khoá chắc, an toàn), embedding cho RAG vs ngoài-phạm-vi (cos RAG 0.84 vs REJECT 0.77). → Route sai = mọi tầng sau sai (hỏi số đi RAG → bịa số).

## ⭐ 2. Multi-vector (1 doc, nhiều embedding)
```
1 doc -> nhiều "góc" embedding:
   - embedding của TÓM TẮT (tìm theo chủ đề tổng)
   - embedding của từng ĐOẠN chi tiết (tìm chi tiết)
   - embedding của CÂU HỎI giả về doc (xem #3)
-> query match góc phù hợp -> linh hoạt hơn 1 embedding/doc
```
→ Giải: tóm tắt tìm tốt câu hỏi tổng, chi tiết tìm tốt câu hỏi cụ thể. Lưu nhiều vector trỏ cùng doc.

## ⭐ 3. Hypothetical Questions (index câu hỏi giả)
```
THƯỜNG: index ĐOẠN văn -> query (câu hỏi) match đoạn (lệch dạng: hỏi vs khai báo)
HYPO:   với mỗi đoạn, LLM sinh "câu hỏi mà đoạn này TRẢ LỜI" -> index CÂU HỎI đó
   -> query (câu hỏi) match câu-hỏi-giả (cùng dạng) -> khớp tốt hơn
```
→ Cùng họ HyDE ([[ae01-self-correcting-rag]]) nhưng làm ở phía INDEX: thu hẹp khoảng cách "câu hỏi ↔ tài liệu" bằng cách index câu hỏi.

## ⭐ 4. RAPTOR (cây tóm tắt phân cấp)
```
chunk lá ─> cluster ─> LLM tóm tắt cụm ─> chunk tóm tắt mức 1
       ─> cluster tiếp ─> tóm tắt mức 2 ... -> CÂY
retrieve: tìm cả lá (chi tiết) lẫn node tóm tắt (tổng quan)
```
→ Câu hỏi tổng quan ("tài liệu nói gì về X") → match node tóm tắt; câu chi tiết → match lá. Giải bài "1 chunk không đủ ngữ cảnh toàn cục".

## Bảng pattern → vấn đề giải
| Pattern | Giải vấn đề |
|---------|-------------|
| Query routing | câu không phải RAG (số/hành động/ngoài phạm vi) |
| Multi-vector | 1 embedding/doc không bắt mọi góc |
| Hypothetical questions | lệch dạng câu hỏi ↔ tài liệu |
| RAPTOR | thiếu ngữ cảnh tổng quan (chunk lẻ) |
| Parent-child ([[am03-advanced-chunking]]) | nhỏ-tìm-to-trả |
| Self-correction ([[ae01-self-correcting-rag]]) | retrieval yếu → reformulate |

## Cạm bẫy
- **Mọi câu đi RAG** → hỏi số → bịa; hành động → không làm được → route trước.
- **Route sai** → mọi tầng sau sai → router chắc (heuristic high-stakes) + fallback.
- **Multi-vector phình index** → nhiều vector/doc → cân cost vs lợi.
- **Hypothetical questions tốn** (LLM sinh mỗi đoạn) → batch offline; đáng cho corpus tĩnh.
- **RAPTOR build đắt** (LLM tóm tắt nhiều tầng) → cho corpus lớn cần tổng quan; over-kill cho nhỏ.
- **Không fallback** router → câu không khớp nhóm nào → mặc định an toàn (RAG/từ chối).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Query routing: 4 đường (SQL/RAG/action/reject); route sai = sai hết.
- [ ] Multi-vector (nhiều góc/doc); hypothetical questions (index câu hỏi).
- [ ] RAPTOR (cây tóm tắt — tổng quan + chi tiết).
- [ ] Pattern → vấn đề giải.
- [ ] Cạm bẫy: mọi câu RAG, route sai, build đắt.
- 🔭 Tự mò: ghép `query_router.py` vào `ai_product.py` ([[aj03-capstone-integration]]) — route TRƯỚC: SQL→text_to_sql, RAG→retrieve, ACTION→"cần duyệt", REJECT→từ chối; in luồng mỗi câu đi đường nào. Đó là entry-point thông minh cho AI data product.

➡️ Tiếp [[an02-agentic-patterns]] — mẫu agentic sâu.
