import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

def run_cortex(prompt: str, model: str):

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    cursor = conn.cursor()

    query = f"""
    SELECT SNOWFLAKE.CORTEX.AI_COMPLETE(
        model => '{model}',
        prompt => %s
    )
    """

    cursor.execute(query, (prompt,))
    response = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return response
