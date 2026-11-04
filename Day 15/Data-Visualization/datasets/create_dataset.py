import pandas as pd
import numpy as np
from pathlib import Path

# Create reproducible sample data
np.random.seed(42)

n = 300

products = ["Laptop", "Mobile", "Tablet", "Headphones", "Keyboard"]
regions = ["South", "North", "East", "West"]
categories = ["Electronics", "Accessories", "Computers"]

df = pd.DataFrame({
    "Date": pd.date_range("2026-01-01", periods=n, freq="D"),
    "Product": np.random.choice(products, n),
    "Region": np.random.choice(regions, n),
    "Category": np.random.choice(categories, n),
    "Sales": np.random.randint(500, 15000, n),
    "Quantity": np.random.randint(1, 20, n),
    "Profit": np.random.randint(100, 5000, n),
    "Discount": np.random.uniform(0, 30, n).round(2),
    "Customer_Age": np.random.randint(18, 65, n),
    "Rating": np.random.randint(1, 6, n)
})

# Save dataset
output_path = Path(__file__).resolve().parent / "sales_data.csv"
df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print("Total records:", len(df))
print("\nFirst 5 records:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nSummary statistics:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())