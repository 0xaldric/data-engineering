# AJ08 — Prompt Optimization (tự động)

> Tối ưu prompt bằng **DATA + metric** thay vì chỉnh tay theo cảm giác. DSPy "compile" prompt từ ví dụ; chọn few-shot tốt nhất tự động. Prompt engineering thành **prompt optimization**. Liên hệ [[aa07-prompt-management]], [[ac03-eval-driven-dev]], [[ab02-rag-eval-harness]].

## Vì sao tối ưu prompt tự động
- Chỉnh prompt tay = thử-sai theo cảm giác → chậm, không nhất quán, không biết tốt thật không.
- Có **golden set + metric** ([[ac03-eval-driven-dev]]) rồi → tại sao không **tối ưu prompt như tối ưu tham số**?
- → Để data + metric chọn prompt/ví dụ tốt nhất, đo được, tái lập được.

## ⭐ Few-shot example selection (đơn giản mà mạnh)
```
pool ví dụ (nhiều) ─> chọn K ví dụ ĐƯA vào prompt (few-shot)
   chọn ngẫu nhiên? -> không tối ưu
   chọn theo: (a) GIỐNG câu hỏi hiện tại (retrieve ví dụ liên quan — như RAG!)
              (b) ĐA DẠNG (cover nhiều case)
              (c) ví dụ làm metric CAO NHẤT (thử trên golden)
```
→ **Dynamic few-shot**: với mỗi câu hỏi, retrieve ví dụ liên quan nhất từ pool (dùng embedding [[ai02-rag-capstone-writeup]]) → prompt thích nghi. DE cung cấp pool ví dụ + cơ chế chọn.

## ⭐ DSPy (compile prompt từ data)
```
DSPy: viết "chương trình" LLM bằng signature (input->output) + metric
   -> COMPILER tự tìm prompt/few-shot tốt nhất (bootstrap ví dụ, thử, giữ cái metric cao)
   -> như compiler tối ưu code, nhưng cho prompt
```
- Thay "viết prompt hoàn hảo" bằng "định nghĩa task + metric, để DSPy tối ưu".
- Bootstrap: chạy model trên train → giữ trace thành công làm few-shot → tự cải thiện.
- Đổi model? Re-compile (prompt tối ưu cho model cũ ≠ model mới).

## ⭐ Automatic Prompt Optimization (APO)
```
prompt v0 ─> đo trên golden ─> LLM đề xuất prompt v1 (sửa chỗ yếu) ─> đo lại
   ─> giữ nếu tốt hơn (như self-correction [[ae01-self-correcting-rag]] cho prompt)
   ─> lặp -> hội tụ prompt tốt
```
- Dùng LLM tối ưu prompt cho LLM (meta). Hoặc search (thử nhiều biến thể, giữ tốt nhất).
- Luôn cần **metric + golden** để biết "tốt hơn" — đúng eval-driven ([[ac03-eval-driven-dev]]).

## Vai trò DE
- **Cung cấp pool ví dụ** (từ data thật/flywheel [[aj07-data-flywheel]]) + golden + metric.
- **Hạ tầng đo**: chạy ablation prompt qua harness ([[ab02-rag-eval-harness]]) — như [[ah02-embedding-benchmark]] cho prompt.
- **Version prompt tối ưu** ([[aa07-prompt-management]]) + re-compile khi đổi model.
- Đây là eval-driven áp cho **prompt** (giống chọn embedding/chunk bằng số).

## Cạm bẫy
- **Tối ưu prompt không metric** → vẫn là cảm giác → cần golden + metric.
- **Overfit golden** → prompt tốt trên golden, tệ ngoài đời → golden đại diện + test riêng.
- **Few-shot ngẫu nhiên** → bỏ lỡ ví dụ tốt → chọn theo liên quan/metric.
- **Prompt tối ưu cho model A dùng cho B** → kém → re-compile khi đổi model.
- **Quên cost**: nhiều ví dụ few-shot → token tăng ([[ah04-tokenization]]) → cân chất lượng vs cost.
- **Không version** → mất prompt tốt → registry ([[aa07-prompt-management]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao tối ưu prompt tự động (có golden+metric thì tối ưu được).
- [ ] Few-shot selection: liên quan/đa dạng/metric (dynamic few-shot = RAG ví dụ).
- [ ] DSPy: compile prompt từ signature + metric (bootstrap).
- [ ] APO: LLM/search tối ưu prompt, cần metric.
- [ ] DE: pool ví dụ + golden + harness + version + re-compile.
- 🔭 Tự mò: làm "dynamic few-shot" mini — pool 10 ví dụ (câu hỏi→nhãn) embed bằng `rag_over_notes.embed`; với câu hỏi mới, retrieve 2 ví dụ giống nhất làm few-shot (thay vì cố định); so "few-shot cố định" vs "few-shot động" trên vài câu — thấy chọn ví dụ đúng quan trọng thế nào.

➡️ Tiếp [[aj09-ai-review9]] — grand finale Module AI.
