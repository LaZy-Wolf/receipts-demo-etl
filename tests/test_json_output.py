import json

from click.testing import CliRunner

from etl.cli import main
from tests.helpers import orders, rates


def test_json_format(tmp_path):
    orders(("1", "C1", "2026-01-05", "100", "EUR", "paid")).to_csv(tmp_path / "o.csv", index=False)
    rates(("2026-01-05", "USD", "0.9")).to_csv(tmp_path / "r.csv", index=False)
    res = CliRunner().invoke(main, ["run", str(tmp_path / "o.csv"), "--rates", str(tmp_path / "r.csv"), "--format", "json"])
    assert res.exit_code == 0, res.output
    assert json.loads(res.output)["checks"]["negative_amount"] == 0
