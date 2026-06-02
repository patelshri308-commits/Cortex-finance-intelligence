import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
import yaml

from src.cortex_runner import run_cortex
from utils.schema_validation import validate_monthly_kpis
from src.snowflake_query import query_snowflake_to_df
from utils.semantic_loader import compute_kpi_metrics, build_kpi_context, format_currency
from semantic.context_builder import build_semantic_context


def calculate_growth(current_value, previous_value):
    if previous_value == 0:
        return 0

    return ((current_value - previous_value) / previous_value) * 100


def calculate_change(current_value, previous_value):
    return current_value - previous_value


def load_prompt_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def generate_variance_analysis(user_query: str = "latest revenue performance") -> str:
    prompt_config = load_prompt_config("prompts/variance_analysis.yaml")

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

    # Pre-calculate KPI metrics in Python to reduce model arithmetic load and improve consistency.
    metrics = compute_kpi_metrics(latest, previous)

    expansion_change = calculate_change(
        latest["expansion_revenue"],
        previous["expansion_revenue"]
    )

    contraction_change = calculate_change(
        latest["contraction_revenue"],
        previous["contraction_revenue"]
    )

    churn_change = calculate_change(
        latest["churned_revenue"],
        previous["churned_revenue"]
    )

    new_business_change = calculate_change(
        latest["new_business_revenue"],
        previous["new_business_revenue"]
    )

    renewal_change = calculate_change(
        latest["renewal_revenue"],
        previous["renewal_revenue"]
    )

    context = f"""
{build_kpi_context(metrics, latest_month=latest['revenue_month'].date(), previous_month=previous['revenue_month'].date())}

Revenue Drivers:
- Expansion revenue change: {format_currency(expansion_change)}
- Contraction revenue change: {format_currency(contraction_change)}
- Churned revenue change: {format_currency(churn_change)}
- New business revenue change: {format_currency(new_business_change)}
- Renewal revenue change: {format_currency(renewal_change)}
"""

    prompt = f"""
{prompt_config["system_prompt"]}

{prompt_config["output_format"]}

Metrics:
{context}
"""
    semantic_context_block = build_semantic_context(user_query)

    prompt = f"""
{prompt_config["system_prompt"]}

Semantic Business Context:
{semantic_context_block}

{prompt_config["output_format"]}

Metrics:
{context}
"""

    response = run_cortex(prompt, model="llama3.1-70b")

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "variance_analysis.txt"

    with open(output_path, "w") as file:
        file.write(response)

    return response


def main():
    summary = generate_variance_analysis()

    print("\nAI Variance Commentary")
    print("----------------------")
    print(summary)
    print("\nSaved output to outputs/variance_analysis.txt")


if __name__ == "__main__":
    main()
