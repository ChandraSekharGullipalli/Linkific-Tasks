
import re

# 1. Email Extraction
text = "Contact us at john@gmail.com and admin@yahoo.com"
print("\n1. Email Extraction:")
print(re.findall(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}', text))

# 2. Phone Number Extraction
text = "Call 9876543210 or 9123456789"
print("\n2. Phone Number Extraction:")
print(re.findall(r'\b[6-9]\d{9}\b', text))

# 3. Indian Mobile Validation
phone = "9876543210"
print("\n3. Indian Mobile Validation:")
print(bool(re.fullmatch(r'[6-9]\d{9}', phone)))

# 4. URL Matching
text = "Visit https://www.google.com and http://example.com"
print("\n4. URL Matching:")
print(re.findall(r'https?://[^\s]+', text))

# 5. Date Extraction
text = "Dates: 12-11-2026, 25/12/2026"
print("\n5. Date Extraction:")
print(re.findall(r'\b\d{2}[-/]\d{2}[-/]\d{4}\b', text))

# 6. Date Format Validation
date = "12-11-2026"
print("\n6. Date Format Validation:")
print(bool(re.fullmatch(r'\d{2}-\d{2}-\d{4}', date)))

# 7. IPv4 Validation (Format)
ip = "192.168.1.10"
print("\n7. IPv4 Format Validation:")
print(bool(re.fullmatch(r'(?:\d{1,3}\.){3}\d{1,3}', ip)))

# 8. Numeric Extraction
text = "Product prices are 100, 250 and 500"
print("\n8. Numeric Extraction:")
print(re.findall(r'\d+', text))

# 9. Decimal Number Matching
text = "Prices: 99.50, 120.75, 300"
print("\n9. Decimal Number Matching:")
print(re.findall(r'\b\d+\.\d{2}\b', text))

# 10. Alphabet-only Validation
name = "Chandra"
print("\n10. Alphabet-only Validation:")
print(bool(re.fullmatch(r'[A-Za-z]+', name)))

# 11. Alphanumeric Matching
text = "ABC123 XYZ456 hello!"
print("\n11. Alphanumeric Matching:")
print(re.findall(r'\b[A-Za-z0-9]+\b', text))

# 12. Whitespace Removal
text = "Python   is   easy"
print("\n12. Whitespace Removal:")
print(re.sub(r'\s+', '', text))

# 13. Special Character Removal
text = "Hello@Python#2026!"
print("\n13. Special Character Removal:")
print(re.sub(r'[^A-Za-z0-9 ]', '', text))

# 14. Multiple Spaces Replacement
text = "Data    Engineering    Python"
print("\n14. Multiple Spaces Replacement:")
print(re.sub(r'\s+', ' ', text))

# 15. Indian PIN Code Validation
pin = "500001"
print("\n15. PIN Code Validation:")
print(bool(re.fullmatch(r'[1-9]\d{5}', pin)))

# 16. Username Validation
username = "chandra_123"
print("\n16. Username Validation:")
print(bool(re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{3,14}', username)))

# 17. Password Strength Format
password = "Python@123"
print("\n17. Password Format Validation:")
pattern = r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}'
print(bool(re.fullmatch(pattern, password)))

# 18. Hashtag Extraction
text = "Learning #Python #DataEngineering #Regex"
print("\n18. Hashtag Extraction:")
print(re.findall(r'#[A-Za-z0-9_]+', text))

# 19. Log Timestamp Extraction
text = "2026-11-12 10:30:45 INFO Application started"
print("\n19. Log Timestamp Extraction:")
print(re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', text))

# 20. Error Message Extraction
text = "INFO Started ERROR Database failed WARNING Low memory ERROR Timeout"
print("\n20. Error Message Extraction:")
print(re.findall(r'ERROR.*', text))

# 21. Duplicate Word Detection
text = "Python is is a powerful language"
print("\n21. Duplicate Word Detection:")
print(re.findall(r'\b(\w+)\s+\1\b', text, re.IGNORECASE))

# 22. HTML Tag Removal
text = "<h1>Hello</h1><p>Welcome to Python</p>"
print("\n22. HTML Tag Removal:")
print(re.sub(r'<[^>]+>', '', text))

# 23. Currency Value Extraction
text = "Products cost Rs. 500, Rs. 1200 and Rs. 250"
print("\n23. Currency Value Extraction:")
print(re.findall(r'Rs\.?\s*\d+', text))

# 24. File Extension Extraction
text = "report.pdf image.png data.csv script.py"
print("\n24. File Extension Extraction:")
print(re.findall(r'\.([A-Za-z0-9]+)\b', text))
