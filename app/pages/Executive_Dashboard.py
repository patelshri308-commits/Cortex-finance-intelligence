import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide"
)

st.title("Executive Dashboard")

df = pd.read_csv("data/monthly_kpis.csv")
df["revenue_month"] = pd.to_datetime(df["revenue_month"])

latest = df.iloc[-1]
previous = df.iloc[-2]

arr_growth = ((latest["total_arr"] - previous["total_arr"]) / previous["total_arr"]) * 100
bookings_growth = ((latest["total_bookings"] - previous["total_bookings"]) / previous["total_bookings"]) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total ARR", f"${latest['total_arr']:,.0f}", f"{arr_growth:.2f}%")
col2.metric("Bookings", f"${latest['total_bookings']:,.0f}", f"{bookings_growth:.2f}%")
col3.metric("Expansion Revenue", f"${latest['expansion_revenue']:,.0f}")
col4.metric("Churned Revenue", f"${latest['churned_revenue']:,.0f}")

st.subheader("ARR Trend")

arr_fig = px.line(
    df,
    x="revenue_month",
    y="total_arr",
    title="Monthly ARR"
)

st.plotly_chart(arr_fig, width="stretch")

st.subheader("Bookings Trend")

bookings_fig = px.line(
    df,
    x="revenue_month",
    y="total_bookings",
    title="Monthly Bookings"
)

st.plotly_chart(bookings_fig, width="stretch")
