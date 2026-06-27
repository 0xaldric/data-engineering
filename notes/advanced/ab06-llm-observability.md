# AB06 — LLM Observability & Tracing Pipeline

> Trace mọi request LLM (input → retrieval → prompt → model → output) như **distributed tracing**; theo dõi token/cost/latency/chất lượng; log để debug, eval, audit. **LLM logs là một nguồn dữ liệu lớn — DE xây pipeline cho nó.** Liên hệ [[k07-observability-tooling]], [[aa10-llmops]], [[c06-case-clickstream]].

## Vì sao LLM khó quan sát hơn hệ thường
- **Non-deterministic**: cùng input → output khác → "bug" không reproduce dễ ([[ai07-testing-nondeterministic]]).
- **Pipeline nhiều bước**: retrieval → rerank → prompt build → LLM → parse → validate. Lỗi ở bước nào? Cần **trace** xuyên suốt.
- **Cost theo token**: phải biết request nào đốt tiền ([[ai08-ai-cost-latency]]).
- **Chất lượng mơ hồ**: "trả lời tệ" — tệ vì retrieval trượt hay vì model? Trace mới biết.

## ⭐ Trace một request (như span trong distributed tracing)
```
trace_id=abc123
 ├─ span: retrieve      | 45ms  | k=5, scores=[.82,.79,...]   ← retrieval tốt không?
 ├─ span: rerank        | 30ms  | reorder top-5
 ├─ span: build_prompt  | 2ms   | tokens_in=1240             ← prompt phình không?
 ├─ span: llm_call      | 1300ms| model=x, tok_out=180, $=0.004  ← chậm/đắt ở đây
 ├─ span: parse+validate| 3ms   | status=valid (ai06)
 └─ outcome: faithfulness=0.91, user_feedback=👍
```
Mỗi span: thời gian + metadata. Ghép lại = **bức tranh đầy đủ** một câu hỏi đi qua hệ. Debug = mở trace, xem span nào đỏ.

## ⭐ Cái cần log mỗi request (provenance đầy đủ)
| Nhóm | Trường |
|------|--------|
| **Định danh** | trace_id, user/session, timestamp |
| **Input** | query, input_hash |
| **Retrieval** | doc_ids lấy ra, scores, k |
| **Prompt** | prompt_version ([[aa07-prompt-management]]), tokens_in |
| **Model** | model + version, params (temp) |
| **Output** | response, tokens_out, status (valid/repaired/quarantine — [[ai06-llm-output-governance]]) |
| **Cost/perf** | $ request, latency mỗi span |
| **Quality** | faithfulness/eval score ([[aa06-llm-eval]]), feedback 👍/👎 |
→ Đây chính là **provenance log** ([[ai06-llm-output-governance]]) mở rộng — đủ để **replay, debug, eval, audit**.

## ⭐ DE góc nhìn: LLM logs = clickstream mới
Volume lớn (mỗi request nhiều span, traffic cao) → đúng bài toán [[c06-case-clickstream]]:
```
app/agent ─> emit trace events ─> [queue: Kafka] ─> [sink: warehouse/lakehouse]
   ─> bảng fact_llm_request (1 dòng/request) + fact_llm_span (1 dòng/span)
   ─> dashboard: cost/ngày, p99 latency, % quarantine, faithfulness theo thời gian (drift)
```
- Mô hình hoá như **fact table** (request = fact, span = fact chi tiết) — dimensional modeling áp y nguyên.
- Aggregate: cost theo model/feature/user, error rate, drift chất lượng ([[aa10-llmops]]).
- Sampling khi volume khổng lồ (không log full 100% nếu quá tải — như tracing thường).

## Công cụ (biết tên + chúng giải quyết gì)
| Công cụ | Cho |
|---------|-----|
| **Langfuse** / **LangSmith** / **Phoenix (Arize)** | trace LLM chuyên dụng: span, token/cost, eval, dataset |
| **OpenTelemetry** | chuẩn tracing chung — LLM span theo OTel convention |
| **Grafana/Prometheus** | metric/dashboard hạ tầng ([[k07-observability-tooling]]) |
→ Bản chất: **distributed tracing + cost accounting + eval store** cho LLM. Tự build được bản nhỏ (chính là provenance log của `llm_output_pipeline.py`).

## 5 trụ observability ([[k07-observability-tooling]]) áp cho LLM
metrics (token/cost/latency) · logs (provenance) · **traces** (span pipeline) · **eval** (faithfulness — thay "metrics chất lượng") · alerting (cost spike, quarantine rate tăng, drift).

## Cạm bẫy
- **Log thiếu** → không replay/debug được (thiếu prompt_version, doc_ids → mù).
- **Log cả PII** vào trace → rò ([[aa02-guardrails]]) → redact trước khi log.
- **Không sample** → chi phí log vượt chi phí LLM khi volume lớn.
- **Có log mà không ai xem** → cần dashboard + alert, không chỉ đổ vào kho.
- **Không nối feedback** → không biết chất lượng thật (online eval [[aa06-llm-eval]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Trace/span cho một request LLM gồm những bước nào.
- [ ] Cần log gì để replay/debug/audit (provenance đầy đủ).
- [ ] Vì sao LLM logs = bài toán clickstream/fact table.
- [ ] 5 trụ observability áp cho LLM (eval thay metrics chất lượng).
- [ ] Cạm bẫy: PII trong log, không sample, log mà không xem.
- 🔭 Tự mò: mở rộng `llm_output_pipeline.py` — gắn `trace_id` + đo "latency" (đếm bước) mỗi request, ghi provenance ra **bảng DuckDB** `fact_llm_request`; viết 1 query tổng hợp: % quarantine theo prompt_version, "cost" trung bình (giả bằng tokens).

➡️ Tiếp [[ab07-vector-search-opt]] — tune ANN recall/latency/RAM.
