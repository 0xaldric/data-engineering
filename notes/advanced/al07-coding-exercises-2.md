# AL07 — AI-DE Coding Exercises 2 (bài tập + lời giải)

> 5 bài coding-round (governance/guardrails/data-quality) — **đề + lời giải + reasoning**. Tự code trước. Liên hệ [[ai06-llm-output-governance]], [[aa02-guardrails]], [[ak06-data-labeling]].

---
## Bài 1 — Validate output LLM theo schema (không pydantic)
**Đề:** `valid(d)` trả True nếu dict có `category ∈ {bil,tec,acc}`, `priority ∈ {low,high}`, `confidence ∈ [0,1]`.
```python
def valid(d):
    try:
        return (d.get("category") in {"bil","tec","acc"}
                and d.get("priority") in {"low","high"}
                and isinstance(d.get("confidence"), (int,float))
                and 0 <= d["confidence"] <= 1)
    except Exception:
        return False
```
**Reasoning:** output LLM = dữ liệu không tin được → validate ở **biên** trước downstream ([[ai06-llm-output-governance]]). Enum check + range check + type check. `try/except` vì input có thể méo (không phải dict). Sai → quarantine, không đẩy xuống.

---
## Bài 2 — Redact PII bằng regex
**Đề:** Che email + số điện thoại VN trong text.
```python
import re
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
PHONE = re.compile(r"\b0\d{9}\b")          # 0 + 9 số (VN)
def redact(text):
    text = EMAIL.sub("[EMAIL]", text)
    text = PHONE.sub("[PHONE]", text)
    return text
```
**Reasoning:** PII redact TRƯỚC khi log/gửi API ([[ad03-privacy-compliance]]). Regex bắt pattern; thực tế thêm CCCD/thẻ. ⚠️ regex không hoàn hảo (tên người khó) → kết hợp NER. Redact ở biên (input + trước log).

---
## Bài 3 — Hard-gate data quality
**Đề:** Giữ mẫu nếu QUA hết hard gate (không rỗng, không toxic, không trùng) VÀ độ dài 5-60 từ.
```python
TOXIC = {"ngu","rác"}
def keep(text, seen_set):
    if not text.strip(): return False           # rỗng
    if any(t in text.lower() for t in TOXIC): return False   # toxic
    key = text.lower().strip()
    if key in seen_set: return False            # trùng exact
    n = len(text.split())
    if not (5 <= n <= 60): return False          # độ dài
    seen_set.add(key); return True
```
**Reasoning:** ⭐ hard gate (toxic/dup/rỗng) loại NGAY — không trung bình ([[ae03-training-data-quality]]). Chiều nghiêm trọng = nhị phân; chỉ thêm vào `seen` mẫu GIỮ (để bắt dup tiếp). Trung bình các chiều sẽ để rác lọt.

---
## Bài 4 — Cohen's kappa
**Đề:** Tính kappa giữa 2 list nhãn.
```python
from collections import Counter
def kappa(x, y):
    n = len(x)
    po = sum(1 for a,b in zip(x,y) if a==b)/n
    cx, cy = Counter(x), Counter(y)
    pe = sum((cx[c]/n)*(cy[c]/n) for c in set(x)|set(y))
    return (po-pe)/(1-pe) if pe < 1 else 1.0
```
**Reasoning:** kappa = đồng thuận TRỪ may rủi ([[ak06-data-labeling]]). `po` quan sát, `pe` kỳ vọng do ngẫu nhiên (tích phân phối). Quan trọng hơn accuracy thô vì lộ annotator đoán bừa (kappa~0 dù accuracy cao).

---
## Bài 5 — Self-consistency check (so FACT không so cosine)
**Đề:** Cho N câu trả lời, trích năm (4 chữ số); nếu các năm MÂU THUẪN → cờ "có thể bịa".
```python
import re
def consistent(answers):
    years = set()
    for a in answers:
        years |= set(re.findall(r"\b(?:19|20)\d{2}\b", a))
    return len(years) <= 1, years        # <=1 năm = không mâu thuẫn
```
**Reasoning:** ⭐ self-consistency phải so **FACT** không so embedding ([[ag02-hallucination-detection]]): câu bịa cùng khuôn khác năm → cosine CAO (đánh lừa) nhưng năm mâu thuẫn → lộ bịa. Trích claim cụ thể (năm/số/entity) + so khớp = đúng cách.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Code cả 5 bài, chạy thử với edge case.
- [ ] Reasoning: vì sao validate ở biên, hard-gate, kappa, so-fact.
- [ ] Nêu giới hạn mỗi bài (regex PII bỏ sót, kappa cần >2 người → Fleiss).
- 🔭 Tự mò: ghép bài 1+2+3 thành "input guardrail": redact PII → check toxic/length → validate schema; chạy trên 5 input (sạch/PII/toxic/rỗng/sai-schema) in quyết định mỗi cái. Đó là tầng guardrail của `ai_product.py` ([[aj03-capstone-integration]]).

➡️ Tiếp [[al08-case-insurance-ai]] — case study bảo hiểm.
