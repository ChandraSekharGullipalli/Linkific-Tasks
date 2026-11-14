
import csv
import os
import random
from decimal import Decimal
from datetime import date

import psycopg2
from faker import Faker

# -----------------------------------------
# 1. Configuration
# -----------------------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "synthetic_financial_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432"),
}

ACCOUNTS_FILE = "data/accounts.csv"
TRANSACTIONS_FILE = "data/financial_transactions.csv"

random.seed(42)
fake = Faker()
Faker.seed(42)


def read_csv(filename):
    with open(filename, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main():

    if not DB_CONFIG["password"]:
        raise ValueError("DB_PASSWORD is not set.")

    accounts = read_csv(ACCOUNTS_FILE)
    transactions = read_csv(TRANSACTIONS_FILE)

    if not accounts or not transactions:
        raise ValueError("Financial CSV files must not be empty.")

    connection = psycopg2.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:

            # -----------------------------------------
            # 2. Clear existing financial data
            # -----------------------------------------

            cursor.execute("""
                TRUNCATE TABLE
                    loans,
                    financial_transactions,
                    accounts,
                    customers,
                    branches
                RESTART IDENTITY CASCADE;
            """)

            # -----------------------------------------
            # 3. Insert unique customers
            # -----------------------------------------

            customer_names = sorted({
                row["customer_name"] for row in accounts
            })

            cursor.executemany("""
                INSERT INTO customers (customer_name)
                VALUES (%s)
            """, [(name,) for name in customer_names])

            cursor.execute("""
                SELECT customer_id, customer_name
                FROM customers
            """)

            customer_map = {
                name: customer_id
                for customer_id, name in cursor.fetchall()
            }

            # -----------------------------------------
            # 4. Generate 10 branches
            # -----------------------------------------

            branch_rows = [
                (f"Branch {i:02d}", fake.city())
                for i in range(1, 11)
            ]

            cursor.executemany("""
                INSERT INTO branches (branch_name, city)
                VALUES (%s, %s)
            """, branch_rows)

            cursor.execute("""
                SELECT branch_id FROM branches
                ORDER BY branch_id
            """)

            branch_ids = [row[0] for row in cursor.fetchall()]

            # -----------------------------------------
            # 5. Insert accounts
            # -----------------------------------------

            account_rows = []

            for row in accounts:
                account_rows.append((
                    int(row["account_id"]),
                    customer_map[row["customer_name"]],
                    random.choice(branch_ids),
                    row["account_type"],
                    Decimal(row["opening_balance"])
                ))

            cursor.executemany("""
                INSERT INTO accounts (
                    account_id, customer_id, branch_id,
                    account_type, opening_balance
                )
                VALUES (%s, %s, %s, %s, %s)
            """, account_rows)

            # -----------------------------------------
            # 6. Insert financial transactions
            # -----------------------------------------

            transaction_rows = []

            for row in transactions:
                transaction_rows.append((
                    int(row["transaction_id"]),
                    int(row["account_id"]),
                    row["transaction_date"],
                    row["transaction_type"],
                    Decimal(row["amount"]),
                    row["description"],
                    row["reference_code"]
                ))

            cursor.executemany("""
                INSERT INTO financial_transactions (
                    transaction_id, account_id,
                    transaction_date, transaction_type,
                    amount, description, reference_code
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, transaction_rows)

            # -----------------------------------------
            # 7. Generate 200 synthetic loan records
            # -----------------------------------------

            account_ids = [
                int(row["account_id"]) for row in accounts
            ]

            loan_rows = []

            for _ in range(200):
                loan_rows.append((
                    random.choice(account_ids),
                    Decimal(str(round(
                        random.uniform(50000, 2000000), 2
                    ))),
                    Decimal(str(round(
                        random.uniform(5.5, 14.5), 2
                    ))),
                    random.choice([
                        "Approved", "Pending", "Active", "Closed"
                    ]),
                    fake.date_between(
                        start_date="-3y",
                        end_date="today"
                    )
                ))

            cursor.executemany("""
                INSERT INTO loans (
                    account_id, loan_amount,
                    interest_rate, loan_status, issue_date
                )
                VALUES (%s, %s, %s, %s, %s)
            """, loan_rows)

        connection.commit()

        print("\nFINANCIAL DATABASE LOADED SUCCESSFULLY")
        print("---------------------------------------")
        print(f"Customers: {len(customer_names)}")
        print(f"Branches: {len(branch_rows)}")
        print(f"Accounts: {len(account_rows)}")
        print(f"Financial transactions: {len(transaction_rows)}")
        print(f"Loans: {len(loan_rows)}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
