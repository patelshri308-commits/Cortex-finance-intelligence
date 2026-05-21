REQUIRED_MONTHLY_KPI_COLUMNS = [
    "revenue_month",
    "total_arr",
    "total_mrr",
    "total_bookings",
    "expansion_revenue",
    "contraction_revenue",
    "churned_revenue",
    "new_business_revenue",
    "renewal_revenue",
]


def validate_required_columns(df, required_columns):
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )


def validate_monthly_kpis(df):
    validate_required_columns(
        df,
        REQUIRED_MONTHLY_KPI_COLUMNS
    )
