--monthly kpi summary

CREATE OR REPLACE VIEW main.default.monthly_kpis AS
SELECT
    revenue_month,

    SUM(arr) AS total_arr,

    SUM(mrr) AS total_mrr,

    SUM(bookings) AS total_bookings,

    SUM(expansion_revenue) AS expansion_revenue,

    SUM(contraction_revenue) AS contraction_revenue,

    SUM(churned_revenue) AS churned_revenue,

    SUM(new_business_revenue) AS new_business_revenue,

    SUM(renewal_revenue) AS renewal_revenue

FROM main.default.fact_revenue_monthly

GROUP BY revenue_month

ORDER BY revenue_month;

--revenue

CREATE OR REPLACE VIEW main.default.revenue_by_region AS
SELECT
    f.revenue_month,
    c.region,

    SUM(f.arr) AS total_arr,

    SUM(f.bookings) AS total_bookings,

    SUM(f.churned_revenue) AS churned_revenue

FROM main.default.fact_revenue_monthly f

JOIN main.default.dim_customers c
    ON f.customer_id = c.customer_id

GROUP BY
    f.revenue_month,
    c.region;

--revenue by industry

CREATE OR REPLACE VIEW main.default.revenue_by_industry AS
SELECT
    f.revenue_month,
    c.industry,

    SUM(f.arr) AS total_arr,

    SUM(f.bookings) AS total_bookings

FROM main.default.fact_revenue_monthly f

JOIN main.default.dim_customers c
    ON f.customer_id = c.customer_id

GROUP BY
    f.revenue_month,
    c.industry;

--customer segment performance

CREATE OR REPLACE VIEW main.default.segment_performance AS
SELECT
    f.revenue_month,
    c.company_size,

    SUM(f.arr) AS total_arr,

    SUM(f.expansion_revenue) AS expansion_revenue,

    SUM(f.churned_revenue) AS churned_revenue

FROM main.default.fact_revenue_monthly f

JOIN main.default.dim_customers c
    ON f.customer_id = c.customer_id

GROUP BY
    f.revenue_month,
    c.company_size;
