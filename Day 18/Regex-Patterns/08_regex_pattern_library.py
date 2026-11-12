
import re


# Reusable Regex Pattern Dictionary
PATTERNS = {

    # Contact Information
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

    "indian_mobile": r"^[6-9]\d{9}$",

    "international_phone": r"^\+?[1-9]\d{7,14}$",

    "website_url": r"https?://[^\s]+",

    # Personal Information
    "username": r"^[A-Za-z][A-Za-z0-9_]{3,14}$",

    "alphabet_only": r"^[A-Za-z]+$",

    "alphanumeric": r"^[A-Za-z0-9]+$",

    "strong_password": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$",

    # Numeric Patterns
    "integer": r"^-?\d+$",

    "decimal": r"^-?\d+\.\d+$",

    "positive_number": r"^\d+$",

    "currency": r"Rs\.?\s?\d+(?:\.\d{2})?",

    "percentage": r"\b\d+(?:\.\d+)?%",

    # Date and Time
    "date_dd_mm_yyyy": r"^\d{2}[-/]\d{2}[-/]\d{4}$",

    "date_yyyy_mm_dd": r"^\d{4}-\d{2}-\d{2}$",

    "time_24_hour": r"^(?:[01]\d|2[0-3]):[0-5]\d$",

    "timestamp": r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",

    # Location
    "pincode_india": r"^[1-9]\d{5}$",

    "ipv4_format": r"^(?:\d{1,3}\.){3}\d{1,3}$",

    # Text Cleaning
    "special_characters": r"[^A-Za-z0-9 ]",

    "extra_spaces": r"\s+",

    "html_tags": r"<[^>]*>",

    "duplicate_words": r"\b(\w+)\s+\1\b",

    "hashtags": r"#[A-Za-z0-9_]+",

    "numbers": r"\d+",

    "alphabets": r"[A-Za-z]+",

    # Files and Logs
    "file_extension": r"\.([A-Za-z0-9]+)$",

    "error_log": r"\bERROR\b.*",

    "warning_log": r"\bWARNING\b.*",

    "word_boundary_cat": r"\bcat\b",

    "leading_trailing_spaces": r"^\s+|\s+$"
}


# Display Pattern Library
print("\nTOTAL PATTERNS:", len(PATTERNS))

for number, (name, pattern) in enumerate(PATTERNS.items(), start=1):
    print(f"\n{number}. {name}")
    print("   Regex:", pattern)


# Reusable validation function
def validate_pattern(pattern_name, value):

    pattern = PATTERNS.get(pattern_name)

    if pattern is None:
        return "Pattern not found"

    return bool(re.fullmatch(pattern, str(value)))


# Reusable extraction function
def extract_pattern(pattern_name, text):

    pattern = PATTERNS.get(pattern_name)

    if pattern is None:
        return "Pattern not found"

    return re.findall(pattern, str(text))


# Reusable cleaning function
def clean_using_pattern(pattern_name, text, replacement=""):

    pattern = PATTERNS.get(pattern_name)

    if pattern is None:
        return "Pattern not found"

    return re.sub(pattern, replacement, str(text))


# Validation Examples

print("Email:", validate_pattern("email", "rahul@gmail.com"))

print("Mobile:", validate_pattern("indian_mobile", "9876543210"))

print("Username:", validate_pattern("username", "chandra_123"))

print("PIN Code:", validate_pattern("pincode_india", "500001"))

print("Password:", validate_pattern("strong_password", "Python@123"))


# Extraction Examples

text = "Contact rahul@gmail.com or priya@yahoo.com"

print("Emails:", extract_pattern("email", text))

text = "Python #DataEngineering #Regex"

print("Hashtags:", extract_pattern("hashtags", text))


# Cleaning Examples


text = "Hello@Python#2026!"

print(
    "Cleaned Text:",
    clean_using_pattern("special_characters", text)
)

text = "Python     is     useful"

print(
    "Standardized Spaces:",
    clean_using_pattern("extra_spaces", text, " ")
)
