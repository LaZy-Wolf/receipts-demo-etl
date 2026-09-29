import pytest

from etl.fx import to_eur
from etl.io import prepare_orders, prepare_rates
from tests.helpers import orders, rates


def test_converts_with_same_day_rate():
    o = prepare_orders(orders(("1", "C1", "2026-03-04", "100", "USD", "paid")))
    r = prepare_rates(rates(("2026-03-04", "USD", "0.92")))
    assert to_eur(o, r)["amount_eur"].tolist() == [92.0]


def test_eur_needs_no_rate():
    o = prepare_orders(orders(("1", "C1", "2026-03-04", "40", "EUR", "paid")))
    r = prepare_rates(rates(("2026-03-04", "USD", "0.92")))
    assert to_eur(o, r)["amount_eur"].tolist() == [40.0]


def test_keeps_order_rows_and_columns():
    o = prepare_orders(orders(("1", "C1", "2026-03-04", "10", "GBP", "paid"), ("2", "C2", "2026-03-04", "10", "USD", "paid")))
    r = prepare_rates(rates(("2026-03-04", "USD", "0.92"), ("2026-03-04", "GBP", "1.17")))
    out = to_eur(o, r)
    assert out["order_id"].tolist() == ["1", "2"]
    assert out["amount_eur"].tolist() == pytest.approx([11.7, 9.2])
