
# Day 18 - Python Regular Expressions (Regex)

## Project Overview

This project demonstrates Python Regular Expressions (Regex) for text processing, pattern matching, data extraction, format validation, and data cleaning.

The project uses Python's built-in `re` module and Pandas to process customer records and application log files.

## Learning Objectives

- Understand regular expression syntax and patterns.
- Master Python's re module.
- Extract emails, phone numbers, URLs, dates, and other information.
- Validate common data formats.
- Clean and standardize text data.
- Build reusable regex pattern libraries.
- Parse application log files.
- Generate structured CSV reports.

## Technologies Used

- Python 3.13
- Regular Expressions (re module)
- Pandas
- CSV files
- Visual Studio Code
- Git and GitHub

## Project Structure

```text
Day 18/
└── Regex-Patterns/
    ├── 01_regex_basics.py
    ├── 02_python_re_module.py
    ├── 03_common_patterns.py
    ├── 04_data_cleaning.py
    ├── 05_customer_data_cleaning.py
    ├── 06_log_file_parsing.py
    ├── 07_data_cleaning_scripts.py
    ├── 08_regex_pattern_library.py
    ├── 09_advanced_log_parser.py
    ├── data/
    │   ├── customers.csv
    │   └── sample.log
    ├── outputs/
    ├── README.md
    └── requirements.txt
```

## 1. Regex Basics

Regular Expressions are patterns used to search, match, extract, validate, and replace text.

### Important Regex Symbols

| Symbol | Description |
|---|---|
| . | Any character except newline by default |
| ^ | Start of string or line |
| $ | End of string or line |
| * | Zero or more repetitions |
| + | One or more repetitions |
| ? | Zero or one repetition |
| \d | Digit |
| \D | Non-digit |
| \w | Word character |
| \W | Non-word character |
| \s | Whitespace |
| \S | Non-whitespace |
| [] | Character class |
| {} | Repetition count |
| () | Group |
| \| | OR operator |
| \b | Word boundary |

### Example

```python
import re

text = "Python 123"

result = re.findall(r"\d+", text)

print(result)
```

Output:

```text
['123']
```

## 2. Python re Module

| Function | Purpose |
|---|---|
| re.search() | Finds the first match anywhere |
| re.match() | Checks for a match at the beginning |
| re.findall() | Returns all non-overlapping matches |
| re.sub() | Replaces matching patterns |
| re.compile() | Creates reusable compiled patterns |
| re.split() | Splits text using a pattern |
| re.fullmatch() | Checks whether the entire string matches |

### Regex Flags

- re.IGNORECASE: Case-insensitive matching.
- re.MULTILINE: Makes ^ and $ work at each line.
- re.DOTALL: Allows dot to match newline characters.

## 3. Common Regex Pattern Library

This project includes 30+ practical patterns.

| No. | Pattern | Purpose |
|---|---|---|
| 1 | Email | Email extraction |
| 2 | Indian mobile | 10-digit mobile validation |
| 3 | International phone | International phone format |
| 4 | Website URL | URL extraction |
| 5 | Username | Username validation |
| 6 | Alphabet only | Letters-only validation |
| 7 | Alphanumeric | Letters and numbers |
| 8 | Strong password | Password format checking |
| 9 | Integer | Integer validation |
| 10 | Decimal | Decimal validation |
| 11 | Positive number | Non-negative integer format |
| 12 | Currency | Currency value extraction |
| 13 | Percentage | Percentage extraction |
| 14 | DD-MM-YYYY date | Date format checking |
| 15 | YYYY-MM-DD date | Standard date format |
| 16 | Time | 24-hour time validation |
| 17 | Timestamp | Log timestamp extraction |
| 18 | PIN code | Indian PIN format validation |
| 19 | IPv4 | IPv4 format matching |
| 20 | Special characters | Special character detection |
| 21 | Extra spaces | Whitespace matching |
| 22 | HTML tags | HTML tag matching |
| 23 | Duplicate words | Repeated word detection |
| 24 | Hashtags | Hashtag extraction |
| 25 | Numbers | Numeric extraction |
| 26 | Alphabets | Alphabet extraction |
| 27 | File extension | File extension extraction |
| 28 | Error log | Error message extraction |
| 29 | Warning log | Warning message extraction |
| 30 | Word boundary | Exact word matching |
| 31 | Leading/trailing spaces | Boundary whitespace matching |

Note: These patterns check formats. Production-level validation may require additional checks. For example, an IPv4 address must have each octet between 0 and 255, and dates must be valid calendar dates.

## 4. Data Cleaning Using Regex

The data cleaning scripts perform the following operations:

1. Remove unwanted special characters.
2. Remove extra spaces.
3. Clean phone numbers.
4. Extract email addresses.
5. Standardize customer names.
6. Extract numeric values.
7. Remove HTML tags.
8. Standardize date formats.
9. Convert text to lowercase.
10. Remove repeated words.

### Example

```python
import re

text = "Hello@@@ Python!!! 2026"

cleaned = re.sub(r"[^A-Za-z0-9 ]", "", text)

print(cleaned)
```

Output:

```text
Hello Python 2026
```

## 5. Customer Data Cleaning Project

Input file: `data/customers.csv`

The project processes customer records containing:

- Customer ID
- Customer name
- Email
- Phone number
- Date
- City

### Cleaning Operations

- Standardize customer names.
- Validate email formats.
- Clean Indian mobile numbers.
- Standardize dates into YYYY-MM-DD.
- Standardize city names.
- Identify invalid records.

### Output

`outputs/cleaned_customers.csv`

The output includes validation columns for email, phone, and date quality.

## 6. Log File Parsing

The log parser reads application logs and extracts:

- Timestamp
- Log level
- Log message
- Error records
- Warning records
- Information records

### Log Levels

| Level | Description |
|---|---|
| INFO | General application information |
| WARNING | Potential issues |
| ERROR | Application errors |
| DEBUG | Diagnostic information |

### Output Files

- parsed_logs.csv
- error_logs.csv
- log_summary.csv
- advanced_parsed_logs.csv
- advanced_error_report.csv
- advanced_warning_report.csv
- invalid_logs.csv
- advanced_log_summary.csv

## 7. Advanced Log Parser

The advanced parser provides:

- Structured log extraction.
- Log level statistics.
- Error and warning filtering.
- Timestamp extraction.
- Database-related log filtering.
- Invalid log detection.
- CSV report generation.

## 8. How to Run the Project

### Step 1: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 2: Navigate to project folder

```powershell
cd "C:\Linkific Tasks\Linkific-Tasks\Day 18\Regex-Patterns"
```

### Step 3: Run individual scripts

```powershell
python 01_regex_basics.py
python 02_python_re_module.py
python 03_common_patterns.py
python 04_data_cleaning.py
python 05_customer_data_cleaning.py
python 06_log_file_parsing.py
python 07_data_cleaning_scripts.py
python 08_regex_pattern_library.py
python 09_advanced_log_parser.py
```

## 9. Project Deliverables

- Regex basics demonstrations.
- Python re module examples.
- 30+ practical regex patterns.
- Data cleaning scripts.
- Customer data cleaning project.
- Regex pattern library.
- Basic log parser.
- Advanced log parser.
- CSV output reports.
- Project documentation.

## 10. Skills Gained

- Python Regular Expressions.
- Text processing and pattern matching.
- Data extraction and validation.
- Data cleaning and standardization.
- CSV data processing.
- Pandas operations.
- Log file analysis.
- Reusable Python functions.
- Error and warning identification.

## Conclusion

Day 18 provided practical experience with Python Regular Expressions and their applications in data engineering and data processing.

The project demonstrates how Regex can be used to extract information, validate formats, clean customer data, standardize text, and analyze application logs.

The completed project contains reusable regex patterns and practical scripts that can be extended for real-world data engineering workflows.

