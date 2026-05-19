from pathlib import Path
from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import datetime

fake = Faker()

# -----------------------------
# CONFIG
# -----------------------------

NUM_CUSTOMERS = 500
MONTHS = 24

industries = [
    "Healthcare",
    "Finance",
    "Retail",
    "Technology",
    "Manufacturing"
]

regions = [
    "North America",
    "EMEA",
    "APAC",
    "LATAM"
]

product_lines = [
    "Core Platform",
    "Analytics",
    "AI Suite",
    "Security",
    "Enterprise"
]

# -----------------------------
# CREATE CUSTOMERS
# -----------------------------

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    customers.append({
        "customer_id": customer_id,
        "customer_name": fake.company(),
        "industry": random.choice(industries),
        "region": random.choice(regions),
        "company_size": random.choice([
            "SMB",
            "Mid-Market",
            "Enterprise"
        ]),
        "signup_date": fake.date_between(
            start_date="-3y",
            end_date="today"
        ),
        "sales_channel": random.choice([
            "Direct Sales",
            "Partner",
            "Self-Service"
        ])
    })

customers_df = pd.DataFrame(customers)

# -----------------------------
# CREATE REVENUE DATA
# -----------------------------

revenue_rows = []

dates = pd.date_range(
    start="2023-01-01",
    periods=MONTHS,
    freq="MS"
)

for date in dates:

    for customer_id in customers_df["customer_id"]:

        base_arr = random.randint(5000, 150000)

        expansion = random.randint(0, 20000)

        contraction = random.randint(0, 10000)

        churn_probability = random.random()

        churned = churn_probability < 0.03

        churned_revenue = base_arr if churned else 0

        arr = max(
            base_arr + expansion - contraction - churned_revenue,
            0
        )

        mrr = arr / 12

        bookings = random.randint(1000, 50000)

        revenue_rows.append({
            "date": date,
            "customer_id": customer_id,
            "product_line": random.choice(product_lines),
            "arr": arr,
            "mrr": round(mrr, 2),
            "bookings": bookings,
            "expansion_revenue": expansion,
            "contraction_revenue": contraction,
            "churned_revenue": churned_revenue,
            "new_business_revenue": random.randint(0, 30000),
            "renewal_revenue": random.randint(0, 40000)
        })

revenue_df = pd.DataFrame(revenue_rows)

# -----------------------------
# CREATE PRODUCTS
# -----------------------------

products = []

for product_id in range(1, 11):

    products.append({
        "product_id": product_id,
        "product_name": f"Product {product_id}",
        "product_category": random.choice([
            "AI",
            "Analytics",
            "Security",
            "Infrastructure"
        ]),
        "pricing_tier": random.choice([
            "Basic",
            "Professional",
            "Enterprise"
        ])
    })

products_df = pd.DataFrame(products)

# -----------------------------
# SAVE FILES
# -----------------------------

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

customers_df.to_csv(
    OUTPUT_DIR / "dim_customers.csv",
    index=False
)

revenue_df.to_csv(
    OUTPUT_DIR / "fact_revenue_monthly.csv",
    index=False
)

products_df.to_csv(
    OUTPUT_DIR / "dim_products.csv",
    index=False
)

print("Datasets generated successfully!")
print("Saved files:")
print("- data/dim_customers.csv")
print("- data/fact_revenue_monthly.csv")
print("- data/dim_products.csv")