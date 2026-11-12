
import re
import pandas as pd
from datetime import datetime
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "customers.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "cleaned_customers.csv"

# Read customer CSV
df = pd.read_csv(INPUT_FILE)

print("\n1. Original Customer Data:")
print(df.to_string(index=False))

# Clean customer names
def clean_name(name):
    name = str(name)
    name = re.sub(r"[^A-Za-z ]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name.title()

# Validate and extract email format
def validate_email(email):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    return bool(re.fullmatch(pattern, str(email).strip()))

# Clean phone numbers
def clean_phone(phone):
    digits = re.sub(r"\D", "", str(phone))

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]

    if re.fullmatch(r"[6-9]\d{9}", digits):
        return digits

    return None

# Standardize dates
def standardize_date(date):
    date = str(date).strip()

    for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
        try:
            parsed = datetime.strptime(date, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None

# Apply cleaning operations
df["Name"] = df["Name"].apply(clean_name)

df["Email"] = df["Email"].astype(str).str.strip()
df["EmailValid"] = df["Email"].apply(validate_email)

df["Phone"] = df["Phone"].apply(clean_phone)
df["PhoneValid"] = df["Phone"].notna()

df["Date"] = df["Date"].apply(standardize_date)
df["DateValid"] = df["Date"].notna()

df["City"] = (
    df["City"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Display cleaned data
print("\n2. Cleaned Customer Data:")
print(df.to_string(index=False))

# Save cleaned dataset
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

# Data quality summary
print("\n3. Data Quality Summary:")
print("Total Customers:", len(df))
print("Valid Emails:", df["EmailValid"].sum())
print("Invalid Emails:", (~df["EmailValid"]).sum())
print("Valid Phones:", df["PhoneValid"].sum())
print("Invalid Phones:", (~df["PhoneValid"]).sum())
print("Valid Dates:", df["DateValid"].sum())
print("Invalid Dates:", (~df["DateValid"]).sum())

print("\n4. Output File:")
print(OUTPUT_FILE)

