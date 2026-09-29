import json

from .pipeline import Result


def _table(headers: list[str], rows: list[list]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(" --- " for _ in headers) + "|"]
    lines += ["| " + " | ".join(str(v) for v in row) + " |" for row in rows]
    return lines


def render(result: Result) -> str:
    lines = ["# Sales report", "", "## Revenue by month (EUR)", ""]
    lines += _table(["Month", "Revenue"], [[m, f"{v:,.2f}"] for m, v in result.monthly.items()])
    lines += ["", "## Top customers", ""]
    lines += _table(["Customer", "Orders", "Revenue (EUR)"],
                    [[r.customer_id, r.orders, f"{r.revenue_eur:,.2f}"] for r in result.top.itertuples()])
    lines += ["", "## Data quality", ""]
    lines += _table(["Check", "Rows"], [[k, v] for k, v in result.checks.items()])
    return "\n".join(lines) + "\n"


def render_json(result: Result) -> str:
    return json.dumps({
        "monthly": {str(k): float(v) for k, v in result.monthly.items()},
        "top_customers": json.loads(result.top.to_json(orient="records")),
        "checks": result.checks,
    }, indent=2)
