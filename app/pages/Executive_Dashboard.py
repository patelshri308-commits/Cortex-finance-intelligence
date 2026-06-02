from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.snowflake_query import query_snowflake_to_df

st.set_page_config(page_title="Executive Dashboard", layout="wide")

LOCAL_KPI_PATH = Path("data/monthly_kpis.csv")


def format_month_label(value) -> str:
    month = pd.to_datetime(value, errors="coerce")
    if pd.isna(month):
        return "Unknown"
    return month.strftime("%b %Y")


def format_month_range(df: pd.DataFrame) -> str:
    if "revenue_month" not in df.columns or df.empty:
        return "range unavailable"

    revenue_months = pd.to_datetime(df["revenue_month"], errors="coerce").dropna()
    if revenue_months.empty:
        return "range unavailable"

    start_month = revenue_months.min().strftime("%b %Y")
    end_month = revenue_months.max().strftime("%b %Y")
    return f"{start_month} - {end_month}"


def get_latest_month_label(df: pd.DataFrame) -> str:
    if "revenue_month" not in df.columns or df.empty:
        return "Unknown"
    return format_month_label(df["revenue_month"].max())


def load_dashboard_data() -> pd.DataFrame:
    table = st.secrets.get("SNOWFLAKE_KPI_TABLE", "FINANCE_AI.RAW.MONTHLY_KPIS")
    query = f"SELECT * FROM {table} ORDER BY revenue_month"

    try:
        return query_snowflake_to_df(query)
    except Exception as exc:
        if LOCAL_KPI_PATH.exists():
            st.warning(f"Using local demo CSV because Snowflake dashboard load failed: {exc}")
            df = pd.read_csv(LOCAL_KPI_PATH)
            df.columns = [col.lower() for col in df.columns]
            df["revenue_month"] = pd.to_datetime(df["revenue_month"], errors="coerce")
            return df
        raise


st.title("Executive Dashboard")
st.caption("Snowflake-backed SaaS finance KPI dashboard.")

df = load_dashboard_data().sort_values("revenue_month")
df["revenue_month"] = pd.to_datetime(df["revenue_month"], errors="coerce")
data_range = format_month_range(df)
latest_month_label = get_latest_month_label(df)

latest = df.iloc[-1]
previous = df.iloc[-2]

arr_growth = ((latest["total_arr"] - previous["total_arr"]) / previous["total_arr"]) * 100
bookings_growth = ((latest["total_bookings"] - previous["total_bookings"]) / previous["total_bookings"]) * 100

col1, col2, col3, col4 = st.columns(4)

st.caption(f"Latest month: {latest_month_label} · Comparison: prior month")

col1.metric("Total ARR", f"${latest['total_arr']:,.0f}", f"{arr_growth:.2f}% MoM Change")
col2.metric("Bookings", f"${latest['total_bookings']:,.0f}", f"{bookings_growth:.2f}% MoM Change")
col3.metric("Expansion Revenue", f"${latest['expansion_revenue']:,.0f}")
col4.metric("Churned Revenue", f"${latest['churned_revenue']:,.0f}")

st.subheader("ARR Trend")
arr_fig = px.line(df, x="revenue_month", y="total_arr", title=f"Monthly ARR Trend: {data_range}")
st.plotly_chart(arr_fig, width="stretch")

st.subheader("Bookings Trend")
bookings_fig = px.line(
    df,
    x="revenue_month",
    y="total_bookings",
    title=f"Monthly Bookings Trend: {data_range}",
)
st.plotly_chart(bookings_fig, width="stretch")

with st.expander("View underlying KPI data"):
    st.caption(f"Dashboard source data range: {data_range}")
    st.dataframe(df, width="stretch")
