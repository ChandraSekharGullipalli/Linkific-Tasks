
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load dataset
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "datasets" / "sales_data.csv"

df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])

# Dashboard title
st.title("📊 Sales Performance Dashboard")
st.write("Interactive Sales Data Analysis")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

products = st.sidebar.multiselect(
    "Select Product",
    options=sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Product"].isin(products))
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# KPI metrics
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Quantity", f"{total_quantity:,}")
col4.metric("Total Orders", f"{total_orders:,}")

st.divider()

# Sales trend
daily_sales = (
    filtered_df.groupby("Date", as_index=False)["Sales"].sum()
)

st.subheader("Sales Trend")

fig1 = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    markers=True,
    title="Daily Sales Performance"
)

st.plotly_chart(fig1, use_container_width=True)

# Product comparison
col1, col2 = st.columns(2)

with col1:
    product_sales = (
        filtered_df.groupby("Product", as_index=False)["Sales"].sum()
    )

    fig2 = px.bar(
        product_sales,
        x="Product",
        y="Sales",
        color="Product",
        title="Sales by Product"
    )

    st.plotly_chart(fig2, use_container_width=True)

with col2:
    region_sales = (
        filtered_df.groupby("Region", as_index=False)["Sales"].sum()
    )

    fig3 = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Regional Sales Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Profit analysis
st.subheader("Profit Analysis")

fig4 = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Region",
    size="Quantity",
    hover_data=["Product"],
    title="Sales vs Profit"
)

st.plotly_chart(fig4, use_container_width=True)

# Raw data
with st.expander("View Sales Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# Download filtered data
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Sales Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.success("Dashboard loaded successfully!")
