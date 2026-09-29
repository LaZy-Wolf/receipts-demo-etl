import pandas as pd

from etl.clean import drop_test_orders, normalize_columns
from etl.io import prepare_orders
from tests.helpers import orders


def test_simple_headers():
    df = pd.DataFrame(columns=["Order ID", "Customer ID", "Status"])
    assert list(normalize_columns(df).columns) == ["order_id", "customer_id", "status"]


def test_headers_already_clean():
    df = pd.DataFrame(columns=["order_id", "amount"])
    assert list(normalize_columns(df).columns) == ["order_id", "amount"]


def test_drop_test_orders():
    df = prepare_orders(orders(("1", "C1", "2026-01-05", "10", "EUR", "paid"), ("2", "TEST-9", "2026-01-05", "10", "EUR", "paid")))
    assert list(drop_test_orders(df)["order_id"]) == ["1"]


def test_prepare_normalises_values():
    df = prepare_orders(orders(("1", "C1", "2026-01-05 13:45", "10.5", " usd", "PAID ")))
    row = df.iloc[0]
    assert row["currency"] == "USD"
    assert row["status"] == "paid"
    assert row["order_date"] == pd.Timestamp("2026-01-05")
    assert row["amount"] == 10.5
