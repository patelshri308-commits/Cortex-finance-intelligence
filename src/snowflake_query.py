import json
import subprocess

import pandas as pd


def query_snowflake_to_df(sql: str) -> pd.DataFrame:
    result = subprocess.run(
        ["snow", "sql", "-q", sql, "--format", "json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Snowflake query failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    data = json.loads(result.stdout)

    df = pd.DataFrame(data)

    # Normalize Snowflake uppercase columns to existing app lowercase columns
    df.columns = [col.lower() for col in df.columns]

    # Convert dates
    if "revenue_month" in df.columns:
        df["revenue_month"] = pd.to_datetime(df["revenue_month"])

    # Convert numeric strings from Snowflake CLI JSON output
    numeric_columns = [
        "total_arr",
        "total_mrr",
        "total_bookings",
        "expansion_revenue",
        "contraction_revenue",
        "churned_revenue",
        "new_business_revenue",
        "renewal_revenue",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df