"""
Optional PostgreSQL loader.
1. Create the tables using database/schema.sql.
2. Set DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT environment variables.
3. Run: python scripts/06_bulk_insert_postgres.py
"""
import csv
import os
from pathlib import Path
import psycopg2

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

TABLES = [
    ("customers", "customers.csv"),
    ("products", "products.csv"),
    ("orders", "orders.csv"),
    ("order_items", "order_items.csv"),
    ("transactions", "transactions.csv"),
]

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    dbname=os.getenv("DB_NAME", "synthetic_data_db"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT", "5432"),
)
try:
    with conn, conn.cursor() as cur:
        for table, filename in TABLES:
            path = DATA / filename
            with path.open("r", encoding="utf-8") as f:
                cur.copy_expert(
                    f"COPY {table} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)",
                    f
                )
            print(f"Loaded {filename} into {table}")
finally:
    conn.close()
print("Bulk loading completed.")
