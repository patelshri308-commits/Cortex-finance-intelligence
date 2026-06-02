import streamlit as st

st.set_page_config(
    page_title="Cortex Finance Intelligence",
    layout="wide",
)

st.sidebar.title("Cortex Finance Intelligence")
st.sidebar.markdown("AI-native finance analytics workspace for SaaS revenue workflows.")

st.title("Cortex Finance Intelligence Platform")
st.caption("AI-native finance analytics, workflow orchestration, and executive reporting automation powered by Snowflake Cortex.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Executive Dashboard")
        st.write("Monitor ARR, bookings, churn, and revenue trends from Snowflake KPI tables.")
        st.page_link("pages/Executive_Dashboard.py", label="Open Dashboard", icon="📊")

with col2:
    with st.container(border=True):
        st.subheader("AI Finance Workspace")
        st.write("Ask finance questions and route them to specialized Snowflake Cortex agents.")
        st.page_link("pages/AI_Finance_Workspace.py", label="Open Workspace", icon="🤖")

with col3:
    with st.container(border=True):
        st.subheader("Reporting Automation")
        st.write("Generate finance reporting packages from KPI data and AI workflow outputs.")
        st.page_link("pages/AI_Finance_Workspace.py", label="Generate Reports", icon="📄")

st.divider()

st.subheader("Workflow Capabilities")

workflow_col1, workflow_col2 = st.columns(2)

with workflow_col1:
    with st.container(border=True):
        st.markdown(
            """
            **AI Workflow Agents**
            - Revenue Summary Agent
            - Variance Analysis Agent
            - Forecast Sensitivity Agent
            - Executive Briefing Agent
            """
        )

with workflow_col2:
    with st.container(border=True):
        st.markdown(
            """
            **Architecture Layers**
            - Snowflake KPI layer
            - Semantic metrics layer
            - Router orchestration layer
            - Snowflake Cortex reasoning layer
            - Report/export automation
            """
        )

st.divider()

st.subheader("How It Works")

st.markdown(
    """
    ```text
    Curated SaaS Finance KPIs in Snowflake
            ↓
    Semantic Business Context
            ↓
    Router Agent
            ↓
    Specialized Finance Agent
            ↓
    Snowflake Cortex COMPLETE
            ↓
    Executive Commentary / Report Export
    ```
    """
)

st.info("This project uses synthetic SaaS finance data to simulate an enterprise finance analytics workflow.")
