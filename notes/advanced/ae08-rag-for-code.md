# AE08 — RAG cho Code (code search & repo context)

> RAG trên **codebase** (code assistant, code search): chunk theo cấu trúc cú pháp (AST/hàm), embedding hiểu code, ngữ cảnh cấp-repo (import/call graph). Khác text RAG ở nhiều điểm cốt lõi. Liên hệ [[ad06-doc-parsing]], [[ai03-chunking]], [[ae02-graphrag-build]].

## Vì sao code khác text (không thể RAG y như văn bản)
| Đặc điểm code | Hệ quả |
|---------------|--------|
| **Cú pháp/cấu trúc** (hàm, class, block) | chunk phải theo ranh giới cú pháp, không cắt giữa hàm |
| **Định danh** (tên biến/hàm) quan trọng | tên `calc_tax` mang nghĩa; matching tên quan trọng hơn văn xuôi |
| **Ngữ cảnh xa** | hàm dùng biến/import định nghĩa ở file khác → context phân tán |
| **Trùng lặp cao** | boilerplate, pattern lặp → near-dup nhiều |
| **Đa ngôn ngữ** | Python/JS/SQL... mỗi cú pháp khác |
→ Chunk + embed + retrieve đều phải **điều chỉnh cho code**.

## ⭐ Chunking theo AST/cú pháp (không cắt giữa hàm)
```
SAI (cắt theo size):              ĐÚNG (cắt theo cấu trúc):
  def foo():                        [chunk] = trọn def foo(): ... (cả thân hàm)
    x = 1                           [chunk] = trọn class Bar: ...
  --- cắt giữa ---                  [chunk] = trọn block logic
    return x   <- mất nửa hàm
```
- Parse **AST** (cây cú pháp) → chunk theo hàm/class/method → mỗi chunk là đơn vị **hoàn chỉnh, có nghĩa**.
- Giữ **metadata**: file, tên hàm, ngôn ngữ, dòng → citation + điều hướng ([[ad06-doc-parsing]]).
- Hàm quá dài → tách theo block logic; quá ngắn → gộp với ngữ cảnh (docstring, signature).

## ⭐ Embedding cho code
- Model **chuyên code** (CodeBERT, jina-code, voyage-code) hiểu cú pháp/định danh tốt hơn model text thường.
- Embed kèm **ngữ cảnh**: signature + docstring + tên file → vector giàu nghĩa hơn chỉ thân hàm.
- Hybrid **đặc biệt quan trọng**: keyword match tên hàm/biến chính xác ([[aa03-rag-production]]) — vector dễ trượt định danh hiếm.

## ⭐ Repo-level context (ngữ cảnh xa — khó nhất)
Code hiểu được cần biết **quan hệ giữa các phần**, không chỉ đoạn lẻ:
```
import graph:   file A import B -> hiểu A cần kéo B
call graph:     foo() gọi bar() gọi baz() -> trace luồng (multi-hop [[ae02-graphrag-build]])
type/def:       biến kiểu User -> kéo định nghĩa class User
```
→ Đây là **GraphRAG cho code**: graph = import/call/inheritance → retrieve không chỉ "đoạn giống" mà cả "đoạn liên quan theo cấu trúc". Kết hợp vector (giống nghĩa) + graph (phụ thuộc).

## Pipeline RAG-for-code
```
repo ─> [parse AST mỗi file] -> chunk theo hàm/class + metadata
    ─> [build graph] import/call/def (cho repo-context)
    ─> [embed code model] + index (hybrid vector+keyword)
query (NL hoặc code) ─> retrieve hàm liên quan + graph-expand phụ thuộc
    ─> rerank ([[ae07-reranking-deep]]) ─> đưa LLM (code assistant)
    incremental: file đổi -> re-chunk/re-embed CHỈ file đó ([[ad01-streaming-rag]])
```

## Ứng dụng
- **Code assistant** (Copilot-style): kéo hàm/ví dụ liên quan vào context khi gợi ý.
- **Code search** ngữ nghĩa: "hàm nào xử lý thanh toán" → tìm theo nghĩa, không chỉ grep.
- **Onboarding/Q&A repo**: "luồng đăng nhập đi qua file nào" → graph + vector.
- **Migration/refactor**: tìm mọi chỗ dùng pattern X.

## Cạm bẫy
- **Chunk theo size** (cắt giữa hàm) → chunk vô nghĩa → chunk theo AST.
- **Model text cho code** → kém hiểu cú pháp/định danh → model chuyên code.
- **Chỉ vector, bỏ keyword** → trượt tên hàm/biến chính xác → hybrid bắt buộc.
- **Bỏ repo-context** → đoạn lẻ thiếu phụ thuộc → import/call graph.
- **Re-index cả repo mỗi commit** → tốn → incremental theo file đổi ([[ad01-streaming-rag]]).
- **Quên near-dup** (boilerplate) → context lặp → dedup ([[aa04-training-data-prep]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Code khác text ở đâu (cú pháp/định danh/ngữ cảnh xa/trùng lặp).
- [ ] Chunk theo AST/hàm, không cắt giữa hàm + metadata.
- [ ] Embedding code chuyên + hybrid (keyword cho định danh).
- [ ] Repo-context = GraphRAG (import/call graph) cho phụ thuộc xa.
- [ ] Pipeline + incremental theo file; ứng dụng (assistant/search/onboarding).
- 🔭 Tự mò: chunk chính các script trong `projects/06-ai-data-engineering/` theo **hàm** (parse bằng `ast` của Python — `ast.FunctionDef`), embed mỗi hàm bằng `rag_over_notes.embed`, thử query "hàm nào tính cosine" / "hàm nào build index" → xem code search ngữ nghĩa hoạt động.

➡️ Tiếp [[ae09-ai-review5]] — review 5 + portfolio.
