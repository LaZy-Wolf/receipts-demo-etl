import pandas as pd


def paid(orders: pd.DataFrame) -> pd.DataFrame:
    return orders[orders["status"] == "paid"]


def monthly_revenue(orders: pd.DataFrame) -> pd.Series:
    """Paid revenue in EUR per calendar month, oldest first."""
    p = paid(orders)
    out = p.groupby(p["order_date"].dt.month)["amount_eur"].sum().round(2)
    out.index.name = "month"
    return out


def top_customers(orders: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Customers by paid revenue, ties broken by customer_id."""
    p = paid(orders)
    totals = p.groupby("customer_id", as_index=False).agg(revenue_eur=("amount_eur", "sum"), orders=("order_id", "count"))
    totals["revenue_eur"] = totals["revenue_eur"].round(2)
    return totals.sort_values(["revenue_eur", "customer_id"], ascending=[False, True]).head(n).reset_index(drop=True)


def cohort_retention(orders: pd.DataFrame) -> pd.DataFrame:
    """Rows: cohort (first paid month, 'YYYY-MM'). Columns: months since first purchase. Values: distinct customers."""
    p = paid(orders).copy()
    p["month"] = p["order_date"].dt.to_period("M")
    first = p.groupby("customer_id")["month"].transform("min")
    p["cohort"] = first.astype(str)
    p["months_since_first"] = (p["month"].dt.month - first.dt.month).abs()
    table = p.groupby(["cohort", "months_since_first"])["customer_id"].nunique().unstack(fill_value=0)
    table.columns.name = "months_since_first"
    return table
