# AG01 — RAG cho BI/Analytics & Conversational Data

> "Chat với dữ liệu": người dùng hỏi tự nhiên → hệ trả **số chính xác + giải thích + viz**. Kết hợp semantic layer + text-to-SQL + RAG metadata. Khác RAG text: phải **đúng số tuyệt đối**. Liên hệ [[ab04-semantic-layer-llm]], [[aa01-text-to-sql]], [[ad05-structured-rag]].

## Vì sao "chat với data" khó hơn RAG text
- RAG text: trả đoạn văn "đủ đúng" là ổn. BI: **sai 1 con số = mất niềm tin toàn hệ** (sếp ra quyết định sai).
- Câu hỏi BI cần **tính toán trên bảng** (tổng/trung bình/so kỳ), không nằm sẵn trong text.
- Cần hiểu **schema + định nghĩa metric** (revenue gross hay net?) → không được đoán.

## ⭐ Kiến trúc: 3 mảnh ghép
```
câu hỏi NL ("doanh thu Q3 theo vùng, so Q2?")
 ─> [1 RAG metadata] hiểu bảng/cột/metric nào liên quan (schema retrieval [[ad05-structured-rag]])
 ─> [2 SEMANTIC LAYER] map sang {metric, dimension, filter} đã governed ([[ab04-semantic-layer-llm]])
 ─> [3 chạy] semantic layer -> SQL chuẩn -> engine -> SỐ chính xác
 ─> LLM diễn giải SỐ thành câu trả lời + gợi ý VIZ (bar/line)
 ─> citation: "số từ bảng fact_sales, định nghĩa revenue = ..."
```
→ LLM **không tự tính**, không viết SQL thô tự do → chỉ **chọn** metric/dim đã định nghĩa → an toàn + nhất quán.

## ⭐ Conversational analytics (follow-up + ngữ cảnh)
BI là hội thoại, không phải 1 câu:
```
U: "doanh thu Q3?"              -> 1.2 tỷ
U: "theo vùng?"                 <- "theo vùng" của CÁI GÌ? -> phải nhớ "doanh thu Q3"
U: "còn Q2?"                    <- so sánh -> nhớ context
```
- Cần **memory hội thoại** ([[ab03-context-engineering]], [[ag07-conversational-memory]]) để giải "theo vùng"/"còn Q2" → câu standalone ([[ae06-query-understanding]] coreference).
- State: metric/filter đang xét → follow-up kế thừa, chỉ đổi phần được nhắc.

## ⭐ Trả lời tốt = SỐ + giải thích + viz
| Thành phần | Vì sao |
|-----------|--------|
| **Số chính xác** | từ engine, không LLM tính |
| **Giải thích** | "tăng 15% so Q2, chủ yếu vùng Bắc" → ngữ cảnh |
| **Viz gợi ý** | so kỳ → line; theo nhóm → bar; tỉ trọng → pie |
| **Citation** | nguồn bảng + định nghĩa metric → kiểm chứng |

## Snippet (luồng NL→metric, không SQL thô)
```python
q = "doanh thu Q3 theo vùng"
spec = llm_map_to_semantic(q, catalog)   # {metric:"revenue", dims:["region"], filter:{quarter:"Q3"}}
validate(spec, catalog)                   # metric/dim có thật? ([[ai06-llm-output-governance]])
sql = semantic_layer.compile(spec)        # -> SQL chuẩn, định nghĩa revenue đã test
rows = engine.run(sql)                     # SỐ chính xác
answer = llm_explain(rows, q)              # diễn giải + gợi ý viz
```

## Cạm bẫy
- **Để LLM tự tính số** → sai → luôn chạy trên engine.
- **SQL thô tự do** → sai metric + nguy hiểm → semantic layer ([[ab04-semantic-layer-llm]]).
- **Quên ngữ cảnh follow-up** → "theo vùng" vô nghĩa → memory + coreference.
- **Không citation** → không kiểm chứng số → ghi nguồn + định nghĩa.
- **Định nghĩa metric mơ hồ** (revenue?) → mỗi lần một số → semantic layer định nghĩa 1 nơi.
- **Hallucinate insight** ("tăng vì marketing") khi data không nói → chỉ diễn giải từ SỐ có thật.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao BI khó hơn RAG text (sai số = mất niềm tin).
- [ ] 3 mảnh: RAG metadata + semantic layer + engine; LLM không tự tính.
- [ ] Conversational: memory + coreference cho follow-up.
- [ ] Trả lời = số + giải thích + viz + citation.
- [ ] Cạm bẫy: LLM tính số, SQL thô, hallucinate insight.
- 🔭 Tự mò: mở rộng `text_to_sql.py` thành "BI chat": định nghĩa 3 metric + 2 dim (semantic model nhỏ [[ab04-semantic-layer-llm]]); cho mock-LLM map câu hỏi → spec JSON → validate → compile SQL → chạy trên `warehouse/star.duckdb`; thêm 1 follow-up ("theo category?") kế thừa metric trước.

➡️ Tiếp [[ag02-hallucination-detection]] — phát hiện bịa (chạy được).
