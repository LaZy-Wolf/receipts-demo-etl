import pandas as pd

from .clean import normalize_columns

ORDER_COLUMNS = ["order_id", "customer_id", "order_date", "amount", "currency", "status", "updated_at"]
TEXT = {"order_id": "string", "customer_id": "string", "currency": "string", "status": "string"}


def as_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series).astype("datetime64[ns]")


def prepare_orders(raw: pd.DataFrame) -> pd.DataFrame:
    """Normalise headers, check columns and parse types of a raw order export."""
    df = normalize_columns(raw)
    missing = [c for c in ORDER_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"orders are missing columns: {', '.join(missing)}")
    df = df.astype({k: v for k, v in TEXT.items()})
    df["currency"] = df["currency"].str.upper().str.strip()
    df["status"] = df["status"].str.lower().str.strip()
    df["order_date"] = as_datetime(df["order_date"]).dt.normalize()
    df["updated_at"] = as_datetime(df["updated_at"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").astype("float64")
    return df


def prepare_rates(raw: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(raw)
    df["date"] = as_datetime(df["date"]).dt.normalize()
    df["currency"] = df["currency"].astype("string").str.upper().str.strip()
    df["rate_to_eur"] = df["rate_to_eur"].astype(float)
    return df


def read_orders(path) -> pd.DataFrame:
    return prepare_orders(pd.read_csv(path, dtype=str))


def read_rates(path) -> pd.DataFrame:
    return prepare_rates(pd.read_csv(path, dtype=str))
