# AF03 — Case Study: AI Coding Assistant Data Platform

> Thiết kế nền **data** cho code assistant (Copilot-style) ở repo scale: index nghìn repo, incremental theo commit, repo-context, latency thấp, code là tài sản nhạy cảm. Liên hệ [[ae08-rag-for-code]], [[ad01-streaming-rag]], [[ae02-graphrag-build]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: gợi ý/giải thích code dựa trên **codebase của tổ chức** (không chỉ kiến thức chung của model).
- **Quy mô**: nghìn repo, triệu file, commit liên tục (mỗi phút).
- **Ràng buộc**: latency rất thấp (gợi ý khi gõ), code = **tài sản** (không rò ra ngoài/giữa team không phép), incremental (không re-index cả repo mỗi commit).
- **Thước đo**: acceptance rate (gợi ý được chấp nhận), latency p99, coverage repo.

## 2. ⭐ Kiến trúc
```
repos (git) ──[webhook commit]──> [diff: file nào đổi]
   ─> parse AST mỗi file đổi ([[ae08-rag-for-code]]) ─> chunk theo HÀM/class
   ─> embed (code model) ─> upsert vector store (INCREMENTAL theo file [[ad01-streaming-rag]])
   ─> build/update graph: import/call/def ([[ae02-graphrag-build]])
IDE (đang gõ) ─> context hiện tại (file, hàm, cursor)
   ─> retrieve: hàm liên quan (vector) + phụ thuộc (graph) + cùng repo (filter)
   ─> rerank ([[ae07-reranking-deep]]) ─> ghép context ─> LLM gợi ý
```

## 3. ⭐ Incremental theo commit (sống còn ở scale)
Re-index cả repo mỗi commit = bất khả thi (nghìn repo × commit/phút):
```
commit ─> git diff ─> CHỈ file thay đổi ─> re-chunk + re-embed file đó
   ─> xoá chunk của hàm bị xoá (reconcile [[ac06-kb-freshness]])
   ─> cập nhật cạnh graph liên quan
```
→ Đúng tư duy **content-hash/CDC incremental** ([[ad01-streaming-rag]]) áp cho code. Chi phí ∝ thay đổi, không ∝ tổng repo.

## 4. ⭐ Repo-context (khác biệt chính so với RAG text)
Gợi ý code tốt cần **ngữ cảnh phụ thuộc**, không chỉ "đoạn giống":
| Nguồn context | Dùng để |
|---------------|---------|
| File hiện tại + cursor | hiểu đang viết gì |
| Import của file | kéo định nghĩa được dùng |
| Call graph | hàm gọi/bị gọi liên quan ([[ae02-graphrag-build]]) |
| Hàm tương tự trong repo | ví dụ pattern của team |
| Type/class định nghĩa | hiểu kiểu dữ liệu |
→ Ghép **vector (giống) + graph (phụ thuộc) + cùng-repo filter** → context giàu mà đúng phạm vi.

## 5. ⭐ Privacy: code là tài sản
- **Cách ly theo tổ chức/repo**: assistant của công ty A **không** học/gợi code công ty B ([[ad03-privacy-compliance]] multi-tenancy).
- **Quyền theo repo**: dev chỉ lấy context từ repo họ có quyền ([[af02-case-enterprise-kb]] permission-aware).
- **Self-host/VPC**: nhiều tổ chức không cho code ra API ngoài → embedding/inference local ([[ae05-edge-ai-data]]).
- Không log code thô ra nơi không kiểm soát.

## 6. Latency (gợi ý real-time)
- Vector pre-computed + ANN nhanh ([[ab07-vector-search-opt]]); cache embedding file mở.
- Giới hạn context (token budget [[ab03-context-engineering]]) → rerank chọn ít-mà-đúng.
- Model nhỏ/nhanh cho gợi ý inline; model lớn cho yêu cầu phức tạp (routing [[ac08-ai-cost-scale]]).

## Cạm bẫy
- **Re-index cả repo mỗi commit** → sập ở scale → incremental theo diff.
- **Chunk theo size** (cắt giữa hàm) → context vô nghĩa → AST chunk ([[ae08-rag-for-code]]).
- **Bỏ repo-context** → gợi ý không khớp codebase team → import/call graph.
- **Rò code giữa tenant** → vi phạm tài sản → cách ly cứng.
- **Latency cao** → dev tắt assistant → pre-compute + cache + model nhỏ.
- **Quên xoá chunk hàm đã xoá** → gợi ý code không còn tồn tại → reconcile.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Kiến trúc: webhook commit → incremental AST chunk → vector + graph.
- [ ] Incremental theo diff (chi phí ∝ thay đổi).
- [ ] Repo-context = vector + graph (import/call) + cùng-repo filter.
- [ ] Privacy: cách ly tenant, quyền repo, self-host.
- [ ] Latency: pre-compute, cache, model nhỏ, token budget.
- 🔭 Tự mò: dùng `ast` parse các script trong `projects/06-ai-data-engineering/`, chunk theo `FunctionDef`, build "call graph" đơn giản (hàm nào gọi hàm nào), embed mỗi hàm; query "hàm build index" → retrieve + graph-expand các hàm nó gọi → context kiểu coding-assistant.

➡️ Tiếp [[af04-vector-db-internals]] — bên trong vector DB.
