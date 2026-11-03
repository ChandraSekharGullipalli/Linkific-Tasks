# Day 14 – Big Data Processing and Data Quality Framework

## 1. Project Overview

Day 14 focuses on understanding Big Data concepts, learning Apache Spark and PySpark, processing large datasets, and implementing a Data Quality Framework.

Two practical projects were completed using Databricks and PySpark:

1. Big Data Processing with PySpark
2. Data Quality Testing and Validation Framework

The objective was to understand how large datasets can be processed efficiently and how data quality issues can be detected, reported, and corrected.

## 2. Tools and Technologies

- Python
- Apache Spark
- PySpark
- Databricks
- Spark DataFrames
- GitHub
- Jupyter Notebook format (`.ipynb`)

## 3. Big Data Concepts

Big Data refers to extremely large or complex datasets that traditional data-processing systems may struggle to handle efficiently.

### The 3 Vs of Big Data

**Volume**

Volume refers to the amount of data generated and stored. For example, an online shopping platform can generate millions of sales records.

**Velocity**

Velocity refers to the speed at which data is generated, collected, and processed. For example, online payment transactions are generated continuously.

**Variety**

Variety refers to different types of data, such as structured data, semi-structured data, and unstructured data.

### Distributed Storage and Processing

Distributed processing divides a large workload into smaller tasks that can be processed across multiple computing resources.

Apache Spark supports distributed data processing and helps process large datasets efficiently.

## 4. Introduction to Apache Spark

Apache Spark is an open-source distributed data-processing engine.

It supports:
- Large-scale data processing
- Distributed computing
- Data transformation
- Data aggregation
- SQL operations
- Batch and streaming workloads

### SparkSession

SparkSession is the entry point for working with Spark DataFrames and executing Spark operations.

Example:

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Day14_Big_Data_Processing")
    .getOrCreate()
)

print("Spark session created successfully!")
print("Spark version:", spark.version)
```

## 5. Project 1 – Big Data Processing with PySpark

### Objective

To generate and process a large sales dataset using PySpark DataFrames and understand common big data operations.

### Dataset Details

A synthetic sales dataset containing 1,000,000 records was generated.

**Dataset columns:**

| Column | Description |
|---|---|
| sales_id | Unique sales record identifier |
| customer_id | Customer identifier |
| category | Product category |
| region | Sales region |
| sales_amount | Transaction amount |
| status | Sales transaction status |

### Tasks Completed

1. Created a SparkSession.
2. Generated a dataset containing 1 million records.
3. Inspected the dataset structure and records.
4. Filtered completed sales.
5. Identified high-value sales.
6. Performed category-wise sales aggregation.
7. Performed region-wise sales analysis.
8. Applied window functions and ranking.
9. Explored Spark execution plans.
10. Examined data partitioning and performance.

### Important PySpark Operations

**Filtering**

Used `filter()` to select records based on conditions.

**Selecting Columns**

Used `select()` to retrieve required columns.

**Grouping and Aggregation**

Used `groupBy()` with functions such as `count()`, `sum()`, `avg()`, `min()`, and `max()`.

**Window Functions**

Used `Window`, `dense_rank()`, and partitioning to rank sales records within each region.

**Performance Analysis**

Used `explain()` to inspect Spark execution plans and `repartition()` to explore data partitioning.

### Processing Results

- Total input records: 1,000,000
- Completed sales: 900,000
- High-value completed sales: 450,000
- Product categories: 5
- Sales regions: 4
- Partitions examined in the performance exercise: 8

## 6. Project 2 – Data Quality Testing and Validation Framework

### Objective

To develop a data quality framework that identifies incorrect, missing, duplicate, and invalid records in a dataset.

A synthetic dataset was generated with 1,000,000 original records. Eight additional test records were added to introduce intentional data quality issues.

Total records after adding test data: 1,000,008.

### Data Quality Dimensions

**1. Completeness**

Checks whether required fields contain missing or null values.

**2. Uniqueness**

Checks whether records contain duplicate identifiers.

**3. Validity**

Checks whether values follow defined rules and acceptable ranges.

**4. Consistency**

Checks whether categories, regions, and statuses contain approved values.

**5. Integrity**

Checks whether important identifiers, such as customer IDs, are valid.

### Validation Rules Implemented

- Missing customer ID validation
- Missing sales amount validation
- Duplicate sales ID validation
- Negative and invalid sales amount validation
- Allowed category validation
- Allowed region validation
- Allowed status validation
- Customer ID integrity validation

### Validation Examples

The following PySpark techniques were used:

**Null validation**

```python
df.filter(
    F.col("customer_id").isNull()
)
```

**Duplicate validation**

```python
df.groupBy("sales_id") \
  .count() \
  .filter(F.col("count") > 1)
```

**Range validation**

```python
df.filter(
    F.col("sales_amount").isNull() |
    (F.col("sales_amount") <= 0)
)
```

**Allowed values validation**

```python
df.filter(
    ~F.col("category").isin(
        ["Electronics", "Clothing", "Furniture",
         "Groceries", "Sports"]
    )
)
```

**Assertion-based validation**

Python `assert` statements were used to verify that the cleaned dataset satisfied the defined quality rules.

### Validation Report

The following results were obtained from the original dataset containing intentional errors:

| Validation Rule | Failed Records |
|---|---:|
| Missing Customer IDs | 1 |
| Missing Sales Amounts | 1 |
| Duplicate Sales IDs | 1 |
| Invalid Sales Amounts | 2 |
| Invalid Categories | 1 |
| Invalid Regions | 1 |
| Invalid Statuses | 1 |

Note: A record may violate more than one validation rule, so the failure counts should not be added to calculate unique invalid records.

## 7. Data Cleaning Results

After identifying invalid records, a cleaned dataset was created by removing records that violated the combined validation conditions.

| Metric | Record Count |
|---|---:|
| Original records | 1,000,008 |
| Invalid records | 7 |
| Cleaned records | 1,000,001 |

The cleaned dataset retained the original 1 million valid records and one additional valid test record.

All final data quality assertions passed.

## 8. Learning Outcomes

Through these projects, I learned:

- Fundamentals of Big Data and its 3 Vs.
- How distributed processing works.
- How to create and use a SparkSession.
- How to generate and process large datasets using PySpark.
- How to filter, select, group, and aggregate data.
- How to use window functions and ranking.
- How to inspect Spark execution plans.
- How to identify missing and duplicate records.
- How to implement data validation rules.
- How to generate validation reports.
- How to clean datasets and verify the results using assertions.

## 9. Project Files

The Day 14 folder contains the following project deliverables:

```text
Day 14/
│
├── Day14_Big_Data_Processing.ipynb
├── Day14_Big_Data_Processing.py
├── Day14_Data_Quality_Framework.ipynb
├── Day14_Data_Quality_Framework.py
└── README.md
```

The Python source files are optional exports of the Databricks notebooks.

## 10. Conclusion

Day 14 provided practical experience in big data processing and data quality engineering.

I used Apache Spark and PySpark to process a dataset containing one million records, perform transformations and aggregations, and explore distributed processing concepts.

I also developed a data quality framework to identify missing values, duplicate records, invalid amounts, and inconsistent values. After applying validation rules, I created a cleaned dataset and verified its quality using Python assertions.

These exercises helped me understand how data engineers process large datasets and maintain data accuracy and reliability in data pipelines.
