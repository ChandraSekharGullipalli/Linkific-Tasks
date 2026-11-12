
import re
import pandas as pd
from pathlib import Path

# 1. Remove special characters
def remove_special_characters(text):
    return re.sub(r"[^A-Za-z0-9 ]", "", str(text))

# 2. Remove extra spaces
def remove_extra_spaces(text):
    return re.sub(r"\s+", " ", str(text)).strip()

# 3. Clean phone numbers
def clean_phone_number(phone):
    digits = re.sub(r"\D", "", str(phone))

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    if re.fullmatch(r"[6-9]\d{9}", digits):
        return digits

    return "Invalid Phone"

# 4. Extract email addresses
def extract_emails(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    return re.findall(pattern, str(text))

# 5. Standardize customer names
def standardize_name(name):
    name = remove_special_characters(name)
    name = remove_extra_spaces(name)
    return name.title()

# 6. Extract numeric values
def extract_numbers(text):
    return re.findall(r"\d+", str(text))

# 7. Remove HTML tags
def remove_html_tags(text):
    return re.sub(r"<[^>]*>", "", str(text))

# 8. Standardize dates
def standardize_date(date):
    match = re.fullmatch(
        r"(\d{2})[-/](\d{2})[-/](\d{4})",
        str(date).strip()
    )

    if match:
        day, month, year = match.groups()
        return f"{year}-{month}-{day}"

    return "Invalid Date Format"

# 9. Clean text to lowercase
def clean_text(text):
    text = re.sub(r"[^A-Za-z0-9 ]", " ", str(text))
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

# 10. Remove duplicate words
def remove_duplicate_words(text):
    return re.sub(
        r"\b(\w+)(\s+\1\b)+",
        r"\1",
        str(text),
        flags=re.IGNORECASE
    )

# Demonstrate all scripts
print("\n1. Special Character Removal:")
print(remove_special_characters("Hello@Python#2026!"))

print("\n2. Extra Space Removal:")
print(remove_extra_spaces("Python     is    useful"))

print("\n3. Phone Number Cleaning:")
print(clean_phone_number("+91 98765-43210"))

print("\n4. Email Extraction:")
print(extract_emails("Contact: rahul@gmail.com, priya@yahoo.com"))

print("\n5. Name Standardization:")
print(standardize_name("  RAHUL@@ KUMAR  "))

print("\n6. Number Extraction:")
print(extract_numbers("Order 101 costs 2500 rupees"))

print("\n7. HTML Tag Removal:")
print(remove_html_tags("<h1>Hello Python</h1>"))

print("\n8. Date Standardization:")
print(standardize_date("12-11-2026"))

print("\n9. Text Lowercase Cleaning:")
print(clean_text("HELLO@PYTHON 2026!"))

print("\n10. Duplicate Word Removal:")
print(remove_duplicate_words("Python is is very very useful"))

# 11. Customer CSV cleaning
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "customers.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "script_cleaned_customers.csv"

df = pd.read_csv(INPUT_FILE)

df["Name"] = df["Name"].apply(standardize_name)
df["Phone"] = df["Phone"].apply(clean_phone_number)
df["Email"] = df["Email"].astype(str).str.strip().str.lower()
df["City"] = df["City"].apply(clean_text)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("\n11. Customer CSV Cleaning:")
print("Total customer records:", len(df))
print("Cleaned customer data saved to:", OUTPUT_FILE)
