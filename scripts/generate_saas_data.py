from pathlib import Path

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

customers_df.to_csv(OUTPUT_DIR / "dim_customers.csv", index=False)
products_df.to_csv(OUTPUT_DIR / "dim_products.csv", index=False)
revenue_df.to_csv(OUTPUT_DIR / "fact_revenue_monthly.csv", index=False)

print("Generated SaaS finance datasets:")
print(f"- {OUTPUT_DIR / 'dim_customers.csv'}")
print(f"- {OUTPUT_DIR / 'dim_products.csv'}")
print(f"- {OUTPUT_DIR / 'fact_revenue_monthly.csv'}")
