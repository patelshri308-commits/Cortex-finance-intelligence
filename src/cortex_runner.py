import json
import subprocess
import textwrap


def run_cortex(prompt: str, model: str = "llama3.1-70b") -> str:
    escaped_prompt = prompt.replace("'", "''")

    sql = f"""
    SELECT SNOWFLAKE.CORTEX.AI_COMPLETE(
        '{model}',
        '{escaped_prompt}'
    ) AS response;
    """

    result = subprocess.run(
        ["snow", "sql", "-q", textwrap.dedent(sql), "--format", "json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Cortex call failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    data = json.loads(result.stdout)

    if not data:
        return ""

    return data[0]["RESPONSE"]
