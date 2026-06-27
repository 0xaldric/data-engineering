# AC03 — Evaluation-Driven Development cho AI

> "Eval trước, code sau" — TDD áp cho hệ LLM. Golden set = **spec**; mọi thay đổi qua **eval gate**. Không eval-first = bay trong sương mù. Liên hệ [[ab02-rag-eval-harness]], [[aa06-llm-eval]], [[ai07-testing-nondeterministic]].

## Vì sao AI cần eval-first (khác phần mềm thường)
- Code thường: đúng/sai rõ → viết xong chạy thử là biết.
- LLM: **non-deterministic + không có "đúng" tuyệt đối** → "có vẻ ổn" đánh lừa. Đổi prompt/chunk/model → chỗ này tốt lên, chỗ kia tệ đi mà **không hay biết** nếu không đo.
- → Phải có **thước đo khách quan** trước, rồi mới sửa, rồi đo lại. Giống TDD: test (đỏ) → code → test (xanh).

## ⭐ Vòng lặp EDD
```
1. ĐỊNH NGHĨA "tốt" = metric + golden set (TRƯỚC khi build)   ← spec
2. Build baseline ─> chạy eval ─> có CON SỐ khởi điểm
3. Thay đổi (prompt/chunk/model/rerank...) ─> chạy eval lại
4. Tốt hơn? GIỮ. Tệ hơn? BỎ.   (quyết định bằng số, không cảm tính)
5. Đưa eval vào CI ─> mỗi PR phải qua ngưỡng ─> chống regression
   (lặp lại; mở rộng golden set khi gặp ca lỗi mới)
```
Đã làm thật ở [[ab02-rag-eval-harness]]: sweep config → bảng số → chọn "hybrid k=5 88%". Đó chính là một bước EDD.

## ⭐ Golden set = spec sống
| Tính chất | Vì sao |
|-----------|--------|
| **Đại diện** | sát truy vấn/ca dùng thật, không phải ví dụ đẹp |
| **Đa dạng** | dễ + khó + edge case + đa ngữ ([[ac01-multilingual-rag]]) |
| **Có nhãn đúng** | mỗi mẫu biết "đáp án" để chấm |
| **Lớn dần** | mỗi bug thật → thêm 1 ca vào golden (regression test) |
| **Versioned** | golden đổi → ghi version, so công bằng ([[ab08-finetune-pipeline]]) |
→ Bug production = "test case còn thiếu". Bắt được lỗi → **thêm vào golden** → không tái diễn (đúng tinh thần regression test).

## Metric theo tầng (đo đúng chỗ)
```
Retrieval:   recall@k / MRR / nDCG ([[ab02-rag-eval-harness]])   <- doc đúng có lọt không
Generation:  faithfulness / answer relevance ([[aa06-llm-eval]] RAGAS) <- trả lời có bám context
Output:      schema valid / % quarantine ([[ai06-llm-output-governance]]) <- đúng format
System:      latency p99 / cost ([[ai08-ai-cost-latency]])       <- nhanh/rẻ đủ không
```
EDD = đặt ngưỡng cho **từng tầng** + gate. Retrieval tốt mà generation tệ → biết ngay tầng nào hỏng.

## ⭐ EDD → CI gate (LLMOps)
```
PR đổi prompt ─> CI chạy eval trên golden ─> recall ≥ 85%? faithfulness ≥ 0.8? cost ≤ X?
   PASS ─> merge        FAIL ─> chặn (regression)
```
Biến "chất lượng AI" thành **test tự động** ([[aa10-llmops]]) — như unit test cho code, nhưng metric thay vì assert nhị phân.

## So với phát triển AI "vibe-based" (phản diện)
| Vibe-based ❌ | Eval-driven ✅ |
|--------------|---------------|
| "thử vài câu thấy ổn" | golden set chấm điểm |
| đổi prompt theo cảm giác | đổi → đo → giữ/bỏ |
| không biết có regression | CI gate chặn |
| tranh luận "tốt hơn không" | nhìn số |
| demo đẹp, production sập | đo trên ca đại diện |

## Cạm bẫy
- **Golden quá nhỏ/lệch** → tối ưu vào nó (overfit eval), thực tế vẫn tệ → đa dạng + lớn dần.
- **Chỉ đo offline** → bỏ lỡ hành vi thật → thêm **online eval** (feedback, A/B [[aa06-llm-eval]]).
- **Metric sai mục tiêu** → tối ưu recall mà người dùng cần precision → chọn metric theo bài toán.
- **LLM-judge thiên vị** ([[aa06-llm-eval]]) → cần calibrate / human spot-check.
- **Eval đắt/chậm** → không ai chạy → giữ golden gọn, sample, cache.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao AI cần eval-first (non-deterministic, không "đúng" tuyệt đối).
- [ ] Vòng lặp EDD 5 bước; golden = spec sống, lớn dần theo bug.
- [ ] Metric theo tầng (retrieval/generation/output/system).
- [ ] EDD → CI gate chống regression.
- [ ] Cạm bẫy overfit-eval, chỉ-offline, metric-sai-mục-tiêu.
- 🔭 Tự mò: biến `rag_eval_harness.py` thành "CI gate" — đặt ngưỡng `recall@5 ≥ 0.8`, exit code ≠ 0 nếu rớt; thêm 3 golden query mới (giả lập "bug production"); chạy lại xem có còn pass không. Đó là EDD thu nhỏ.

➡️ Tiếp [[ac04-multi-agent]] — orchestration nhiều agent.
