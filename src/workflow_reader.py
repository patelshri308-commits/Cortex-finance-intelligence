from __future__ import annotations

from src.snowflake_query import query_snowflake_to_df


def get_recent_agent_runs(limit: int = 5) -> list[dict]:
    sql = f"""
    SELECT
        id,
        agent_name,
        model_name,
        workflow_type,
        created_at
    FROM FINANCE_AI.WORKFLOWS.AGENT_RUN_HISTORY
    ORDER BY created_at DESC
    LIMIT {int(limit)};
    """

    try:
        return query_snowflake_to_df(sql).to_dict(orient="records")
    except Exception:
        # Workflow history should never break the public demo.
        return []
