# AB01 — Synthetic Data Generation với LLM ⭐ (có code chạy được)

> Sinh dữ liệu giả bằng LLM khi thiếu data thật (train model, test pipeline, augment lớp hiếm). **Vai trò DE không phải "gọi LLM" — mà kiểm soát CHẤT LƯỢNG data sinh ra.** Code: [`synthetic_data.py`](../../projects/06-ai-data-engineering/synthetic_data.py). Liên hệ [[aa04-training-data-prep]].

## Khi nào cần synthetic data
| Tình huống | Vì sao synthetic giúp |
|-----------|----------------------|
| **Thiếu data** | sản phẩm mới, chưa có log thật → sinh để bootstrap |
| **Lớp hiếm** (imbalanced) | fraud 0.1% → sinh thêm ca gian lận để model học |
| **Privacy** | data thật có PII → sinh bản giả "giống phân phối" để dev/test ([[aa02-guardrails]]) |
| **Test pipeline** | cần 1tr bản ghi đa dạng để test tải, edge case |
| **Augment** | xoay/diễn đạt lại để model robust hơn |

## ⭐ Tư duy DE: 4 cổng chất lượng (KHÔNG bỏ qua)
LLM sinh data **dễ** — sinh data **tốt** mới khó. Pipeline đúng = 4 cổng:

```
LLM sinh thô  →  [1] Quality filter  →  [2] Dedup  →  [3] Diversity check  →  [4] Balance
  (N lớn)          (bỏ rác: rỗng,        (bỏ near-dup    (đo mode collapse:    (cân nhãn:
                    quá ngắn/dài,         — Jaccard/       bigram unique/tổng    ≤K mỗi lớp)
                    sai format)           MinHash)         thấp = lặp khuôn)
```

## ⭐ Cạm bẫy lớn nhất: **Mode Collapse**
LLM hay sinh **lặp khuôn** (cùng vài mẫu câu, từ vựng nghèo) → data "nhìn nhiều" nhưng thông tin ít.
- **Đo**: diversity = (số bigram unique) / (tổng bigram). Thấp → đang collapse.
- Trong demo: data thô diversity **0.09** (rất lặp) → sau dedup tăng **0.34**.
- **Chống**: đa dạng prompt (persona/temperature/seed khác nhau), trộn nhiều template, dedup mạnh.

## Cạm bẫy khác
| Bẫy | Hậu quả | Chống |
|-----|---------|-------|
| **Bias amplification** | LLM có sẵn bias → sinh data khuếch đại bias → model học bias | audit phân phối, fairness check |
| **Distribution drift** | data giả khác phân phối data thật → model train xong fail thật | so sánh thống kê synthetic vs real (KS test, phân phối nhãn) |
| **Self-consumption / model collapse** | train model trên chính output của nó qua nhiều vòng → thoái hoá | giữ tỉ lệ data thật, không train thuần synthetic |
| **Leakage** | synthetic test trùng synthetic train | decontaminate ([[aa04-training-data-prep]]) |
| **Label noise** | LLM gán nhãn sai | human-in-loop spot-check, confidence filter |

## Code minh hoạ (chạy thật)
`synthetic_data.py` — mock-LLM (tổ hợp template, không cần API) + 4 cổng chất lượng:
```
1. Sinh thô: 144 records | billing:48 technical:48 account:48
2. Quality filter (độ dài): 144 (-0 rác)
3. Dedup (Jaccard>=0.5): 47 (-97 near-dup) | diversity=0.09 -> 0.34
4. Balance (≤14/lớp): 42 | billing:14 technical:14 account:14
-> Dataset cuối: 42 records sạch, đa dạng, cân bằng (từ 144 thô)
```
→ **Điểm chốt**: 144 thô → chỉ **42** thực sự dùng được. Phần lớn là near-dup. Đây chính là lý do cần cổng chất lượng — không thì "tưởng nhiều mà ít".

## Synthetic vs Real — luôn nhớ
- Synthetic **bổ sung**, không **thay thế** data thật.
- Luôn giữ một tập **real holdout** để eval cuối (model phải tốt trên data THẬT).
- Tỉ lệ trộn (vd 70% real + 30% synthetic) là hyperparameter cần thử.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 4 cổng chất lượng (quality/dedup/diversity/balance) — mỗi cổng chống gì.
- [ ] Mode collapse là gì, đo bằng diversity ra sao.
- [ ] 4 rủi ro (bias amplify / drift / model collapse / leakage).
- [ ] Vì sao luôn cần real holdout.
- 🔭 Tự mò: sửa `synthetic_data.py` — thêm cột `priority`, sinh **lệch nhãn** (billing nhiều gấp 5) rồi xem `balance()` cắt thế nào; thêm hàm so phân phối độ dài synthetic vs một tập "real" bịa ra (drift check).

➡️ Tiếp [[ab02-rag-eval-harness]] — đo chất lượng retrieval bằng số.
