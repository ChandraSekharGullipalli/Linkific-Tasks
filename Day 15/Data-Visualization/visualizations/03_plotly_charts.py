import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

df = pd.read_csv(BASE_DIR / "datasets" / "sales_data.csv")

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 19. Interactive Line Chart
daily = df.groupby("Date", as_index=False)["Sales"].sum()

fig1 = px.line(
    daily,
    x="Date",
    y="Sales",
    title="Interactive Daily Sales Trend",
    markers=True
)
fig1.write_html(OUTPUT_DIR / "19_interactive_line.html")
fig1.show()

# 20. Interactive Scatter Plot
fig2 = px.scatter(
    df,
    x="Quantity",
    y="Sales",
    color="Region",
    size="Profit",
    hover_data=["Product"],
    title="Interactive Quantity vs Sales"
)
fig2.write_html(OUTPUT_DIR / "20_interactive_scatter.html")
fig2.show()

# 21. Interactive 3D Scatter Plot
fig3 = px.scatter_3d(
    df,
    x="Sales",
    y="Profit",
    z="Quantity",
    color="Region",
    title="3D Sales Analysis"
)
fig3.write_html(OUTPUT_DIR / "21_3d_scatter.html")
fig3.show()

# 22. Animated Bar Chart
animation_data = df.copy()
animation_data["Month"] = pd.to_datetime(
    animation_data["Date"]
).dt.strftime("%Y-%m")

monthly_product = (
    animation_data.groupby(
        ["Month", "Product"],
        as_index=False
    )["Sales"].sum()
)

fig4 = px.bar(
    monthly_product,
    x="Product",
    y="Sales",
    color="Product",
    animation_frame="Month",
    title="Animated Monthly Product Sales"
)
fig4.write_html(OUTPUT_DIR / "22_animated_bar.html")
fig4.show()

# 23. Interactive Bar Chart
product_summary = (
    df.groupby("Product", as_index=False)["Profit"].sum()
)

fig5 = px.bar(
    product_summary,
    x="Product",
    y="Profit",
    color="Product",
    title="Interactive Product Profit Comparison"
)
fig5.write_html(OUTPUT_DIR / "23_interactive_bar.html")
fig5.show()

print("All 5 Plotly charts created successfully!")
print("Interactive HTML charts saved in outputs folder.")
