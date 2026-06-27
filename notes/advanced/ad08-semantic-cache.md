# AD08 — Semantic Caching & Serving Infra ⭐ (có code chạy được)

> Cache câu trả lời theo **NGỮ NGHĨA** (câu gần nghĩa → trả cache), không chỉ exact match → tiết kiệm lớn LLM call. Nhưng đầy bẫy: cosine **≠** tương đương ngữ nghĩa. Code: [`semantic_cache.py`](../../projects/06-ai-data-engineering/semantic_cache.py). Liên hệ [[ac08-ai-cost-scale]], [[ab07-vector-search-opt]].

## Vì sao cần & ý tưởng
- LLM call **đắt + chậm** ([[ai08-ai-cost-latency]]). Traffic thật **lặp nhiều** (nhiều người hỏi gần giống nhau).
- **Exact cache** (string khớp) bắt được quá ít (chỉ chữ y hệt).
- **Semantic cache**: embed câu hỏi; câu mới có cosine ≥ ngưỡng với câu đã hỏi → trả lại đáp án cũ, **khỏi gọi LLM**.
```
hỏi mới ─embed─> tìm câu cũ gần nhất ─ cos ≥ ngưỡng? ─ HIT  -> trả cache (gần free)
                                       └ MISS -> gọi LLM -> lưu (q, vec, answer) vào cache
```

## ⭐⭐ Bài học cốt lõi (code chạy ra): cosine ≠ ngữ nghĩa
Kết quả thật (ngưỡng 0.93):
```
[HIT ] EXACT   cos=1.000  idempotency... = idempotency...
[MISS] REWORD  cos=0.821  "idempotent nghĩa là gì" ⚠️ FALSE-MISS (cùng nghĩa mà trượt)
[MISS] MISS    cos=0.655  câu khác hẳn ✓
[HIT ] TRICKY  cos=0.976  "vì sao CSV nhanh hơn parquet" ⚠️ FALSE-HIT (NGƯỢC ý mà trúng!)
```
**NGHỊCH LÝ**: câu cùng nghĩa (REWORD, 0.821) điểm **THẤP HƠN** câu ngược nghĩa (TRICKY, 0.976)!
- "vì sao **csv** nhanh hơn **parquet**" vs "vì sao **parquet** nhanh hơn **csv**" → **trùng hết từ**, chỉ đổi thứ tự → cosine **rất cao** dù **ngược nghĩa hoàn toàn**.
- Reword cùng nghĩa lại đổi nhiều từ (idempotent/idempotency, nghĩa-là-gì/là-gì) → cosine thấp hơn.
→ ⭐ **KHÔNG ngưỡng đơn nào** vừa bắt được reword vừa loại negation. Embedding gần **bất biến thứ tự từ** → mù với phủ định/đảo vế. Đây là **giới hạn thật** của semantic cache, không phải bug.

## ⭐ Hệ quả thiết kế (vì giới hạn trên)
| Rủi ro | Giảm thiểu |
|--------|-----------|
| **False-hit** (trả đáp án SAI) — tệ nhất | ngưỡng CAO + chặn pattern phủ định/đảo; ưu tiên an toàn hơn tiết kiệm |
| **False-miss** (bỏ lỡ cache) — chỉ tốn tiền | chấp nhận; hoặc dùng model embedding tốt hơn cho câu hỏi |
| cosine mù ngữ nghĩa | thêm tầng kiểm: so cả keyword/cấu trúc, hoặc LLM nhỏ xác nhận trước khi trả cache |
> Nguyên tắc: **false-hit nguy hiểm hơn false-miss** (trả sai > tốn thêm 1 call) → thà miss còn hơn hit sai → ngưỡng nghiêng về cao.

## Cache nhiều tầng (ghép với [[ac08-ai-cost-scale]])
```
exact cache (hash câu)        ─ hit ─> trả (chắc chắn đúng, gần free)
   └ miss ─> semantic cache (cosine ≥ ngưỡng CAO) ─ hit ─> trả (rủi ro false-hit)
        └ miss ─> embedding cache (khỏi re-embed)
             └ miss ─> gọi LLM ─> lưu mọi tầng
```
- Exact trước (an toàn) → semantic sau (rủi ro hơn). 
- Cache cả **embedding** (đã làm ở capstone — incremental theo hash).

## ⭐ Invalidation (đừng quên!)
- KB đổi ([[ac06-kb-freshness]]) → đáp án cache **cũ → sai** → phải **invalidate** cache liên quan.
- TTL cho cache entry; version theo KB/prompt ([[aa07-prompt-management]]) — đổi prompt → cache cũ vô hiệu.
- Cache không invalidate = trả lời lỗi thời tự tin.

## Đo hiệu quả
- **Hit rate**: % câu được phục vụ từ cache → tiết kiệm = hit_rate × cost_per_call.
- **False-hit rate**: % hit trả sai (đo trên tập có nhãn) → phải gần 0.
- Cân: ngưỡng ↑ → false-hit ↓ nhưng hit-rate ↓ (ít tiết kiệm). Calibrate trên câu thật ([[ac03-eval-driven-dev]]).

## Cạm bẫy
- **Tin cosine = ngữ nghĩa** → false-hit trả sai (negation/đảo vế) → ngưỡng cao + chặn phủ định.
- **Ngưỡng quá thấp** để "tiết kiệm nhiều" → trả đáp án sai → mất uy tín.
- **Quên invalidate** khi KB/prompt đổi → cache lỗi thời.
- **Cache câu cá nhân hoá** (có ngữ cảnh user) → trả nhầm của người khác → không cache hoặc key theo user.
- **Không đo false-hit** → nghĩ cache tốt mà đang trả sai ngầm.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Semantic cache khác exact cache; tiết kiệm = hit_rate × cost.
- [ ] ⭐ Vì sao cosine ≠ ngữ nghĩa (negation/đảo vế điểm cao; reword điểm thấp).
- [ ] False-hit nguy hiểm hơn false-miss → ngưỡng nghiêng cao.
- [ ] Cache nhiều tầng (exact→semantic→embedding).
- [ ] Invalidation khi KB/prompt đổi; đo false-hit.
- 🔭 Tự mò: chạy `semantic_cache.py`, hạ `threshold` xuống 0.80 → xem REWORD hit nhưng TRICKY cũng hit (false-hit tăng); thêm bước chặn: nếu 2 câu trùng từ nhưng có từ phủ định/đảo ("không", "nhanh hơn" đảo vế) thì KHÔNG cho hit dù cosine cao. Đo lại hit-rate vs false-hit.

➡️ Tiếp [[ad09-ai-review4]] — review 4 + tích hợp + drill cuối.
