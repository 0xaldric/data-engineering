"""Unit tests cho transforms.py — chạy: pytest projects/02-python-de -q"""
from __future__ import annotations

import pandas as pd
import pytest

from transforms import (
    compute_line_total,
    price_tier,
    revenue_by_category,
    validate_records,
)


# --------------------------- compute_line_total ----------------------
class TestComputeLineTotal:
    def test_basic_no_discount(self):
        assert compute_line_total(100.0, 2) == 200.0

    def test_with_discount(self):
        assert compute_line_total(100.0, 2, 0.1) == 180.0

    def test_rounding_to_2dp(self):
        # 9.99 * 3 = 29.97 (kiểm tra làm tròn)
        assert compute_line_total(9.99, 3) == 29.97

    def test_raises_on_zero_quantity(self):
        with pytest.raises(ValueError, match="quantity"):
            compute_line_total(10.0, 0)

    def test_raises_on_discount_out_of_range(self):
        with pytest.raises(ValueError, match="discount"):
            compute_line_total(10.0, 1, 1.5)


# --------------------------- price_tier (parametrized) ---------------
@pytest.mark.parametrize("price,expected", [
    (250.0, "premium"),
    (200.0, "premium"),   # ranh giới dưới của premium
    (199.99, "mid"),
    (50.0, "mid"),        # ranh giới dưới của mid
    (49.99, "budget"),
    (0.0, "budget"),
])
def test_price_tier_boundaries(price, expected):
    assert price_tier(price) == expected


# --------------------------- validate_records ------------------------
def test_validate_records_splits_valid_and_invalid():
    records = [
        {"order_id": 1, "product_id": 1, "quantity": 2, "unit_price": 10.0, "discount": 0.1},  # ok
        {"order_id": 2, "product_id": 1, "quantity": 1, "unit_price": 5.0},                      # ok (discount default)
        {"order_id": 3, "product_id": 1, "quantity": 0, "unit_price": 5.0},                      # bad: qty
        {"order_id": 4, "product_id": 1, "quantity": 1, "unit_price": 5.0, "discount": 2.0},     # bad: discount
    ]
    result = validate_records(records)
    assert result.n_valid == 2
    assert result.n_errors == 2
    # lỗi giữ đúng index của record gốc
    bad_indices = [i for i, _ in result.errors]
    assert bad_indices == [2, 3]


# --------------------------- revenue_by_category ---------------------
@pytest.fixture
def items() -> pd.DataFrame:
    return pd.DataFrame({
        "product_id": [1, 2, 3],
        "line_total": [100.0, 50.0, 25.0],
    })


@pytest.fixture
def products() -> pd.DataFrame:
    return pd.DataFrame({
        "product_id": [1, 2, 3],
        "category": ["A", "A", "B"],
    })


def test_revenue_by_category_aggregates_and_sorts(items, products):
    out = revenue_by_category(items, products)
    # A = 100 + 50 = 150, B = 25; sắp giảm dần -> A trước
    assert list(out["category"]) == ["A", "B"]
    assert list(out["revenue"]) == [150.0, 25.0]


def test_revenue_by_category_inner_join_drops_unknown_product(products):
    # product_id=99 không có trong products -> bị loại (inner join)
    items = pd.DataFrame({"product_id": [1, 99], "line_total": [10.0, 999.0]})
    out = revenue_by_category(items, products)
    assert out["revenue"].sum() == 10.0  # 999 bị loại
