# AN08 — AI-DE Coding Exercises 4 (bài tập + lời giải)

> 5 bài coding-round (router/agent/data) — **đề + lời giải + reasoning**. Tự code trước. Liên hệ [[an01-rag-advanced-patterns]], [[an02-agentic-patterns]], [[ac07-feature-store]].

---
## Bài 1 — Query router heuristic
**Đề:** Route câu hỏi → "sql"/"action"/"rag" theo từ khoá.
```python
import re
ACTION = re.compile(r"\b(gửi|tạo|xoá|đặt|hủy)\b", re.I)
QUANT  = re.compile(r"\b(bao nhiêu|tổng|trung bình|đếm|top)\b", re.I)
def route(q):
    if ACTION.search(q): return "action"     # high-stakes -> ưu tiên
    if QUANT.search(q):  return "sql"
    return "rag"                              # mặc định an toàn
```
**Reasoning:** route theo thứ tự ưu tiên: action (nguy hiểm, cần duyệt) → sql (định lượng) → mặc định rag ([[an01-rag-advanced-patterns]]). Route sai = tầng sau sai. Production thêm embedding cho rag-vs-reject.

---
## Bài 2 — ReAct loop mini (max steps)
**Đề:** Agent: nghĩ → gọi tool → quan sát, tối đa N bước, dừng khi có answer.
```python
def react(query, tools, max_steps=3):
    trace = []
    for step in range(max_steps):
        action, arg = decide(query, trace)        # mock "nghĩ" -> chọn tool
        if action == "answer":
            return arg, trace
        obs = tools[action](arg)                   # gọi tool
        trace.append((action, arg, obs))
    return "không đủ thông tin (hết bước)", trace   # FALLBACK khi hết bước
```
**Reasoning:** ReAct ([[an02-agentic-patterns]]) xen nghĩ-làm; **max_steps bắt buộc** chống loop vô hạn ([[aa05-agentic-pipelines]]); fallback khi hết bước (không bịa). `trace` để debug/audit ([[ab06-llm-observability]]).

---
## Bài 3 — Provenance log
**Đề:** Ghi provenance mỗi câu trả lời: input hash, model, prompt version, status.
```python
import hashlib, time
def provenance(inp, model, prompt_ver, output, status):
    return {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "input_hash": hashlib.md5(inp.encode()).hexdigest()[:8],
        "model": model, "prompt_version": prompt_ver,
        "status": status,                          # valid/repaired/quarantine
        "output_len": len(output),
    }
```
**Reasoning:** provenance ([[ai06-llm-output-governance]]) = lineage cho output LLM → replay/debug/audit ([[af06-ai-data-governance]]). Hash input (không lưu PII thô [[ad03-privacy-compliance]]); ghi model+prompt version để truy "output từ đâu".

---
## Bài 4 — Budget cap counter
**Đề:** Theo dõi token/cost, chặn khi vượt budget (chống agent loop đốt tiền).
```python
class Budget:
    def __init__(self, cap): self.cap, self.spent = cap, 0
    def charge(self, tokens):
        if self.spent + tokens > self.cap:
            raise RuntimeError(f"vượt budget ({self.spent}+{tokens}>{self.cap})")
        self.spent += tokens
        return self.spent
```
**Reasoning:** agent loop có thể đốt tiền vô hạn ([[aa05-agentic-pipelines]]) → **budget cap** chặn cứng. `charge` raise khi vượt → dừng agent. Cùng họ rate-limit ([[ac08-ai-cost-scale]]).

---
## Bài 5 — Point-in-time as-of join
**Đề:** Cho `events` (user,ts,amount) + `labels` (user,event_ts), tính "tổng amount TRƯỚC event_ts" mỗi label (chống leakage).
```python
def as_of_sum(events, label_user, label_ts):
    return sum(e["amount"] for e in events
              if e["user"] == label_user and e["ts"] < label_ts)   # CHỈ trước mốc
```
**Reasoning:** point-in-time ([[ac07-feature-store]], [[aj06-case-finance-ai]]): feature dùng data **trước** thời điểm sự kiện (`ts < label_ts`), KHÔNG nhìn tương lai → chống leakage. Dùng `<=` hay `<` tuỳ định nghĩa (có tính chính event đó không).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Code 5 bài, chạy với edge case.
- [ ] Reasoning: route ưu tiên, max-steps fallback, provenance hash, budget cap, as-of `<`.
- [ ] Giới hạn mỗi bài (router cần embedding, ReAct decide là mock).
- 🔭 Tự mò: ghép bài 1+2+4 — router chọn đường, ReAct gọi tool theo đường, Budget charge mỗi bước → "agent có kiểm soát" mini; thêm provenance (bài 3) log mỗi câu. Đó là khung agent an toàn thu nhỏ.

➡️ Tiếp [[an09-ai-review13]] — review 13.
