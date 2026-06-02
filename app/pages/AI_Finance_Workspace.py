from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from agents.executive_briefing_agent import generate_executive_briefing
from agents.forecast_sensitivity_agent import (
    generate_forecast_sensitivity,
    generate_forecast_sensitivity_from_question,
)
from agents.revenue_summary_agent import generate_revenue_summary
from agents.router_agent import route_query
from agents.variance_analysis_agent import generate_variance_analysis
from evaluation.evaluation_history import get_latest_evaluation
from exports.excel_exporter import export_finance_report

st.set_page_config(page_title="AI Finance Workspace", layout="wide")

WORKFLOW_LABELS = {
    "revenue_summary": "Revenue Summary Agent",
    "variance_analysis": "Variance Analysis Agent",
    "forecast_sensitivity": "Forecast Sensitivity Agent",
    "executive_briefing": "Executive Briefing Agent",
}


def _format_eval_pass_rate(summary: dict | None) -> str:
    if not summary:
        return "N/A"
    return f"{summary.get('pass_rate', 0):.0f}%"


def _get_latest_evaluation_status() -> dict | None:
    try:
        return get_latest_evaluation()
    except Exception:
        return None


st.title("AI Finance Workspace")
st.caption("Router-agent finance analytics powered by Snowflake Cortex.")

with st.container(border=True):
    latest_evaluation = _get_latest_evaluation_status()
    if latest_evaluation:
        router_rate = _format_eval_pass_rate(latest_evaluation.get("router"))
        semantic_rate = _format_eval_pass_rate(latest_evaluation.get("semantic"))
        e2e_rate = _format_eval_pass_rate(latest_evaluation.get("end_to_end"))
        st.markdown(
            f"**AI Quality Checks:** Router {router_rate} · Semantic {semantic_rate} · E2E {e2e_rate}  \n"
            f"_Latest local evaluation: {latest_evaluation.get('timestamp', 'Unknown')}_"
        )
    else:
        st.markdown("**AI Quality Checks:** run evaluation_runner.py to generate latest status.")

if "workflow_history" not in st.session_state:
    st.session_state.workflow_history = []

with st.sidebar:
    st.subheader("Snowflake Cortex Settings")
    st.write(f"Model: `{st.secrets.get('CORTEX_MODEL', 'llama3.1-70b')}`")
    st.write(f"Warehouse: `{st.secrets.get('SNOWFLAKE_WAREHOUSE', 'Not configured')}`")
    st.write(f"Role: `{st.secrets.get('SNOWFLAKE_ROLE', 'Not configured')}`")
    st.write(f"KPI table: `{st.secrets.get('SNOWFLAKE_KPI_TABLE', 'FINANCE_AI.RAW.MONTHLY_KPIS')}`")

st.write("Ask a finance question and the router will select the correct specialized Cortex workflow.")

with st.form("ai_query_form"):
    user_query = st.text_input(
        "Ask a finance question",
        placeholder="Example: Summarize the latest revenue performance and identify key risks.",
    )
    submitted = st.form_submit_button("Run AI Analysis", type="primary")

if submitted:
    if not user_query.strip():
        st.warning("Please enter a finance question.")
    else:
        selected_workflow = route_query(user_query)
        st.info(f"Selected workflow: {WORKFLOW_LABELS.get(selected_workflow, selected_workflow)}")

        with st.spinner("Running Snowflake Cortex workflow..."):
            try:
                if selected_workflow == "revenue_summary":
                    result = generate_revenue_summary()
                elif selected_workflow == "variance_analysis":
                    result = generate_variance_analysis(user_query)
                elif selected_workflow == "forecast_sensitivity":
                    result = generate_forecast_sensitivity_from_question(user_query)
                elif selected_workflow == "executive_briefing":
                    result = generate_executive_briefing()
                else:
                    result = "No workflow matched."

                st.markdown(result)

                st.session_state.workflow_history.insert(
                    0,
                    {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "query": user_query,
                        "workflow": selected_workflow,
                        "result": result,
                    },
                )
                st.session_state.workflow_history = st.session_state.workflow_history[:5]

            except Exception as exc:
                st.error(f"Cortex workflow failed: {exc}")

st.divider()

st.subheader("Finance Report Export")
st.write("Generate a multi-tab Excel report containing KPI data and AI workflow outputs.")

if st.button("Generate Finance Report"):
    with st.spinner("Generating report..."):
        try:
            report_path = export_finance_report()
            st.success("Finance report generated successfully.")

            with open(report_path, "rb") as file:
                st.download_button(
                    label="Download Excel Report",
                    data=file,
                    file_name="cortex_finance_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        except Exception as exc:
            st.error(f"Report generation failed: {exc}")

st.divider()

st.subheader("Interactive Forecast Scenario")
st.write("Adjust forecast assumptions and generate Cortex-powered scenario commentary.")

col1, col2 = st.columns(2)

with col1:
    arr_growth_adjustment = st.slider("ARR Growth Adjustment (%)", -20, 20, 5)
    bookings_growth_adjustment = st.slider("New ARR Bookings Growth Adjustment (%)", -20, 20, 3)
    churn_change = st.slider("Churned ARR Change (%)", -50, 50, 10)

with col2:
    expansion_change = st.slider("Expansion ARR Change (%)", -50, 50, 5)
    contraction_change = st.slider("Contraction ARR Change (%)", -50, 50, 0)

if st.button("Run Forecast Scenario"):
    with st.spinner("Running forecast sensitivity analysis with Snowflake Cortex..."):
        try:
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

            st.session_state.workflow_history.insert(
                0,
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "query": "Interactive forecast scenario",
                    "workflow": "forecast_sensitivity",
                    "result": forecast_result,
                },
            )
            st.session_state.workflow_history = st.session_state.workflow_history[:5]
        except Exception as exc:
            st.error(f"Forecast scenario failed: {exc}")

st.divider()

st.subheader("Recent AI Analyses")

if not st.session_state.workflow_history:
    st.caption("No analyses have been run yet.")
else:
    for item in st.session_state.workflow_history:
        with st.expander(f"{item['timestamp']} · {item['workflow']} · {item['query']}"):
            st.markdown(item["result"])
