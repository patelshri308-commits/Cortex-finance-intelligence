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
)

from utils.schema_validation import validate_monthly_kpis


def calculate_growth(current_value, previous_value):
    if previous_value == 0:
        return 0

    return ((current_value - previous_value) / previous_value) * 100


def load_prompt_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def generate_revenue_summary() -> str:
    prompt_config = load_prompt_config("prompts/revenue_summary.yaml")

    df = pd.read_csv("data/monthly_kpis.csv")
    validate_monthly_kpis(df)

    df["revenue_month"] = pd.to_datetime(df["revenue_month"])
    df = df.sort_values("revenue_month")

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    arr_growth = calculate_growth(
        latest["total_arr"],
        previous["total_arr"]
    )

    bookings_growth = calculate_growth(
        latest["total_bookings"],
        previous["total_bookings"]
    )

    semantic_model = load_semantic_model(
        "semantic_models/finance_metrics.yaml"
    )

    semantic_context = build_metric_context(
        semantic_model
    )

    context = f"""
Latest revenue month: {latest['revenue_month'].date()}

Total ARR: ${latest['total_arr']:,.2f}
ARR growth rate: {arr_growth:.2f}%

Total bookings: ${latest['total_bookings']:,.2f}
Bookings growth rate: {bookings_growth:.2f}%

Expansion revenue: ${latest['expansion_revenue']:,.2f}
Churned revenue: ${latest['churned_revenue']:,.2f}
"""

    prompt = f"""
{prompt_config["system_prompt"]}

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