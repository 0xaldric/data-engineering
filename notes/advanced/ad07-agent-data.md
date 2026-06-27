# AD07 — Data cho AI Agents Production

> Agent chạy thật cần **hạ tầng data** bên dưới: memory, tool data-access có governance, state/checkpoint để resume, action audit log. **DE dựng nền cho agent — không có nền, agent chỉ là demo.** Liên hệ [[ac04-multi-agent]], [[ab03-context-engineering]], [[aa05-agentic-pipelines]].

## Demo agent vs Production agent
| | Demo | Production |
|--|------|-----------|
| Memory | trong RAM 1 phiên | persistent store (short + long) |
| Tool | gọi đại | data-access layer có quyền/scope |
| Lỗi giữa chừng | chạy lại từ đầu | **checkpoint** → resume |
| Hành động | tin tưởng | audit log + (nguy hiểm) human approve |
| Quan sát | print | trace mọi step ([[ab06-llm-observability]]) |
→ Khoảng cách demo→prod chủ yếu là **data infrastructure**, đúng phần DE.

## ⭐ 4 trụ data cho agent
```
        ┌─ MEMORY ──────────── short-term (phiên) + long-term (vector store) [[ab03-context-engineering]]
agent ──┼─ TOOL DATA LAYER ─── cổng truy cập data có governance (read/write scope, tenant)
        ├─ STATE/CHECKPOINT ── lưu tiến trình -> resume khi fail (idempotent step)
        └─ AUDIT/TRACE ─────── log mọi quyết định + tool-call (debug/compliance)
```

### 1. Memory store
- **Short-term**: lịch sử phiên, kết quả tool gần đây → rolling summary khi đầy ([[ab03-context-engineering]]).
- **Long-term**: fact bền (hồ sơ, lịch sử) trong vector store → retrieve khi liên quan = **RAG**.
- DE: ingest/dedup/version/TTL cho memory; tách phiên (chống rò chéo [[ad03-privacy-compliance]]).

### 2. ⭐ Tool = data-access layer có governance (quan trọng nhất)
- Agent **không chạm thẳng DB/API** → qua tool có: scope (read vs write), quyền theo tenant, rate-limit, validate ([[ad04-llm-security]] least privilege).
- Tool tốt = mô tả rõ, schema chặt, lỗi rõ, **idempotent** (gọi lại an toàn) ([[ac04-multi-agent]]).
- Đây là chỗ DE biến "data" thành "khả năng có kiểm soát" cho agent.

### 3. ⭐ State & checkpoint (resume khi fail)
Agent chạy lâu (nhiều bước, phút–giờ) → **không thể chạy lại từ đầu** khi lỗi:
```
mỗi bước xong -> ghi state (đã làm gì, kết quả) -> checkpoint
lỗi/restart   -> đọc checkpoint -> resume từ bước dở, không lặp lại bước đã xong
```
→ Đúng tư duy **idempotency + backfill** của pipeline ([[i07-backfill-reprocessing]]) áp cho agent. Bước có side-effect (gửi mail/ghi DB) phải idempotent để resume không nhân đôi.

### 4. Audit/trace
- Log mọi **quyết định + tool-call + input/output** ([[ab06-llm-observability]] tracing) → debug "vì sao agent làm X".
- Compliance: agent đụng data nào, làm hành động gì ([[ad03-privacy-compliance]] audit).
- Cost/step để chặn loop đốt tiền ([[ac08-ai-cost-scale]] budget cap).

## Sơ đồ vòng đời 1 task agent (production)
```
nhận task ─> load memory + state ─> [vòng: nghĩ ─> gọi tool (governed) ─> ghi state/checkpoint ─> trace]
   ─> hành động nguy hiểm? ─> human approve ─> tiếp
   ─> xong ─> ghi long-term memory + audit ─> trả kết quả
   (lỗi giữa chừng ─> resume từ checkpoint)
```

## Cạm bẫy
- **Agent chạm thẳng DB/API** → không kiểm soát, nguy hiểm ([[ad04-llm-security]]) → qua tool layer.
- **Không checkpoint** → task dài fail = mất hết, chạy lại từ đầu (tốn + side-effect lặp).
- **Tool không idempotent** → resume/retry nhân đôi hành động (gửi mail 2 lần).
- **Memory không tách phiên/tenant** → rò chéo data người dùng.
- **Không audit/trace** → agent thành hộp đen, không debug/không compliance.
- **Không budget cap** → agent loop đốt tiền ([[aa05-agentic-pipelines]]).
- **Memory phình không dọn** → context nhiễu + tốn → TTL + dedup + summary.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Khoảng cách demo→prod agent = data infrastructure.
- [ ] 4 trụ: memory / tool-data-layer / state-checkpoint / audit-trace.
- [ ] Tool = cổng data có governance (scope/quyền/idempotent).
- [ ] Checkpoint + idempotent step để resume (như backfill pipeline).
- [ ] Audit/trace cho debug + compliance + cost.
- 🔭 Tự mò: viết "agent" giả nhiều bước (vd: retrieve → tóm tắt → lưu) với **checkpoint ra file JSON** sau mỗi bước; cố tình crash giữa chừng (raise) rồi chạy lại → xác nhận nó resume từ bước dở, không lặp bước đã xong. Thêm audit-log mỗi tool-call.

➡️ Tiếp [[ad08-semantic-cache]] — semantic caching (chạy được).
