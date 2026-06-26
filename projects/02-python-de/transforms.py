"""Pure transform logic — tách khỏi I/O để TEST được.

Nguyên tắc: hàm transform nên là **pure** (input -> output, không đọc file/gọi
mạng, không side-effect) → dễ test, dễ tái dùng, dễ suy luận. I/O (đọc/ghi)
để ở lớp ngoài (etl_pipeline.py).

Gồm: validation schema bằng pydantic + vài hàm transform thuần trên pandas.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator


# ---------------------------------------------------------------------
# 1) Schema validation với pydantic (bắt dữ liệu bẩn ngay cửa ngõ)
# ---------------------------------------------------------------------
class OrderItemRecord(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    discount: float = 0.0

    @field_validator("quantity")
    @classmethod
    def _qty_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("quantity must be > 0")
        return v

    @field_validator("unit_price")
    @classmethod
    def _price_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("unit_price must be >= 0")
        return v

    @field_validator("discount")
    @classmethod
    def _discount_range(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError("discount must be within [0, 1]")
        return v


@dataclass
class ValidationResult:
    valid: list[OrderItemRecord] = field(default_factory=list)
    errors: list[tuple[int, str]] = field(default_factory=list)  # (index, message)

    @property
    def n_valid(self) -> int:
        return len(self.valid)

    @property
    def n_errors(self) -> int:
        return len(self.errors)


def validate_records(records: list[dict]) -> ValidationResult:
    """Chia records thành hợp lệ / lỗi — KHÔNG raise, gom lỗi để xử lý mềm."""
    result = ValidationResult()
    for i, rec in enumerate(records):
        try:
            result.valid.append(OrderItemRecord(**rec))
        except ValidationError as exc:
            msg = "; ".join(e["msg"] for e in exc.errors())
            result.errors.append((i, msg))
    return result


# ---------------------------------------------------------------------
# 2) Pure transform functions
# ---------------------------------------------------------------------
def compute_line_total(unit_price: float, quantity: int, discount: float = 0.0) -> float:
    """Thành tiền 1 dòng hàng = giá * số lượng * (1 - chiết khấu), làm tròn 2 số."""
    if quantity <= 0:
        raise ValueError("quantity must be > 0")
    if not 0.0 <= discount <= 1.0:
        raise ValueError("discount must be within [0, 1]")
    return round(unit_price * quantity * (1.0 - discount), 2)


def price_tier(price: float) -> str:
    """Phân hạng giá. Ranh giới: >=200 premium, >=50 mid, còn lại budget."""
    if price >= 200:
        return "premium"
    if price >= 50:
        return "mid"
    return "budget"


def revenue_by_category(items: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Doanh thu theo category. Pure: chỉ nhận DataFrame, trả DataFrame.

    Tránh fan-out: line_total ở grain item nên sum trực tiếp an toàn.
    """
    merged = items.merge(products[["product_id", "category"]], on="product_id", how="inner")
    out = (merged.groupby("category", as_index=False)["line_total"].sum()
           .rename(columns={"line_total": "revenue"})
           .sort_values("revenue", ascending=False, ignore_index=True))
    out["revenue"] = out["revenue"].round(2)
    return out
