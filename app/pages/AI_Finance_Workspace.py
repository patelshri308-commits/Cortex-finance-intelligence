import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from agents.executive_briefing_agent import generate_executive_briefing
from agents.forecast_sensitivity_agent import generate_forecast_sensitivity
from agents.revenue_summary_agent import generate_revenue_summary
from agents.router_agent import route_query
from agents.variance_analysis_agent import generate_variance_analysis
from exports.excel_exporter import export_finance_report


st.set_page_config(
    page_title="AI Finance Workspace",
    layout="wide"
)

st.title("AI Finance Workspace")

st.write(
    "Ask a finance question and the router will select the correct AI workflow."
)

user_query = st.text_input(
    "Ask a finance question",
    placeholder="Example: What happens if churn increases by 10%?"
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

            elif selected_workflow == "forecast_sensitivity":
                result = generate_forecast_sensitivity(
                    arr_growth_adjustment_pct=5,
                    bookings_growth_adjustment_pct=3,
                    churn_change_pct=10,
                    expansion_change_pct=5,
                    contraction_change_pct=0,
                )

            elif selected_workflow == "executive_briefing":
                result = generate_executive_briefing()

            else:
                result = "No workflow matched."

        st.markdown(result)
    st.divider()

st.subheader("Finance Report Export")

st.write(
    "Generate a multi-tab Excel report containing KPI data and AI workflow outputs."
)

if st.button("Generate Finance Report"):
    with st.spinner("Generating report..."):
        report_path = export_finance_report()

    st.success("Finance report generated successfully.")

    with open(report_path, "rb") as file:
        st.download_button(
            label="Download Excel Report",
            data=file,
            file_name="cortex_finance_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

st.divider()

st.subheader("Interactive Forecast Scenario")

st.write(
    "Adjust forecast assumptions and generate AI-powered scenario commentary."
)

col1, col2 = st.columns(2)

with col1:
    arr_growth_adjustment = st.slider(
        "ARR Growth Adjustment (%)",
        min_value=-20,
        max_value=20,
        value=5
    )

    bookings_growth_adjustment = st.slider(
        "Bookings Growth Adjustment (%)",
        min_value=-20,
        max_value=20,
        value=3
    )

    churn_change = st.slider(
        "Churned Revenue Change (%)",
        min_value=-50,
        max_value=50,
        value=10
    )

with col2:
    expansion_change = st.slider(
        "Expansion Revenue Change (%)",
        min_value=-50,
        max_value=50,
        value=5
    )

    contraction_change = st.slider(
        "Contraction Revenue Change (%)",
        min_value=-50,
        max_value=50,
        value=0
    )

if st.button("Run Forecast Scenario"):
    with st.spinner("Running forecast sensitivity analysis..."):
        forecast_result = generate_forecast_sensitivity(
            arr_growth_adjustment_pct=arr_growth_adjustment,
            bookings_growth_adjustment_pct=bookings_growth_adjustment,
            churn_change_pct=churn_change,
            expansion_change_pct=expansion_change,
            contraction_change_pct=contraction_change,
        )

    st.success("Forecast scenario generated.")

    with st.container(border=True):
        st.markdown(forecast_result)