# Day 21 – Multi-Source Data Collection & Integration

## 1. Project Overview

This project demonstrates how to collect, process, convert, and integrate data from multiple sources using Python.

The objective is to build a reliable data collection workflow that extracts information from APIs, databases, files, websites, and SFTP servers, then transforms the collected information into standardized datasets.

**Technologies Used**

- Python 3
- Pandas
- Requests
- SQLAlchemy
- PostgreSQL
- SQLite
- BeautifulSoup
- Paramiko
- XML
- JSON
- CSV
- Excel
- Parquet
- Avro
- Logging

## 2. Project Objectives

- Collect data from three or more APIs.
- Extract records from PostgreSQL and SQLite databases.
- Read and process CSV, JSON, and Excel files.
- Extract structured information through web scraping.
- Transfer files using SFTP.
- Convert data between CSV, JSON, XML, Parquet, and Avro formats.
- Standardize schemas from different sources.
- Integrate datasets and identify duplicate records.
- Generate data lineage reports.
- Implement logging and validation.

## 3. Project Folder Structure

```text
01_Multi_Source_Collection/
│
├── APIs/
│   └── 01_collect_api_data.py
│
├── Databases/
│   ├── 02_collect_database_data.py
│   └── source_data.db
│
├── Files/
│   ├── input/
│   │   ├── customers.csv
│   │   ├── products.json
│   │   └── employees.xlsx
│   │
│   ├── Format_Conversion/
│   │   └── 04_format_conversion.py
│   │
│   ├── Integration_Pipeline/
│   │   └── 05_integration_pipeline.py
│   │
│   └── 03_collect_file_data.py
│
├── Web_Scraping/
│   └── 04_collect_web_data.py
│
├── FTP_SFTP/
│   ├── local_server/
│   │   └── employees.csv
│   └── 05_sftp_collection.py
│
├── output/
│   ├── APIs/
│   ├── Databases/
│   ├── Files/
│   ├── Web_Scraping/
│   ├── FTP_SFTP/
│   ├── Format_Conversion/
│   └── Integration_Pipeline/
│
├── logs/
│
├── requirements.txt
├── .env
└── README.md
```

## 4. Environment Setup

### Step 1: Open the project directory

```powershell
cd "C:\Linkific Tasks\Linkific-Tasks\Day 21\01_Multi_Source_Collection"
```

### Step 2: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 3: Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```powershell
pip install -r requirements.txt
```

The format conversion task also uses:

```powershell
pip install pyarrow fastavro
```

### Step 5: Configure database credentials

Create a `.env` file in the project root:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=synthetic_data_db
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
```

Replace the password placeholder with your own local PostgreSQL password. Never publish this file.

## 5. Data Collection Modules

### Module 1: API Data Collection

**Script:** `APIs/01_collect_api_data.py`

The API module collects data from three endpoints:

| API | Purpose |
|---|---|
| JSONPlaceholder | User information |
| DummyJSON | Product information |
| Open-Meteo | Weather information |

Endpoints:

- `https://jsonplaceholder.typicode.com/users`
- `https://dummyjson.com/products?limit=30`
- `https://api.open-meteo.com/v1/forecast`

The collected API data is saved in JSON and CSV formats.

**Run command:**

```powershell
python .\APIs\01_collect_api_data.py
```

**Expected collection results:**

- Users: 10 records
- Products: 30 records
- Weather: 1 record

**Output directory:** `output/APIs/`

### Module 2: Database Collection

**Script:** `Databases/02_collect_database_data.py`

This module extracts information from:

- PostgreSQL database: `synthetic_data_db`
- SQLite database: `source_data.db`

PostgreSQL tables collected:

- customers
- orders
- order_items
- products
- transactions

SQLite tables collected:

- departments
- employees

Each extracted table is exported into CSV and JSON files.

**Run command:**

```powershell
python .\Databases\02_collect_database_data.py
```

**Output directory:** `output/Databases/`

### Module 3: File Data Collection

**Script:** `Files/03_collect_file_data.py`

This module reads three different file formats:

| Input file | Format |
|---|---|
| customers.csv | CSV |
| products.json | JSON |
| employees.xlsx | Excel |

The data is loaded using Pandas and exported into standardized CSV and JSON outputs.

**Run command:**

```powershell
python .\Files\03_collect_file_data.py
```

**Output directory:** `output/Files/`

### Module 4: Web Scraping

**Script:** `Web_Scraping/04_collect_web_data.py`

This module uses Requests and BeautifulSoup to collect structured quote information from:

`https://quotes.toscrape.com/`

Collected fields include:

- Quote text
- Author
- Tags

The scraped records are saved in CSV and JSON formats.

**Run command:**

```powershell
python .\Web_Scraping\04_collect_web_data.py
```

**Expected result:** 10 quote records.

**Output directory:** `output/Web_Scraping/`

### Module 5: FTP/SFTP Collection

**Script:** `FTP_SFTP/05_sftp_collection.py`

This module demonstrates secure file transfer using SFTP and the Paramiko library.

Workflow:

1. Prepare the employee CSV file.
2. Connect to the local SFTP server.
3. Authenticate using SSH public-key authentication.
4. Upload the CSV file.
5. Download the file.
6. Validate the downloaded records.
7. Export the downloaded data into JSON.

**Run command:**

```powershell
python .\FTP_SFTP\05_sftp_collection.py
```

The local SFTP server requires Windows OpenSSH Server and the configured SSH key.

**Output directory:** `output/FTP_SFTP/`

## 6. Data Format Conversion

**Script:** `Files/Format_Conversion/04_format_conversion.py`

This module converts employee data between five formats.

| Format | Description |
|---|---|
| CSV | Comma-separated tabular data |
| JSON | Structured key-value data |
| XML | Extensible Markup Language |
| Parquet | Column-oriented storage format |
| Avro | Schema-based data serialization format |

**Run command:**

```powershell
python .\Files\Format_Conversion\04_format_conversion.py
```

**Validation result:**

| Format | Records verified | Status |
|---|---:|---|
| CSV | 5 | PASS |
| JSON | 5 | PASS |
| XML | 5 | PASS |
| Parquet | 5 | PASS |
| Avro | 5 | PASS |

All five formats were successfully converted and read back for verification.

**Output directory:** `output/Format_Conversion/`

## 7. Multi-Source Data Integration Pipeline

**Script:** `Files/Integration_Pipeline/05_integration_pipeline.py`

The integration pipeline combines data from different collection sources into three standardized datasets.

### Customer Integration

Sources:

- PostgreSQL customer data
- File-based customer data

Standardized fields:

- source_record_id
- customer_name
- email
- phone
- city
- age
- created_at
- source_system
- ingested_at

### Product Integration

Sources:

- API product data
- PostgreSQL product data
- File-based product data

Standardized fields:

- source_record_id
- product_name
- category
- price
- stock_quantity
- brand
- source_system
- ingested_at

### Employee Integration

Sources:

- SQLite employee data
- File-based employee data
- SFTP employee data

Standardized fields:

- source_record_id
- employee_name
- email
- department
- department_id
- salary
- source_system
- ingested_at

### Integration Workflow

1. Load collected source files.
2. Map source columns to standardized column names.
3. Normalize text values.
4. Generate matching keys for duplicate detection.
5. Apply source priority when duplicate records are found.
6. Combine the records.
7. Save integrated datasets as CSV and JSON.
8. Generate a data lineage report.
9. Validate the final record counts.

**Run command:**

```powershell
python .\Files\Integration_Pipeline\05_integration_pipeline.py
```

### Verified Integration Results

| Entity | Input records | Output records | Duplicates removed |
|---|---:|---:|---:|
| Customers | 1,005 | 1,005 | 0 |
| Products | 235 | 235 | 0 |
| Employees | 15 | 15 | 0 |
| **Total** | **1,255** | **1,255** | **0** |

All three integrated datasets passed final validation.

Zero duplicates were detected using the implemented matching rules.

### Integration Output Files

```text
output/Integration_Pipeline/
│
├── integrated_customers.csv
├── integrated_customers.json
├── integrated_products.csv
├── integrated_products.json
├── integrated_employees.csv
├── integrated_employees.json
└── data_lineage.csv
```

The `data_lineage.csv` report records:

- Entity name
- Input record count
- Output record count
- Duplicate count
- Source systems

## 8. Logging and Error Handling

The project uses Python's logging module to record collection and processing activities.

Logs are stored in the `logs/` directory.

Important log files include:

- `api_collection.log`
- `file_collection.log`
- `web_scraping.log`
- `sftp_collection.log`
- `format_conversion.log`
- `integration_pipeline.log`

The logs help track:

- Source loading
- Number of records collected
- Processing activities
- Output file creation
- Validation results
- Errors and exceptions

## 9. Project Validation Summary

| Module | Validation |
|---|---|
| API collection | 10 users, 30 products, 1 weather record |
| Database collection | 7 database tables extracted |
| File collection | CSV, JSON, Excel successfully processed |
| Web scraping | 10 quotes collected |
| SFTP | 5 employee records transferred and validated |
| Format conversion | 5 formats successfully verified |
| Integration pipeline | 1,255 input records integrated |

## 10. How to Run the Project

Activate the virtual environment first:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run each module from the project root:

```powershell
python .\APIs\01_collect_api_data.py

python .\Databases\02_collect_database_data.py

python .\Files\00_create_sample_files.py

python .\Files\03_collect_file_data.py

python .\Web_Scraping\04_collect_web_data.py

python .\FTP_SFTP\05_sftp_collection.py

python .\Files\Format_Conversion\04_format_conversion.py

python .\Files\Integration_Pipeline\05_integration_pipeline.py
```

Run the sample-file creation script before file collection if the input files do not already exist.

Run database collection only after PostgreSQL and its configured database are available. Run SFTP collection only when the local SFTP server and SSH authentication are configured.

## 11. Security and Best Practices

- Keep database passwords inside `.env`.
- Never upload `.env` to GitHub.
- Never upload SSH private keys.
- Add `.venv/` and generated secrets to `.gitignore`.
- Use environment variables for sensitive configuration.
- Validate source data before integration.
- Maintain logs for troubleshooting.
- Use standardized schemas for data integration.
- Verify output record counts after processing.
- Handle missing values and inconsistent data carefully.

## 12. Key Learning Outcomes

Through this project, I gained practical experience in:

- Extracting data from REST APIs.
- Connecting to PostgreSQL and SQLite.
- Processing CSV, JSON, and Excel files.
- Web scraping with BeautifulSoup.
- Secure file transfer using SFTP and Paramiko.
- Converting data into XML, Parquet, and Avro.
- Using Pandas for data transformation.
- Mapping schemas across multiple sources.
- Performing duplicate detection and source-priority handling.
- Creating integrated datasets and lineage reports.
- Implementing logging and validation in Python pipelines.

## 13. Conclusion

The Day 21 project demonstrates an end-to-end multi-source data collection and integration workflow using Python.

Data was collected from APIs, relational databases, local files, web pages, and an SFTP server. The collected data was converted into multiple formats, standardized, integrated, and validated.

The final integration pipeline successfully processed **1,255 records across three integrated entities: customers, products, and employees**.

This project strengthened my understanding of real-world data engineering concepts, including data ingestion, transformation, integration, data quality, secure data transfer, and lineage tracking.

---

**Project:** Day 21 – Multi-Source Data Collection & Integration  
**Role:** Data Engineer Intern  
**Primary Language:** Python  
**Status:** Completed and validated
