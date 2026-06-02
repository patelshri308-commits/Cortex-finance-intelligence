from __future__ import annotations

from src.snowflake_query import get_connection


def log_agent_run(
    agent_name: str,
    model_name: str,
    workflow_type: str,
    prompt: str,
    response: str,
) -> None:
    sql = """
    INSERT INTO FINANCE_AI.WORKFLOWS.AGENT_RUN_HISTORY
        (agent_name, model_name, workflow_type, prompt, response)
    VALUES
        (%s, %s, %s, %s, %s)
    """

    try:
        with get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (agent_name, model_name, workflow_type, prompt, response))
            finally:
                cur.close()
    except Exception:
        # Logging is non-critical and should not interrupt the user-facing demo.
        pass
