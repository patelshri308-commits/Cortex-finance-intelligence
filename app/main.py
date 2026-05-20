import streamlit as st

st.set_page_config(
    page_title="Cortex Finance Intelligence",
    layout="wide"
)

st.title("Cortex Finance Intelligence Platform")

st.write(
    """
    AI-native finance analytics workspace for SaaS revenue analysis,
    variance commentary, forecast sensitivity, and executive briefing workflows.
    """
)

st.subheader("Available Workflows")

st.markdown(
    """
    - **Executive Dashboard** — KPI cards and revenue trend visualizations
    - **AI Finance Workspace** — natural-language router for finance workflows
    - **Revenue Summary Agent** — executive revenue performance commentary
    - **Variance Analysis Agent** — month-over-month business driver analysis
    - **Forecast Sensitivity Agent** — what-if scenario analysis
    - **Executive Briefing Agent** — CFO-ready synthesis of multiple AI workflows
    """
)
