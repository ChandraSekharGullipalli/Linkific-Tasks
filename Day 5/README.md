# Day 5 – Pandas Practice and Data Analysis

## Project Overview
This project focuses on learning and practicing Pandas for data manipulation, data cleaning, and data analysis using Python.

## Tools and Technologies
- Python
- Pandas
- Jupyter Notebook
- VS Code
- Git and GitHub
- CSV datasets

## Tasks Completed

### 1. Employee Data Cleaning
- Handled missing and invalid values.
- Removed duplicate records.
- Standardized text columns.
- Exported cleaned employee data to CSV.

### 2. Sales Data Cleaning
- Cleaned product, category, and region names.
- Converted columns to appropriate data types.
- Removed duplicate transactions.
- Validated quantities, prices, and dates.
- Calculated total sales.

### 3. Customer Data Cleaning
- Standardized customer names and email addresses.
- Validated email and phone number formats.
- Handled missing and invalid ages.
- Removed duplicate customers.
- Exported cleaned customer data.

### 4. GroupBy and Aggregation
- Grouped records by department, city, and product.
- Calculated total and average salary.
- Found minimum and maximum values.
- Counted records in each group.
- Practiced multiple aggregation functions.

### 5. Real Dataset Analysis
- Explored a sales dataset using Pandas.
- Checked dataset dimensions, data types, and missing values.
- Analyzed revenue by product and region.
- Identified top-performing products and regions.
- Generated and exported a sales analysis report.

### 6. Pandas Patterns Practiced
- `head()` and `tail()` – view records.
- `info()` and `describe()` – understand the dataset.
- `isnull()` – identify missing values.
- `drop_duplicates()` – remove duplicate records.
- `fillna()` – handle missing values.
- `groupby()` – group data.
- `agg()` – perform multiple calculations.
- `sort_values()` – sort records.
- `merge()` – combine DataFrames.
- `to_csv()` – export results.

## Folder Structure

```text
Day5/
├── Project1_Employee_Cleaning/
│   ├── employee_data.csv
│   ├── employee_cleaning.ipynb
│   ├── cleaned_employees.csv
│   └── README.md
├── Project2_Sales_Cleaning/
│   ├── sales_data.csv
│   ├── sales_cleaning.ipynb
│   ├── cleaned_sales.csv
│   └── README.md
├── Project3_Customer_Cleaning/
│   ├── customer_data.csv
│   ├── customer_cleaning.ipynb
│   ├── cleaned_customers.csv
│   └── README.md
└── Day5_Real_Dataset_Analysis/
    ├── sales_dataset.csv
    ├── sales_analysis.ipynb
    ├── sales_analysis_report.csv
    └── README.md
```

## How to Run
1. Install Python.
2. Install the required libraries:

   ```bash
   pip install pandas jupyter
   ```

3. Open the project folder in VS Code.
4. Open the required `.ipynb` notebook.
5. Select your Python environment and run the cells sequentially.
6. Review the generated CSV files.

## Learning Outcomes
- Improved understanding of Pandas DataFrames and Series.
- Practiced cleaning real-world-style datasets.
- Learned to handle missing values and duplicates.
- Applied GroupBy and aggregation functions.
- Developed basic data analysis and reporting skills.
- Practiced exporting processed data for further use.

## Conclusion
This training helped me develop practical skills in Python Pandas for data cleaning, transformation, analysis, and reporting. These skills are useful for preparing reliable datasets for data engineering and analytics workflows.
