import pandas as pd

KNOWN_CURRENCIES = {"EUR", "USD", "GBP", "CHF", "SEK", "NOK", "DKK", "PLN"}


def run_checks(orders: pd.DataFrame) -> dict[str, int]:
    """Data-quality counts. Each value is the number of offending rows."""
    return {
        "missing_amount": int(orders["amount"].isna().sum()),
        "negative_amount": int((~(orders["amount"] >= 0)).sum()),
        "duplicate_order_id": int(orders["order_id"].duplicated().sum()),
        "unknown_currency": int((~orders["currency"].isin(KNOWN_CURRENCIES)).sum()),
    }
