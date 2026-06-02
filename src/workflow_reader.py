from src.snowflake_query import query_snowflake_to_df


def get_recent_workflows(limit: int = 10):
    sql = f"""
        SELECT
            run_timestamp,
            user_query,
            selected_agent,
            status,
            response_summary
        FROM FINANCE_AI.WORKFLOWS.AGENT_RUN_HISTORY
        ORDER BY run_timestamp DESC
        LIMIT {int(limit)}
    """

    try:
        return query_snowflake_to_df(sql)
    except Exception:
        return None