
"""
DAY 22 - COMPLETE DATA TRANSFORMATION PIPELINE

Database: synthetic_data_db

Transformation activities:
1. Data cleaning
2. Type conversions
3. Business logic
4. Joining multiple source tables
5. Sales aggregations
6. Saving transformed datasets
7. Logging and exception handling
"""

import os
import logging
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "data" / "transformed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(PROJECT_ROOT / ".env")


# ==================================================
# 2. LOGGING CONFIGURATION
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "transformation.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ==================================================
# 3. DATABASE CONNECTION
# ==================================================

def create_database_connection():

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "synthetic_data_db")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([host, port, database, username, password]):
        raise ValueError(
            "Database configuration is missing in the .env file."
        )

    # URL.create safely handles special characters
    # in the PostgreSQL username and password.

    connection_string = URL.create(
        drivername="postgresql+psycopg2",
        username=username,
        password=password,
        host=host,
        port=int(port),
        database=database
    )

    engine = create_engine(connection_string)

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    logger.info("Database connection successful.")

    return engine


# ==================================================
# 4. EXTRACT SOURCE TABLES
# ==================================================

def extract_source_data(engine):

    logger.info("Starting source data extraction.")

    customers = pd.read_sql(
        "SELECT * FROM public.customers",
        engine
    )

    products = pd.read_sql(
        "SELECT * FROM public.products",
        engine
    )

    orders = pd.read_sql(
        "SELECT * FROM public.orders",
        engine
    )

    order_items = pd.read_sql(
        "SELECT * FROM public.order_items",
        engine
    )

    transactions = pd.read_sql(
        "SELECT * FROM public.transactions",
        engine
    )

    logger.info("Source data extraction completed.")

    for name, dataframe in {
        "Customers": customers,
        "Products": products,
        "Orders": orders,
        "Order Items": order_items,
        "Transactions": transactions
    }.items():

        logger.info("%s: %s records", name, len(dataframe))

    return customers, products, orders, order_items, transactions


# ==================================================
# 5. CUSTOMER TRANSFORMATION
# ==================================================

def transform_customers(customers):

    logger.info("Transforming customer data.")

    customers = customers.copy()

    customers = customers.drop_duplicates(
        subset=["customer_id"],
        keep="last"
    )

    for column in ["customer_name", "email", "phone", "city"]:

        customers[column] = (
            customers[column]
            .astype("string")
            .str.strip()
        )

    customers["customer_name"] = (
        customers["customer_name"].replace("", pd.NA)
    )

    customers["email"] = customers["email"].str.lower()

    customers["city"] = customers["city"].str.title()

    customers["created_at"] = pd.to_datetime(
        customers["created_at"],
        errors="coerce"
    )

    customers["customer_name"] = (
        customers["customer_name"].fillna("Unknown")
    )

    customers["city"] = customers["city"].fillna("Unknown")

    logger.info("Customer transformation completed.")

    return customers


# ==================================================
# 6. PRODUCT TRANSFORMATION
# ==================================================

def transform_products(products):

    logger.info("Transforming product data.")

    products = products.copy()

    products = products.drop_duplicates(
        subset=["product_id"],
        keep="last"
    )

    products["product_name"] = (
        products["product_name"]
        .astype("string")
        .str.strip()
    )

    products["category"] = (
        products["category"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    products["price"] = pd.to_numeric(
        products["price"],
        errors="coerce"
    )

    products["stock_quantity"] = pd.to_numeric(
        products["stock_quantity"],
        errors="coerce"
    )

    products["product_name"] = (
        products["product_name"].fillna("Unknown Product")
    )

    products["category"] = (
        products["category"].fillna("Uncategorized")
    )

    logger.info("Product transformation completed.")

    return products


# ==================================================
# 7. ORDER TRANSFORMATION
# ==================================================

def transform_orders(orders):

    logger.info("Transforming order data.")

    orders = orders.copy()

    orders = orders.drop_duplicates(
        subset=["order_id"],
        keep="last"
    )

    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    orders["status"] = (
        orders["status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    orders["status"] = (
        orders["status"].replace("", pd.NA).fillna("unknown")
    )

    logger.info("Order transformation completed.")

    return orders


# ==================================================
# 8. ORDER ITEM TRANSFORMATION
# ==================================================

def transform_order_items(order_items):

    logger.info("Transforming order item data.")

    order_items = order_items.copy()

    order_items = order_items.drop_duplicates(
        subset=["order_item_id"],
        keep="last"
    )

    order_items["quantity"] = pd.to_numeric(
        order_items["quantity"],
        errors="coerce"
    )

    order_items["unit_price"] = pd.to_numeric(
        order_items["unit_price"],
        errors="coerce"
    )

    order_items["line_total"] = pd.to_numeric(
        order_items["line_total"],
        errors="coerce"
    )

    calculated_total = (
        order_items["quantity"] * order_items["unit_price"]
    )

    order_items["line_total"] = (
        order_items["line_total"].fillna(calculated_total)
    )

    logger.info("Order item transformation completed.")

    return order_items


# ==================================================
# 9. TRANSACTION TRANSFORMATION
# ==================================================

def transform_transactions(transactions):

    logger.info("Transforming transaction data.")

    transactions = transactions.copy()

    transactions = transactions.drop_duplicates(
        subset=["transaction_id"],
        keep="last"
    )

    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"],
        errors="coerce"
    )

    transactions["amount"] = pd.to_numeric(
        transactions["amount"],
        errors="coerce"
    )

    transactions["payment_method"] = (
        transactions["payment_method"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    transactions["payment_status"] = (
        transactions["payment_status"]
        .astype("string")
        .str.strip()
        .str.lower()
        .fillna("unknown")
    )

    logger.info("Transaction transformation completed.")

    return transactions


# ==================================================
# 10. SALES DATA JOIN
# ==================================================

def create_sales_dataset(
    customers,
    products,
    orders,
    order_items
):

    logger.info("Joining sales source tables.")

    sales = order_items.merge(
        orders,
        on="order_id",
        how="left",
        validate="many_to_one"
    )

    sales = sales.merge(
        customers,
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    sales = sales.merge(
        products,
        on="product_id",
        how="left",
        suffixes=("_item", "_product"),
        validate="many_to_one"
    )

    sales["unit_price"] = sales["unit_price"].fillna(
        sales["price"]
    )

    calculated_total = (
        sales["quantity"] * sales["unit_price"]
    )

    sales["line_total"] = (
        sales["line_total"].fillna(calculated_total)
    )

    sales["order_value_category"] = pd.cut(
        sales["line_total"],
        bins=[-float("inf"), 500, 2000, float("inf")],
        labels=["Low Value", "Medium Value", "High Value"]
    )

    logger.info("Sales dataset created: %s records", len(sales))

    return sales


# ==================================================
# 11. TRANSACTION DATA JOIN
# ==================================================

def create_transaction_dataset(
    transactions,
    orders,
    customers
):

    logger.info("Joining transaction source tables.")

    transaction_data = transactions.merge(
        orders,
        on="order_id",
        how="left",
        validate="many_to_one"
    )

    transaction_data = transaction_data.merge(
        customers,
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    logger.info(
        "Transaction dataset created: %s records",
        len(transaction_data)
    )

    return transaction_data


# ==================================================
# 12. SALES AGGREGATIONS
# ==================================================

def create_sales_aggregations(sales):

    logger.info("Creating sales aggregations.")

    sales = sales.copy()

    sales["order_month"] = (
        sales["order_date"]
        .dt.to_period("M")
        .astype("string")
    )

    monthly_summary = (
        sales.groupby("order_month", dropna=False)
        .agg(
            total_orders=("order_id", "nunique"),
            total_items=("order_item_id", "count"),
            total_quantity=("quantity", "sum"),
            total_revenue=("line_total", "sum")
        )
        .reset_index()
    )

    customer_summary = (
        sales.groupby(
            ["customer_id", "customer_name"],
            dropna=False
        )
        .agg(
            total_orders=("order_id", "nunique"),
            total_items=("order_item_id", "count"),
            total_quantity=("quantity", "sum"),
            total_revenue=("line_total", "sum")
        )
        .reset_index()
    )

    logger.info("Sales aggregations completed.")

    return monthly_summary, customer_summary


# ==================================================
# 13. SAVE TRANSFORMED DATA
# ==================================================

def save_transformed_data(
    customers,
    products,
    sales,
    transactions,
    monthly_summary,
    customer_summary
):

    logger.info("Saving transformed datasets.")

    datasets = {
        "customers_transformed.csv": customers,
        "products_transformed.csv": products,
        "sales_transformed.csv": sales,
        "transactions_transformed.csv": transactions,
        "monthly_sales_summary.csv": monthly_summary,
        "customer_sales_summary.csv": customer_summary
    }

    for filename, dataframe in datasets.items():

        output_path = OUTPUT_DIR / filename

        dataframe.to_csv(
            output_path,
            index=False
        )

        logger.info(
            "Saved %s with %s records",
            filename,
            len(dataframe)
        )


# ==================================================
# 14. MAIN PIPELINE
# ==================================================

def main():

    engine = None

    try:

        logger.info("=" * 55)
        logger.info("DAY 22 TRANSFORMATION PIPELINE STARTED")
        logger.info("=" * 55)

        engine = create_database_connection()

        # Extract source tables
        (
            customers,
            products,
            orders,
            order_items,
            transactions
        ) = extract_source_data(engine)

        # Transform source tables
        customers = transform_customers(customers)
        products = transform_products(products)
        orders = transform_orders(orders)
        order_items = transform_order_items(order_items)
        transactions = transform_transactions(transactions)

        # Join multiple sources
        sales = create_sales_dataset(
            customers,
            products,
            orders,
            order_items
        )

        transaction_data = create_transaction_dataset(
            transactions,
            orders,
            customers
        )

        # Create aggregations
        monthly_summary, customer_summary = (
            create_sales_aggregations(sales)
        )

        # Save transformed outputs
        save_transformed_data(
            customers,
            products,
            sales,
            transaction_data,
            monthly_summary,
            customer_summary
        )

        logger.info("=" * 55)
        logger.info("TRANSFORMATION PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 55)

    except Exception:

        logger.exception("Transformation pipeline failed.")
        raise

    finally:

        if engine is not None:
            engine.dispose()


if __name__ == "__main__":
    main()
