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


def format_currency_compact(value: float) -> str:
    amount = float(value)
    sign = "-" if amount < 0 else ""
    amount = abs(amount)

    if amount >= 1_000_000:
        return f"{sign}${amount / 1_000_000:.1f}M"
    if amount >= 1_000:
        return f"{sign}${amount / 1_000:.0f}K"
    return f"{sign}${amount:,.0f}"


def build_arr_bridge_insight(
    arr_movement: float,
    growth_drivers: float,
    retention_headwinds: float,
    expansion_revenue: float,
    churned_revenue: float,
) -> str:
    if arr_movement < 0:
        if retention_headwinds > growth_drivers:
            return "ARR declined primarily because churned ARR and contraction ARR exceeded expansion ARR and new ARR bookings."
        return (
            "ARR declined month-over-month despite positive growth drivers; contraction ARR and churned ARR remain the "
            "main visible retention headwinds."
        )

    if expansion_revenue >= churned_revenue:
        return "ARR growth was supported by expansion ARR offsetting churned ARR pressure."
    return "ARR grew month-over-month, with new ARR bookings carrying growth despite churned ARR pressure."


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

col1.metric("Ending ARR", f"${latest['total_arr']:,.0f}", f"{arr_growth:.2f}% MoM Change")
col2.metric("New ARR Bookings", f"${latest['total_bookings']:,.0f}", f"{bookings_growth:.2f}% MoM Change")
col3.metric("Expansion ARR", f"${latest['expansion_revenue']:,.0f}")
col4.metric("Churned ARR", f"${latest['churned_revenue']:,.0f}")

with st.expander("Finance metric definitions"):
    st.markdown(
        "- **New ARR Bookings** = new recurring revenue from new customers.\n"
        "- **Expansion ARR** = additional recurring revenue from existing customers.\n"
        "- **Churned ARR** = recurring revenue lost from customers who left.\n"
        "- **Contraction ARR** = recurring revenue lost from existing customers reducing spend.\n"
        "- **Ending ARR** = ARR balance at the end of the period."
    )

st.subheader("ARR Bridge")

starting_arr = previous["total_arr"]
ending_arr = latest["total_arr"]
new_arr_bookings = latest.get("new_business_revenue", latest["total_bookings"])
expansion_revenue = latest["expansion_revenue"]
churned_revenue = latest["churned_revenue"]
contraction_revenue = latest["contraction_revenue"]
arr_movement = ending_arr - starting_arr
growth_drivers = new_arr_bookings + expansion_revenue
retention_headwinds = churned_revenue + contraction_revenue
bridge_insight = build_arr_bridge_insight(
    arr_movement,
    growth_drivers,
    retention_headwinds,
    expansion_revenue,
    churned_revenue,
)

bridge_col1, bridge_col2, bridge_col3 = st.columns(3)
bridge_col1.metric("Starting ARR", format_currency_compact(starting_arr), help="Prior month ending ARR.")
bridge_col2.metric(
    "Ending ARR",
    format_currency_compact(ending_arr),
    f"{format_currency_compact(arr_movement)} vs Prior Month",
)
bridge_col3.metric("Net ARR Movement", format_currency_compact(arr_movement))

driver_col, headwind_col = st.columns(2)
with driver_col:
    st.success(
        f"+ New ARR Bookings: {format_currency_compact(new_arr_bookings)}\n\n"
        f"+ Expansion ARR: {format_currency_compact(expansion_revenue)}"
    )
with headwind_col:
    st.error(
        f"- Churned ARR: {format_currency_compact(churned_revenue)}\n\n"
        f"- Contraction ARR: {format_currency_compact(contraction_revenue)}"
    )

st.caption(
    f"Growth Drivers = New ARR Bookings + Expansion ARR "
    f"({format_currency_compact(growth_drivers)}) · "
    f"Retention Headwinds = Churned ARR + Contraction ARR "
    f"({format_currency_compact(retention_headwinds)})"
)
with st.container(border=True):
    st.markdown("**Executive Insight**")
    st.write(bridge_insight)

st.subheader("ARR Trend")
arr_fig = px.line(df, x="revenue_month", y="total_arr", title=f"Monthly ARR Trend: {data_range}")
st.plotly_chart(arr_fig, width="stretch")

st.subheader("New ARR Bookings Trend")
bookings_fig = px.line(
    df,
    x="revenue_month",
    y="total_bookings",
    title=f"Monthly New ARR Bookings Trend: {data_range}",
)
st.plotly_chart(bookings_fig, width="stretch")

with st.expander("View underlying KPI data"):
    st.caption(f"Dashboard source data range: {data_range}")
    st.dataframe(df, width="stretch")
