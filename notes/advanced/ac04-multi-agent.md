# AC04 — Agentic sâu: Multi-agent & Tool Design

> Nhiều agent phối hợp (planner/executor/critic) + thiết kế **tool** tốt. Cảnh báo: đa số bài toán **1 agent + tool là đủ** — multi-agent đắt và khó. Sâu hơn [[aa05-agentic-pipelines]], [[ab03-context-engineering]].

## Một agent vs nhiều agent — quyết định trước
| Dùng | Khi |
|------|-----|
| **1 agent + tools** (mặc định) | hầu hết: task tuần tự, 1 vai trò, vài tool. Đơn giản, rẻ, dễ debug |
| **Multi-agent** | task **phân tách rõ vai trò**, cần **chuyên môn hoá** hoặc **chạy song song** nhánh độc lập |
> ⚠️ Multi-agent **nhân chi phí & độ trễ & lỗi** (mỗi agent vài lời gọi LLM; lỗi lan; context đồng bộ khó). **Đừng dùng cho ngầu** — chỉ khi tách vai trò thật sự giúp.

## ⭐ Các mẫu orchestration
```
PLANNER → EXECUTOR        : planner chia kế hoạch ─> executor làm từng bước
SUPERVISOR (router)       : 1 agent điều phối, gọi sub-agent chuyên môn theo nhu cầu
PIPELINE (tuần tự)        : agent A ─> B ─> C, mỗi cái 1 khâu (như ETL)
PARALLEL + AGGREGATOR     : nhiều agent chạy nhánh độc lập ─> gộp kết quả
CRITIC / REFLECTION       : executor làm ─> critic chấm/bắt lỗi ─> sửa (self-correct)
```
- **Supervisor** phổ biến nhất: 1 "não" điều phối, sub-agent là "tool cấp cao".
- **Critic** tăng chất lượng (bắt lỗi trước khi trả) nhưng tốn thêm vòng.

## ⭐⭐ Thiết kế TOOL tốt (quan trọng hơn số agent)
Agent chỉ mạnh bằng **tool** nó có. Tool tốt = agent giỏi.
| Nguyên tắc | Vì sao |
|-----------|--------|
| **Tên + mô tả rõ** | LLM chọn tool dựa vào mô tả; mơ hồ → chọn sai |
| **Input schema chặt** | typed params, validate ([[ai06-llm-output-governance]]) → ít gọi sai |
| **Output gọn, có cấu trúc** | trả JSON nhỏ; tránh nhồi context ([[ab03-context-engineering]]) |
| **Lỗi rõ ràng** | "thiếu param X" để agent tự sửa, không "Error 500" mù |
| **Idempotent / an toàn** | tool ghi dữ liệu phải an toàn khi gọi lại; phân biệt read vs write |
| **Ít mà tinh** | 50 tool → agent rối; gộp thành vài tool mạnh |
→ **Vai trò DE**: tool thường là **cổng truy cập data có kiểm soát** (query metric [[ab04-semantic-layer-llm]], search [[ai02-rag-capstone-writeup]], đọc/ghi store) — bạn thiết kế cổng an toàn, không để agent chạm thẳng DB.

## ⭐ Error recovery & độ bền
```
tool lỗi ─> trả lỗi có cấu trúc ─> agent thử lại / đổi cách / hỏi người
vòng lặp vô tận ─> giới hạn số bước (max steps) + timeout
hành động nguy hiểm (xoá/ghi/tiền) ─> human-in-the-loop approve ([[aa05-agentic-pipelines]])
chi phí phình ─> budget cap (token/$/số tool-call)
```
Bền = **giả định mọi bước có thể fail**, có đường lui (retry/fallback/escalate) — đúng tư duy pipeline ([[i07-backfill-reprocessing]]).

## Vai trò DE trong multi-agent
- **Tool = data access layer** có governance (quyền, PII, rate limit).
- **State/memory store** chia sẻ giữa agent ([[ab03-context-engineering]] long-term memory).
- **Trace mọi agent + tool-call** ([[ab06-llm-observability]]) — debug multi-agent rất khó nếu không trace.
- **Cost/eval gate** ([[ac03-eval-driven-dev]]): đo agent có hoàn thành task không (task success rate), tốn bao nhiêu.

## Cạm bẫy
- **Multi-agent vì "nghe ngầu"** → đa số chỉ cần 1 agent + tool tốt; phức tạp thừa.
- **Tool mô tả tệ** → agent chọn/gọi sai → lỗi gốc, không phải do "model ngu".
- **Không giới hạn bước/budget** → loop vô tận đốt tiền ([[aa05-agentic-pipelines]]).
- **Agent chạm thẳng DB/API nguy hiểm** → phải qua tool có guardrail ([[aa02-guardrails]]).
- **Không trace** → multi-agent thành hộp đen, không debug nổi.
- **Context bùng nổ**: nhiều agent trao đổi dài → "lost in middle" + tốn token → nén/tóm tắt.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Khi nào 1 agent đủ vs khi nào multi-agent (mặc định 1 agent).
- [ ] 5 mẫu orchestration (planner/supervisor/pipeline/parallel/critic).
- [ ] 6 nguyên tắc tool tốt; tool = data access layer có governance.
- [ ] Error recovery: max steps, budget cap, human approve, lỗi có cấu trúc.
- [ ] Vai trò DE: tool/state/trace/cost-eval.
- 🔭 Tự mò: ghép có kỷ luật — agent "supervisor" giả: nhận câu hỏi → quyết định gọi `text_to_sql.py` (số liệu) hay `rag_over_notes.py` (giải thích) → trả kết quả; thêm "critic" kiểm output hợp lệ (dùng `llm_output_pipeline` validate). Đó là multi-agent mini bằng các script đã có.

➡️ Tiếp [[ac05-voice-audio-pipeline]] — pipeline dữ liệu audio/voice.
