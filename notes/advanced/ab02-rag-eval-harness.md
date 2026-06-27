# AB02 — RAG Eval Harness ⭐ (có code chạy được)

> Chọn cấu hình RAG (chunk size / hybrid on-off / k) bằng **SỐ**, không "vibe check". Code: [`rag_eval_harness.py`](../../projects/06-ai-data-engineering/rag_eval_harness.py). Sâu hơn [[ai05-retrieval-eval]], [[aa06-llm-eval]].

## Vì sao cần harness (không đoán)
RAG có **rất nhiều nút vặn**: chunk size, overlap, embedding model, hybrid weight, k, reranker. Đổi 1 nút → chất lượng đổi. Không đo → "tôi nghĩ nó tốt hơn" = sai lầm kinh điển. Harness = **golden set + metric + sweep cấu hình + bảng so sánh** → quyết định bằng dữ liệu (giống A/B test cho retrieval).

## Vòng đời harness
```
Golden set (query, expected_doc)  ──┐
                                    ├─> chạy retrieval mỗi config ─> metric ─> bảng so sánh ─> chọn
Configs: {chunk, hybrid?, k, ...} ──┘                                                         (rồi gate CI)
```

## ⭐ Metric retrieval (nhớ ý nghĩa, đừng học vẹt)
| Metric | Hỏi gì | Công thức (ý) |
|--------|--------|---------------|
| **recall@k** | doc đúng có nằm trong top-k không? | #query có hit / #query |
| **precision@k** | trong top-k bao nhiêu phần đúng? | #relevant trong k / k |
| **MRR** | doc đúng đứng **thứ mấy**? (hạng đầu tiên) | mean(1/rank_hit) |
| **nDCG** | xếp hạng tốt cỡ nào? (thưởng relevant ở đầu) | DCG / **IDCG** (chuẩn hoá ∈ [0,1]) |

- **recall** = "có tìm thấy không", **MRR/nDCG** = "xếp đúng vị trí không".
- ⚠️ **nDCG phải chia IDCG** (DCG lý tưởng) để ∈ [0,1]. Quên chia → ra số > 1 = sai (tôi mắc đúng lỗi này lúc viết code, sửa lại: `dcg(rels)/dcg(sorted(rels,reverse=True))`).

## Kết quả thật (sweep trên capstone, golden 8 câu)
```
config                 recall@k    MRR    nDCG
hybrid, k=3               62%     0.479   0.516
hybrid, k=5               88%     0.535   0.608
hybrid, k=10             100%     0.556   0.657
vector-only, k=5          75%     0.490   0.565
```
**Đọc bảng — 3 bài học:**
1. **k↑ → recall↑** (62→88→100%): lấy nhiều chunk hơn thì dễ trúng. Nhưng đổi lại context dài hơn, tốn token/nhiễu ([[ai08-ai-cost-latency]]).
2. **MRR gần như đứng yên** (0.479→0.556) khi k tăng: doc đúng *có mặt* nhưng *không lên hạng cao hơn* → muốn cải thiện hạng phải **rerank**, không phải tăng k.
3. **hybrid k=5 (88%) > vector-only k=5 (75%)**: lai keyword bắt được ca mà vector trượt (tên riêng, từ khoá hiếm) → bằng chứng số cho "hybrid đáng dùng".

## Chọn metric mục tiêu theo bài toán
- **RAG cho LLM đọc**: ưu tiên **recall@k** (chỉ cần doc đúng lọt vào context, LLM tự đọc).
- **Search trả người dùng**: ưu tiên **MRR/nDCG** (phải đúng ngay top-1, top-3).
- → harness cho phép tối ưu đúng cái mình cần.

## ⭐ Harness → CI gate (LLMOps)
Mỗi lần đổi prompt/chunk/model → **chạy lại harness**; nếu recall tụt quá ngưỡng → **chặn merge** (regression). Đây là cách [[aa10-llmops]] / [[aa06-llm-eval]] biến eval thành "test tự động" cho hệ phi-quyết-định ([[ai07-testing-nondeterministic]]).

## Cạm bẫy
- **Golden set quá nhỏ/lệch** → metric đẹp giả. Cần đủ lớn, đa dạng, sát truy vấn thật.
- **Leakage**: golden trùng data index một cách tầm thường → recall ảo cao.
- **Chỉ đo retrieval, quên end-to-end**: retrieval tốt nhưng answer vẫn sai (generation) → cần thêm faithfulness/answer-eval ([[aa06-llm-eval]] RAGAS).
- **Đo 1 lần rồi quên**: chất lượng drift theo thời gian (tài liệu đổi) → đo định kỳ.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Phân biệt recall@k vs MRR vs nDCG — khi nào ưu tiên cái nào.
- [ ] Vì sao nDCG phải chia IDCG.
- [ ] Đọc được bảng sweep: k↑ ảnh hưởng recall/MRR ra sao, hybrid vs vector-only.
- [ ] Harness → CI gate chống regression.
- 🔭 Tự mò: thêm config **k=20** và **hybrid weight** khác vào `rag_eval_harness.py`; thêm metric **precision@k**; thử cố tình giảm chunk size trong `rag_over_notes.py` rồi chạy lại harness xem recall đổi thế nào.

➡️ Tiếp [[ab03-context-engineering]] — quản context cho agent.
