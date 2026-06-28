# AN07 — AI-DE Mock Interview 3 (đề + lời giải đầy đủ)

> Mock 3: system-design **multimodal ở scale** + khái niệm kỹ thuật sâu + behavioral. Kèm lời giải + thang chấm. Liên hệ [[am03-advanced-chunking]], [[am04-hybrid-fusion]], [[al06-mock-interview-2]].

---
## 🎯 Phần 1 — System Design (35 phút)
**Đề:** "Thiết kế hệ tìm kiếm + kiểm duyệt nội dung cho nền tảng chia sẻ ảnh/video: triệu nội dung mới/ngày, người dùng search bằng text, nội dung phải an toàn. Vẽ kiến trúc."

**Lời giải mẫu** (khung 7 bước [[af09-ai-review6]], nhấn multimodal + scale + safety):
1. **Clarify**: loại nội dung (ảnh/video), search bằng gì (text→ảnh), "an toàn" = gì (NSFW/harm/bản quyền), quy mô (triệu/ngày), latency search.
2. **Data flow (ingest)**: upload → transcode + **frame sampling** (video [[ag06-multimodal-production]]) → embed visual (CLIP) + STT audio + OCR → index; object store + CDN.
3. **Search**: cross-modal (text→ảnh, shared embedding [[ae04-multimodal-rag]]) + filter + **rerank** ([[ae07-reranking-deep]]); hybrid ([[am04-hybrid-fusion]]).
4. **Moderation (safety)**: tier-1 model nhanh lọc rõ vi phạm → tier-2 / **human queue** ([[an06-case-social-ai]]); multimodal + recall an toàn cao.
5. **Eval**: search recall + moderation recall/precision (bỏ sót harm = tệ); fairness ([[ak04-case-govt-ai]]).
6. **Scale**: vector DB + quantization ([[aj04-nextgen-vector]]); incremental ([[ad01-streaming-rag]]); **cost GPU video** lớn nhất → frame sampling + tiering + batch.
7. **Cost**: GPU batch giờ thấp điểm, cache embedding, model nhỏ tier-1.

**Thang chấm:** ⭐ nhận ra **frame sampling** (không xử lý mọi frame) + **moderation tầng** (AI lọc + human) + **cost GPU là nghẽn** = pass. Quên cost video / xử lý mọi frame = fail (scale sẽ sập).

---
## 🎯 Phần 2 — Câu hỏi kỹ thuật sâu (20 phút)

**Q1. Chunk thế nào cho RAG tốt? Có chiến lược nào hơn fixed-size?**
> Fixed-size cắt giữa ý → structure-aware (heading), semantic (cắt điểm đổi nghĩa), **parent-child** (nhỏ tìm, to trả — mặc định tốt), late chunking (embed cả doc rồi cắt) ([[am03-advanced-chunking]]). Chọn theo loại doc; code theo AST.

**Q2. Kết hợp vector + keyword sao cho đúng?**
> Khác thang điểm (cosine vs BM25) → không cộng thẳng. **RRF** (gộp thứ hạng, không cần chuẩn hoá) robust hơn weighted; đo thật thấy weighted thêm keyword có thể TỤT, RRF giữ vững ([[am04-hybrid-fusion]]). Weighted khi cần tune α (đã chuẩn hoá).

**Q3. Hệ AI "im lặng hỏng" — phát hiện?**
> Drift: input drift (centroid embedding dịch [[ag04-drift-detection]]), quality drift (eval tụt [[af07-continuous-eval]]). Không exception → chủ động đo + alert + playbook (re-eval/re-index).

**Q4. Cost AI ở scale — tối ưu?**
> Routing/cascade (model nhỏ trước), cache nhiều tầng ([[ad08-semantic-cache]]), nén prompt, batch, frame sampling (video), quantize. Đo $/query + budget cap ([[ac08-ai-cost-scale]]). Đo đừng tin mặc định (thêm tín hiệu không luôn tốt).

---
## 🎯 Phần 3 — Behavioral (10 phút)
**Đề:** "Kể về lần bạn phải đơn giản hoá một giải pháp phức tạp."
> **STAR mẫu**: *S* — định dùng multi-agent cho 1 task. *T* — nhưng phức tạp + đắt + khó debug. *A* — nhận ra **1 agent ReAct + tool tốt là đủ** ([[an02-agentic-patterns]]); bỏ multi-agent. *R* — đơn giản hơn, rẻ hơn, dễ debug, chất lượng tương đương. *Bài học*: đừng phức tạp hoá vì "ngầu"; đơn giản nhất mà đủ.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Giải system-design multimodal 35', nhấn frame-sampling + cost + moderation tầng.
- [ ] Trả 4 câu kỹ thuật sâu (chunk/fusion/drift/cost).
- [ ] Kể STAR về đơn giản hoá.
- 🔭 Tự mò: với đề multimodal, ước cost: triệu video/ngày × N frame/video × $embed/frame → thấy frame sampling giảm cost bao nhiêu lần; đó là phép tính interviewer thích nghe.

➡️ Tiếp [[an08-coding-exercises-4]] — bài tập router/agent/data.
