from faker import Faker
import random

fake = Faker("en_IN")
Faker.seed(42)
random.seed(42)

print("CUSTOMER")
print("Name:", fake.name())
print("Address:", fake.address().replace("\\n", ", "))
print("Email:", fake.email())
print("Phone:", fake.phone_number())

print("\\nCOMPANY")
print("Company:", fake.company())
print("Job:", fake.job())
print("Website:", fake.url())

print("\\nDATE AND NUMBERS")
print("Date:", fake.date_between(start_date="-2y", end_date="today"))
print("Amount:", round(random.uniform(100, 50000), 2))

print("\\nLOCALIZATION")
print("Indian city:", fake.city())
print("Postcode:", fake.postcode())
