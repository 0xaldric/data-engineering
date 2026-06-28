# AN02 — Agentic Patterns Deep

> Các mẫu thiết kế agent: planner-executor, reflection, tool-use, multi-agent debate. Khi nào dùng cái nào (đa số bài toán đơn giản hơn ta nghĩ). Sâu hơn [[aa05-agentic-pipelines]], [[ac04-multi-agent]], [[am02-prompt-patterns]].

## ⭐ Phổ pattern (từ đơn giản → phức tạp)
```
1. ReAct (1 agent)        : reason -> act (tool) -> observe -> lặp  (mặc định, đa số đủ)
2. Plan-first             : lập KẾ HOẠCH đầy đủ trước -> thực thi từng bước
3. Reflection             : làm -> tự PHÊ -> sửa -> lặp (tăng chất lượng)
4. Planner-Executor       : 1 agent lập kế hoạch, agent khác thực thi
5. Multi-agent debate     : nhiều agent tranh luận -> đồng thuận (giảm sai)
6. Supervisor + workers   : 1 điều phối, nhiều chuyên môn ([[ac04-multi-agent]])
```
→ **Đa số: ReAct 1 agent + tool tốt là ĐỦ**. Phức tạp hơn = đắt + khó debug, chỉ khi cần.

## ⭐ ReAct vs Plan-first
| | ReAct | Plan-first |
|--|-------|-----------|
| Cách | nghĩ-làm xen kẽ, thích nghi | lập kế hoạch trước rồi làm |
| Hợp | task khám phá, kết quả tool ảnh hưởng bước sau | task rõ ràng, nhiều bước độc lập |
| Rủi ro | đi lạc/loop ([[aa05-agentic-pipelines]]) | kế hoạch sai từ đầu → sai hết |
→ ReAct linh hoạt (thích nghi theo observation); plan-first rõ ràng (dễ kiểm trước khi chạy).

## ⭐ Reflection (tự phê — tăng chất lượng)
```
executor làm -> CRITIC chấm ("đúng chưa? thiếu gì? lỗi gì?") -> executor sửa -> lặp
   vd: viết code -> critic review -> sửa bug -> review lại
```
- Tăng chất lượng đáng kể (bắt lỗi trước khi trả) nhưng **tốn thêm vòng** (cost/latency).
- Critic = self ([[ae01-self-correcting-rag]] cho RAG) hoặc agent/model khác (khách quan hơn).

## ⭐ Multi-agent debate (giảm sai)
```
câu khó -> agent A trả lời + agent B trả lời -> tranh luận (chỉ ra lỗi của nhau)
   -> đồng thuận / agent thứ 3 phán xử
-> nhiều góc nhìn -> giảm sai 1 chiều (như ensemble [[g08-probabilistic-ds]])
```
→ Cho task khó/cao rủi ro; đắt (nhiều LLM call) → chỉ khi đáng. Cùng họ self-consistency ([[am02-prompt-patterns]]).

## ⭐ Tool-use patterns (quan trọng nhất thực tế)
| Pattern | Ý |
|---------|---|
| **Tool selection** | mô tả tool rõ → agent chọn đúng ([[ac04-multi-agent]]) |
| **Error recovery** | tool lỗi → lỗi có cấu trúc → agent thử lại/đổi cách |
| **Tool result caching** | cache kết quả tool lặp ([[ad08-semantic-cache]]) |
| **Confirmation** | hành động nguy hiểm → human approve ([[ad04-llm-security]]) |
→ Agent mạnh = **tool tốt** > pattern phức tạp ([[ac04-multi-agent]] "tool tốt > nhiều agent").

## Vai trò DE
- **Tool = data access** có governance (scope/quyền/idempotent) ([[ag05-agent-platform]]).
- **State/checkpoint** để resume ([[ad07-agent-data]]); **trace** mọi bước ([[ab06-llm-observability]]).
- **Budget cap** + max-steps chống loop ([[aa05-agentic-pipelines]]); **eval** task success rate.

## Cạm bẫy
- **Multi-agent vì "ngầu"** → đa số ReAct 1 agent đủ → đơn giản trước.
- **Reflection vô hạn** → loop/cost → giới hạn vòng.
- **Plan-first cho task khám phá** → kế hoạch sai từ đầu → ReAct.
- **Debate cho task dễ** → đốt tiền vô ích → chỉ task khó.
- **Tool mô tả tệ** → agent chọn sai (lỗi gốc, không phải model) → mô tả rõ.
- **Không max-steps/budget** → loop đốt tiền → cap.
- **Không trace** → multi-agent thành hộp đen → log mọi bước.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 6 pattern; đa số ReAct 1 agent đủ.
- [ ] ReAct (thích nghi) vs plan-first (rõ ràng).
- [ ] Reflection (tự phê tăng chất lượng); debate (nhiều góc giảm sai).
- [ ] Tool-use patterns (selection/error-recovery/cache/confirm) — tool tốt > pattern phức tạp.
- [ ] Cạm bẫy: multi-agent thừa, reflection loop, không cap.
- 🔭 Tự mò: viết ReAct mini — agent giả: nghĩ → chọn tool (`text_to_sql` hay `rag_over_notes` theo `query_router` [[an01-rag-advanced-patterns]]) → quan sát kết quả → trả lời; thêm reflection: critic kiểm output hợp lệ ([[ai06-llm-output-governance]]), không thì làm lại 1 lần; log mỗi bước + max_steps=3.

➡️ Tiếp [[an03-case-telecom-ai]] — case study viễn thông.
