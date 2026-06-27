# AK01 — Case Study: E-commerce AI Platform

> Thiết kế nền AI cho thương mại điện tử: search + reco + review + chatbot + sinh mô tả. Nhấn: **scale catalog lớn**, real-time tồn kho/giá, đa ngữ, cold-start. Khung 7 bước ([[af09-ai-review6]]). Liên hệ [[ac02-recsys-llm]], [[ae04-multimodal-rag]].

## 1. Làm rõ yêu cầu
- **Mục tiêu**: tăng chuyển đổi (tìm đúng, gợi đúng, tin tưởng) + giảm chi phí support.
- **Quy mô**: triệu sản phẩm, triệu user, traffic cao, catalog đổi liên tục (giá/tồn kho/sản phẩm mới).
- **Ràng buộc**: latency thấp (search/reco real-time), đa ngữ (chợ đa quốc gia), cold-start (sản phẩm/user mới).

## 2. ⭐ Các thành phần AI (mỗi cái 1 mảnh đã học)
| Thành phần | Kỹ thuật | Note |
|-----------|----------|------|
| **Product search** | hybrid (vector ngữ nghĩa + keyword) + ảnh | [[aa03-rag-production]], [[ae04-multimodal-rag]] |
| **Recommendation** | two-tower embedding + LLM re-rank | [[ac02-recsys-llm]], [[af08-case-personalization]] |
| **Review summarization** | LLM tóm tắt + trích sentiment | [[ai06-llm-output-governance]] |
| **Shopping chatbot** | RAG (sản phẩm + chính sách) + tool (tồn kho/giá) | [[ad05-structured-rag]] |
| **Sinh mô tả/SEO** | LLM sinh từ thuộc tính + validate | [[ai06-llm-output-governance]] |

## 3. ⭐ Kiến trúc
```
catalog (sản phẩm + thuộc tính + ảnh) ─stream─> [embed text+ảnh] -> vector store
   ─> real-time: giá/tồn kho đổi -> cập nhật metadata (filter) ([[af08-case-personalization]])
user hành vi ─stream─> profile (real-time + lịch sử)
truy vấn/duyệt ─> search/reco (ANN + filter tồn-kho/giá) -> rerank -> LLM (giải thích/chatbot)
   ─> filter: còn hàng? đúng vùng? đúng ngân sách? (pre-filter [[ab07-vector-search-opt]])
```

## 4. ⭐ Thách thức đặc thù e-commerce
| Thách thức | Giải |
|-----------|------|
| **Real-time tồn kho/giá** | metadata cập nhật streaming; filter "còn hàng" lúc retrieve (đừng gợi hàng hết) |
| **Cold-start sản phẩm mới** | content embedding (thuộc tính/ảnh) gợi được ngay, không chờ tương tác ([[ac02-recsys-llm]]) |
| **Catalog đa ngữ** | embedding đa ngữ ([[ac01-multilingual-rag]]); 1 sản phẩm nhiều ngôn ngữ |
| **Long-tail** | sản phẩm hiếm ít data → content-based + search tốt |
| **Mùa vụ/drift** | hành vi đổi theo mùa → drift detection ([[ag04-drift-detection]]) |
| **Gian lận review** | review giả → lọc ([[ae03-training-data-quality]]) trước tóm tắt |

## 5. Eval & cost
- **Eval kinh doanh**: CTR, conversion, GMV (không chỉ recall) — A/B test ([[ac03-eval-driven-dev]]).
- **Cost**: traffic cao → semantic cache câu hỏi lặp ([[ad08-semantic-cache]]), reco pre-compute, LLM chỉ cho chatbot/sinh mô tả ([[ac08-ai-cost-scale]]).
- Filter bubble → thêm đa dạng/khám phá ([[ae07-reranking-deep]] MMR).

## Cạm bẫy
- **Gợi hàng hết kho/giá sai** → filter real-time lúc retrieve, không chỉ lúc index.
- **Cold-start kém** → sản phẩm mới vô hình → content embedding.
- **Search chỉ keyword** → trượt ý nghĩa ("áo ấm mùa đông") → hybrid.
- **Tóm tắt review bịa** → mất tin → grounding + validate; lọc review giả trước.
- **Sinh mô tả sai thuộc tính** → khiếu nại → validate output theo thuộc tính thật.
- **Đo recall không đo conversion** → tối ưu sai mục tiêu → metric kinh doanh.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 5 thành phần AI e-commerce + kỹ thuật mỗi cái.
- [ ] Kiến trúc: catalog stream → embed → search/reco + filter real-time.
- [ ] Thách thức: tồn kho real-time, cold-start, đa ngữ, long-tail, drift.
- [ ] Eval kinh doanh (CTR/conversion) + cost (cache/pre-compute).
- [ ] Cạm bẫy: gợi hàng hết, tóm tắt review bịa, sinh mô tả sai.
- 🔭 Tự mò: mở rộng `semantic_recsys.py` ([[ac02-recsys-llm]]) — thêm metadata `in_stock` + `price` cho mỗi "sản phẩm", filter loại hàng hết kho + ngoài ngân sách TRƯỚC khi gợi ý; thêm 1 sản phẩm "mới" chỉ có mô tả (cold-start) xem có lọt gợi ý không.

➡️ Tiếp [[ak02-case-legal-ai]] — case study pháp lý.
