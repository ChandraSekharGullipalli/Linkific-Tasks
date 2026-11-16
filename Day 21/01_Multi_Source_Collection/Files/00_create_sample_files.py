
"""
Day 21 - Create Sample Source Files
Creates CSV, JSON and Excel files for collection practice.
"""

import json
from pathlib import Path

import pandas as pd


# Input folder
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"

INPUT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------
# 1. CREATE CSV FILE
# -----------------------------------------

customers = [
    {"customer_id": 1, "name": "Rahul", "city": "Bengaluru", "age": 25},
    {"customer_id": 2, "name": "Priya", "city": "Hyderabad", "age": 27},
    {"customer_id": 3, "name": "Arjun", "city": "Chennai", "age": 29},
    {"customer_id": 4, "name": "Sneha", "city": "Mumbai", "age": 24},
    {"customer_id": 5, "name": "Kiran", "city": "Delhi", "age": 30}
]

customers_df = pd.DataFrame(customers)

customers_df.to_csv(
    INPUT_DIR / "customers.csv",
    index=False
)

print("Created customers.csv")


# -----------------------------------------
# 2. CREATE JSON FILE
# -----------------------------------------

products = [
    {"product_id": 101, "product_name": "Laptop", "price": 55000},
    {"product_id": 102, "product_name": "Mobile", "price": 25000},
    {"product_id": 103, "product_name": "Keyboard", "price": 1500},
    {"product_id": 104, "product_name": "Mouse", "price": 800},
    {"product_id": 105, "product_name": "Monitor", "price": 12000}
]

with open(
    INPUT_DIR / "products.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(products, file, indent=4)

print("Created products.json")


# -----------------------------------------
# 3. CREATE EXCEL FILE
# -----------------------------------------

employees = [
    {"employee_id": 201, "employee_name": "Amit", "department": "IT", "salary": 45000},
    {"employee_id": 202, "employee_name": "Neha", "department": "HR", "salary": 40000},
    {"employee_id": 203, "employee_name": "Vijay", "department": "Finance", "salary": 50000},
    {"employee_id": 204, "employee_name": "Pooja", "department": "IT", "salary": 48000},
    {"employee_id": 205, "employee_name": "Ravi", "department": "Sales", "salary": 42000}
]

employees_df = pd.DataFrame(employees)

employees_df.to_excel(
    INPUT_DIR / "employees.xlsx",
    index=False,
    engine="openpyxl"
)

print("Created employees.xlsx")


# -----------------------------------------
# 4. COMPLETION
# -----------------------------------------

print("\nAll sample source files created successfully!")

print(f"Input folder: {INPUT_DIR}")
