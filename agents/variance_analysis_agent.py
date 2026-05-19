import os
from pathlib import Path

import google.generativeai as genai
import pandas as pd
import yaml
from dotenv import load_dotenv


def calculate_growth(current_value, previous_value):
    if previous_value == 0:
        return 0

    return ((current_value - previous_value) / previous_value) * 100


def calculate_change(current_value, previous_value):
    return current_value - previous_value


def load_prompt_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def generate_variance_analysis() -> str:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-3.5-flash")

    prompt_config = load_prompt_config("prompts/variance_analysis.yaml")

    df = pd.read_csv("data/monthly_kpis.csv")

    df["revenue_month"] = pd.to_datetime(df["revenue_month"])
    df = df.sort_values("revenue_month")

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    arr_change = calculate_change(
        latest["total_arr"],
        previous["total_arr"]
    )

    arr_growth = calculate_growth(
        latest["total_arr"],
        previous["total_arr"]
    )

    bookings_change = calculate_change(
        latest["total_bookings"],
        previous["total_bookings"]
    )

    bookings_growth = calculate_growth(
        latest["total_bookings"],
        previous["total_bookings"]
    )

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
Current month: {latest['revenue_month'].date()}
Previous month: {previous['revenue_month'].date()}

ARR:
- Previous ARR: ${previous['total_arr']:,.2f}
- Current ARR: ${latest['total_arr']:,.2f}
- ARR change: ${arr_change:,.2f}
- ARR growth rate: {arr_growth:.2f}%

Bookings:
- Previous bookings: ${previous['total_bookings']:,.2f}
- Current bookings: ${latest['total_bookings']:,.2f}
- Bookings change: ${bookings_change:,.2f}
- Bookings growth rate: {bookings_growth:.2f}%

Revenue Drivers:
- Expansion revenue change: ${expansion_change:,.2f}
- Contraction revenue change: ${contraction_change:,.2f}
- Churned revenue change: ${churn_change:,.2f}
- New business revenue change: ${new_business_change:,.2f}
- Renewal revenue change: ${renewal_change:,.2f}
"""

    prompt = f"""
{prompt_config["system_prompt"]}

{prompt_config["output_format"]}

Metrics:
{context}
"""

    response = model.generate_content(prompt)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "variance_analysis.txt"

    with open(output_path, "w") as file:
        file.write(response.text)

    return response.text


def main():
    summary = generate_variance_analysis()

    print("\nAI Variance Commentary")
    print("----------------------")
    print(summary)
    print("\nSaved output to outputs/variance_analysis.txt")


if __name__ == "__main__":
    main()