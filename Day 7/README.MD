# Day 7 – Exploratory Data Analysis (EDA)

**Date:** 26 October 2026
**Module:** Exploratory Data Analysis
**Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy, ydata-profiling, Jupyter Notebook

## 1. Project Overview

This project focuses on Exploratory Data Analysis (EDA) using Python. The goal is to understand datasets, identify data-quality issues, calculate statistical summaries, visualize distributions, discover patterns, and extract meaningful insights.

Three datasets are explored:

1. **E-commerce Data:** Analyzing product, sales, price, and quantity information.
2. **Time-Series Data:** Examining changes and patterns over time.
3. **Customer Behavior Data:** Exploring customer characteristics and purchasing behavior.

## 2. Project Structure

```text
Day 7/
├── Project_1_Ecommerce_EDA/
│   └── ecommerce_eda.ipynb
├── Project_2_Timeseries_EDA/
│   └── timeseries_eda.ipynb
├── Project_3_Customer_EDA/
│   └── customer_eda.ipynb
├── outputs/
│   ├── ecommerce_profiling_report.html
│   ├── timeseries_profiling_report.html
│   ├── customer_profiling_report.html
│   └── statistical_analysis_summary.csv
└── README.md
```

*Note: The output files for the time-series and customer reports should be added after you generate them.*

## 3. Exploratory Data Analysis Checklist

### A. Data Inspection

- [x] Load the dataset using Pandas.
- [x] Check the number of rows and columns.
- [x] Inspect the first and last few records.
- [x] Review column names and data types.
- [x] Generate descriptive statistics.

### B. Data Quality and Cleaning

- [x] Identify missing values.
- [x] Check for duplicate records.
- [x] Correct inappropriate data types.
- [x] Clean inconsistent text values.
- [x] Check for invalid or inconsistent values.

### C. Statistical Analysis

- [x] Calculate mean, median, minimum, and maximum.
- [x] Calculate variance and standard deviation.
- [x] Analyze percentiles and quartiles.
- [x] Calculate skewness and kurtosis.
- [x] Examine correlations between numerical columns.
- [x] Perform a suitable hypothesis test where applicable.

### D. Data Visualization

- [x] Create histograms to understand distributions.
- [x] Use boxplots to identify potential outliers.
- [x] Create bar charts for categorical data.
- [x] Use line charts for time-series trends.
- [x] Visualize correlations using a correlation matrix.

### E. Pattern Identification

- [x] Identify increasing and decreasing trends.
- [x] Investigate recurring seasonal patterns where relevant.
- [x] Analyze relationships between variables.
- [x] Detect potential anomalies.
- [x] Group customers based on available behavioral data.

### F. Automated Data Profiling

- [x] Install the `ydata-profiling` package.
- [x] Generate the E-commerce profiling report.
- [x] Generate the time-series profiling report.
- [x] Generate the customer-behavior profiling report.
- [x] Review report warnings and data-quality observations.

### G. Documentation and Deliverables

- [x] Complete all three EDA notebooks.
- [x] Save relevant charts and statistical summaries.
- [x] Record important findings in each notebook.
- [x] Verify that generated HTML reports open correctly.
- [x] Update the README with completed tasks.
- [x] Commit and push the project to GitHub.

## 4. Example Commands

Install the required libraries:

```bash
python -m pip install pandas numpy matplotlib seaborn scipy ydata-profiling jupyter
```

Import commonly used libraries:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

Inspect a dataset:

```python
print(eda.shape)
display(eda.head())
eda.info()
display(eda.describe())
print(eda.isnull().sum())
print("Duplicate rows:", eda.duplicated().sum())
```

## 5. Expected Learning Outcomes

After completing this project, I should be able to:

- Inspect and clean datasets using Pandas.
- Calculate descriptive and statistical measures.
- Visualize numerical and categorical data.
- Identify trends, correlations, and potential anomalies.
- Understand time-series and customer-behavior patterns.
- Generate automated data-profiling reports.
- Document findings in a clear and organized manner.

## 6. Conclusion

This project provides practical experience with EDA using Python. It combines data inspection, data cleaning, statistical analysis, visualization, pattern identification, and automated profiling. These techniques help prepare reliable datasets and support informed decisions in data analytics and data engineering workflows.
