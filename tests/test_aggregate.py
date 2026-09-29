from etl.aggregate import cohort_retention, monthly_revenue, top_customers
from etl.io import prepare_orders
from tests.helpers import orders


def with_eur(df):
    df = df.copy()
    df["amount_eur"] = df["amount"]
    return df


def test_monthly_revenue_single_year():
    df = with_eur(prepare_orders(orders(
        ("1", "C1", "2026-01-05", "100", "EUR", "paid"),
        ("2", "C2", "2026-01-20", "50", "EUR", "paid"),
        ("3", "C1", "2026-02-02", "30", "EUR", "paid"),
        ("4", "C1", "2026-02-03", "999", "EUR", "refunded"),
    )))
    assert list(monthly_revenue(df).values) == [150.0, 30.0]


def test_top_customers_ties_by_id():
    df = with_eur(prepare_orders(orders(
        ("1", "B", "2026-01-05", "10", "EUR", "paid"),
        ("2", "A", "2026-01-05", "10", "EUR", "paid"),
        ("3", "C", "2026-01-05", "5", "EUR", "paid"),
    )))
    top = top_customers(df, n=2)
    assert top["customer_id"].tolist() == ["A", "B"]


def test_cohort_retention_same_year():
    df = with_eur(prepare_orders(orders(
        ("1", "C1", "2026-01-05", "10", "EUR", "paid"),
        ("2", "C1", "2026-02-05", "10", "EUR", "paid"),
        ("3", "C2", "2026-01-09", "10", "EUR", "paid"),
    )))
    table = cohort_retention(df)
    assert table.loc["2026-01", 0] == 2
    assert table.loc["2026-01", 1] == 1
