from __future__ import annotations

from src.snowflake_query import _secret, get_connection


def run_cortex(prompt: str, model: str | None = None) -> str:
    """Run Snowflake Cortex COMPLETE through the Snowflake Python connector."""
    selected_model = model or _secret("CORTEX_MODEL", "llama3.1-70b")

    sql = "SELECT SNOWFLAKE.CORTEX.COMPLETE(%s, %s) AS response"

    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql, (selected_model, prompt))
            row = cur.fetchone()
            return row[0] if row else ""
        finally:
            cur.close()
