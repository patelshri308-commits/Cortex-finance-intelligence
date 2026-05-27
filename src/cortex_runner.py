import subprocess
import textwrap


def run_cortex(prompt: str, model: str = "llama3.1-70b") -> str:
    escaped_prompt = prompt.replace("'", "''")

    sql = f"""
    SELECT SNOWFLAKE.CORTEX.AI_COMPLETE(
        '{model}',
        '{escaped_prompt}'
    );
    """

    result = subprocess.run(
        ["snow", "sql", "-q", textwrap.dedent(sql)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout