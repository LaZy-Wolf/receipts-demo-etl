from etl.io import prepare_orders
from etl.validate import run_checks
from tests.helpers import orders


def test_clean_data_has_no_findings():
    df = prepare_orders(orders(("1", "C1", "2026-01-05", "10", "EUR", "paid")))
    assert run_checks(df) == {"missing_amount": 0, "negative_amount": 0, "duplicate_order_id": 0, "unknown_currency": 0}


def test_negative_amount():
    df = prepare_orders(orders(("1", "C1", "2026-01-05", "-5", "EUR", "paid"), ("2", "C1", "2026-01-05", "5", "EUR", "paid")))
    assert run_checks(df)["negative_amount"] == 1


def test_missing_amount_counted():
    df = prepare_orders(orders(("1", "C1", "2026-01-05", "", "EUR", "paid"), ("2", "C1", "2026-01-05", "5", "EUR", "paid")))
    assert run_checks(df)["missing_amount"] == 1


def test_duplicates_and_currency():
    df = prepare_orders(orders(("1", "C1", "2026-01-05", "5", "EUR", "paid"), ("1", "C1", "2026-01-06", "5", "XYZ", "paid")))
    checks = run_checks(df)
    assert checks["duplicate_order_id"] == 1
    assert checks["unknown_currency"] == 1
