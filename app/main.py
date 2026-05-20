import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))
import pandas as pd
import plotly.express as px
import streamlit as st
from agents.router_agent import route_query
from agents.revenue_summary_agent import generate_revenue_summary
from agents.variance_analysis_agent import generate_variance_analysis

st.set_page_config(
    page_title="Cortex Finance Intelligence",
    layout="wide"
)

st.title("Cortex Finance Intelligence Platform")

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("data/monthly_kpis.csv")

df["revenue_month"] = pd.to_datetime(df["revenue_month"])

latest = df.iloc[-1]
previous = df.iloc[-2]

# -----------------------------
# KPI CARDS
# -----------------------------

arr_growth = (
    (
        latest["total_arr"] - previous["total_arr"]
    ) / previous["total_arr"]
) * 100

bookings_growth = (
    (
        latest["total_bookings"] - previous["total_bookings"]
    ) / previous["total_bookings"]
) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total ARR",
    f"${latest['total_arr']:,.0f}",
    f"{arr_growth:.2f}%"
)

col2.metric(
    "Bookings",
    f"${latest['total_bookings']:,.0f}",
    f"{bookings_growth:.2f}%"
)

col3.metric(
    "Expansion Revenue",
    f"${latest['expansion_revenue']:,.0f}"
)

col4.metric(
    "Churned Revenue",
    f"${latest['churned_revenue']:,.0f}"
)

# -----------------------------
# ARR TREND
# -----------------------------

st.subheader("ARR Trend")

arr_fig = px.line(
    df,
    x="revenue_month",
    y="total_arr",
    title="Monthly ARR"
)

st.plotly_chart(arr_fig, use_container_width=True)

# -----------------------------
# BOOKINGS TREND
# -----------------------------

st.subheader("Bookings Trend")

bookings_fig = px.line(
    df,
    x="revenue_month",
    y="total_bookings",
    title="Monthly Bookings"
)

st.plotly_chart(bookings_fig, use_container_width=True)

# -----------------------------
# AGENT SECTION
# -----------------------------

st.subheader("AI Workflow Agents")

if st.button("Run Revenue Summary Agent"):
    with open("outputs/revenue_summary.txt", "r") as file:
        st.text(file.read())

if st.button("Run Variance Analysis Agent"):
    with open("outputs/variance_analysis.txt", "r") as file:
        st.text(file.read())

st.subheader("AI Finance Workspace")

user_query = st.text_input(
    "Ask a finance question",
    placeholder="Example: Why did ARR decline this month?"
)

if st.button("Run AI Analysis"):
    if not user_query.strip():
        st.warning("Please enter a finance question.")
    else:
        selected_workflow = route_query(user_query)

        st.info(f"Selected workflow: {selected_workflow}")

        with st.spinner("Running AI workflow..."):
            if selected_workflow == "revenue_summary":
                result = generate_revenue_summary()

            elif selected_workflow == "variance_analysis":
                result = generate_variance_analysis()

            else:
                result = "Executive briefing agent is not built yet."

        st.markdown(result)
