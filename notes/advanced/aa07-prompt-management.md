# AA07 — Prompt Management & Versioning

> Prompt là **"config" điều khiển hành vi LLM** — đổi prompt = đổi output. Phải quản như code/schema, không sửa tuỳ tiện trong code. Liên hệ [[ai06-llm-output-governance]], [[13-logging-config]].

## Vì sao prompt cần quản lý nghiêm
- Đổi 1 từ trong prompt → output đổi (đôi khi đột ngột) → như đổi business logic.
- Prompt rải rác trong code, hardcode, không version → không reproduce/rollback/audit.
- Nhiều prompt + nhiều version + nhiều model → hỗn loạn nếu không quản.
→ Prompt = **artifact** cần version, test, review như code (tách khỏi code, như config — [[13-logging-config]]).

## Prompt as Code
- Prompt trong **git** (không hardcode trong code logic), review qua PR.
- **Template + variable**: tách khung prompt khỏi dữ liệu chèn vào.
```python
TEMPLATE = """Bạn là trợ lý phân loại ticket. Chỉ trả JSON đúng schema.
Category phải thuộc: {categories}.
Ticket: {ticket}"""
prompt = TEMPLATE.format(categories=CATS, ticket=text)
```
- Tránh prompt injection: tách rõ "instruction" (cố định) vs "data" (user input) — [[aa02-guardrails]].

## ⭐ Versioning & lineage
Mỗi output lưu **prompt_version + model + input → output** (provenance — [[ai06-llm-output-governance]]):
- **Reproduce**: tái dựng output cần biết prompt+model nào.
- **Rollback**: prompt mới tệ → quay version cũ.
- **A/B**: chạy v1 vs v2 trên traffic → so metric.
- **Audit**: output này do prompt nào sinh.
SemVer cho prompt (như contract — [[k06-data-contract-impl]]): patch (chỉnh chữ), minor (thêm hướng dẫn), major (đổi format output → breaking cho downstream).

## Prompt Registry
Kho prompt tập trung (như feature store/model registry): tên + version + metadata + metric. Ứng dụng lấy prompt theo `name@version` thay vì hardcode. Công cụ: LangSmith, PromptLayer, Langfuse, hoặc tự build (git + DB).

## ⭐ Regression khi đổi prompt
Đổi prompt → **chạy eval** (golden set — [[aa06-llm-eval]]) trước khi deploy:
```
sửa prompt → eval (faithfulness/accuracy trên golden) → metric không tụt? → deploy
                                                       → tụt? → giữ version cũ
```
Như CI cho code: prompt change = code change → test + gate. Không "sửa prompt thẳng prod".

## A/B test prompt
Chạy 2 prompt song song trên traffic thật → so metric (accuracy, faithfulness, user feedback, cost) → chọn thắng. Cần versioning + online eval ([[aa06-llm-eval]]).

## ⚠️ Cạm bẫy
- Hardcode prompt trong code logic → không version/test/reuse.
- Sửa prompt thẳng prod không eval → tụt chất lượng (regression).
- Không lưu prompt_version với output → không reproduce/audit.
- Đổi prompt major (đổi format output) mà downstream không biết → vỡ (breaking — cần contract).
- Prompt trộn instruction + user data → injection.
- Không A/B → đổi prompt theo cảm tính.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao prompt = config cần version (đổi prompt = đổi logic).
- [ ] Prompt as code (git, template/variable, tách instruction/data).
- [ ] Versioning + lineage (reproduce/rollback/audit/A-B); SemVer.
- [ ] Regression eval khi đổi prompt; prompt registry.
- 🔭 Trong `llm_output_pipeline.py`, đổi `PROMPT_VERSION` khi sửa "prompt" (template phân loại); lưu version vào provenance (đã có) → thấy lineage prompt→output.

➡️ Tiếp: [[aa08-multimodal]].
