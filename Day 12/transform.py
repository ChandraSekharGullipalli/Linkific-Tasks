import pandas as pd
import logging


def transform_data(sales, customers):

    logging.info("Starting data transformation")

    print("\n========== TRANSFORMATION STARTED ==========")

    # 1. Check original records
    print("Original sales records:", len(sales))

    # 2. Remove duplicate orders
    sales = sales.drop_duplicates(
        subset=["order_id"],
        keep="first"
    ).copy()

    print("After removing duplicates:", len(sales))

    # 3. Handle missing values in important columns
    sales = sales.dropna(
        subset=["order_id", "customer_id", "product", "order_date"]
    ).copy()

    # 4. Convert numeric columns
    sales["quantity"] = pd.to_numeric(
        sales["quantity"], errors="coerce"
    )

    sales["price"] = pd.to_numeric(
        sales["price"], errors="coerce"
    )

    sales["order_id"] = pd.to_numeric(
        sales["order_id"], errors="coerce"
    )

    sales["customer_id"] = pd.to_numeric(
        sales["customer_id"], errors="coerce"
    )

    # 5. Remove invalid numeric records
    sales = sales.dropna(
        subset=["order_id", "customer_id", "quantity", "price"]
    ).copy()

    sales = sales[
        (sales["quantity"] > 0) &
        (sales["price"] >= 0)
    ].copy()

    # 6. Convert columns to correct data types
    sales["order_id"] = sales["order_id"].astype(int)
    sales["customer_id"] = sales["customer_id"].astype(int)
    sales["quantity"] = sales["quantity"].astype(int)

    # 7. Convert order date
    sales["order_date"] = pd.to_datetime(
        sales["order_date"],
        errors="coerce"
    )

    sales = sales.dropna(subset=["order_date"]).copy()

    # 8. Calculate total amount
    sales["total_amount"] = (
        sales["quantity"] * sales["price"]
    )

    # 9. Clean customer data
    customers = customers.drop_duplicates(
        subset=["customer_id"],
        keep="first"
    ).copy()

    customers = customers.dropna(
        subset=["customer_id"]
    ).copy()

    customers["customer_id"] = pd.to_numeric(
        customers["customer_id"],
        errors="coerce"
    )

    customers = customers.dropna(
        subset=["customer_id"]
    ).copy()

    customers["customer_id"] = (
        customers["customer_id"].astype(int)
    )

    customers["customer_name"] = (
        customers["customer_name"].fillna("Unknown")
    )

    customers["city"] = (
        customers["city"].fillna("Unknown")
    )

    # 10. Merge sales and customer datasets
    final_data = pd.merge(
        sales,
        customers,
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    # 11. Handle customers not found in customer dataset
    final_data["customer_name"] = (
        final_data["customer_name"].fillna("Unknown")
    )

    final_data["city"] = (
        final_data["city"].fillna("Unknown")
    )

    # 12. Display transformation results
    print("Final transformed records:", len(final_data))
    print(
        "Total revenue:",
        final_data["total_amount"].sum()
    )

    print("\n========== TRANSFORMED DATA ==========")
    print(final_data.to_string(index=False))

    logging.info(
        f"Transformation completed: {len(final_data)} records"
    )

    return final_data


if __name__ == "__main__":

    from extract import extract_sales, extract_customers

    sales_data = extract_sales()
    customer_data = extract_customers()

    transformed_data = transform_data(
        sales_data,
        customer_data
    )

    print("\nTransformation completed successfully!")