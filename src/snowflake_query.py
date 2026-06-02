import pandas as pd
import streamlit as st
import snowflake.connector

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def get_connection():
    private_key_text = st.secrets.get("SNOWFLAKE_PRIVATE_KEY")

    connection_kwargs = {
        "account": st.secrets["SNOWFLAKE_ACCOUNT"],
        "user": st.secrets["SNOWFLAKE_USER"],
        "warehouse": st.secrets["SNOWFLAKE_WAREHOUSE"],
        "role": st.secrets["SNOWFLAKE_ROLE"],
    }

    if private_key_text:
        private_key = serialization.load_pem_private_key(
            private_key_text.encode("utf-8"),
            password=None,
            backend=default_backend(),
        )

        private_key_der = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        return snowflake.connector.connect(
            **connection_kwargs,
            private_key=private_key_der,
        )

    return snowflake.connector.connect(
        **connection_kwargs,
        password=st.secrets["SNOWFLAKE_PASSWORD"],
    )


def query_snowflake_to_df(sql: str) -> pd.DataFrame:
    with get_connection() as conn:
        df = pd.read_sql(sql, conn)

    df.columns = [col.lower() for col in df.columns]

    if "revenue_month" in df.columns:
        df["revenue_month"] = pd.to_datetime(df["revenue_month"])

    numeric_columns = [
        "total_arr",
        "total_mrr",
        "total_bookings",
        "expansion_revenue",
        "contraction_revenue",
        "churned_revenue",
        "new_business_revenue",
        "renewal_revenue",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df