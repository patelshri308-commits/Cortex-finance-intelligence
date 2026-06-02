import sys
from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.cortex_runner import run_cortex
from utils.schema_validation import validate_monthly_kpis
from src.snowflake_query import query_snowflake_to_df
from utils.semantic_loader import compute_kpi_metrics, build_kpi_context


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

    # Pre-calculate business metrics in Python so the agent receives a structured KPI context
    # and the model can focus on explanation and insight rather than arithmetic.
    metrics = compute_kpi_metrics(latest, previous)

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
{build_kpi_context(metrics, latest_month=latest['revenue_month'].date(), previous_month=previous['revenue_month'].date())}

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


def generate_forecast_sensitivity_from_question(user_query: str) -> str:
    df = query_snowflake_to_df("""
        SELECT *
        FROM FINANCE_AI.RAW.MONTHLY_KPIS
        ORDER BY revenue_month
    """)

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else latest

    metrics = compute_kpi_metrics(latest, previous)

    prompt = f"""
You are the Forecast Sensitivity Agent for a SaaS finance analytics workflow.

The user asked:
{user_query}

Important instruction:
This is a written user question, not an interactive slider scenario.
Always use KPI values provided in the context.
Show calculations explicitly.
When a user changes one metric, isolate that metric first.
Do not assume changes to other KPIs.
Do not estimate ARR impact unless the calculation can be directly derived from the provided KPI values.
Do not invent ranges like 4–6%.
Use plain-text arithmetic only.
Distinguish observed impact from possible implications.
Use numeric reasoning before recommendations.
Do not mention pricing issues, customer satisfaction, customer success, product quality, or customer loyalty unless those metrics are explicitly present in the data.

CALCULATION OUTPUT RULES
------------------------
CRITICAL: All calculations must be output in plain text business format.

Never use mathematical markup.
Never use LaTeX.
Never use equation formatting.
Use plain business language.

Examples:
✅ GOOD:   "568,663 × 1.10 = 625,529"
✅ GOOD:   "Expansion revenue of $2.5M increases 8% to $2.7M"
❌ BAD:    Use of $ symbols in equations or mathematical notation
❌ BAD:    Line breaks in numbers (568,663 split across lines)
❌ BAD:    Using LaTeX or mathematical rendering

Use the KPI data below to estimate the impact of the user's requested scenario.

{build_kpi_context(metrics, latest_month=latest['revenue_month'], previous_month=previous['revenue_month'])}

Response rules:
- Directly answer the user's scenario.
- If the user changes one metric, isolate that metric first.
- Use numeric values from the KPI data.
- Do not discuss slider assumptions.
- Do not assume changes to other metrics.
- Explain the impact on ARR quality and revenue risk.
- Keep the answer executive-ready.

Required Output Format:
Direct Impact:
Financial Impact:
ARR Quality Impact:
Key Risk:
Executive Takeaway:
"""
    return run_cortex(prompt)


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