# AG05 — Agent Platform Data Infrastructure (sâu)

> Vận hành **nhiều agent ở scale** cần một "platform": tool registry, state machine, coordination, run store, human-in-loop queue. Sâu hơn [[ad07-agent-data]] (1 agent) → nền tảng cho cả đội agent. Liên hệ [[ac04-multi-agent]], [[ab06-llm-observability]].

## Từ "1 agent" tới "platform"
| 1 agent ([[ad07-agent-data]]) | Agent platform (nhiều agent, nhiều team) |
|-------------------------------|------------------------------------------|
| memory + tool + checkpoint | + registry tool dùng chung, versioned |
| 1 run | run store: mọi run replay/audit được |
| tự gọi tool | tool có scope/quota/quyền tập trung |
| — | coordination giữa agent (message/blackboard) |
| — | human-in-loop queue tập trung |
→ Platform = **hạ tầng chung** để team xây agent an toàn, nhất quán, quan sát được.

## ⭐ 5 thành phần nền tảng
```
        ┌─ TOOL REGISTRY ───── đăng ký tool: schema, version, scope, quyền, quota
agent ──┼─ STATE MACHINE ───── trạng thái run (pending→running→waiting→done/failed) + checkpoint
platform├─ COORDINATION ────── nhiều agent trao đổi: message queue / shared blackboard
        ├─ RUN STORE ───────── mỗi run = trace đầy đủ (input/step/tool-call/output) replay được
        └─ HUMAN-IN-LOOP Q ─── hàng đợi việc cần người duyệt (hành động nguy hiểm)
```

### 1. ⭐ Tool Registry (tool = data product có governance)
- Đăng ký mỗi tool: tên, mô tả, **schema I/O** (validate [[ai06-llm-output-governance]]), **version**, **scope** (read/write), **quyền** (agent nào được gọi), **quota/rate-limit**.
- Agent chọn tool từ registry → nhất quán, an toàn, đổi tool không phá agent (versioned [[ag08-ai-data-contracts]]).
- DE: tool thường = cổng data có kiểm soát ([[ad04-llm-security]] least privilege).

### 2. ⭐ State Machine & Checkpoint
```
pending -> running -> [waiting tool / waiting human] -> running -> done
                                                      └-> failed -> retry/resume từ checkpoint
```
- Agent chạy lâu → trạng thái rõ ràng + checkpoint mỗi bước → resume khi fail ([[ad07-agent-data]]).
- Bước side-effect phải **idempotent** → resume không nhân đôi.

### 3. Coordination (nhiều agent)
- **Message passing**: agent gửi/nhận task qua queue ([[ad03-kafka-internals|kafka]]-style).
- **Shared blackboard**: vùng nhớ chung (state/kết quả) các agent đọc/ghi → cẩn thận tranh chấp (lock/version).
- **Supervisor** điều phối ([[ac04-multi-agent]]) → tránh agent giẫm chân/loop.

### 4. ⭐ Run Store (replay & audit)
- Mỗi run lưu **trace đầy đủ**: input, mỗi step nghĩ gì, tool-call nào, kết quả, output ([[ab06-llm-observability]]).
- Dùng để: **replay** (tái hiện bug), **audit** (agent làm gì — compliance [[af06-ai-data-governance]]), **eval** (task success rate), **debug**.
- Volume lớn (mỗi run nhiều step) → bài toán data như clickstream ([[c06-case-clickstream]]).

### 5. Human-in-loop Queue
- Hành động nguy hiểm/không chắc → đẩy vào **hàng đợi người duyệt** ([[ad04-llm-security]]).
- Người duyệt/sửa → agent tiếp tục (resume từ checkpoint).
- Phản hồi người → online eval cải thiện ([[ag03-rlhf-preference-data]]).

## Cạm bẫy
- **Tool không registry/version** → đổi tool phá agent đang chạy; quyền lung tung → tập trung hoá registry.
- **Không run store** → agent là hộp đen, không replay/audit nổi → lưu trace đầy đủ.
- **State không checkpoint** → run dài fail = mất hết → state machine + checkpoint.
- **Coordination tranh chấp** (nhiều agent ghi blackboard) → race → lock/version.
- **Không budget/quota tập trung** → 1 agent loop đốt tài nguyên cả platform → quota ở registry.
- **Bỏ human-in-loop** → agent tự làm hành động nguy hiểm → queue duyệt.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Khác biệt 1-agent vs platform (registry/run-store/coordination/queue).
- [ ] Tool registry: schema/version/scope/quyền/quota.
- [ ] State machine + checkpoint + idempotent resume.
- [ ] Run store: replay/audit/eval; volume như clickstream.
- [ ] Human-in-loop queue cho hành động nguy hiểm.
- 🔭 Tự mò: dựng "tool registry" mini bằng dict: mỗi tool có `{schema, version, scope}`; "agent" giả chọn tool theo tên, validate input theo schema trước khi gọi (`llm_output_pipeline` style); lưu mỗi "run" ra JSONL (trace) → đọc lại replay 1 run.

➡️ Tiếp [[ag06-multimodal-production]] — multimodal ở scale.
