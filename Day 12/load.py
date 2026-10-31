import logging
from sqlalchemy import text
from config import get_database_engine

def load_data(data, table_name="sales_data"):
    logging.info("Starting database loading")

    engine = get_database_engine()

    try:
        # Create the table if it does not exist
        create_table_query = text("""
            CREATE TABLE IF NOT EXISTS sales_data (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product VARCHAR(100),
                quantity INTEGER,
                price NUMERIC(12,2),
                order_date DATE,
                total_amount NUMERIC(12,2),
                customer_name VARCHAR(100),
                city VARCHAR(100)
            )
        """)

        with engine.begin() as connection:
            connection.execute(create_table_query)

            # Insert or update records
            for _, row in data.iterrows():
                insert_query = text("""
                    INSERT INTO sales_data (
                        order_id, customer_id, product, quantity,
                        price, order_date, total_amount,
                        customer_name, city
                    )
                    VALUES (
                        :order_id, :customer_id, :product, :quantity,
                        :price, :order_date, :total_amount,
                        :customer_name, :city
                    )
                    ON CONFLICT (order_id)
                    DO UPDATE SET
                        customer_id = EXCLUDED.customer_id,
                        product = EXCLUDED.product,
                        quantity = EXCLUDED.quantity,
                        price = EXCLUDED.price,
                        order_date = EXCLUDED.order_date,
                        total_amount = EXCLUDED.total_amount,
                        customer_name = EXCLUDED.customer_name,
                        city = EXCLUDED.city
                """)

                connection.execute(insert_query, row.to_dict())

        print("Data loaded successfully into PostgreSQL!")
        print("Records loaded:", len(data))

        logging.info("Database loading completed successfully")

    except Exception:
        logging.exception("Database loading failed")
        raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    from extract import extract_sales, extract_customers
    from transform import transform_data

    sales = extract_sales()
    customers = extract_customers()

    transformed_data = transform_data(sales, customers)

    load_data(transformed_data)