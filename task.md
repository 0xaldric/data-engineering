# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, **MAX OUTPUT**). Notes trong `notes/advanced/`.
> 🔥 **ƯU TIÊN AI/LLM** (user yêu cầu đẩy mạnh). **ĐƯỢC viết code chạy được** (local fastembed/DuckDB/pydantic, KHÔNG API key). Project: `projects/06-ai-data-engineering/` (đã có 22 script).

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

**Batch hiện tại:** #33 — AI-Advanced 10: Vertical AI Case Studies ⭐
**Nguồn:** đào sâu AI/LLM — system design theo ngành

---

## BATCH HIỆN TẠI

### [x] AK01 — Case Study: E-commerce AI Platform
- **Note:** `notes/advanced/ak01-case-ecommerce-ai.md`. AI cho thương mại điện tử: product search ngữ nghĩa + ảnh ([[ae04-multimodal-rag]]), reco ([[ac02-recsys-llm]]), tóm tắt review, chatbot mua hàng, tạo mô tả sản phẩm. Nhấn: scale catalog lớn, real-time tồn kho/giá ([[af08-case-personalization]]), đa ngữ ([[ac01-multilingual-rag]]), cold-start sản phẩm mới. Khung 7 bước ([[af09-ai-review6]]).

### [x] AK02 — Case Study: Legal AI Platform
- **Note:** `notes/advanced/ak02-case-legal-ai.md`. AI cho pháp lý: phân tích hợp đồng, RAG case law/luật, citation BẮT BUỘC (trích điều luật thật, không bịa — [[ag02-hallucination-detection]]), privilege/bảo mật, audit. Nhấn: grounding + citation chính xác tuyệt đối, privacy tài liệu, human (luật sư) quyết. Tương tự y tế ([[aj05-case-healthcare-ai]]) về độ gắt.

### [x] AK03 — Case Study: Education AI Platform
- **Note:** `notes/advanced/ak03-case-education-ai.md`. AI giáo dục: gia sư cá nhân hoá, sinh nội dung/câu hỏi, chấm bài tự động + feedback, theo dõi tiến độ. Nhấn: personalization ([[af08-case-personalization]]), eval chất lượng sư phạm, an toàn trẻ em ([[aj02-ai-alignment]]), chống gian lận, đa trình độ. Data flywheel từ tương tác học ([[aj07-data-flywheel]]).

### [x] AK04 — Case Study: Government/Public Service AI
- **Note:** `notes/advanced/ak04-case-govt-ai.md`. AI dịch vụ công: trợ lý thủ tục hành chính, RAG văn bản pháp quy, đa ngữ/dân tộc, accessibility, minh bạch (giải trình quyết định công), công bằng (không thiên lệch nhóm — [[af06-ai-data-governance]]). Nhấn: transparency + fairness + privacy công dân + độ phủ ngôn ngữ.

### [x] AK05 — Case Study: Manufacturing/IoT AI
- **Note:** `notes/advanced/ak05-case-manufacturing-ai.md`. AI sản xuất/IoT: predictive maintenance (sensor + LLM giải thích), anomaly detection, RAG tài liệu kỹ thuật/máy, edge AI ([[ae05-edge-ai-data]]), digital twin. Nhấn: time-series sensor scale lớn ([[c04-case-iot]]), real-time edge, LLM bổ trợ chẩn đoán không tự dừng máy.

### [ ] AK06 — Data Labeling & Annotation Infrastructure ⭐ (CHẠY ĐƯỢC)
- **Note:** `notes/advanced/ak06-data-labeling.md` + code `annotation_agreement.py`. Hạ tầng gán nhãn (con người + AI): inter-annotator agreement (Cohen's kappa), gold questions, guideline, active learning (chọn mẫu đáng gán nhất), weak supervision, AI pre-label + human verify. Code: tính kappa giữa 2-3 annotator trên mẫu giả, phát hiện annotator lệch. Liên hệ [[ag03-rlhf-preference-data]], [[ae03-training-data-quality]].

### [ ] AK07 — Knowledge Graph Construction với LLM
- **Note:** `notes/advanced/ak07-kg-construction.md`. Dựng KG từ text bằng LLM: trích entity + relation (triple), entity resolution (gộp trùng), ontology/schema, validate triple, KG + vector hybrid ([[ae02-graphrag-build]]). Sâu hơn [[aa09-graphrag]] (dùng) → đây là XÂY KG. Vai trò DE: pipeline trích → resolve → store → query.

### [ ] AK08 — Time-series & Tabular Foundation Models
- **Note:** `notes/advanced/ak08-timeseries-tabular-fm.md`. Foundation model cho dữ liệu CÓ CẤU TRÚC (không phải text): time-series FM (TimeGPT/Chronos — forecast zero-shot), tabular FM (TabPFN), LLM cho tabular (serialize bảng → text), khi nào FM vs model truyền thống. Data đặc thù (chuỗi/bảng). Liên hệ [[ac07-feature-store]], [[c04-case-iot]].

### [ ] AK09 — AI review 10 + tổng kết vertical
- **Note:** `notes/advanced/ak09-ai-review10.md` + cập nhật `00-INDEX.md`. Tổng kết vertical case studies; bảng "ngành → nhấn gì → kỹ thuật"; pattern chung vs đặc thù ngành; tổng kết 10 batch Module AI.

---
*Hết batch → sinh batch AI tiếp (đào sâu trục yếu, case study ngành mới, hoặc chủ đề kỹ thuật mới) — vẫn ưu tiên AI/LLM.*
