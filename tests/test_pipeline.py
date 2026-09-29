from datetime import datetime

from click.testing import CliRunner

from etl.cli import main
from etl.pipeline import build
from tests.helpers import orders, rates

ORDERS = orders(
    ("1", "C1", "2026-01-05", "100", "EUR", "paid"),
    ("2", "C2", "2026-02-10", "200", "USD", "paid"),
    ("3", "TEST-1", "2026-02-11", "999", "EUR", "paid"),
)
RATES = rates(("2026-02-10", "USD", "0.9"))


def test_build():
    result = build(ORDERS, RATES)
    assert result.orders["order_id"].tolist() == ["1", "2"]
    assert list(result.monthly.values) == [100.0, 180.0]
    assert result.top["customer_id"].tolist() == ["C2", "C1"]


def test_since_drops_older_orders():
    result = build(ORDERS, RATES, since=datetime(2026, 2, 1))
    assert result.orders["order_id"].tolist() == ["2"]


def test_cli_run(tmp_path):
    ORDERS.to_csv(tmp_path / "orders.csv", index=False)
    RATES.to_csv(tmp_path / "rates.csv", index=False)
    res = CliRunner().invoke(main, ["run", str(tmp_path / "orders.csv"), "--rates", str(tmp_path / "rates.csv")])
    assert res.exit_code == 0, res.output
    assert "# Sales report" in res.output
    assert "180.00" in res.output


def test_cli_validate_fails_on_findings(tmp_path):
    orders(("1", "C1", "2026-01-05", "-1", "EUR", "paid")).to_csv(tmp_path / "o.csv", index=False)
    res = CliRunner().invoke(main, ["validate", str(tmp_path / "o.csv")])
    assert res.exit_code == 1
    assert "negative_amount: 1" in res.output
