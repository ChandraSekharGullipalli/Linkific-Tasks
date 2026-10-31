DAY 12 – MULTI-SOURCE EXTRACTION TRANSFORMATION LOGIC AND WAREHOUSE
LOADING

1.  PROJECT OVERVIEW

This document describes the transformation and warehouse-loading stages
of the separate Multi_Source_Extraction project.

The project extracts data from three sources: - CSV file:
hospital_patients.csv - REST API: JSONPlaceholder Posts API - JSON file:
online_courses.json

The extracted data is transformed using Python and Pandas. The
transformed datasets are then saved as CSV files and loaded into
PostgreSQL warehouse tables.

2.  TRANSFORMATION LOGIC

Transformation is the process of cleaning, validating, and modifying
extracted data so it is more consistent and suitable for analysis.

2.1 Hospital patient data transformation

Input: Hospital patient records from the CSV file.

Operations performed: - Remove duplicate records using patient_id. -
Remove leading and trailing spaces from text fields. - Standardize
patient names, department names, and city names. - Convert age and
consultation_fee columns to numeric data types. - Remove records that
have missing required values such as patient_id, patient_name, age, or
consultation_fee.

Output file: output/transformed_hospital_patients.csv

2.2 API posts data transformation

Input: Posts retrieved from the JSONPlaceholder API.

Operations performed: - Remove duplicate posts using the post id. -
Replace missing title and body values with empty text. - Remove
unnecessary leading and trailing spaces. - Create title_length to store
the number of characters in each title. - Create body_length to store
the number of characters in each post body.

Output file: output/transformed_api_posts.csv

2.3 Online course data transformation

Input: Course records from online_courses.json.

Operations performed: - Remove duplicate courses using course_id. -
Remove unnecessary spaces from course names and categories. -
Standardize course names and categories. - Convert duration_hours and
price into numeric data types. - Create duration_category based on
course duration: Short: less than 30 hours Medium: 30 to 50 hours Long:
more than 50 hours

Output file: output/transformed_online_courses.csv

3.  TRANSFORMED DATA OUTPUT

After running the integrated extraction and transformation program, the
output folder contains:

-   transformed_hospital_patients.csv
-   transformed_api_posts.csv
-   transformed_online_courses.csv

These files contain the cleaned and transformed datasets that are ready
for warehouse loading.

4.  WAREHOUSE LOADING

Warehouse loading is the process of transferring prepared data into
database tables so that it can be queried and analyzed.

Technology used: - PostgreSQL - SQLAlchemy - Pandas - psycopg2 -
python-dotenv

The warehouse loader reads the transformed CSV files and loads them into
the PostgreSQL database named etl_database.

5.  POSTGRESQL WAREHOUSE TABLES

The project uses three separate warehouse tables:

1.  hospital_patients Source: transformed_hospital_patients.csv

2.  api_posts Source: transformed_api_posts.csv

3.  online_courses Source: transformed_online_courses.csv

The loader uses Pandas to_sql() to write each dataset into its
corresponding PostgreSQL table.

The current implementation uses if_exists=‘replace’. This recreates the
named project table when the loader runs. It does not modify the
separate sales_data table from the earlier ETL project.

6.  WAREHOUSE VALIDATION

After loading, the program checks the number of records in each
warehouse table using SQL COUNT(*).

Example SQL validation queries:

SELECT COUNT(*) FROM hospital_patients;

SELECT COUNT(*) FROM api_posts;

SELECT COUNT(*) FROM online_courses;

To inspect the loaded records:

SELECT * FROM hospital_patients;

SELECT * FROM api_posts;

SELECT * FROM online_courses;

7.  EXPECTED RESULTS

If all extraction and transformation stages complete successfully and
the API returns all records, the expected record counts are:

-   Hospital patients: 8 records
-   API posts: 100 records
-   Online courses: 5 records

Total expected records: 113

The actual counts should be confirmed from the program output and
PostgreSQL validation queries.

8.  HOW TO RUN THE PROJECT

Open PowerShell in the Multi_Source_Extraction folder.

Install the required packages:

python -m pip install pandas requests sqlalchemy psycopg2-binary
python-dotenv

Run extraction and transformation:

python main.py

Run warehouse loading:

python warehouse_load.py

The .env file should contain the PostgreSQL connection settings:

DB_HOST=localhost DB_PORT=5432 DB_NAME=etl_database DB_USER=postgres
DB_PASSWORD=your_actual_postgresql_password

Replace the password placeholder with the local PostgreSQL password. Do
not share the password or commit the .env file to GitHub. Add .env to
.gitignore.

9.  CONCLUSION

In this project, I implemented transformation logic for data collected
from CSV, API, and JSON sources. I cleaned text fields, handled missing
values, removed duplicate records, converted data types, and created
additional columns for analysis.

I then loaded the transformed datasets into separate PostgreSQL
warehouse tables and used SQL queries to validate the loaded record
counts.

This work demonstrates the transformation and warehouse-loading stages
of a multi-source data pipeline.