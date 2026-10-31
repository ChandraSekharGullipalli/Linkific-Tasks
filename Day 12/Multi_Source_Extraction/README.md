# Day 12 – Multi-Source ETL Pipeline with Error Handling

**Date:** Friday, 30 October 2026  
**Training:** Data Engineering Internship  
**Project:** Multi-Source Data Extraction, Transformation and Loading

## 1. Project Overview

Today, I worked on developing a multi-source ETL pipeline using Python. The project extracts data from three different sources: CSV files, REST APIs, and JSON files.

The extracted data is processed using Pandas and prepared for loading into PostgreSQL. I also worked on a separate error-handling module to manage extraction errors and maintain log records.

## 2. Architecture

```text
              DATA SOURCES
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
      CSV         REST API     JSON
       |           |           |
       v           v           v
  Extract CSV  Extract API  Extract JSON
       |           |           |
       +-----------+-----------+
                   |
                   v
             TRANSFORMATION
               transform.py
                   |
                   v
              DATA LOADING
             warehouse_load.py
                   |
                   v
              POSTGRESQL
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
    Hospital    API Posts   Online Courses
    Patients

       SEPARATE ERROR HANDLING
                   |
                   v
           error_handling.py
                   |
                   v
             Logging File
```

## 3. Technologies Used

- Python
- Pandas
- Requests
- JSON
- PostgreSQL
- SQLAlchemy
- Python Logging
- VS Code
- Git and GitHub

## 4. Tasks Completed

1. Extracted hospital patient data from a CSV file.
2. Retrieved 100 records from the JSONPlaceholder REST API.
3. Extracted online course information from a JSON file.
4. Practiced data transformation using Python and Pandas.
5. Worked on loading processed datasets into PostgreSQL.
6. Created a separate error-handling Python module.
7. Implemented exception handling for missing files, invalid data, and API request failures.
8. Configured logging to record errors in a log file.
9. Prepared project architecture and technical documentation.

## 5. Measurable Progress

| Activity | Records |
|---|---:|
| Hospital patient CSV | 8 |
| REST API posts | 100 |
| Online courses JSON | 5 |
| Total extracted records | 113 |

## 6. Error Handling

The separate error-handling module covers:

- CSV file-not-found errors.
- Empty or invalid CSV data.
- API connection and request errors.
- Invalid API responses.
- Missing JSON files.
- Invalid JSON formatting.
- Error logging.

Log file: `output/error_handling.log`

## 7. Project Structure

```text
Multi_Source_Extraction/
│
├── Data/
│   ├── hospital_patients.csv
│   └── online_courses.json
│
├── output/
│
├── Error_Handling/
│   └── error_handling.py
│
├── extract_csv.py
├── extract_api.py
├── extract_json.py
├── transform.py
├── warehouse_load.py
├── main.py
└── README.md
```

## 8. Learning Outcomes

- Understood multi-source ETL architecture.
- Practiced CSV, JSON, and API extraction.
- Improved Python data-processing skills.
- Learned error handling and logging.
- Practiced PostgreSQL data loading.
- Understood how different ETL components work together.

## 9. Conclusion

Today, I worked on a multi-source ETL pipeline that combines data from CSV files, REST APIs, and JSON files. I also implemented a separate error-handling module and documented the project architecture.

This practical work helped me understand how data engineers extract, process, validate, and prepare data for database storage.