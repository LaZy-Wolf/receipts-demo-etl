# sales-etl

Nightly job that turns raw order exports into the revenue report finance reads every morning.

```
orders.csv ─┐
            ├─> normalise columns ─> validate ─> dedupe ─> filter --since ─> convert to EUR ─> report.md
rates.csv ──┘
```

## Usage

```bash
pip install -e ".[test]"
sales-etl run data/orders.csv --rates data/rates.csv --since 2026-01-01 --out report.md
sales-etl validate data/orders.csv
pytest
```

## Input

**orders.csv**: `order_id, customer_id, order_date, amount, currency, status, updated_at`.
Header spelling varies between source systems; headers are normalised to snake_case
(`"Order ID"`, `"Amount (EUR)"`, `"Customer-Name"` become `order_id`, `amount_eur`, `customer_name`).
The same `order_id` can appear several times when an order is edited. The row with the latest `updated_at` wins.

**rates.csv**: `date, currency, rate_to_eur`, one row per currency per publication day. Rates are published on
business days only; an order uses the latest rate published **on or before** its order date, per currency.
EUR orders need no rate.

## Report

- Revenue per calendar month (paid orders only, in EUR)
- Top customers
- Cohort retention: for each first-purchase month, how many customers bought again N months later
- Data-quality counts from `validate`

`--since YYYY-MM-DD` keeps orders placed on or after that date.
