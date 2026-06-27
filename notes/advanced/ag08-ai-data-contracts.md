# AG08 — Data Contracts cho AI I/O & Schema Evolution

> Hợp đồng dữ liệu cho **đầu vào/ra của AI**: schema output LLM, version prompt+schema, breaking change phá downstream. Mở rộng data contract kinh điển ([[k06-data-contract-impl]]) cho thế giới AI phi-quyết-định. Liên hệ [[ai06-llm-output-governance]], [[aa07-prompt-management]].

## Vì sao AI I/O cần contract (gắt hơn data thường)
- Output LLM **không xác định** ([[ai07-testing-nondeterministic]]) → downstream (code/DB/API) cần **đảm bảo cấu trúc** mới dùng được.
- Đổi prompt/model → output đổi hình dạng ngầm → **phá downstream** mà không ai báo.
- → Contract = "LLM phải trả đúng schema này; đổi schema = breaking change phải quản".

## ⭐ Contract cho OUTPUT LLM
```
prompt yêu cầu JSON: {category: enum, priority: enum, confidence: float[0,1]}
   ─> LLM trả ─> VALIDATE theo schema (pydantic [[ai06-llm-output-governance]])
        ├─ hợp lệ ─> downstream dùng (an toàn)
        └─ sai ─> repair / quarantine (KHÔNG đẩy rác xuống downstream)
```
→ Schema = **hợp đồng**: producer (LLM) hứa trả đúng; consumer (code) tin tưởng. Validate là "biên giới" thực thi hợp đồng.

## ⭐ Versioning prompt + schema cùng nhau
Prompt và schema output **gắn chặt** — đổi prompt thường đổi output:
```
prompt v1 -> schema v1 (category, priority)
prompt v2 -> schema v2 (category, priority, SENTIMENT mới)   <- thêm field
```
- Version **cả hai cùng** ([[aa07-prompt-management]]): "output này từ prompt v2 + schema v2".
- Lineage: output → prompt version → schema version → debug/audit ([[af06-ai-data-governance]]).

## ⭐ Breaking vs Non-breaking change (như API/Avro)
| Loại | Ví dụ | An toàn? |
|------|-------|----------|
| **Non-breaking** | thêm field OPTIONAL, thêm enum value mới (consumer bỏ qua) | ✅ backward compat |
| **Breaking** | xoá/đổi tên field, đổi kiểu, bỏ enum value đang dùng | ❌ phá downstream |
→ Giống **schema evolution** Avro/Protobuf ([[../10-json-avro.md|json-avro]]): thêm optional OK, xoá/đổi = breaking. AI thừa hưởng nguyên tắc này.

## ⭐ Quản breaking change (đừng phá ngầm)
```
muốn đổi schema output (breaking) ─> 
   1. version mới (v2) song song v1 (đừng đổi tại chỗ)
   2. consumer migrate dần sang v2
   3. contract TEST: chạy mẫu, validate output v2 đúng schema v2 ([[af07-continuous-eval]] style)
   4. deprecate v1 khi hết consumer
```
- **Contract test**: CI chạy prompt → validate output đúng schema → đổi prompt mà phá schema = test fail (như [[af07-continuous-eval]] gate).
- Backward compat: giữ field cũ, thêm field mới optional → consumer cũ vẫn chạy.

## Contract cho INPUT (RAG/agent)
- **Context contract**: chunk đưa vào prompt đúng định dạng (có nguồn, độ dài giới hạn).
- **Tool I/O contract**: agent gọi tool đúng schema input, tool trả đúng schema output ([[ag05-agent-platform]] registry).
- **Embedding contract**: cùng model/version cho index + query ([[ai04-embedding-versioning]]).

## Cạm bẫy
- **Không validate output** → rác xuống downstream → validate ở biên ([[ai06-llm-output-governance]]).
- **Đổi schema tại chỗ** (breaking) → phá consumer ngầm → version song song + migrate.
- **Prompt/schema version rời rạc** → không truy được output từ đâu → version cùng nhau.
- **Không contract test** → đổi prompt phá schema không ai biết → CI gate.
- **Coi enum mở rộng là an toàn luôn** → thêm enum value mà consumer không xử lý → vẫn cần check.
- **Quên embedding contract** → query model khác index model → cosine vô nghĩa ([[ai04-embedding-versioning]]).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao AI I/O cần contract (output non-det + đổi prompt phá downstream).
- [ ] Schema output = hợp đồng; validate ở biên (repair/quarantine).
- [ ] Version prompt + schema cùng nhau; lineage output→prompt→schema.
- [ ] Breaking vs non-breaking (như Avro); quản breaking = version song song + contract test.
- [ ] Contract input: context/tool/embedding.
- 🔭 Tự mò: mở rộng `llm_output_pipeline.py` — định nghĩa schema v1 + v2 (v2 thêm field `sentiment` optional); chạy output cũ qua cả hai → v1 pass, v2 pass (backward compat); thử "breaking" (đổi `priority` từ enum sang int) → thấy output cũ fail validate v2 = breaking change bắt được.

➡️ Tiếp [[ag09-ai-review7]] — review 7 + tổng kết Module AI.
