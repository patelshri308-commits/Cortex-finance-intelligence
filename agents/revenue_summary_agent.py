import os

import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv


def calculate_growth(current_value, previous_value):
    if previous_value == 0:
        return 0

    return ((current_value - previous_value) / previous_value) * 100


def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-3.5-flash")

    df = pd.read_csv("data/monthly_kpis.csv")

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

    print("Revenue Summary")
    print("----------------")
    print(f"Latest Month: {latest['revenue_month'].date()}")
    print(f"Total ARR: ${latest['total_arr']:,.2f}")
    print(f"ARR Growth vs Previous Month: {arr_growth:.2f}%")
    print(f"Total Bookings: ${latest['total_bookings']:,.2f}")
    print(f"Bookings Growth vs Previous Month: {bookings_growth:.2f}%")
    print(f"Expansion Revenue: ${latest['expansion_revenue']:,.2f}")
    print(f"Churned Revenue: ${latest['churned_revenue']:,.2f}")

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
You are a strategic finance analyst.

Generate concise executive-level revenue commentary for leadership based on the following KPI metrics.

Focus on:
- ARR trends
- bookings performance
- churn risk
- business trajectory
- expansion revenue versus churned revenue

Use a professional, CFO-ready tone.

Return the output in this format:

Executive Summary:
- 3 concise bullets

Key Risks:
- 2 concise bullets

Recommended Follow-Up:
- 2 concise bullets

Metrics:
{context}
"""

    response = model.generate_content(prompt)

    print("\nAI Executive Summary")
    print("--------------------")
    print(response.text)


if __name__ == "__main__":
    main()