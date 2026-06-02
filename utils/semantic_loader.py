import yaml


def load_semantic_model(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def build_metric_context(semantic_model):
    metrics = semantic_model.get("metrics", {})

    context_lines = []

    for metric_name, metric_info in metrics.items():
        definition = metric_info.get("definition", "")
        interpretation = metric_info.get("interpretation", "")

        context_lines.append(
            f"""
Metric: {metric_name}
Definition: {definition}
Business Interpretation: {interpretation}
"""
        )

    return "\n".join(context_lines)


def calculate_percentage_change(current_value, previous_value):
    """Calculate percent change in Python so the model receives pre-computed figures."""
    if previous_value == 0:
        return 0.0
    return ((current_value - previous_value) / previous_value) * 100.0


def format_currency(value):
    return f"${value:,.2f}"


def format_percentage(value):
    return f"{value:.2f}%"


def compute_kpi_metrics(latest, previous):
    """Compute business KPI metrics in Python to keep the model focused on insight rather than arithmetic."""
    current_arr = latest["total_arr"]
    previous_arr = previous["total_arr"]
    arr_change = current_arr - previous_arr
    arr_change_pct = calculate_percentage_change(current_arr, previous_arr)

    current_bookings = latest["total_bookings"]
    previous_bookings = previous["total_bookings"]
    bookings_change = current_bookings - previous_bookings
    bookings_change_pct = calculate_percentage_change(current_bookings, previous_bookings)

    current_expansion = latest["expansion_revenue"]
    previous_expansion = previous["expansion_revenue"]
    expansion_change = current_expansion - previous_expansion

    current_churn = latest["churned_revenue"]
    previous_churn = previous["churned_revenue"]
    churn_change = current_churn - previous_churn

    current_contraction = latest["contraction_revenue"]
    previous_contraction = previous["contraction_revenue"]
    contraction_change = current_contraction - previous_contraction

    net_revenue_impact = (
        current_expansion
        - current_churn
        - current_contraction
    )

    return {
        "current_arr": current_arr,
        "previous_arr": previous_arr,
        "arr_change": arr_change,
        "arr_change_pct": arr_change_pct,
        "current_bookings": current_bookings,
        "previous_bookings": previous_bookings,
        "bookings_change": bookings_change,
        "bookings_change_pct": bookings_change_pct,
        "current_expansion": current_expansion,
        "previous_expansion": previous_expansion,
        "expansion_change": expansion_change,
        "current_churn": current_churn,
        "previous_churn": previous_churn,
        "churn_change": churn_change,
        "current_contraction": current_contraction,
        "previous_contraction": previous_contraction,
        "contraction_change": contraction_change,
        "net_revenue_impact": net_revenue_impact,
    }


def build_kpi_context(metrics, latest_month=None, previous_month=None):
    """Build a consistent KPI context block for all finance agents."""
    header = ""
    if latest_month is not None:
        header += f"Latest revenue month: {latest_month}\n"
    if previous_month is not None:
        header += f"Previous revenue month: {previous_month}\n"
    if header:
        header += "\n"

    return f"""
{header}ARR
- Current ARR: {format_currency(metrics['current_arr'])}
- Previous ARR: {format_currency(metrics['previous_arr'])}
- ARR Change: {format_currency(metrics['arr_change'])}
- ARR Change %: {format_percentage(metrics['arr_change_pct'])}

Bookings
- Current Bookings: {format_currency(metrics['current_bookings'])}
- Previous Bookings: {format_currency(metrics['previous_bookings'])}
- Bookings Change: {format_currency(metrics['bookings_change'])}
- Bookings Change %: {format_percentage(metrics['bookings_change_pct'])}

Expansion Revenue
- Current: {format_currency(metrics['current_expansion'])}
- Previous: {format_currency(metrics['previous_expansion'])}
- Change: {format_currency(metrics['expansion_change'])}

Churned Revenue
- Current: {format_currency(metrics['current_churn'])}
- Previous: {format_currency(metrics['previous_churn'])}
- Change: {format_currency(metrics['churn_change'])}

Contraction Revenue
- Current: {format_currency(metrics['current_contraction'])}
- Previous: {format_currency(metrics['previous_contraction'])}
- Change: {format_currency(metrics['contraction_change'])}

Net Revenue Impact
- Expansion - Churn - Contraction
- Result: {format_currency(metrics['net_revenue_impact'])}
"""
