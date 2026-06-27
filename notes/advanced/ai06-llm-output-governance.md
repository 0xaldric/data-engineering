# AI06 — LLM-as-Data-Producer Governance ⭐⭐

> **Gap quan trọng nhất** của DE thời LLM: dữ liệu **do LLM sinh ra** (nhãn, JSON, tóm tắt, thực thể) đổ thẳng vào bảng production. Code chạy được: [`llm_output_pipeline.py`](../../projects/06-ai-data-engineering/llm_output_pipeline.py).

## Vì sao khó hơn ETL truyền thống
| | ETL nguồn truyền thống | Dữ liệu LLM sinh |
|--|------------------------|------------------|
| Tất định | có (cùng input → cùng output) | **KHÔNG** (cùng input có thể khác output) |
| Format | schema cố định | JSON đôi khi lỗi/thiếu field/kèm chữ thừa/sai enum |
| Đúng/sai | rõ | **mơ hồ** (đúng cú pháp nhưng sai ngữ nghĩa / hallucination) |
| Version | schema version | model + prompt + output đều có thể đổi |
→ Cần một **lớp governance** giữa LLM và bảng production. DE sở hữu lớp này.

## Pipeline governance (đã triển khai, chạy được)
```
LLM output (raw, có thể lỗi)
   │ 1. PARSE (bóc JSON khỏi markdown fence / chữ thừa)
   ▼
   │ 2. VALIDATE theo CONTRACT (pydantic: schema + enum + range)
   ▼ fail?
   │ 3. REPAIR (sửa nhẹ / retry: map enum sai, clamp confidence) → validate lại
   ▼ vẫn fail?
   │ 4. QUARANTINE (tách ra, human-in-the-loop review)
   ▼ pass
   PRODUCTION TABLE  ──(+ PROVENANCE log: model + prompt_version + input_hash + status + ts)──►
```
Kết quả demo (8 input): **4 valid, 2 repaired, 2 quarantine** → chỉ 6 dòng sạch vào production; 2 dòng xấu cách ly.

## ⭐ Các thành phần (mỗi cái là một skill)
### 1. Data contract cho output LLM
Định nghĩa schema bằng **pydantic** (hoặc JSON Schema) — bắt dữ liệu bẩn ngay cửa ngõ ([[k06-data-contract-impl]], [[12-testing-de]]):
```python
class TicketExtraction(BaseModel):
    category: str   # validator: phải thuộc {billing, technical, account, other}
    priority: str   # validator: {low, medium, high}
    confidence: float  # validator: [0, 1]
    summary: str
```
LLM trả `category="feedback"` (sai enum) hay `confidence=1.4` → **bị chặn**.

### 2. Parse + Repair (LLM hay trả "bẩn")
LLM thật trả: ```` ```json ... ``` ````, kèm "Đây là kết quả: {...}", thiếu field, JSON hỏng. → bóc JSON + repair heuristic (map enum gần đúng, clamp số) + **retry** (gọi lại với prompt sửa). Repair được thì cứu; không thì quarantine.

### 3. Quarantine + Human-in-the-loop
Dòng không validate được → bảng `quarantine` (không vào production) + cờ cho người review. Không "fail cả pipeline" (soft validation — [[60-data-quality]]), không để rác xuống dashboard.

### 4. ⭐ Provenance / Versioning (lineage LLM-era)
Lưu cho MỖI output: **model + prompt_version + input_hash + status + timestamp**. Vì sao:
- **Reproducibility**: output này do model/prompt nào sinh? (cùng input khác output → phải biết version).
- **Drift**: nâng cấp model → output đổi → so version cũ/mới.
- **Audit**: dòng này đáng tin không (status: valid/repaired/quarantined)?
- Gần bitemporal ([[e04-bitemporal]]): "cái gì được sinh, khi nào, bởi model nào".

## Drift khi model nâng cấp
Đổi LLM version → cùng input ra output khác (phân phối nhãn đổi, format đổi) → cần:
- Theo dõi phân phối output (% mỗi category) theo thời gian → alert nếu lệch ([[k07-observability-tooling]]).
- Re-validate contract (model mới có giữ schema không).
- A/B model cũ vs mới trên golden set.

## ⚠️ Cạm bẫy
- Đổ thẳng output LLM vào production không validate → JSON lỗi/sai enum làm vỡ dashboard.
- Không lưu provenance (model+prompt) → không reproduce/audit được.
- "Repair" quá tay (đoán bừa) → tạo dữ liệu sai tinh vi.
- Không quarantine → 1 record xấu chặn cả batch hoặc lọt rác.
- Quên drift khi model nâng cấp (output đổi âm thầm).
- Tin confidence của LLM mù quáng (LLM "tự tin" cả khi sai).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao dữ liệu LLM cần lớp governance (non-deterministic + format bẩn).
- [ ] 4 bước: parse → validate (contract) → repair → quarantine + provenance.
- [ ] Provenance gồm gì & vì sao (reproduce/drift/audit).
- 🔭 Chạy `python projects/06-ai-data-engineering/llm_output_pipeline.py`; thêm 1 kiểu lỗi mới vào `mock_llm` (vd priority sai) xem pipeline xử lý; xem `data/processed/llm_pipeline/provenance.json`.

➡️ Tiếp: [[ai07-testing-nondeterministic]].
