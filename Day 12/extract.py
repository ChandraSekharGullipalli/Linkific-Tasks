import pandas as pd
import logging

def extract_sales(file_path="Data/raw_sales.csv"):

    logging.info("Starting sales data extraction")

    try:
        sales_df = pd.read_csv(file_path)

        print("Sales data extracted successfully!")
        print("Total sales records:", len(sales_df))

        logging.info(
            f"Sales extraction completed: {len(sales_df)} records"
        )

        return sales_df

    except Exception as error:
        logging.exception("Sales extraction failed")
        raise error


def extract_customers(file_path="Data/customers.csv"):

    logging.info("Starting customer data extraction")

    try:
        customers_df = pd.read_csv(file_path)

        print("Customer data extracted successfully!")
        print("Total customer records:", len(customers_df))

        logging.info(
            f"Customer extraction completed: {len(customers_df)} records"
        )

        return customers_df

    except Exception as error:
        logging.exception("Customer extraction failed")
        raise error


if __name__ == "__main__":

    sales = extract_sales()
    customers = extract_customers()

    print("\nSales Dataset:")
    print(sales)

    print("\nCustomer Dataset:")
    print(customers)