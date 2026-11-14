import csv
import random
from pathlib import Path
from faker import Faker

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
fake = Faker("en_IN")
Faker.seed(43)
random.seed(43)

departments = ["Data Engineering", "IT", "HR", "Finance", "Sales", "Operations"]
roles = ["Intern", "Analyst", "Engineer", "Associate", "Manager"]

rows = []
for employee_id in range(1, 1001):
    join_date = fake.date_between(start_date="-8y", end_date="today")
    rows.append({
        "employee_id": employee_id,
        "employee_name": fake.name(),
        "email": f"employee{employee_id}@example.com",
        "department": random.choice(departments),
        "job_role": random.choice(roles),
        "salary": random.randint(180000, 1800000),
        "city": fake.city(),
        "join_date": join_date.isoformat(),
        "employment_status": random.choices(["Active", "Inactive"], weights=[90, 10])[0]
    })

with (DATA / "employees.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Created employees.csv: {len(rows):,} rows")
