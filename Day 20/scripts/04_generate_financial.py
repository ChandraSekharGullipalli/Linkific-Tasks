import csv
import random
from pathlib import Path
from faker import Faker

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
fake = Faker("en_IN")
Faker.seed(44)
random.seed(44)

accounts = [{
    "account_id": i,
    "customer_name": fake.name(),
    "account_type": random.choice(["Savings", "Current"]),
    "opening_balance": round(random.uniform(1000, 500000), 2)
} for i in range(1, 1001)]

transactions = []
for transaction_id in range(1, 10001):
    account = random.choice(accounts)
    transactions.append({
        "transaction_id": transaction_id,
        "account_id": account["account_id"],
        "transaction_date": fake.date_between(start_date="-2y", end_date="today").isoformat(),
        "transaction_type": random.choice(["Credit", "Debit"]),
        "amount": round(random.uniform(10, 100000), 2),
        "description": fake.sentence(nb_words=4),
        "reference_code": fake.bothify(text="TXN-########")
    })

for filename, rows in [("accounts.csv", accounts), ("financial_transactions.csv", transactions)]:
    with (DATA / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created {filename}: {len(rows):,} rows")
