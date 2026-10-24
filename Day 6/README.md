# Day 6 – Advanced Pandas Guide

## Overview
This project focuses on advanced Pandas operations for data engineering and data analysis. I practiced combining datasets, analyzing time-based data, automating Excel reports, and improving performance and memory usage.

## Tools and Technologies
- Python
- Pandas
- NumPy
- Jupyter Notebook
- OpenPyXL
- XlsxWriter
- VS Code

## Project Structure

```text
Day 6/
├── data/
│   ├── employees.csv
│   ├── departments.csv
│   └── sales.csv
├── Output/
│   ├── 01_multi_table_merging.ipynb
│   ├── 02_time_series_analysis.ipynb
│   ├── 04_excel_automation.ipynb
│   ├── 05_performance_optimization.ipynb
│   ├── employee_report.xlsx
│   ├── formatted_employee_report.xlsx
│   ├── time_series_results.csv
│   ├── large_employees.csv
│   └── optimized_employees.csv
└── README.md
```

*Note: This structure lists the main expected files. Keep only the filenames that actually exist in your repository.*

## 1. Multi-Table Merging

Practiced combining data from multiple CSV files using Pandas.

Topics covered:
- `merge()` to combine related datasets
- Inner, left, right, and outer joins
- Merging tables using common keys
- Merging employee, department, and sales data
- `concat()` to combine datasets
- Saving merged data to CSV

Example:

```python
merged_data = pd.merge(
    employees,
    departments,
    on="DepartmentID",
    how="left"
)
```

## 2. Time Series Analysis

Practiced working with dates and time-based datasets.

Topics covered:
- Converting columns using `pd.to_datetime()`
- Setting a DatetimeIndex
- Filtering records by date
- Resampling daily data into weekly or monthly summaries
- Calculating rolling averages
- Using `shift()` to compare previous periods
- Working with time zones
- Visualizing and exporting results

Example:

```python
df["Date"] = pd.to_datetime(df["Date"])
df = df.set_index("Date")

weekly_sales = df["Sales"].resample("W").sum()
```

## 3. Excel Automation

Practiced creating, reading, formatting, and automating Excel reports.

Topics covered:
- Exporting DataFrames to Excel
- Reading Excel worksheets
- Creating multiple worksheets
- Generating department-wise reports
- Applying header formatting
- Adjusting column widths
- Highlighting high salary values
- Using OpenPyXL and XlsxWriter

Example:

```python
with pd.ExcelWriter(
    "employee_report.xlsx",
    engine="openpyxl"
) as writer:
    employees.to_excel(
        writer,
        sheet_name="Employees",
        index=False
    )
    department_summary.to_excel(
        writer,
        sheet_name="Department Summary",
        index=False
    )
```

## 4. Performance Optimization

Practiced techniques to improve data-processing efficiency and reduce memory consumption.

Topics covered:
- Comparing loops with vectorized operations
- Comparing `apply()` with vectorized calculations
- Optimizing data types
- Using categorical data for repeated text values
- Filtering DataFrames efficiently
- Performing groupby aggregations
- Reading large CSV files in chunks
- Measuring execution time and memory usage

Example:

```python
df["Bonus"] = df["Salary"] * 0.10
```

Vectorized calculations are generally more efficient than Python loops for simple numerical operations on large columns.

## 5. Data Analysis and Reporting

Practiced producing useful summaries from raw data.

Examples:
- Employee counts by department
- Average and total salary by department
- High-salary employee filtering
- Weekly sales summaries
- Exporting cleaned and summarized datasets

## Key Learnings

- Combining multiple datasets using joins
- Handling dates and time-based records
- Automating Excel reports with Python
- Improving memory usage with suitable data types
- Using vectorized calculations for better performance
- Processing large CSV files in chunks
- Organizing Python notebooks and output files

## How to Run

1. Install Python.
2. Install the required libraries:

```bash
python -m pip install pandas numpy openpyxl xlsxwriter jupyter
```

3. Open the project folder in VS Code.
4. Open the required notebook from the `Output` folder.
5. Select the correct Python kernel.
6. Run the notebook cells in order.

## Conclusion

This project provided practical experience with advanced Pandas features used in data analysis and data engineering. The exercises demonstrate how to combine datasets, analyze time-based information, automate Excel reporting, and process data more efficiently.

These skills are useful for preparing structured datasets for reporting, analytics, and downstream data pipelines.
