import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lower-case, snake_case column names."""
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return out


def dedupe_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """One row per order_id: the most recent version of each order."""
    latest = orders.sort_values("updated_at", kind="stable").drop_duplicates(subset="order_id", keep="last")
    return latest.sort_index().reset_index(drop=True)


def drop_test_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Internal QA orders use customer ids starting with 'TEST-'."""
    return orders[~orders["customer_id"].str.startswith("TEST-")].reset_index(drop=True)
