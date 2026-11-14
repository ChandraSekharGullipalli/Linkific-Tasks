# Day 20 – Synthetic Data Generation

## 1. Project Overview

This project focuses on generating realistic synthetic datasets using Python and the Faker library, validating generated data, and working with PostgreSQL databases.

The project covers e-commerce, human resources, financial data, and large-scale sales dataset generation.

### Objectives

- Generate realistic synthetic data using Python Faker.
- Create multiple datasets in CSV format.
- Build relational PostgreSQL databases.
- Perform data validation and integrity checks.
- Load CSV data into PostgreSQL using Python.
- Generate a large dataset containing 100,000 records.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.13 | Data generation and processing |
| Faker | Synthetic data generation |
| Pandas | Data handling and analysis |
| PostgreSQL 18 | Relational database |
| psycopg2 | Python-PostgreSQL connectivity |
| CSV | Data storage |
| VS Code | Development environment |
| PowerShell | Running Python scripts |

## 3. Project Structure

```text
Day 20/
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── transactions.csv
│   ├── employees.csv
│   ├── accounts.csv
│   ├── financial_transactions.csv
│   └── large_sales_dataset_100k.csv
│
├── database/
│   └── schema.sql
│
├── scripts/
│   ├── 01_faker_basics.py
│   ├── 02_generate_ecommerce.py
│   ├── 03_generate_hr.py
│   ├── 04_generate_financial.py
│   ├── 05_validate_data.py
│   ├── 06_bulk_insert_postgres.py
│   ├── 07_load_hr_database.py
│   ├── 08_load_financial_database.py
│   └── 09_generate_large_dataset.py
│
├── requirements.txt
└── README.md
```

## 4. Environment Setup

Open the project folder in VS Code.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Important packages:

```text
Faker
psycopg2-binary
pandas
```

## 5. Synthetic Data Generation Guide

### Step 1 – Faker Basics

Run:

```powershell
python scripts/01_faker_basics.py
```

Learned to generate:

- Random names
- Email addresses
- Addresses
- Company names
- Dates
- Localized data

### Step 2 – E-commerce Dataset

Run:

```powershell
python scripts/02_generate_ecommerce.py
```

Generated datasets:

| Dataset | Records |
|---|---:|
| Customers | 1,000 |
| Products | 200 |
| Orders | 1,000 |
| Order Items | 2,516 |
| Transactions | 1,000 |
| Total | 5,716 |

### Step 3 – HR Dataset

Run:

```powershell
python scripts/03_generate_hr.py
```

Generated 1,000 synthetic employee records.

The employee dataset contains:

- Employee ID
- Employee Name
- Email
- Department
- Job Role
- Salary
- City
- Join Date
- Employment Status

### Step 4 – Financial Dataset

Run:

```powershell
python scripts/04_generate_financial.py
```

Generated:

| Dataset | Records |
|---|---:|
| Accounts | 1,000 |
| Financial Transactions | 10,000 |
| Total | 11,000 |

### Step 5 – Data Validation

Run:

```powershell
python scripts/05_validate_data.py
```

Validation checks included:

1. Unique customer IDs.
2. Unique product IDs.
3. Unique order IDs.
4. Valid customer references in orders.
5. Valid order references in order items.
6. Valid product references in order items.
7. Valid order references in transactions.
8. Positive product prices.
9. Positive item quantities.

**Result:** All nine validation checks passed.

## 6. PostgreSQL Database Implementation

Three separate PostgreSQL databases were created.

### Database 1 – E-commerce

Database name: `synthetic_data_db`

Tables:

1. customers
2. products
3. orders
4. order_items
5. transactions

Total records loaded: **5,716**

### Database 2 – Human Resources

Database name: `synthetic_hr_db`

Tables:

1. departments
2. employees
3. salaries
4. attendance
5. performance_reviews

| Table | Records |
|---|---:|
| departments | 6 |
| employees | 1,000 |
| salaries | 1,000 |
| attendance | 20,000 |
| performance_reviews | 1,000 |
| Total | 23,006 |

### Database 3 – Financial

Database name: `synthetic_financial_db`

Tables:

1. customers
2. branches
3. accounts
4. financial_transactions
5. loans

| Table | Records |
|---|---:|
| customers | 998 |
| branches | 10 |
| accounts | 1,000 |
| financial_transactions | 10,000 |
| loans | 200 |
| Total | 12,208 |

Note: There are 998 unique customer names across 1,000 accounts because some customers have multiple accounts.

## 7. Loading Data into PostgreSQL

### E-commerce Database

Run:

```powershell
python scripts/06_bulk_insert_postgres.py
```

This script uses PostgreSQL bulk loading through `COPY`.

### HR Database

Set the database name:

```powershell
$env:DB_NAME = "synthetic_hr_db"
```

Run:

```powershell
python scripts/07_load_hr_database.py
```

The loader creates department relationships and inserts employee, salary, attendance, and performance-review records.

### Financial Database

Set the database name:

```powershell
$env:DB_NAME = "synthetic_financial_db"
```

Run:

```powershell
python scripts/08_load_financial_database.py
```

The loader inserts customer, branch, account, and financial transaction data, and generates supplementary loan records.

### Database Connection Configuration

Set the PostgreSQL environment variables in PowerShell:

```powershell
$env:DB_HOST = "localhost"
$env:DB_USER = "postgres"
$env:DB_PORT = "5432"
$env:DB_PASSWORD = Read-Host "Enter PostgreSQL password" -AsSecureString
$env:DB_PASSWORD = [System.Net.NetworkCredential]::new("", $env:DB_PASSWORD).Password
```

Use the appropriate `DB_NAME` before running each database loader.

Never store your actual password in the Python source code or GitHub repository.

## 8. Large Dataset Generation – 100K Records

A large synthetic sales dataset was generated using Faker and Python's CSV module.

Run:

```powershell
python scripts/09_generate_large_dataset.py
```

Output file:

```text
data/large_sales_dataset_100k.csv
```

### Dataset Information

Total records: **100,000**

Columns:

| Column | Description |
|---|---|
| transaction_id | Unique transaction identifier |
| customer_id | Customer reference |
| product_id | Product reference |
| transaction_date | Transaction date |
| quantity | Purchased quantity |
| unit_price | Price per unit |
| total_amount | Quantity multiplied by unit price |
| payment_method | Payment method |
| payment_status | Payment status |
| city | Customer transaction city |

### Verify the Record Count

Run:

```powershell
python -c "import csv; f=open('data/large_sales_dataset_100k.csv', encoding='utf-8'); print('Total data records:', sum(1 for _ in csv.DictReader(f))); f.close()"
```

Expected output:

```text
Total data records: 100000
```

Check file size:

```powershell
Get-Item .\data\large_sales_dataset_100k.csv | Select-Object Name, Length
```

This large dataset is generated as a CSV file and is separate from the three PostgreSQL databases.

## 9. Final Project Summary

| Deliverable | Result |
|---|---|
| Faker basics | Completed |
| E-commerce data generation | Completed |
| HR data generation | Completed |
| Financial data generation | Completed |
| Data validation | 9 checks passed |
| PostgreSQL databases | 3 created |
| PostgreSQL tables | 15 created |
| HR database loading | Completed |
| Financial database loading | Completed |
| E-commerce bulk loading | Completed |
| Large sales dataset | 100,000 records generated |

### Database Record Summary

| Database | Records |
|---|---:|
| E-commerce | 5,716 |
| HR | 23,006 |
| Financial | 12,208 |
| Total database records | 40,930 |

Additional CSV dataset: 100,000 sales records.

## 10. Skills Learned

- Synthetic data generation with Faker.
- Python scripting and CSV file handling.
- Random data generation.
- Relational database design.
- Primary keys and foreign keys.
- PostgreSQL table creation.
- Python database connectivity using psycopg2.
- Bulk data loading.
- Data quality validation.
- Handling large datasets.
- Database record verification.

## 11. Conclusion

Successfully completed the Day 20 Synthetic Data Generation project.

Generated realistic synthetic datasets for e-commerce, HR, and financial domains, created three PostgreSQL databases with 15 relational tables, implemented data validation, and loaded the generated data into PostgreSQL.

Also generated a separate large sales dataset containing 100,000 records in CSV format.

This project provided practical experience in Python-based data generation, data quality, relational database management, and large-scale data preparation.

**Internship Task: Day 20 – Synthetic Data Generation**
