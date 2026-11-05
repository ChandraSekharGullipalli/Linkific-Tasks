# Day 16 – Power BI: Complete Learning Guide

## 1. Project Overview

This project focuses on learning Microsoft Power BI Desktop and developing interactive dashboards using multiple data sources.

The objective is to understand data connections, data transformation, data modeling, DAX calculations, and data visualization.

## 2. Learning Objectives

- Install and configure Power BI Desktop.
- Connect multiple data sources.
- Import Excel and CSV files.
- Connect to PostgreSQL databases.
- Understand Power Query transformations.
- Create data models and relationships.
- Learn basic DAX calculations.
- Build interactive dashboards and reports.

## 3. Tools and Technologies

| Tool | Purpose |
|---|---|
| Power BI Desktop | Data visualization and reporting |
| Microsoft Excel | Spreadsheet data source |
| CSV | Structured data source |
| PostgreSQL | Relational database |
| Power Query | Data cleaning and transformation |
| DAX | Data analysis calculations |

## 4. Power BI Desktop Setup

Power BI Desktop was successfully installed on Windows.

The following interface components were explored:

- Report View – Create visual reports and dashboards.
- Data View – Inspect imported tables and records.
- Model View – Manage relationships between tables.

Power BI Desktop allows users to develop and save reports locally in `.pbix` format.

## 5. Data Source Connections

The following data connections were practiced:

### Excel Connection
- Imported employee information from an Excel workbook.
- Selected the required worksheet.
- Loaded employee records into Power BI.

### CSV Connection
- Created an employee CSV dataset.
- Connected the CSV file using Text/CSV.
- Checked the imported columns and records.

### PostgreSQL Connection
- Connected Power BI Desktop to a PostgreSQL database.
- Configured database connection details.
- Established a successful database connection.

### Additional Sources for Further Practice
- Microsoft SQL Server.
- Web data sources.
- REST API connections.

## 6. Power Query Transformation

Power Query is used to clean and prepare data before loading it into the Power BI data model.

Topics covered in the learning plan:

- Removing unnecessary columns.
- Filtering rows.
- Changing data types.
- Splitting columns.
- Merging columns.
- Appending queries.
- Merging queries.

### Append Queries

Excel and CSV employee datasets were combined using Append Queries as New.

The resulting table was named:

`all_employees`

The combined dataset contains 10 employee records.

## 7. Data Modeling

Data modeling helps establish relationships between different tables.

Important concepts:

- One-to-One (1:1).
- One-to-Many (1:*).
- Many-to-Many (*:*).
- Fact tables and dimension tables.
- Star schema.
- Cardinality settings.
- Cross-filter direction.

Relationships should be created using matching key columns with appropriate data types and unique values on the one side.

## 8. DAX Calculations

DAX stands for Data Analysis Expressions.

It is used to create measures and calculated columns for data analysis.

The following measures were prepared for the `all_employees` table.

### Total Employees

```dax
Total Employees =
COUNTROWS('all_employees')
```

### Total Salary

```dax
Total Salary =
SUM('all_employees'[Salary])
```

### Average Salary

```dax
Average Salary =
AVERAGE('all_employees'[Salary])
```

### Total Departments

```dax
Total Departments =
DISTINCTCOUNT('all_employees'[Department])
```

### IT Employees

```dax
IT Employees =
CALCULATE(
    COUNTROWS('all_employees'),
    'all_employees'[Department] = "IT"
)
```

## 9. Interactive Dashboard Development

An Employee Analytics Dashboard was planned using the combined employee dataset.

The dashboard includes:

- Total Employees KPI.
- Total Salary KPI.
- Average Salary KPI.
- Total Departments KPI.
- Employee Count by Department.
- Employee Count by City.
- Salary by Department.
- Department Slicer.
- City Slicer.

### Dashboard Interactivity

Slicers allow users to filter employee information by department and city.

The KPI cards and charts respond to the selected filters.

## 10. Expected Dataset Validation

Based on the sample Excel and CSV records:

| Metric | Expected Result |
|---|---:|
| Total Employees | 10 |
| Total Salary | 377,000 |
| Average Salary | 37,700 |
| Total Departments | 4 |
| IT Employees | 4 |

These are expected values from the sample datasets and should be checked against the loaded data.

## 11. Project Folder Structure

```text
Day 16
└── Power-BI
    ├── 01_Setup
    ├── 02_Data_Sources
    │   ├── Excel
    │   ├── CSV
    │   └── PostgreSQL
    ├── 03_Data_Model
    ├── 04_Interactive_Dashboard
    │   └── Employee_Analytics_Dashboard.pbix
    └── README.md
```

## 12. Skills Gained

- Power BI Desktop installation and configuration.
- Data source connectivity.
- Excel and CSV data importing.
- PostgreSQL connectivity.
- Power Query fundamentals.
- Data modeling concepts.
- DAX measure creation.
- KPI development.
- Interactive data visualization.

## 13. Conclusion

Through this learning activity, I gained practical knowledge of Microsoft Power BI Desktop, data source connectivity, data preparation, DAX calculations, and interactive dashboard development.

This project helped me understand how raw data from different sources can be combined, analyzed, and presented through meaningful visual reports.

**Project:** Linkific Internship – Day 16  
**Technology:** Microsoft Power BI  
**Level:** Beginner / Practical Learning
