import pandas as pd


def to_eur(orders: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
    """Add amount_eur using the rate for each order's currency and date."""
    merged = orders.merge(
        rates.rename(columns={"date": "order_date"}),
        on=["order_date", "currency"],
        how="left",
    )
    merged.loc[merged["currency"] == "EUR", "rate_to_eur"] = 1.0
    merged["amount_eur"] = (merged["amount"] * merged["rate_to_eur"]).round(2)
    return merged.drop(columns=["rate_to_eur"])
