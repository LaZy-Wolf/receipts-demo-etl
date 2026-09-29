import pandas as pd

HEADER = ["order_id", "customer_id", "order_date", "amount", "currency", "status", "updated_at"]


def orders(*rows) -> pd.DataFrame:
    """Raw order export (all strings, like read_csv(dtype=str)). Rows follow HEADER; updated_at defaults to order_date."""
    full = [list(r) + [r[2]] if len(r) == 6 else list(r) for r in rows]
    return pd.DataFrame([[str(v) if v is not None else None for v in r] for r in full], columns=HEADER)


def rates(*rows) -> pd.DataFrame:
    return pd.DataFrame([[str(v) for v in r] for r in rows], columns=["date", "currency", "rate_to_eur"])
