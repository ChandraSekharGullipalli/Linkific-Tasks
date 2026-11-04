
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# =====================================
# 1. Load Dataset
# =====================================

BASE_DIR = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    BASE_DIR / "datasets" / "sales_data.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

print("Dataset loaded successfully!")
print(df.head())

# =====================================
# 2. Histogram with KDE
# =====================================

plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="Sales",
    kde=True
)

plt.title("Sales Distribution with KDE")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "27_histogram_kde.png")
plt.show()

# =====================================
# 3. Box Plot
# =====================================

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Region",
    y="Sales"
)

plt.title("Sales Outlier Analysis by Region")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "28_statistical_boxplot.png")
plt.show()

# =====================================
# 4. Violin Plot
# =====================================

plt.figure(figsize=(8, 5))

sns.violinplot(
    data=df,
    x="Product",
    y="Profit"
)

plt.title("Profit Distribution by Product")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "29_statistical_violin.png")
plt.show()

# =====================================
# 5. Pair Plot
# =====================================

pair = sns.pairplot(
    df[["Sales", "Profit", "Quantity", "Discount"]],
    diag_kind="kde"
)

pair.fig.suptitle(
    "Statistical Pairwise Relationships",
    y=1.02
)

pair.savefig(OUTPUT_DIR / "30_statistical_pairplot.png")
plt.show()

# =====================================
# 6. Correlation Heatmap
# =====================================

plt.figure(figsize=(9, 6))

correlation = df[
    ["Sales", "Profit", "Quantity",
     "Discount", "Customer_Age", "Rating"]
].corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Statistical Correlation Heatmap")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "31_statistical_heatmap.png")
plt.show()

# =====================================
# 7. Regression Plot
# =====================================

plt.figure(figsize=(8, 5))

sns.regplot(
    data=df,
    x="Discount",
    y="Sales",
    scatter_kws={"alpha": 0.5}
)

plt.title("Discount and Sales Regression Analysis")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "32_regression_analysis.png")
plt.show()

# =====================================
# 8. Swarm Plot
# =====================================

plt.figure(figsize=(9, 5))

sns.swarmplot(
    data=df.head(100),
    x="Region",
    y="Sales"
)

plt.title("Individual Sales Distribution by Region")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "33_swarm_analysis.png")
plt.show()

# =====================================
# 9. Strip Plot
# =====================================

plt.figure(figsize=(9, 5))

sns.stripplot(
    data=df,
    x="Category",
    y="Profit",
    jitter=True,
    alpha=0.6
)

plt.title("Profit Distribution by Category")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "34_strip_plot.png")
plt.show()

# =====================================
# 10. ECDF Plot
# =====================================

plt.figure(figsize=(8, 5))

sns.ecdfplot(
    data=df,
    x="Sales",
    hue="Region"
)

plt.title("Cumulative Sales Distribution")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "35_ecdf_plot.png")
plt.show()

# =====================================
# 11. Joint Plot
# =====================================

joint = sns.jointplot(
    data=df,
    x="Sales",
    y="Profit",
    kind="reg"
)

joint.fig.suptitle(
    "Joint Statistical Analysis: Sales vs Profit",
    y=1.02
)

joint.savefig(OUTPUT_DIR / "36_joint_plot.png")
plt.show()

# =====================================
# Final Validation
# =====================================

print("\nStatistical visualizations completed!")

print("Total records:", len(df))

print("\nStatistical Summary:")
print(df[["Sales", "Profit", "Quantity", "Discount"]].describe())

print("\nCorrelation Matrix:")
print(correlation)

print("\nAll statistical charts saved successfully!")
