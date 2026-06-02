from __future__ import annotations

import os
from typing import Any

import pandas as pd
import snowflake.connector

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

try:
    import streamlit as st
except Exception:  # Allows command-line use outside Streamlit.
    st = None


def _secret(name: str, default: str | None = None) -> str | None:
    """Read config from Streamlit secrets first, then environment variables."""
    if st is not None:
        try:
            value = st.secrets.get(name)
            if value is not None:
                return value
        except Exception:
            pass

    return os.getenv(name, default)


def _private_key_der(private_key_text: str) -> bytes:
    private_key = serialization.load_pem_private_key(
        private_key_text.encode("utf-8"),
        password=None,
        backend=default_backend(),
    )

    return private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def get_connection():
    """Create a Snowflake connection for Streamlit Cloud/public deployment.

    Uses key-pair auth when SNOWFLAKE_PRIVATE_KEY exists. Password auth is kept
    only as a local fallback. Database/schema are intentionally not passed into
    the connection so object access is controlled through fully-qualified SQL.
    """
    account = _secret("SNOWFLAKE_ACCOUNT")
    user = _secret("SNOWFLAKE_USER")
    warehouse = _secret("SNOWFLAKE_WAREHOUSE")
    role = _secret("SNOWFLAKE_ROLE")
    private_key_text = _secret("SNOWFLAKE_PRIVATE_KEY")
    password = _secret("SNOWFLAKE_PASSWORD")

    if not account or not user or not warehouse:
        raise RuntimeError(
            "Missing Snowflake configuration. Required: SNOWFLAKE_ACCOUNT, "
            "SNOWFLAKE_USER, and SNOWFLAKE_WAREHOUSE."
        )

    connection_kwargs: dict[str, Any] = {
        "account": account,
        "user": user,
        "warehouse": warehouse,
    }

    if role:
        connection_kwargs["role"] = role

    if private_key_text:
        connection_kwargs["private_key"] = _private_key_der(private_key_text)
    elif password:
        connection_kwargs["password"] = password
    else:
        raise RuntimeError(
            "Missing Snowflake authentication. Provide SNOWFLAKE_PRIVATE_KEY "
            "for Streamlit Cloud or SNOWFLAKE_PASSWORD for local development."
        )

    return snowflake.connector.connect(**connection_kwargs)


def query_snowflake_to_df(sql: str) -> pd.DataFrame:
    """Run SQL against Snowflake and return a normalized pandas DataFrame."""
    with get_connection() as conn:
        df = pd.read_sql(sql, conn)

    df.columns = [str(col).lower() for col in df.columns]

    if "revenue_month" in df.columns:
        df["revenue_month"] = pd.to_datetime(df["revenue_month"], errors="coerce")

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
