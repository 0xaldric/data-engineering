# AA01 — Text-to-SQL / NL2SQL Pipeline ⭐

> "Hỏi tự nhiên → SQL" đang phổ biến (BI copilot, chatbot data). Vai trò DE: **bọc lớp an toàn** quanh SQL do LLM sinh — không tin mù quáng. Code chạy được: [`text_to_sql.py`](../../projects/06-ai-data-engineering/text_to_sql.py).

## Vì sao DE quan trọng ở đây (không chỉ "gọi LLM")
LLM sinh SQL có thể: sai cú pháp, sai cột, **nguy hiểm** (DROP/DELETE), trả triệu dòng, lộ dữ liệu. DE xây pipeline **đáng tin** quanh nó — đúng nghề DE, chỉ input là NL.

## Pipeline (đã triển khai, chạy được)
```
Câu hỏi NL
   │ 1. SCHEMA LINKING (đưa schema context: bảng/cột nào có)
   ▼
LLM sinh SQL
   │ 2. GUARDRAIL (chỉ SELECT; chặn DROP/DELETE/UPDATE/...; 1 câu lệnh; ép LIMIT)
   ▼ block?
   │ 3. VALIDATE (EXPLAIN/parse TRƯỚC khi chạy — bắt sai cú pháp/cột)
   ▼ invalid?
   │ 4. SANDBOX EXECUTE (read-only: chỉ VIEW, không quyền ghi)
   ▼
Kết quả (+ citation SQL đã chạy)
```
Demo (5 câu): 3 câu hợp lệ → SQL đúng (revenue/category, top khách, count) chạy ra số khớp; **2 câu độc (DROP, UPDATE) bị guardrail CHẶN**.

## Các thành phần (mỗi cái là skill)
### 1. Schema linking
LLM cần biết schema để sinh SQL đúng cột/bảng. Đưa **schema context** (tên bảng/cột, quan hệ, ví dụ giá trị) vào prompt. Schema lớn → chọn lọc bảng liên quan (retrieval trên schema). Liên hệ semantic layer ([[e05-semantic-layer]]) để LLM hiểu "doanh thu" = gì.

### 2. ⭐ Guardrail (an toàn — quan trọng nhất)
```python
DANGER = r"\b(drop|delete|update|insert|alter|attach|truncate|grant|copy)\b"
# chỉ cho SELECT/WITH; chặn DANGER; 1 câu lệnh (chặn ';'); ép LIMIT
```
- **Read-only**: chặn mọi lệnh sửa/xoá (LLM "ngây thơ" hoặc bị prompt-inject sinh `DROP TABLE`).
- **Single statement**: chặn `;` (SQL injection nhiều lệnh).
- **LIMIT**: tránh trả về triệu dòng (cost/timeout).
- Mạnh hơn: chạy bằng **user DB chỉ có quyền SELECT** trên view được phép (defense in depth).

### 3. Validate trước khi chạy
`EXPLAIN <sql>` parse + kiểm cột tồn tại **không thực thi** → bắt lỗi sớm, không chạy SQL rác trên warehouse.

### 4. Sandbox execution
Chạy trong môi trường **read-only**, timeout, row limit. Không cho LLM-SQL đụng dữ liệu thật với quyền ghi.

### 5. Eval (text-to-SQL có đúng không?)
- **Execution accuracy**: SQL chạy ra kết quả đúng (so với golden SQL/answer).
- **Exact/semantic match** SQL.
- Golden set (NL → SQL đúng) → regression khi đổi model/prompt ([[ai05-retrieval-eval]]).

## ⚠️ Cạm bẫy
- Chạy thẳng SQL của LLM không guardrail → DROP/DELETE/lộ data.
- Không validate → SQL rác chạy trên prod warehouse (cost/lock).
- Không LIMIT → trả triệu dòng.
- Schema context thiếu → LLM "bịa" cột → sai.
- Tin "LLM tự tin" → vẫn phải eval execution accuracy.
- Quên quyền DB (defense in depth) — guardrail regex có thể lách; user read-only là lớp cuối.

## ✅ "Tự kiểm tra & tự mò"
- [ ] 4 lớp: schema linking → guardrail → validate → sandbox.
- [ ] Guardrail chặn gì (read-only, single-statement, LIMIT) + defense in depth (user read-only).
- [ ] Eval = execution accuracy + golden set.
- 🔭 Chạy `python projects/06-ai-data-engineering/text_to_sql.py`; thêm câu hỏi + SQL độc mới (vd `ATTACH`) xem guardrail bắt; thử SQL sai cột xem validate chặn.

➡️ Tiếp: [[aa02-guardrails]].
