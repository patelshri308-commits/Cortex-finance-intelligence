import json
import subprocess


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
    LIMIT {limit};
    """

    result = subprocess.run(
        ["snow", "sql", "-q", sql, "--format", "json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to fetch workflow history.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    data = json.loads(result.stdout)

    return data
