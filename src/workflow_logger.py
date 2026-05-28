import json
import subprocess


def _sql_string(value: str) -> str:
    """
    Safely formats Python text as a Snowflake SQL string literal.
    Uses dollar-quoted strings so multiline prompts/responses do not break SQL.
    """
    if value is None:
        return "NULL"

    value = str(value)

    # Avoid rare delimiter collision
    delimiter = "$$"
    if "$$" in value:
        value = value.replace("$$", "$ $")

    return f"{delimiter}{value}{delimiter}"


def log_agent_run(
    agent_name: str,
    model_name: str,
    workflow_type: str,
    prompt: str,
    response: str
) -> None:
    sql = f"""
    INSERT INTO FINANCE_AI.WORKFLOWS.AGENT_RUN_HISTORY
        (agent_name, model_name, workflow_type, prompt, response)
    VALUES
        (
            {_sql_string(agent_name)},
            {_sql_string(model_name)},
            {_sql_string(workflow_type)},
            {_sql_string(prompt)},
            {_sql_string(response)}
        );
    """

    result = subprocess.run(
        ["snow", "sql", "-q", sql],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to log agent run.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    print("Workflow log inserted successfully.")
