import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

def load(name):
    with (DATA / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

customers = load("customers.csv")
products = load("products.csv")
orders = load("orders.csv")
items = load("order_items.csv")
transactions = load("transactions.csv")

customer_ids = {r["customer_id"] for r in customers}
product_ids = {r["product_id"] for r in products}
order_ids = {r["order_id"] for r in orders}

checks = {
    "Unique customer IDs": len(customer_ids) == len(customers),
    "Unique product IDs": len(product_ids) == len(products),
    "Unique order IDs": len(order_ids) == len(orders),
    "Orders reference existing customers": all(r["customer_id"] in customer_ids for r in orders),
    "Order items reference existing orders": all(r["order_id"] in order_ids for r in items),
    "Order items reference existing products": all(r["product_id"] in product_ids for r in items),
    "Transactions reference existing orders": all(r["order_id"] in order_ids for r in transactions),
    "Positive product prices": all(float(r["price"]) > 0 for r in products),
    "Positive item quantities": all(int(r["quantity"]) > 0 for r in items),
}

print("DATA VALIDATION")
for label, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'} - {label}")

print("\\nROW COUNTS")
for label, rows in [("Customers", customers), ("Products", products),
                    ("Orders", orders), ("Order items", items),
                    ("Transactions", transactions)]:
    print(f"{label}: {len(rows):,}")

if not all(checks.values()):
    raise SystemExit("Validation failed. Review the generated data.")
print("\\nAll validation checks passed.")
