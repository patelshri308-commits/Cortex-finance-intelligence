USE ROLE ACCOUNTADMIN;
USE DATABASE FINANCE_AI;

CREATE TABLE IF NOT EXISTS ANALYTICS.MONTHLY_REVENUE (
    month DATE,
    revenue NUMBER(12,2),
    enterprise_growth_pct FLOAT,
    smb_churn_pct FLOAT,
    infrastructure_cost_growth_pct FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);


