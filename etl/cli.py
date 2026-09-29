import sys

import click
import pandas as pd

from . import pipeline, report, validate
from .io import read_orders


@click.group()
def main():
    """Sales reporting pipeline."""


@main.command()
@click.argument("orders_csv", type=click.Path(exists=True, dir_okay=False))
@click.option("--rates", "rates_csv", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--since", type=click.DateTime(formats=["%Y-%m-%d"]), help="Keep orders on or after this date.")
@click.option("--out", type=click.File("w", encoding="utf-8"), default="-")
def run(orders_csv, rates_csv, since, out):
    """Build the revenue report."""
    result = pipeline.build(pd.read_csv(orders_csv, dtype=str), pd.read_csv(rates_csv, dtype=str), since=since)
    out.write(report.render(result))


@main.command(name="validate")
@click.argument("orders_csv", type=click.Path(exists=True, dir_okay=False))
def validate_cmd(orders_csv):
    """Print data-quality counts; exit 1 if any check fails."""
    checks = validate.run_checks(read_orders(orders_csv))
    for name, count in checks.items():
        click.echo(f"{name}: {count}")
    sys.exit(1 if any(checks.values()) else 0)
