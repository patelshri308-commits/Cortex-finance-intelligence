import sys
from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.cortex_runner import run_cortex
from utils.schema_validation import validate_monthly_kpis
from src.snowflake_query import query_snowflake_to_df


def load_prompt_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def calculate_growth(current_value, previous_value):
    if previous_value == 0:
        return 0

    return ((current_value - previous_value) / previous_value) * 100


def generate_forecast_sensitivity(
    arr_growth_adjustment_pct: float = 0,
    bookings_growth_adjustment_pct: float = 0,
    churn_change_pct: float = 0,
    expansion_change_pct: float = 0,
    contraction_change_pct: float = 0,
) -> str:
    prompt_config = load_prompt_config("prompts/forecast_sensitivity.yaml")

    df = query_snowflake_to_df("""
    SELECT *
    FROM FINANCE_AI.RAW.MONTHLY_KPIS
    ORDER BY REVENUE_MONTH;
    """)
    validate_monthly_kpis(df)

    df["revenue_month"] = pd.to_datetime(df["revenue_month"])
    df = df.sort_values("revenue_month")

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    baseline_arr_growth = calculate_growth(
        latest["total_arr"],
        previous["total_arr"]
    )

    baseline_bookings_growth = calculate_growth(
        latest["total_bookings"],
        previous["total_bookings"]
    )

    projected_arr = latest["total_arr"] * (1 + arr_growth_adjustment_pct / 100)
    projected_bookings = latest["total_bookings"] * (
        1 + bookings_growth_adjustment_pct / 100
    )
    projected_churn = latest["churned_revenue"] * (1 + churn_change_pct / 100)
    projected_expansion = latest["expansion_revenue"] * (
        1 + expansion_change_pct / 100
    )
    projected_contraction = latest["contraction_revenue"] * (
        1 + contraction_change_pct / 100
    )

    net_revenue_impact = (
        projected_expansion
        - projected_churn
        - projected_contraction
    )

    context = f"""
Latest actual month: {latest['revenue_month'].date()}

Baseline Metrics:
- Current ARR: ${latest['total_arr']:,.2f}
- Previous ARR: ${previous['total_arr']:,.2f}
- Baseline ARR growth: {baseline_arr_growth:.2f}%
- Current bookings: ${latest['total_bookings']:,.2f}
- Previous bookings: ${previous['total_bookings']:,.2f}
- Baseline bookings growth: {baseline_bookings_growth:.2f}%
- Current churned revenue: ${latest['churned_revenue']:,.2f}
- Current expansion revenue: ${latest['expansion_revenue']:,.2f}
- Current contraction revenue: ${latest['contraction_revenue']:,.2f}

Scenario Assumptions:
- ARR growth adjustment: {arr_growth_adjustment_pct:.2f}%
- Bookings growth adjustment: {bookings_growth_adjustment_pct:.2f}%
- Churned revenue change: {churn_change_pct:.2f}%
- Expansion revenue change: {expansion_change_pct:.2f}%
- Contraction revenue change: {contraction_change_pct:.2f}%

Projected Scenario:
- Projected ARR: ${projected_arr:,.2f}
- Projected bookings: ${projected_bookings:,.2f}
- Projected churned revenue: ${projected_churn:,.2f}
- Projected expansion revenue: ${projected_expansion:,.2f}
- Projected contraction revenue: ${projected_contraction:,.2f}
- Net revenue impact from expansion/churn/contraction: ${net_revenue_impact:,.2f}
"""

    prompt = f"""
{prompt_config["system_prompt"]}

{prompt_config["output_format"]}

Metrics:
{context}
"""

    response = run_cortex(prompt, model="llama3.1-70b")

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "forecast_sensitivity.txt"

    with open(output_path, "w") as file:
        file.write(response)

    return response


def main():
    summary = generate_forecast_sensitivity(
        arr_growth_adjustment_pct=5,
        bookings_growth_adjustment_pct=3,
        churn_change_pct=10,
        expansion_change_pct=5,
        contraction_change_pct=0,
    )

    print("\nAI Forecast Sensitivity Analysis")
    print("--------------------------------")
    print(summary)
    print("\nSaved output to outputs/forecast_sensitivity.txt")


if __name__ == "__main__":
    main()