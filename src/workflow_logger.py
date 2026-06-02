from src.snowflake_query import get_connection


def log_workflow_run(user_query: str, selected_agent: str, status: str, response_summary: str):
    sql = """
        INSERT INTO FINANCE_AI.WORKFLOWS.AGENT_RUN_HISTORY
            (run_timestamp, user_query, selected_agent, status, response_summary)
        VALUES
            (CURRENT_TIMESTAMP(), %s, %s, %s, %s)
    """

    try:
        with get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (user_query, selected_agent, status, response_summary))
            finally:
                cur.close()
    except Exception:
        # Logging should never break the user-facing demo
        pass