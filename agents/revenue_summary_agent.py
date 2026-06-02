import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
import yaml

from src.cortex_runner import run_cortex

from utils.semantic_loader import (
    load_semantic_model,
    build_metric_context,
    compute_kpi_metrics,
    build_kpi_context,
)
from semantic.context_builder import build_semantic_context

from utils.schema_validation import validate_monthly_kpis
from src.snowflake_query import query_snowflake_to_df


def calculate_growth(current_value, previous_value):
    if previous_value == 0:
        return 0

    return ((current_value - previous_value) / previous_value) * 100


def load_prompt_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def generate_revenue_summary() -> str:
    prompt_config = load_prompt_config("prompts/revenue_summary.yaml")

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

    # Pre-calculate business metrics in Python so the model receives a consistent KPI context
    # and can focus on analysis and explanation instead of arithmetic.
    metrics = compute_kpi_metrics(latest, previous)

    semantic_model = load_semantic_model(
        "semantic_models/finance_metrics.yaml"
    )

    semantic_context = build_metric_context(
        semantic_model
    )

    context = build_kpi_context(
        metrics,
        latest_month=latest['revenue_month'].date(),
        previous_month=previous['revenue_month'].date(),
    )

    prompt = f"""
{prompt_config["system_prompt"]}

Business Metric Definitions:
{semantic_context}

{prompt_config["output_format"]}

Metrics:
{context}
"""
    # Inject semantic business context for LLMs (no user query available)
    semantic_context_block = build_semantic_context("latest revenue performance")

    prompt = f"""
{prompt_config["system_prompt"]}

Semantic Business Context:
{semantic_context_block}

Business Metric Definitions:
{semantic_context}

{prompt_config["output_format"]}

Metrics:
{context}
"""

    response = run_cortex(prompt, model="llama3.1-70b")

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "revenue_summary.txt"

    with open(output_path, "w") as file:
        file.write(response)

    return response


def main():
    summary = generate_revenue_summary()

    print("\nAI Executive Summary")
    print("--------------------")
    print(summary)
    print("\nSaved output to outputs/revenue_summary.txt")


if __name__ == "__main__":
    main()