from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

try:
    import snowflake.connector
except ImportError:
    snowflake = None

st.set_page_config(page_title="Executive Dashboard", layout="wide")

KPI_TABLE = st.secrets.get("SNOWFLAKE_KPI_TABLE", "MONTHLY_KPIS")
LOCAL_KPI_PATH = Path("data/monthly_kpis.csv")


def get_connection():
    """Create a Snowflake connection.

    Public Streamlit deployments should use Snowflake key-pair auth through
    SNOWFLAKE_PRIVATE_KEY so MFA does not block the app. Password auth is kept
    only as a local/dev fallback.
    """
    if snowflake is None:
        raise RuntimeError("snowflake-connector-python is not installed.")

    private_key_text = st.secrets.get("SNOWFLAKE_PRIVATE_KEY")

    connection_kwargs = {
        "account": st.secrets["SNOWFLAKE_ACCOUNT"],
        "user": st.secrets["SNOWFLAKE_USER"],
        "warehouse": st.secrets["SNOWFLAKE_WAREHOUSE"],
        "role": st.secrets.get("SNOWFLAKE_ROLE"),
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


@st.cache_data(ttl=600)
def load_kpis() -> pd.DataFrame:
    try:
        with get_connection() as conn:
            return pd.read_sql(f"SELECT * FROM {KPI_TABLE} ORDER BY revenue_month", conn)
    except Exception as exc:
        if LOCAL_KPI_PATH.exists():
            st.warning(f"Using local demo CSV because Snowflake KPI load failed: {exc}")
            return pd.read_csv(LOCAL_KPI_PATH)
        raise


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.lower() for col in df.columns]
    df["revenue_month"] = pd.to_datetime(df["revenue_month"])
    return df


st.title("Executive Dashboard")
st.caption("Snowflake finance KPI layer for SaaS revenue analytics.")

df = normalize_columns(load_kpis())

latest = df.iloc[-1]
previous = df.iloc[-2]

arr_growth = ((latest["total_arr"] - previous["total_arr"]) / previous["total_arr"]) * 100
bookings_growth = ((latest["total_bookings"] - previous["total_bookings"]) / previous["total_bookings"]) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total ARR", f"${latest['total_arr']:,.0f}", f"{arr_growth:.2f}%")
col2.metric("Bookings", f"${latest['total_bookings']:,.0f}", f"{bookings_growth:.2f}%")
col3.metric("Expansion Revenue", f"${latest['expansion_revenue']:,.0f}")
col4.metric("Churned Revenue", f"${latest['churned_revenue']:,.0f}")

st.subheader("ARR Trend")
st.plotly_chart(px.line(df, x="revenue_month", y="total_arr", title="Monthly ARR"), width="stretch")

st.subheader("Bookings Trend")
st.plotly_chart(px.line(df, x="revenue_month", y="total_bookings", title="Monthly Bookings"), width="stretch")

with st.expander("View KPI data"):
    st.dataframe(df, use_container_width=True)
