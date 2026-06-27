# AE07 — Reranking sâu

> Retrieve **rộng** (nhanh, recall cao) rồi rerank **tinh** (chậm, chính xác) top-N → cải thiện **thứ hạng** (precision/MRR/nDCG) mà tăng k không làm được. Kiến trúc 2 tầng kinh điển của search/RAG. Liên hệ [[ab07-vector-search-opt]], [[ab02-rag-eval-harness]], [[aa03-rag-production]].

## Vì sao cần tầng rerank (đã thấy ở [[ab02-rag-eval-harness]])
- Tăng k → recall↑ (62→100%) nhưng **MRR gần như đứng yên** (0.479→0.556): doc đúng *có mặt* nhưng *không lên hạng*.
- Bi-encoder (vector search) **nhanh nhưng thô**: embed query và doc **riêng rẽ** → mất tương tác chi tiết.
- → Tầng 2 **rerank**: chấm lại top-N kỹ hơn → đẩy doc đúng lên #1.

## ⭐ Kiến trúc 2 tầng (retrieve → rerank)
```
query ─> [Tầng 1: RETRIEVE] bi-encoder + ANN, lấy top-50  (nhanh, recall cao, thô)
      ─> [Tầng 2: RERANK]  cross-encoder chấm 50 cặp,    (chậm, chính xác)
                            sắp lại -> top-5 đưa LLM
```
- Tầng 1 quét **triệu doc** → phải nhanh (ANN [[ab07-vector-search-opt]]).
- Tầng 2 chỉ chấm **50 doc** → được phép chậm/kỹ.
- → Cân **recall (tầng 1) × precision (tầng 2)**: lấy rộng để không bỏ sót, lọc tinh để đúng top.

## ⭐ Bi-encoder vs Cross-encoder (mấu chốt)
```
BI-ENCODER (retrieve):                CROSS-ENCODER (rerank):
  query ─embed─> vq                     [query + doc] ─> 1 model ─> điểm liên quan
  doc   ─embed─> vd  (RIÊNG rẽ)         (đọc CẶP cùng lúc -> tương tác sâu)
  score = cosine(vq, vd)
  + nhanh (embed doc TRƯỚC, index)       + chính xác hơn nhiều
  - thô (không thấy tương tác q×d)        - chậm (phải chạy model mỗi cặp, không cache được)
```
→ Bi-encoder để **lọc nhanh** từ triệu xuống 50; cross-encoder để **xếp đúng** 50 đó. Không dùng cross-encoder cho cả triệu (quá chậm).

## Các kiểu rerank
| Kiểu | Cách | Đặc điểm |
|------|------|----------|
| **Cross-encoder** | model chấm cặp (query, doc) | chính xác, phổ biến (bge-reranker, Cohere rerank) |
| **ColBERT** (late interaction) | embed token-level, so chi tiết hơn bi nhưng rẻ hơn cross | cân bằng tốc độ/chính xác |
| **LLM-rerank** | hỏi LLM "doc nào liên quan nhất" | mạnh nhưng đắt/chậm; bias ([[ad02-llm-judge]]) |
| **MMR** (Maximal Marginal Relevance) | cân liên quan **×** đa dạng | chống top-k trùng lặp ý |

## ⭐ MMR — chống trùng lặp (hay quên)
Top-5 mà cả 5 nói **cùng một ý** → lãng phí context. MMR chọn doc vừa **liên quan** vừa **khác** cái đã chọn:
```
chọn lần lượt: max [ λ·liên_quan(d,q) − (1−λ)·giống_nhất(d, đã_chọn) ]
λ cao -> ưu tiên liên quan ; λ thấp -> ưu tiên đa dạng
```
→ Đưa LLM 5 góc nhìn khác nhau thay vì 5 bản sao → trả lời đầy đủ hơn.

## Trade-off & khi nào dùng
- Rerank thêm **latency + cost** (chạy model mỗi cặp) → chỉ rerank top-N (20–100), không phải tất cả.
- **Đo bằng harness** ([[ab02-rag-eval-harness]]): rerank có tăng MRR/nDCG đủ bù latency không?
- Bài toán **recall đủ, hạng chưa tốt** → rerank đáng giá nhất.
- LLM tự đọc context (RAG) → đôi khi recall@k đủ, rerank ít quan trọng hơn search-trả-người.

## Cạm bẫy
- **Tăng k thay vì rerank** → recall tăng, hạng không đổi → MRR ì → cần rerank.
- **Cross-encoder cho cả triệu doc** → quá chậm → chỉ rerank top-N sau bi-encoder.
- **Rerank mọi query** kể cả đã tốt → tốn latency thừa → chỉ khi cần.
- **Quên MMR** → top-k trùng ý → context nghèo dù "liên quan cao".
- **Không đo** → thêm rerank mà không biết có lợi → harness trước/sau.
- **LLM-rerank vô tội vạ** → đắt + bias vị trí ([[ad02-llm-judge]]) → cân nhắc cross-encoder rẻ hơn.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao cần rerank (tăng k không sửa hạng — MRR ì).
- [ ] Kiến trúc 2 tầng: retrieve rộng × rerank tinh.
- [ ] Bi-encoder (riêng rẽ, nhanh) vs cross-encoder (cặp, chính xác, chậm).
- [ ] ColBERT/LLM-rerank/MMR; MMR chống trùng lặp.
- [ ] Trade-off latency/cost; chỉ rerank top-N; đo bằng harness.
- 🔭 Tự mò: thêm rerank vào `rag_over_notes.py` — lấy top-20 bằng cosine, rerank bằng "keyword overlap + cosine" (cross-encoder giả) xuống top-5; chạy `rag_eval_harness.py` so MRR/nDCG trước/sau; thử MMR (phạt doc giống cái đã chọn) xem đa dạng top-k đổi không.

➡️ Tiếp [[ae08-rag-for-code]] — RAG cho codebase.
