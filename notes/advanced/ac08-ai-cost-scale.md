# AC08 — Cost Optimization sâu cho AI ở scale

> Khi traffic LLM lớn, **cost bùng nổ** (mỗi query nhiều token × triệu request). Tối ưu = routing + cascade + cache nhiều tầng + nén + distill. Quyết bằng **unit economics ($/query)**. Sâu hơn [[ai08-ai-cost-latency]], [[aa10-llmops]].

## Vì sao cost AI khác cost hạ tầng thường
- Trả theo **token** (input + output), không theo CPU-giờ → prompt phình = tiền phình.
- LLM lớn đắt gấp **10–100×** model nhỏ → chọn sai model = đốt tiền.
- Retrieval nhồi nhiều chunk → input token tăng tuyến tính ([[ab03-context-engineering]]).
- → Phải nghĩ **$/query** và tổng $/ngày, không chỉ "nó chạy được".

## ⭐ Các đòn tối ưu (từ rẻ-dễ tới khó)
| Đòn | Ý tưởng | Tiết kiệm |
|-----|---------|-----------|
| **Semantic cache** ([[aa03-rag-production]]) | câu hỏi giống đã trả → trả lại, không gọi LLM | rất lớn nếu traffic lặp |
| **Prompt compression** | bỏ token thừa, tóm context, ít chunk hơn | giảm input token mỗi call |
| **Model routing** | câu dễ → model nhỏ/rẻ; khó → model lớn | lớn (đa số câu là dễ) |
| **Cascade** | thử model nhỏ trước; không tự tin → escalate model lớn | lớn, giữ chất lượng |
| **Batching** | gộp nhiều request (nhất là embedding) | giảm overhead/đơn giá |
| **Distillation** | dùng LLM lớn dạy model nhỏ làm 1 task hẹp | rẻ + nhanh ở scale |
| **Self-host** | tự chạy model mở khi volume đủ lớn | rẻ ở scale, mất phí vận hành |

## ⭐ Model routing & cascade (đòn mạnh nhất)
```
ROUTING:  query ─> [classifier rẻ] ─> dễ? ─> model NHỎ ($)      Phần lớn traffic đi nhánh rẻ
                                    └─ khó? ─> model LỚN ($$$)

CASCADE:  query ─> model NHỎ ─> đủ tự tin / qua eval? ─> TRẢ
                                └─ không ─> model LỚN ─> TRẢ     Chỉ leo thang khi cần
```
- Đa số câu hỏi **đơn giản** → đừng dùng model đắt cho tất cả.
- Đo: % đi nhánh rẻ, chất lượng mỗi nhánh ([[ac03-eval-driven-dev]]) → cân cost vs quality.

## ⭐ Cache nhiều tầng
```
exact cache (query y hệt)      ─ hit ─> trả ngay (gần như free)
   └ miss ─> semantic cache (query gần nghĩa, cosine ≥ ngưỡng) ─ hit ─> trả
        └ miss ─> embedding cache (đừng re-embed cái đã có)
             └ miss ─> gọi LLM (đắt nhất) ─> ghi vào cache các tầng
```
- Cache **embedding** (incremental, đã làm ở capstone), cache **câu trả lời**, cache **kết quả tool** ([[ab03-context-engineering]]).
- ⚠️ Cache phải **invalidations** khi KB đổi ([[ac06-kb-freshness]]) — không trả câu cũ sai.

## ⭐ Unit economics (quyết định bằng số)
```
$/query = (input_tok × giá_in) + (output_tok × giá_out) + (embed + retrieval + hạ tầng)
$/ngày  = $/query × số query × (1 − cache_hit_rate)
```
- Tính ra **biên lợi nhuận**: nếu mỗi user trả $X mà tốn $Y/query → còn lời không?
- Dashboard cost theo model/feature/user ([[ab06-llm-observability]]) → biết đốt ở đâu.
- Đặt **budget cap + alert** (đặc biệt agent vòng lặp [[ac04-multi-agent]]).

## Quality ⇄ Cost ⇄ Latency (tam giác)
Mọi đòn cost đều đụng tam giác này — không free:
- routing model nhỏ → rẻ/nhanh nhưng có thể kém chất lượng câu khó.
- cache → rẻ/nhanh nhưng rủi ro trả đồ cũ.
- nén prompt → rẻ nhưng mất ngữ cảnh nếu quá tay.
→ **Đo bằng eval** ([[ac03-eval-driven-dev]]): tối ưu cost tới mức **chất lượng vẫn qua ngưỡng**, không hơn.

## Cạm bẫy
- **Dùng model đắt cho mọi câu** → đốt tiền; route/cascade ngay.
- **Cache không invalidate** → trả lời sai khi KB đổi.
- **Tối ưu cost mù** (không đo quality) → rẻ nhưng tệ → mất khách.
- **Quên output token** (thường đắt hơn input) → giới hạn độ dài trả lời.
- **Prompt phình âm thầm** (few-shot, context dài) → đo token/request theo thời gian (cost drift [[aa10-llmops]]).
- **Agent loop không budget cap** → 1 request đốt $$$.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao cost AI = token, model lớn đắt 10–100×.
- [ ] 7 đòn tối ưu; routing/cascade mạnh nhất.
- [ ] Cache nhiều tầng (exact/semantic/embedding) + invalidation.
- [ ] Công thức $/query, $/ngày; budget cap + alert.
- [ ] Tam giác quality⇄cost⇄latency: tối ưu tới ngưỡng chất lượng.
- 🔭 Tự mò: viết "router" giả trong Python — phân loại câu hỏi (ngắn/factoid → "model nhỏ", dài/suy luận → "model lớn") bằng heuristic; mô phỏng cost (giá nhỏ vs lớn), chạy trên 8 golden query, in **$/query trung bình** khi route vs khi luôn dùng model lớn → thấy tiết kiệm.

➡️ Tiếp [[ac09-ai-review3]] — tổng kết + ngân hàng câu hỏi phỏng vấn.
