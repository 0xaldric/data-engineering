# AF07 — Continuous RAG Eval & Regression Gate ⭐ (có code chạy được)

> Biến eval thành **CI gate**: mỗi đổi prompt/chunk/model → chạy harness → so baseline → **PASS/FAIL theo exit code** → chặn regression tự động. "Test tự động cho RAG". Code: [`continuous_eval.py`](../../projects/06-ai-data-engineering/continuous_eval.py). Sâu hơn [[ab02-rag-eval-harness]], [[ac03-eval-driven-dev]].

## Vì sao cần (eval 1 lần là chưa đủ)
- Eval thủ công 1 lần → tốt. Nhưng RAG **đổi liên tục**: prompt mới, chunk size mới, đổi model, KB cập nhật.
- Mỗi đổi có thể **âm thầm làm tệ đi** chỗ khác (regression) → không ai biết tới khi user phàn nàn.
- → Cần eval **tự động + liên tục**, gắn vào CI: đổi gì cũng phải qua **gate** → không cho chất lượng tụt lọt vào production.

## ⭐ Cơ chế: baseline + gate + exit code
```
đổi code/prompt ─> chạy eval (harness) ─> so với BASELINE đã lưu
   ├─ recall >= baseline - TOL ─> PASS (exit 0) ─> cho merge
   └─ recall <  baseline - TOL ─> FAIL (exit 1) ─> CHẶN merge (regression!)
   (cải tiến có chủ đích -> cập nhật baseline = mốc mới)
```
- **Exit code** là chìa khoá: CI đọc exit ≠ 0 → fail build → chặn PR (như unit test).
- **TOL** (tolerance): cho dao động nhỏ (noise embedding/đo) qua, chỉ chặn tụt thật.

## ⭐ Kết quả thật (code chạy 3 kịch bản)
```
Run 1 (chưa có baseline):  recall=0.750 -> lưu baseline, PASS (exit 0)
Run 2 (ổn định):           recall=0.750 vs 0.750, delta +0.000 -> PASS (exit 0)
Run 3 (baseline=1.0 giả):  recall=0.750 vs 1.000, delta -0.250 ⬇️ -> FAIL (exit 1) CHẶN
```
→ Exit code thật = **1** khi regression → CI sẽ chặn merge. Đây là eval-driven dev ([[ac03-eval-driven-dev]]) **tự động hoá**.

## ⭐ Chọn metric gate & ngưỡng
- **RAG**: gate trên **recall@k** (doc đúng có lọt context không — quan trọng nhất cho LLM đọc).
- Search-trả-người: gate **MRR/nDCG** (thứ hạng).
- Generation: gate **faithfulness** ([[aa06-llm-eval]]) bằng LLM-judge ([[ad02-llm-judge]]).
- **TOL** cân: nhỏ quá → noise gây false-fail; lớn quá → regression lọt. Calibrate trên lịch sử đo.

## Đưa vào CI/CD (LLMOps)
```yaml
# pseudo CI step
- run: python continuous_eval.py     # exit 1 -> job fail -> PR bị chặn
  # PASS -> merge; cải tiến -> UPDATE_BASELINE=1 để chốt mốc mới
```
- Chạy mỗi PR đổi prompt/retrieval/model.
- Lưu lịch sử metric → **dashboard drift** ([[aa10-llmops]]): chất lượng theo thời gian.
- Golden set lớn dần theo bug ([[ac03-eval-driven-dev]]) → gate ngày càng chặt.

## ⭐ Baseline management
- Baseline = **mốc chất lượng hiện tại** (lưu JSON). Cải tiến có chủ đích → cập nhật baseline (`UPDATE_BASELINE=1`).
- ⚠️ Đừng cập nhật baseline **mù** sau mỗi run → sẽ "trôi xuống" (mỗi lần tụt chút lại nhận làm mốc mới → chất lượng giảm dần không ai biết). Chỉ cập nhật khi **cố ý cải tiến** và đã review.
- Baseline tied to corpus version → KB đổi nhiều thì re-baseline ([[ac06-kb-freshness]]).

## Cạm bẫy
- **Eval 1 lần rồi quên** → regression âm thầm → cần liên tục + gate.
- **Không exit code** → CI không chặn được → phải return code đúng.
- **TOL sai**: quá nhỏ → false-fail vì noise; quá lớn → regression lọt.
- **Cập nhật baseline mù** → chất lượng trôi xuống dần → chỉ update khi cải tiến có review.
- **Golden nhỏ/lệch** → gate đo sai → golden đại diện + lớn dần.
- **Gate chỉ retrieval, quên generation** → retrieval ổn mà answer tệ → thêm faithfulness gate.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao cần eval liên tục (regression âm thầm khi đổi).
- [ ] Cơ chế baseline + gate + exit code (CI chặn merge).
- [ ] Chọn metric gate (recall/MRR/faithfulness) + TOL.
- [ ] Baseline management: đừng cập nhật mù (trôi xuống).
- [ ] Cạm bẫy: không exit code, TOL sai, golden lệch.
- 🔭 Tự mò: thêm vào `continuous_eval.py` **lưu lịch sử** (append mỗi run vào `eval_history.jsonl` với timestamp truyền vào) → vẽ/đọc xu hướng recall theo thời gian (drift dashboard mini); thử đổi chunk size trong `rag_over_notes.py` rồi chạy gate xem PASS/FAIL.

➡️ Tiếp [[af08-case-personalization]] — real-time AI personalization.
