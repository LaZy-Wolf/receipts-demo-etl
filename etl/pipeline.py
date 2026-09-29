from dataclasses import dataclass
from datetime import date, datetime

import pandas as pd

from . import aggregate, clean, fx, validate
from .io import prepare_orders, prepare_rates


@dataclass
class Result:
    orders: pd.DataFrame
    monthly: pd.Series
    top: pd.DataFrame
    cohorts: pd.DataFrame
    checks: dict[str, int]


def build(raw_orders: pd.DataFrame, raw_rates: pd.DataFrame, since: date | datetime | None = None) -> Result:
    orders = prepare_orders(raw_orders)
    checks = validate.run_checks(orders)
    orders = clean.drop_test_orders(clean.dedupe_orders(orders))
    if since is not None:
        orders = orders[orders["order_date"] > pd.Timestamp(since)]
    orders = fx.to_eur(orders, prepare_rates(raw_rates))
    return Result(
        orders=orders,
        monthly=aggregate.monthly_revenue(orders),
        top=aggregate.top_customers(orders),
        cohorts=aggregate.cohort_retention(orders),
        checks=checks,
    )
