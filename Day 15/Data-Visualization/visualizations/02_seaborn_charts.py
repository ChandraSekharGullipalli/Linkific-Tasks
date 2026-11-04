import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

df = pd.read_csv(BASE_DIR / "datasets" / "sales_data.csv")

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# 11. Distribution Plot
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Sales", kde=True)
plt.title("Sales Distribution")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "11_seaborn_distribution.png")
plt.show()

# 12. Violin Plot
plt.figure(figsize=(8, 5))
sns.violinplot(data=df, x="Region", y="Sales")
plt.title("Sales Distribution by Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "12_violin_plot.png")
plt.show()

# 13. Count Plot
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Product")
plt.title("Product Transaction Count")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "13_count_plot.png")
plt.show()

# 14. Box Plot
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Category", y="Profit")
plt.title("Profit by Category")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "14_seaborn_boxplot.png")
plt.show()

# 15. Heatmap
plt.figure(figsize=(9, 6))
correlation = df[
    ["Sales", "Quantity", "Profit", "Discount",
     "Customer_Age", "Rating"]
].corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Sales Data Correlation Heatmap")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "15_heatmap.png")
plt.show()

# 16. Pair Plot
pair_plot = sns.pairplot(
    df[["Sales", "Profit", "Quantity", "Discount"]],
    diag_kind="hist"
)
pair_plot.fig.suptitle("Pair Plot Analysis", y=1.02)
pair_plot.savefig(OUTPUT_DIR / "16_pair_plot.png")
plt.show()

# 17. Bar Plot
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Product", y="Sales", errorbar=None)
plt.title("Average Sales by Product")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "17_seaborn_barplot.png")
plt.show()

# 18. Regression Plot
plt.figure(figsize=(8, 5))
sns.regplot(data=df, x="Discount", y="Sales")
plt.title("Discount vs Sales Regression")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "18_regression_plot.png")
plt.show()

print("All 8 Seaborn charts created successfully!")