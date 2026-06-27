# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 13 script).

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt** (nhắm 3–4/lượt) giữ chất lượng. Mỗi task = 1 note đầy đủ tiếng Việt trong `notes/advanced/` (khái niệm + "tại sao" + sơ đồ + snippet + cạm bẫy + checklist + "tự mò"). **Task có code: viết + CHẠY THỬ verify rồi mới tick.**
3. Mỗi task xong: `[ ]`→`[x]` + dòng vào `PROGRESS.md`.
4. **Cuối lượt: commit + push** (KHÔNG Claude/co-author):
   ```
   git add -A && git commit -m "<mô tả ngắn>" && git push
   ```
   Commit message TUYỆT ĐỐI không có "Co-Authored-By"/"Generated with Claude". Push lỗi → commit local, lượt sau push.
5. **Khi tất cả `[x]`**: sinh batch AI tiếp (vẫn AI/LLM — user ưu tiên). Cập nhật `00-INDEX.md`. Giữ PROTOCOL.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp note đã có.

**Batch hiện tại:** #28 — AI-Advanced 5 (self-correcting RAG, GraphRAG, data quality, multimodal sâu) ⭐
**Nguồn:** đào sâu AI/LLM (tiếp)

---

## BATCH HIỆN TẠI

### [x] AE01 — Self-Correcting / Self-Improving RAG ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ae01-self-correcting-rag.md` + code `self_correcting_rag.py`. RAG tự đánh giá retrieval: điểm thấp/không tự tin → **reformulate query** (mở rộng/đổi từ/HyDE-style) → retry → giữ kết quả tốt hơn. Vòng lặp self-correction; khi nào dừng. Code: query yếu (score thấp) → tự viết lại → đo retrieval cải thiện trên rag.duckdb. Liên hệ [[aa03-rag-production]], [[aa05-agentic-pipelines]].

### [x] AE02 — GraphRAG từ Wikilinks ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ae02-graphrag-build.md` + code `graphrag_links.py`. Dựng **knowledge graph THẬT** từ `[[links]]` giữa các note → multi-hop traversal + vector hybrid. Trả lời câu cần "đi qua nhiều bước" (note A liên quan B liên quan C). Code: parse `[[...]]` trong notes/advanced → graph (dict adjacency), BFS multi-hop + kết hợp vector retrieve. Sâu hơn [[aa09-graphrag]].

### [x] AE03 — Data Quality cho LLM Training Data ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ae03-training-data-quality.md` + code `data_quality_score.py`. Chấm CHẤT LƯỢNG dataset train: chiều đo (độ dài, trùng lặp, đa dạng, ngôn ngữ, toxic-flag heuristic, format-valid), quality score tổng hợp, lọc theo ngưỡng. Code: chấm 1 tập mẫu (tốt + xấu trộn), in điểm từng chiều + quyết định giữ/bỏ. Liên hệ [[aa04-training-data-prep]], [[ab01-synthetic-data]], [[ab08-finetune-pipeline]].

### [ ] AE04 — Multimodal RAG sâu (ảnh + text)
- **Note:** `notes/advanced/ae04-multimodal-rag.md`. Sâu hơn [[aa08-multimodal]]: shared embedding space (CLIP), cross-modal retrieval (text→ảnh, ảnh→text), multimodal chunking (ảnh+caption), khi nào OCR vs visual embedding, pipeline data ảnh (object store, cost, incremental). Liên hệ [[ad06-doc-parsing]], [[ac05-voice-audio-pipeline]].

### [ ] AE05 — On-device / Edge AI Data
- **Note:** `notes/advanced/ae05-edge-ai-data.md`. AI chạy trên thiết bị (điện thoại/IoT): model lượng tử hoá nhỏ, local embedding (như fastembed!), vì sao (privacy/latency/offline/cost), thách thức data (sync, eval phân tán, model update OTA), federated learning (khái niệm). Liên hệ [[ad03-privacy-compliance]], [[c04-case-iot]].

### [ ] AE06 — Query Understanding & Routing
- **Note:** `notes/advanced/ae06-query-understanding.md`. Trước retrieval: hiểu câu hỏi → intent classification, query rewriting (chính tả/đồng nghĩa/mở rộng), query decomposition (câu phức → nhiều câu con), routing (RAG vs SQL vs cache vs từ chối). "Hỏi đúng mới tìm đúng". Liên hệ [[ad05-structured-rag]], [[ae01-self-correcting-rag]].

### [ ] AE07 — Reranking sâu
- **Note:** `notes/advanced/ae07-reranking-deep.md`. Sâu về rerank: bi-encoder (nhanh, retrieve) vs cross-encoder (chậm, chính xác, rerank top-N), ColBERT (late interaction), LLM-rerank, MMR (đa dạng chống trùng); trade-off recall→precision, latency/cost. Vì sao 2 tầng (retrieve rộng → rerank tinh). Liên hệ [[ab07-vector-search-opt]], [[ab02-rag-eval-harness]].

### [ ] AE08 — RAG cho Code (code search & repo context)
- **Note:** `notes/advanced/ae08-rag-for-code.md`. RAG trên codebase: chunk theo AST/hàm (không cắt giữa hàm), embedding cho code, repo-level context (import/call graph), khác text RAG (cú pháp, định danh, ngữ cảnh xa); ứng dụng (code assistant, search). Liên hệ [[ad06-doc-parsing]], [[ai03-chunking]].

### [ ] AE09 — AI review 5 + final portfolio & career
- **Note:** `notes/advanced/ae09-ai-review5.md` + cập nhật `00-INDEX.md`. Tổng kết AI-Advanced 5; **portfolio AI-DE hoàn chỉnh** (13+ script → kể chuyện), lộ trình học tiếp, định vị career "AI Data Engineer", tổng kết 5 batch Module AI.

---
*Hết batch → sinh batch AI tiếp (RAG benchmark tự động, LLM data pipeline ở scale petabyte, vector DB internals, AI data governance, real-world case studies AI-DE...) — vẫn ưu tiên AI/LLM.*
