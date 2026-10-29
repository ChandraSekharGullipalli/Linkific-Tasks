# Day 10 – Data Integration Patterns

## 1. Overview

This project demonstrates practical data integration patterns using Python, REST APIs, CSV files, SQLAlchemy ORM, and PostgreSQL.

The goal is to extract data from different sources, transform and validate it, and load it into a relational database.

## 2. Technologies Used

- Python 3
- REST API and Requests
- PostgreSQL
- Psycopg2
- SQLAlchemy ORM
- CSV files
- VS Code

## 3. Project Structure

```text
Day 10/
├── 01_test_connection.py
├── 02_test_connection.py
├── 04_retail_sales_etl.py
├── 05_sqlalchemy_orm_demo.py
├── 06_api_to_database.py
├── retail_sales.csv
└── README.md
```

## 4. Integration Patterns Implemented

### Pattern 1: API to Database

**File:** `06_api_to_database.py`

- Extract user records from a REST API.
- Validate and transform the response.
- Insert records into PostgreSQL.
- Update existing records using an upsert operation.
- Verify the loaded record count.

**Result:** Successfully loaded 10 API user records into the `api_users` table.

### Pattern 2: CSV to Database

**File:** `04_retail_sales_etl.py`

- Read retail sales data from a CSV file.
- Inspect and validate sales records.
- Clean the data before loading.
- Store the processed data in PostgreSQL.

### Pattern 3: SQLAlchemy ORM

**File:** `05_sqlalchemy_orm_demo.py`

- Define a Python class mapped to a database table.
- Create the table using SQLAlchemy.
- Insert or update a retail sales record.
- Retrieve, update, and query records.

### Pattern 4: Database Connection Management

**Files:** `01_test_connection.py` and `02_test_connection.py`

- Establish a connection to PostgreSQL.
- Verify the database version.
- Check connection errors and close database connections.

## 5. ETL Workflow

1. **Extract:** Retrieve data from an API or CSV file.
2. **Transform:** Validate records, select required fields, and clean the data.
3. **Load:** Insert or update the processed data in PostgreSQL.
4. **Validate:** Execute SQL queries to verify the stored records.

## 6. Best Practices

- Use request timeouts when calling APIs.
- Handle HTTP and database errors.
- Validate required fields before loading.
- Use parameterized SQL or database library helpers.
- Use primary keys and upsert operations to handle repeated records.
- Use transactions to maintain data consistency.
- Store database credentials in environment variables.
- Never commit passwords or secrets to GitHub.
- Close database connections after processing.
- Log pipeline progress and errors for easier troubleshooting.

## 7. Validation Queries

Check API user records:

```sql
SELECT *
FROM api_users
ORDER BY user_id;
```

Count the records:

```sql
SELECT COUNT(*) AS total_users
FROM api_users;
```

Group records by city:

```sql
SELECT city, COUNT(*) AS total_users
FROM api_users
GROUP BY city
ORDER BY total_users DESC;
```

## 8. Execution

Run the API-to-database pipeline from the project root:

```powershell
python ".\Day 10\06_api_to_database.py"
```

Set the required PostgreSQL environment variables in the terminal before execution.

## 9. Outcome

The API integration pipeline successfully extracted 10 records, transformed the data, and loaded the records into PostgreSQL. The database record count was verified.

The project provided hands-on practice with API integration, ETL workflows, relational databases, ORM operations, data validation, and database error handling.

## 10. Future Improvements

- Add automated retries for temporary API failures.
- Introduce structured logging.
- Store API credentials securely when authentication is required.
- Add data quality checks and automated tests.
- Schedule the pipeline for periodic execution.
- Add incremental loading for larger datasets.

## Conclusion

This project demonstrates fundamental data engineering integration patterns and provides a foundation for building reliable, maintainable ETL pipelines.
