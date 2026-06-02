import streamlit as st

from src.snowflake_query import get_connection


def run_cortex(prompt: str, model: str | None = None) -> str:
    model = model or st.secrets.get("CORTEX_MODEL", "llama3.1-70b")

    sql = """
        SELECT SNOWFLAKE.CORTEX.COMPLETE(%s, %s) AS response
    """

    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql, (model, prompt))
            row = cur.fetchone()
            return row[0] if row else ""
        finally:
            cur.close()