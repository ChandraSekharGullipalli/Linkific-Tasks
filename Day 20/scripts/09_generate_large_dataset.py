
import csv
import random
import os
from datetime import date
from faker import Faker

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Configuration
TOTAL_RECORDS = 100_000
OUTPUT_FILE = "data/large_sales_dataset_100k.csv"

os.makedirs("data", exist_ok=True)

print("Starting large dataset generation...")

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    # CSV columns
    writer.writerow([
        "transaction_id",
        "customer_id",
        "product_id",
        "transaction_date",
        "quantity",
        "unit_price",
        "total_amount",
        "payment_method",
        "payment_status",
        "city"
    ])

    for i in range(1, TOTAL_RECORDS + 1):

        customer_id = random.randint(1, 1000)
        product_id = random.randint(1, 200)

        transaction_date = fake.date_between(
            start_date=date(2024, 1, 1),
            end_date=date.today()
        )

        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(100, 50000), 2)
        total_amount = round(quantity * unit_price, 2)

        payment_method = random.choice([
            "Credit Card",
            "Debit Card",
            "UPI",
            "Net Banking",
            "Cash"
        ])

        payment_status = random.choice([
            "Completed",
            "Pending",
            "Failed"
        ])

        city = fake.city()

        writer.writerow([
            i,
            customer_id,
            product_id,
            transaction_date,
            quantity,
            f"{unit_price:.2f}",
            f"{total_amount:.2f}",
            payment_method,
            payment_status,
            city
        ])

        if i % 20000 == 0:
            print(f"Generated {i:,} records")

print("\nDATASET GENERATION COMPLETED")
print("-----------------------------")
print(f"Total records: {TOTAL_RECORDS:,}")
print(f"Output file: {OUTPUT_FILE}")
print(f"File size: {os.path.getsize(OUTPUT_FILE) / (1024 * 1024):.2f} MB")

