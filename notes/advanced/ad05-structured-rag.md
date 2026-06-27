# AD05 — RAG trên Dữ Liệu CÓ CẤU TRÚC (tables/SQL)

> RAG không chỉ cho văn bản. Khi câu hỏi cần **SỐ chính xác** ("doanh thu Q3?"), kéo text vào prompt là sai cách — phải truy **bảng/DB**. Kết hợp retrieval + text-to-SQL/semantic layer. Liên hệ [[aa01-text-to-sql]], [[ab04-semantic-layer-llm]], [[ai02-rag-capstone-writeup]].

## Vì sao text-RAG KHÔNG hợp cho dữ liệu có cấu trúc
- Hỏi "tổng doanh thu tháng 7 theo vùng?" → câu trả lời là **phép tính trên bảng**, không nằm sẵn trong đoạn text nào.
- Nhồi cả bảng vào context → tốn token, LLM **tự tính tay → sai số** (LLM tính toán dở).
- → Cần: LLM **sinh truy vấn** (SQL/metric) chạy trên engine → trả số **chính xác**, không hallucinate.

## ⭐ Hai thế giới — và cách ghép
```
UNSTRUCTURED (text/PDF)        STRUCTURED (bảng/DB)
   -> vector RAG                  -> text-to-SQL / semantic layer
   "giải thích chính sách"        "doanh thu Q3 = ?"
            \                        /
             route theo loại câu hỏi
        (LLM router phân loại: cần SỐ hay cần VĂN?)
```
- **Câu định tính** ("vì sao", "mô tả") → vector RAG ([[ai02-rag-capstone-writeup]]).
- **Câu định lượng** ("bao nhiêu", "top N", "theo tháng") → query trên bảng.
- **Hybrid**: "doanh thu giảm vì sao?" → số (SQL) + giải thích (RAG).

## ⭐ Table/Schema Retrieval — vấn đề "chọn bảng nào"
DB lớn có **hàng trăm bảng/nghìn cột** — không nhồi hết schema vào prompt được. Phải **retrieve schema liên quan** trước:
```
câu hỏi ─> embed ─> tìm BẢNG/CỘT liên quan (mô tả schema đã embed)
   ─> đưa CHỈ schema liên quan + vài dòng mẫu vào prompt
   ─> LLM sinh SQL trên schema đó (schema linking [[aa01-text-to-sql]])
```
→ Chính là **RAG nhưng "tài liệu" = mô tả bảng/cột**. Metadata schema tốt (mô tả cột, ví dụ giá trị) = retrieval schema tốt.

## ⭐ An toàn: đừng để LLM viết SQL thô tự do
- SQL thô nguy hiểm + sai metric ([[aa01-text-to-sql]]) → guardrail (chỉ SELECT, EXPLAIN, sandbox read-only).
- Tốt hơn: **semantic layer** ([[ab04-semantic-layer-llm]]) — LLM chọn `{metric, dimension, filter}` đã governed thay vì viết SQL → nhất quán + an toàn.
- Câu khám phá ngoài metric → text-to-SQL có guardrail (80/20).

## Pipeline structured-RAG đầy đủ
```
câu hỏi
 ─> [router] định lượng / định tính / hybrid?
 ─> (định lượng) schema retrieval ─> sinh SQL/metric ─> validate+sandbox ─> chạy ─> SỐ
 ─> (định tính)  vector retrieval ─> context ─> LLM trả lời
 ─> (hybrid) gộp SỐ + VĂN ─> LLM tổng hợp câu trả lời có cả con số lẫn giải thích
 ─> citations: chỉ rõ "số từ bảng X", "giải thích từ doc Y" ([[aa03-rag-production]])
```

## Snippet (ý tưởng schema linking)
```python
# mô tả mỗi bảng -> embed -> index (như RAG)
schema_docs = {
  "fact_sales": "doanh thu theo đơn: order_id, date, region, product, amount, refund",
  "dim_region": "vùng: region_id, name, country",
}
# câu hỏi -> retrieve bảng liên quan -> chỉ đưa schema đó cho LLM sinh SQL
relevant = vector_search(question, schema_docs, k=3)
sql = llm_generate_sql(question, schema=relevant)   # rồi GUARDRAIL + EXPLAIN + sandbox
```

## Cạm bẫy
- **Dùng text-RAG cho câu hỏi số** → LLM tính tay → sai; phải query engine.
- **Nhồi cả schema DB** vào prompt → tốn token + nhiễu → schema retrieval.
- **SQL thô không guardrail** → nguy hiểm + sai metric → semantic layer / sandbox.
- **Metadata schema nghèo** (tên cột khó hiểu, không mô tả) → LLM sinh SQL sai → đầu tư mô tả schema.
- **Không citation nguồn số** → không kiểm chứng được → ghi rõ số từ bảng/truy vấn nào.
- **Quên hybrid**: câu cần cả số lẫn giải thích mà chỉ làm một → trả lời thiếu.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao text-RAG không hợp câu hỏi định lượng.
- [ ] Router định tính/định lượng/hybrid.
- [ ] Schema/table retrieval = RAG trên mô tả bảng (chống nhồi cả DB).
- [ ] An toàn: semantic layer / guardrail thay SQL thô tự do.
- [ ] Citation nguồn số; metadata schema tốt.
- 🔭 Tự mò: ghép `text_to_sql.py` + `rag_over_notes.py` — viết "router" heuristic (câu có "bao nhiêu/tổng/top" → SQL path; "vì sao/mô tả" → RAG path); với SQL path, embed mô tả 2-3 bảng rồi retrieve bảng liên quan trước khi sinh SQL (schema retrieval thu nhỏ).

➡️ Tiếp [[ad06-doc-parsing]] — chất lượng RAG bắt đầu từ parse.
