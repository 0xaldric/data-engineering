# AA05 — Agentic Data Pipelines

> LLM không chỉ sinh text — còn **điều phối công việc** (gọi tool, chạy SQL, sửa pipeline). "Agent" đang vào data engineering. DE phải hiểu để xây + **giám sát** an toàn.

## Agent là gì (góc DE)
LLM + **vòng lặp lý luận** + **công cụ** (tools): LLM quyết định gọi tool nào, đọc kết quả, lặp tới khi xong. Khác "1 lần gọi LLM" — agent **nhiều bước, có trạng thái, tự quyết**.
```
Câu hỏi → [LLM nghĩ] → chọn tool (SQL/search/API) → chạy → [LLM đọc kết quả]
              ▲                                                    │
              └──────────────── lặp (ReAct) ───────────────────────┘ → trả lời
```

## ReAct loop (Reason + Act)
```
Thought: cần biết doanh thu theo tháng
Action: run_sql("SELECT month, sum(...) ...")
Observation: [kết quả]
Thought: tháng 6 giảm, cần so tháng trước...
Action: run_sql(...)
...
Answer: ...
```
Mỗi vòng: LLM **suy nghĩ** → **hành động** (tool) → **quan sát** kết quả → lặp.

## Tool use cho data agent
- `run_sql(query)` — query warehouse (qua **guardrail** text-to-SQL — [[aa01-text-to-sql]]).
- `search_docs(q)` — RAG retrieval ([[ai02-rag-capstone-writeup]]).
- `call_api`, `read_file`, `python_exec` (sandbox).
- DE cung cấp tool **an toàn** (read-only, guardrail, sandbox) cho agent gọi.

## Ứng dụng trong DE
- **Data analyst agent**: hỏi NL → agent tự query + phân tích + trả lời (text-to-SQL + reasoning).
- **Self-healing pipeline**: pipeline lỗi → agent đọc log, đoán nguyên nhân, đề xuất/áp fix (có human approval).
- **Text-to-pipeline**: mô tả NL → agent sinh dbt model/DAG (DE review trước khi chạy).
- **Data exploration**: agent tự khám phá schema, sinh insight.

## ⚠️ Rủi ro (vì sao DE phải giám sát) ⭐
| Rủi ro | Hệ quả | Kiểm soát |
|--------|--------|-----------|
| **Non-determinism** | agent làm khác nhau mỗi lần | guardrail + eval + human approval cho hành động quan trọng |
| **Loop vô hạn** | agent lặp không dừng → đốt tiền | giới hạn số bước (max iterations) + budget |
| **Cost bùng nổ** | nhiều LLM call/bước | đếm token, cap budget ([[ai08-ai-cost-latency]]) |
| **Hành động nguy hiểm** | agent chạy DROP/xoá/gửi tiền | tool **read-only**/least-privilege + **human-in-the-loop** cho hành động ghi |
| **Sai lệnh do prompt injection** | dữ liệu chứa lệnh lái agent | guardrail injection ([[aa02-guardrails]]) |
| **Hallucinated action** | gọi tool với tham số bịa | validate tham số trước khi chạy |

## DE giám sát agent thế nào
- **Guardrail tool**: mọi tool agent gọi đi qua lớp an toàn (SQL guardrail, sandbox).
- **Human approval** cho hành động **ghi/xoá/tốn tiền** (agent đề xuất, người duyệt).
- **Budget/step cap**: giới hạn số bước + token mỗi task.
- **Observability**: log mọi thought/action/observation (trace) → audit + debug ([[k07-observability-tooling]]).
- **Eval**: agent hoàn thành task đúng không (success rate trên golden tasks).
- **Least privilege**: agent chỉ có quyền tối thiểu (read-only mặc định).

## ⚠️ Cạm bẫy
- Cho agent quyền ghi/xoá không human approval → thảm hoạ.
- Không cap step/budget → loop vô hạn đốt tiền.
- Không log trace → không debug được agent làm gì.
- Tin agent "tự sửa pipeline" chạy thẳng prod (phải review/staging trước).
- Over-agentic: dùng agent cho việc deterministic (script thường rẻ + tin cậy hơn).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Agent = LLM + ReAct loop + tools; khác 1-lần-gọi.
- [ ] Rủi ro (loop/cost/hành động nguy hiểm/injection) + kiểm soát.
- [ ] DE giám sát: guardrail tool + human approval + budget cap + trace + least privilege.
- 🔭 Phác một "data analyst agent" tối giản: tool = `text_to_sql.py` (đã có, guardrail sẵn) + vòng lặp gọi LLM (mock) ≤3 bước; nghĩ chỗ nào cần human approval.

➡️ Tiếp: [[aa06-llm-eval]].
