"""LLM-as-data-producer Governance — pipeline cho dữ liệu LLM sinh ra.

Bài toán AI-era: LLM trích xuất dữ liệu CÓ CẤU TRÚC từ text thô (nhãn, JSON, tóm tắt)
rồi đổ vào bảng production. Khác ETL: output KHÔNG TẤT ĐỊNH (cùng input có thể khác output,
đôi khi JSON lỗi/thiếu field/sai enum). DE phải: validate → repair → quarantine → log provenance.

Chạy: python projects/06-ai-data-engineering/llm_output_pipeline.py
(Mô phỏng LLM bằng hàm local — KHÔNG cần API key. Logic governance là thật.)
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from pydantic import BaseModel, ValidationError, field_validator

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed" / "llm_pipeline"
OUT.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "mock-llm-v1"
PROMPT_VERSION = "ticket-extract@2024-06"
CATEGORIES = {"billing", "technical", "account", "other"}
PRIORITIES = {"low", "medium", "high"}


# --------------------------- Data contract (pydantic) ----------------
class TicketExtraction(BaseModel):
    """Schema/contract cho output LLM — bắt dữ liệu bẩn ngay cửa ngõ."""
    category: str
    priority: str
    sentiment: str
    confidence: float
    summary: str

    @field_validator("category")
    @classmethod
    def _cat(cls, v):
        if v not in CATEGORIES:
            raise ValueError(f"category '{v}' không thuộc {CATEGORIES}")
        return v

    @field_validator("priority")
    @classmethod
    def _pri(cls, v):
        if v not in PRIORITIES:
            raise ValueError(f"priority '{v}' không hợp lệ")
        return v

    @field_validator("confidence")
    @classmethod
    def _conf(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError("confidence phải trong [0,1]")
        return v


# --------------------------- Mock LLM (non-deterministic, đôi khi lỗi) -
TICKETS = [
    "Tôi bị tính phí hai lần tháng này, hoàn tiền giúp!",            # billing
    "App crash mỗi khi mở dashboard, rất bực.",                      # technical
    "Quên mật khẩu, không đăng nhập được.",                          # account
    "Cảm ơn team, dịch vụ tuyệt vời.",                               # other (positive)
    "Hóa đơn sai số tiền, cần xem lại gấp.",                         # billing
    "Tính năng export không hoạt động.",                            # technical
    "Muốn đổi email tài khoản.",                                     # account
    "Trang thanh toán load mãi không xong.",                        # billing/technical
]


def mock_llm(text: str, i: int) -> str:
    """Mô phỏng LLM trả JSON — CỐ Ý tạo lỗi đa dạng để minh hoạ governance.
    Trả về CHUỖI thô (như LLM thật), không phải dict."""
    base = {
        "category": "billing", "priority": "high", "sentiment": "negative",
        "confidence": 0.88, "summary": text[:40],
    }
    # các kiểu output thực tế gặp ở LLM:
    if i == 1:   # bọc trong markdown fence ```json ... ```
        return "```json\n" + json.dumps({**base, "category": "technical"}) + "\n```"
    if i == 2:   # kèm chữ thừa quanh JSON
        return "Đây là kết quả: " + json.dumps({**base, "category": "account"}) + " (hết)"
    if i == 3:   # sai enum (category không hợp lệ)
        return json.dumps({**base, "category": "feedback", "sentiment": "positive"})
    if i == 4:   # thiếu field (mất 'summary')
        d = {**base}; d.pop("summary"); return json.dumps(d)
    if i == 5:   # confidence ngoài [0,1]
        return json.dumps({**base, "confidence": 1.4})
    if i == 6:   # JSON hỏng (không parse được)
        return '{"category": "account", "priority": "low", ...'
    return json.dumps({**base, "category": "billing", "priority": "medium"})  # hợp lệ


# --------------------------- Parse + Repair --------------------------
def extract_json(raw: str) -> dict | None:
    """Bóc JSON khỏi output thô (LLM hay kèm fence/chữ thừa)."""
    s = raw.strip()
    if "```" in s:                       # bỏ markdown fence
        s = s.split("```")[1].replace("json", "", 1).strip() if s.count("```") >= 2 else s
    start, end = s.find("{"), s.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(s[start:end + 1])
    except json.JSONDecodeError:
        return None


def repair(d: dict) -> dict:
    """Sửa nhẹ output (như "retry with fix" / heuristic). Trả dict đã vá."""
    d = dict(d)
    if d.get("category") == "feedback":          # map enum sai → 'other'
        d["category"] = "other"
    if isinstance(d.get("confidence"), (int, float)):
        d["confidence"] = max(0.0, min(1.0, d["confidence"]))   # clamp về [0,1]
    return d


# --------------------------- Pipeline --------------------------------
def run() -> None:
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    valid, quarantine, provenance = [], [], []

    for i, text in enumerate(TICKETS):
        raw = mock_llm(text, i)
        in_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        status, record, err = "valid", None, None

        parsed = extract_json(raw)
        if parsed is None:
            status, err = "quarantine_parse", "JSON không parse được"
        else:
            try:                                   # validate theo contract
                record = TicketExtraction(**parsed).model_dump()
            except ValidationError as e:
                fixed = repair(parsed)             # thử REPAIR rồi validate lại
                try:
                    record = TicketExtraction(**fixed).model_dump()
                    status = "repaired"
                except ValidationError:
                    status, err = "quarantine_schema", str(e).splitlines()[0][:60]

        # PROVENANCE: ai (model+prompt) sinh, từ input nào, khi nào, trạng thái
        provenance.append({
            "input_hash": in_hash, "model": MODEL_NAME, "prompt_version": PROMPT_VERSION,
            "status": status, "ts": now, "error": err,
        })
        if record is not None:
            record.update({"_input_hash": in_hash, "_model": MODEL_NAME, "_status": status})
            valid.append(record)
        else:
            quarantine.append({"input_hash": in_hash, "raw": raw[:60], "error": err})

    # LOAD: bảng production (valid) + quarantine + provenance log
    (OUT / "extractions.json").write_text(json.dumps(valid, ensure_ascii=False, indent=2))
    (OUT / "quarantine.json").write_text(json.dumps(quarantine, ensure_ascii=False, indent=2))
    (OUT / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2))

    # Report
    from collections import Counter
    by_status = Counter(p["status"] for p in provenance)
    print(f"== LLM output pipeline ({len(TICKETS)} inputs) ==")
    print("  trạng thái:", dict(by_status))
    print(f"  -> production: {len(valid)} (gồm {by_status.get('repaired',0)} đã repair) | "
          f"quarantine: {len(quarantine)}")
    print("\n  Bảng production (valid + repaired):")
    for r in valid:
        print(f"    [{r['_status']:8s}] {r['category']:9s} {r['priority']:6s} conf={r['confidence']:.2f} :: {r['summary'][:32]}")
    print("\n  Quarantine (cần xem tay / human-in-the-loop):")
    for q in quarantine:
        print(f"    {q['input_hash']} -> {q['error']}")
    print("\n  Provenance mẫu:", provenance[0])
    print("\nDONE ✅ governance pipeline chạy xong. (Output ở data/processed/llm_pipeline/)")


if __name__ == "__main__":
    run()
