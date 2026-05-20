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
