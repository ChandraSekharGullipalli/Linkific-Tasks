
import pandas as pd
import psycopg2

# 1. EXTRACT
df = pd.read_csv(r"Day 10\retail_sales.csv")

print("Original rows:", len(df))

# 2. TRANSFORM
df.columns = df.columns.str.strip()
df["product"] = df["product"].astype("string").str.strip()
df["city"] = df["city"].astype("string").str.strip()

df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce"
)
df["quantity"] = pd.to_numeric(
    df["quantity"], errors="coerce"
)
df["unit_price"] = pd.to_numeric(
    df["unit_price"], errors="coerce"
)

# Remove duplicate orders
df = df.drop_duplicates(subset=["order_id"], keep="first")

# Remove invalid or incomplete records
df = df.dropna(
    subset=[
        "order_id", "order_date", "product",
        "category", "quantity", "unit_price", "city"
    ]
)
df = df[
    (df["quantity"] > 0) &
    (df["unit_price"] >= 0) &
    (df["product"] != "") &
    (df["city"] != "")
].copy()

# Calculate sales amount
df["total_amount"] = df["quantity"] * df["unit_price"]

print("Clean rows:", len(df))
print("\nSales by city:")
print(
    df.groupby("city")["total_amount"]
      .sum()
      .sort_values(ascending=False)
)

# 3. LOAD
connection = None

try:
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="Chandu@123"
    )

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS day10_retail_sales (
                    order_id INT PRIMARY KEY,
                    order_date DATE,
                    product VARCHAR(100),
                    category VARCHAR(50),
                    quantity INT,
                    unit_price NUMERIC(12, 2),
                    city VARCHAR(50),
                    total_amount NUMERIC(14, 2)
                );
            """)

            insert_query = """
                INSERT INTO day10_retail_sales
                (order_id, order_date, product, category,
                 quantity, unit_price, city, total_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO UPDATE SET
                    order_date = EXCLUDED.order_date,
                    product = EXCLUDED.product,
                    category = EXCLUDED.category,
                    quantity = EXCLUDED.quantity,
                    unit_price = EXCLUDED.unit_price,
                    city = EXCLUDED.city,
                    total_amount = EXCLUDED.total_amount;
            """

            records = [
                (
                    int(row.order_id),
                    row.order_date.date(),
                    str(row.product),
                    str(row.category),
                    int(row.quantity),
                    float(row.unit_price),
                    str(row.city),
                    float(row.total_amount)
                )
                for row in df.itertuples(index=False)
            ]

            cursor.executemany(insert_query, records)

    print("\nRetail sales ETL completed successfully!")
    print("Records loaded:", len(records))

except Exception as error:
    print("ETL failed:", error)

finally:
    if connection is not None:
        connection.close()
