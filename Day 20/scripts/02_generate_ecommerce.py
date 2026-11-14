import argparse
import csv
import random
from pathlib import Path
from faker import Faker

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

fake = Faker("en_IN")
Faker.seed(42)
random.seed(42)

def write_csv(filename, rows, headers):
    with (DATA / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created {filename}: {len(rows):,} rows")

def main(customer_count=1000, product_count=200, order_count=1000):
    customers = [{
        "customer_id": i,
        "customer_name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
        "created_at": fake.date_between(start_date="-3y", end_date="today").isoformat()
    } for i in range(1, customer_count + 1)]

    categories = ["Electronics", "Clothing", "Home", "Books", "Sports", "Beauty"]
    products = [{
        "product_id": i,
        "product_name": fake.catch_phrase(),
        "category": random.choice(categories),
        "price": round(random.uniform(99, 50000), 2),
        "stock_quantity": random.randint(0, 500)
    } for i in range(1, product_count + 1)]

    orders, items, transactions = [], [], []
    for order_id in range(1, order_count + 1):
        customer = random.choice(customers)
        order_date = fake.date_between(start_date="-2y", end_date="today")
        status = random.choices(
            ["Delivered", "Shipped", "Processing", "Cancelled"],
            weights=[65, 15, 15, 5]
        )[0]
        orders.append({
            "order_id": order_id,
            "customer_id": customer["customer_id"],
            "order_date": order_date.isoformat(),
            "status": status
        })

        order_total = 0
        for _ in range(random.randint(1, 4)):
            product = random.choice(products)
            qty = random.randint(1, 5)
            line_total = round(product["price"] * qty, 2)
            order_total += line_total
            items.append({
                "order_item_id": len(items) + 1,
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": qty,
                "unit_price": product["price"],
                "line_total": line_total
            })

        transactions.append({
            "transaction_id": order_id,
            "order_id": order_id,
            "transaction_date": order_date.isoformat(),
            "amount": round(order_total, 2),
            "payment_method": random.choice(["UPI", "Card", "Net Banking", "Cash"]),
            "payment_status": "Success" if status != "Cancelled" else "Refunded"
        })

    write_csv("customers.csv", customers, customers[0].keys())
    write_csv("products.csv", products, products[0].keys())
    write_csv("orders.csv", orders, orders[0].keys())
    write_csv("order_items.csv", items, items[0].keys())
    write_csv("transactions.csv", transactions, transactions[0].keys())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate related e-commerce CSV datasets.")
    parser.add_argument("--customers", type=int, default=1000)
    parser.add_argument("--products", type=int, default=200)
    parser.add_argument("--orders", type=int, default=1000)
    args = parser.parse_args()
    main(args.customers, args.products, args.orders)
