import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
BASE_DIR = Path(__file__).resolve().parents[1]
df = pd.read_csv(BASE_DIR / "datasets" / "sales_data.csv")

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Prepare summary data
product_sales = df.groupby("Product")["Sales"].sum()
region_sales = df.groupby("Region")["Sales"].sum()
daily_sales = df.groupby("Date")["Sales"].sum()

# 1. Line Plot
plt.figure(figsize=(10, 5))
plt.plot(daily_sales.index, daily_sales.values, marker="o")
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_line_plot.png")
plt.show()

# 2. Bar Chart
plt.figure(figsize=(8, 5))
plt.bar(product_sales.index, product_sales.values)
plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_bar_chart.png")
plt.show()

# 3. Horizontal Bar Chart
plt.figure(figsize=(8, 5))
plt.barh(region_sales.index, region_sales.values)
plt.title("Sales by Region")
plt.xlabel("Total Sales")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_horizontal_bar.png")
plt.show()

# 4. Scatter Plot
plt.figure(figsize=(8, 5))
plt.scatter(df["Quantity"], df["Sales"], alpha=0.6)
plt.title("Quantity vs Sales")
plt.xlabel("Quantity")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_scatter_plot.png")
plt.show()

# 5. Histogram
plt.figure(figsize=(8, 5))
plt.hist(df["Sales"], bins=20, edgecolor="black")
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_histogram.png")
plt.show()

# 6. Pie Chart
plt.figure(figsize=(7, 7))
plt.pie(
    region_sales.values,
    labels=region_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Regional Sales Share")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "06_pie_chart.png")
plt.show()

# 7. Box Plot
plt.figure(figsize=(8, 5))
plt.boxplot(df["Sales"])
plt.title("Sales Distribution - Box Plot")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "07_box_plot.png")
plt.show()

# 8. Area Chart
plt.figure(figsize=(10, 5))
plt.fill_between(
    daily_sales.index,
    daily_sales.values,
    alpha=0.4
)
plt.plot(daily_sales.index, daily_sales.values)
plt.title("Daily Sales Area Chart")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "08_area_chart.png")
plt.show()

# 9. Stem Plot
plt.figure(figsize=(9, 5))
plt.stem(range(1, 16), df["Sales"].head(15))
plt.title("Sales Stem Plot")
plt.xlabel("Record Number")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "09_stem_plot.png")
plt.show()

# 10. Subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].bar(product_sales.index, product_sales.values)
axes[0, 0].set_title("Product Sales")

axes[0, 1].hist(df["Profit"], bins=15)
axes[0, 1].set_title("Profit Distribution")

axes[1, 0].scatter(df["Discount"], df["Sales"])
axes[1, 0].set_title("Discount vs Sales")

axes[1, 1].boxplot(df["Customer_Age"])
axes[1, 1].set_title("Customer Age")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "10_subplots.png")
plt.show()

print("All 10 Matplotlib charts created successfully!")