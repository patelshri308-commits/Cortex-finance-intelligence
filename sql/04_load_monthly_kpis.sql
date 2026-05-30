CREATE OR REPLACE TABLE RAW.MONTHLY_KPIS (
    revenue_month DATE,
    total_arr NUMBER(14,2),
    total_mrr NUMBER(14,2),
    total_bookings NUMBER(14,2),
    expansion_revenue NUMBER(14,2),
    contraction_revenue NUMBER(14,2),
    churned_revenue NUMBER(14,2),
    new_business_revenue NUMBER(14,2),
    renewal_revenue NUMBER(14,2)
);