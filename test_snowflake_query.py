from src.snowflake_query import query_snowflake_to_df

df = query_snowflake_to_df("""
SELECT *
FROM FINANCE_AI.RAW.MONTHLY_KPIS
ORDER BY REVENUE_MONTH
LIMIT 5;
""")

print(df)