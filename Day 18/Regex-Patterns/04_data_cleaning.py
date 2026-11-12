
import re

# 1. Clean Phone Numbers
phone_numbers = [
    "+91 98765-43210",
    "98765 43210",
    "91-9123456789",
    "(98765) 12345"
]

print("\n1. Clean Phone Numbers:")
for phone in phone_numbers:
    cleaned = re.sub(r'\D', '', phone)
    if cleaned.startswith("91") and len(cleaned) == 12:
        cleaned = cleaned[2:]
    print(phone, "->", cleaned)

# 2. Extract Email Addresses
text = """
Customer Rahul: rahul@gmail.com
Customer Priya: priya@yahoo.com
Invalid email: priya@com
"""

print("\n2. Extract Email Addresses:")
emails = re.findall(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    text
)
print(emails)

# 3. Parse Dates
dates = [
    "12-11-2026",
    "25/12/2026",
    "01-01-2025"
]

print("\n3. Parse Dates:")
for date in dates:
    match = re.fullmatch(r'(\d{2})[-/](\d{2})[-/](\d{4})', date)
    if match:
        day, month, year = match.groups()
        print(date, "->", f"{year}-{month}-{day}")
    else:
        print("Invalid format:", date)

# 4. Standardize Text Formats
names = [
    "  RAHUL KUMAR  ",
    "priya sharma",
    "  Anjali DEVI "
]

print("\n4. Standardize Names:")
for name in names:
    cleaned = " ".join(name.split()).title()
    print(name, "->", cleaned)

# 5. Remove Special Characters
text = "Hello@Python#2026! Data$Engineering%"
print("\n5. Remove Special Characters:")
cleaned = re.sub(r'[^A-Za-z0-9 ]', '', text)
print(cleaned)

# 6. Remove Extra Spaces
text = "Python     is       useful"
print("\n6. Remove Extra Spaces:")
cleaned = re.sub(r'\s+', ' ', text).strip()
print(cleaned)

# 7. Extract Numbers from Text
text = "Rahul purchased 5 products worth 2500 rupees"
print("\n7. Extract Numbers:")
print(re.findall(r'\d+', text))

# 8. Remove HTML Tags
text = "<p>Python <b>Regex</b> Data Cleaning</p>"
print("\n8. Remove HTML Tags:")
print(re.sub(r'<[^>]+>', '', text))

# 9. Standardize Phone Number
phone = "+91-98765-43210"
print("\n9. Standardize Phone Number:")
digits = re.sub(r'\D', '', phone)
if digits.startswith("91") and len(digits) == 12:
    digits = digits[2:]
print(digits)

# 10. Clean Customer Text
text = "  RAHUL@@@KUMAR### "
print("\n10. Clean Customer Text:")
cleaned = re.sub(r'[^A-Za-z ]', '', text)
cleaned = re.sub(r'\s+', ' ', cleaned).strip().title()
print(cleaned)

