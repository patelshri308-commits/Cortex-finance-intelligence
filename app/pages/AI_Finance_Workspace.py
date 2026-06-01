from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st

try:
    import snowflake.connector
except ImportError:  # keeps the page readable if dependencies are not installed yet
    snowflake = None

st.set_page_config(page_title="AI Finance Workspace", layout="wide")

CORTEX_MODEL = st.secrets.get("CORTEX_MODEL", "llama3.1-70b")
KPI_TABLE = st.secrets.get("SNOWFLAKE_KPI_TABLE", "MONTHLY_KPIS")
LOCAL_KPI_PATH = Path("data/monthly_kpis.csv")

AGENT_INSTRUCTIONS: Dict[str, str] = {
    "revenue_summary": """
You are the Revenue Summary Agent for a SaaS finance analytics workflow.
Focus on ARR, bookings, expansion revenue, churned revenue, and month-over-month performance.
Return concise executive commentary with business interpretation, not generic definitions.
""",
    "variance_analysis": """
You are the Variance Analysis Agent for a SaaS finance analytics workflow.
Explain what changed, why it matters, and which KPI movements most likely drove performance variance.
Separate favorable and unfavorable movements when useful.
""",
    "forecast_sensitivity": """
You are the Forecast Sensitivity Agent for a SaaS finance analytics workflow.
Explain how changes in ARR growth, bookings growth, churn, expansion, and contraction affect future revenue quality.
Highlight risks, upside cases, and operational actions.
""",
    "executive_briefing": """
You are the Executive Briefing Agent for a SaaS finance analytics workflow.
Write a CFO-ready briefing with headline, key movements, risks, opportunities, and recommended next actions.
Keep it direct, polished, and board-deck appropriate.
""",
}

WORKFLOW_LABELS = {
    "revenue_summary": "Revenue Summary Agent",
    "variance_analysis": "Variance Analysis Agent",
    "forecast_sensitivity": "Forecast Sensitivity Agent",
    "executive_briefing": "Executive Briefing Agent",
}


def get_connection():
    if snowflake is None:
        raise RuntimeError("snowflake-connector-python is not installed.")

    return snowflake.connector.connect(
        account=st.secrets["SNOWFLAKE_ACCOUNT"],
        user=st.secrets["SNOWFLAKE_USER"],
        password=st.secrets["SNOWFLAKE_PASSWORD"],
        warehouse=st.secrets["SNOWFLAKE_WAREHOUSE"],
        database=st.secrets["SNOWFLAKE_DATABASE"],
        schema=st.secrets["SNOWFLAKE_SCHEMA"],
        role=st.secrets.get("SNOWFLAKE_ROLE"),
    )


@st.cache_data(ttl=600)
def load_kpis() -> pd.DataFrame:
    """Load KPI data from Snowflake. Fall back to local synthetic CSV for demo resilience."""
    try:
        with get_connection() as conn:
            query = f"SELECT * FROM {KPI_TABLE} ORDER BY revenue_month"
            return pd.read_sql(query, conn)
    except Exception as exc:
        if LOCAL_KPI_PATH.exists():
            st.warning(f"Using local demo CSV because Snowflake KPI load failed: {exc}")
            return pd.read_csv(LOCAL_KPI_PATH)
        raise


def normalize_kpi_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.lower() for col in df.columns]
    if "revenue_month" in df.columns:
        df["revenue_month"] = pd.to_datetime(df["revenue_month"])
    return df


def build_kpi_context(df: pd.DataFrame) -> str:
    df = normalize_kpi_columns(df)
    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else latest

    def pct_change(column: str) -> float:
        if column not in df.columns or previous[column] == 0:
            return 0.0
        return ((latest[column] - previous[column]) / previous[column]) * 100

    key_columns = [
        "revenue_month",
        "total_arr",
        "total_bookings",
        "expansion_revenue",
        "churned_revenue",
        "contraction_revenue",
    ]
    available_columns = [col for col in key_columns if col in df.columns]
    recent_rows = df[available_columns].tail(6).to_markdown(index=False)

    return f"""
Latest month: {latest.get('revenue_month', 'N/A')}
Latest total ARR: {latest.get('total_arr', 'N/A')}
Latest total bookings: {latest.get('total_bookings', 'N/A')}
Latest expansion revenue: {latest.get('expansion_revenue', 'N/A')}
Latest churned revenue: {latest.get('churned_revenue', 'N/A')}
Latest contraction revenue: {latest.get('contraction_revenue', 'N/A')}
ARR month-over-month change: {pct_change('total_arr'):.2f}%
Bookings month-over-month change: {pct_change('total_bookings'):.2f}%

Recent KPI table:
{recent_rows}
"""


def route_query(user_query: str) -> str:
    q = user_query.lower()
    if any(term in q for term in ["forecast", "scenario", "sensitivity", "what happens", "churn increases", "increase", "decrease"]):
        return "forecast_sensitivity"
    if any(term in q for term in ["variance", "why", "driver", "changed", "movement", "difference"]):
        return "variance_analysis"
    if any(term in q for term in ["executive", "brief", "board", "cfo", "summary for leadership"]):
        return "executive_briefing"
    return "revenue_summary"


def cortex_complete(prompt: str) -> str:
    """Run Snowflake Cortex COMPLETE through the Snowflake Python connector."""
    escaped_prompt = prompt.replace("'", "''")
    escaped_model = CORTEX_MODEL.replace("'", "''")
    sql = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{escaped_model}', '{escaped_prompt}') AS RESPONSE"

    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql)
            return cur.fetchone()[0]
        finally:
            cur.close()


def run_agent(workflow: str, user_query: str, scenario_assumptions: str = "") -> str:
    df = load_kpis()
    kpi_context = build_kpi_context(df)
    agent_instruction = AGENT_INSTRUCTIONS[workflow]

    prompt = f"""
{agent_instruction}

User question:
{user_query}

Scenario assumptions:
{scenario_assumptions or 'None provided.'}

Finance KPI context:
{kpi_context}

Response requirements:
- Start with a direct answer.
- Use the KPI context provided.
- Mention the selected agent role.
- Keep the response executive-ready.
- Do not invent data that is not in the KPI context.
"""
    return cortex_complete(prompt)


def add_history(query: str, workflow: str, result: str) -> None:
    st.session_state.workflow_history.insert(
        0,
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "query": query,
            "workflow": workflow,
            "result": result,
        },
    )
    st.session_state.workflow_history = st.session_state.workflow_history[:5]


st.title("AI Finance Workspace")
st.caption("Router-agent finance analytics powered by Snowflake Cortex.")

if "workflow_history" not in st.session_state:
    st.session_state.workflow_history = []

with st.sidebar:
    st.subheader("Cortex Settings")
    st.write(f"Model: `{CORTEX_MODEL}`")
    st.write(f"KPI table: `{KPI_TABLE}`")

st.write("Ask a finance question and the router will select the correct specialized Cortex workflow.")

user_query = st.text_input(
    "Ask a finance question",
    placeholder="Example: What happens if churn increases by 10%?",
)

if st.button("Run AI Analysis", type="primary"):
    if not user_query.strip():
        st.warning("Please enter a finance question.")
    else:
        selected_workflow = route_query(user_query)
        st.info(f"Selected workflow: {WORKFLOW_LABELS[selected_workflow]}")

        with st.spinner("Running Snowflake Cortex workflow..."):
            try:
                result = run_agent(selected_workflow, user_query)
                st.markdown(result)
                add_history(user_query, selected_workflow, result)
            except Exception as exc:
                st.error(f"Cortex workflow failed: {exc}")

st.divider()

st.subheader("Interactive Forecast Scenario")
st.write("Adjust forecast assumptions and generate Cortex-powered scenario commentary.")

col1, col2 = st.columns(2)

with col1:
    arr_growth_adjustment = st.slider("ARR Growth Adjustment (%)", -20, 20, 5)
    bookings_growth_adjustment = st.slider("Bookings Growth Adjustment (%)", -20, 20, 3)
    churn_change = st.slider("Churned Revenue Change (%)", -50, 50, 10)

with col2:
    expansion_change = st.slider("Expansion Revenue Change (%)", -50, 50, 5)
    contraction_change = st.slider("Contraction Revenue Change (%)", -50, 50, 0)

if st.button("Run Forecast Scenario"):
    assumptions = f"""
ARR growth adjustment: {arr_growth_adjustment}%
Bookings growth adjustment: {bookings_growth_adjustment}%
Churned revenue change: {churn_change}%
Expansion revenue change: {expansion_change}%
Contraction revenue change: {contraction_change}%
"""
    with st.spinner("Running forecast sensitivity analysis with Snowflake Cortex..."):
        try:
            forecast_result = run_agent(
                "forecast_sensitivity",
                "Generate a forecast sensitivity analysis from the selected assumptions.",
                scenario_assumptions=assumptions,
            )
            st.success("Forecast scenario generated.")
            with st.container(border=True):
                st.markdown(forecast_result)
            add_history("Interactive forecast scenario", "forecast_sensitivity", forecast_result)
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
