# Day 11 – Data Warehouse Modeling Guide

## 1. Introduction

This document explains Data Warehouse concepts, dimensional modeling, Star Schema design, Entity Relationship Diagrams (ERD), and Slowly Changing Dimensions (SCD).

The objective is to understand how data is organized, stored, and managed for analytical processing and business intelligence.

## 2. Data Warehouse Concepts

A Data Warehouse is a centralized repository that stores integrated historical data from multiple sources. It is mainly used for reporting, analysis, and decision-making.

### OLTP vs OLAP

| OLTP | OLAP |
|---|---|
| Online Transaction Processing | Online Analytical Processing |
| Handles daily transactions | Handles analytical queries |
| Frequently inserts and updates data | Frequently reads and aggregates data |
| Used in operational systems | Used in reporting systems |

### Data Warehouse vs Database

A database mainly supports operational applications and daily transactions, while a Data Warehouse organizes historical and integrated data for analysis.

### Data Mart

A Data Mart is a smaller, subject-oriented part of a Data Warehouse designed for a specific department or business area.

## 3. Dimensional Modeling

Dimensional Modeling is a data design technique used to organize warehouse data into Fact Tables and Dimension Tables.

### Fact Table

A Fact Table stores measurable business information.

Common characteristics:
- Contains numerical measures.
- Contains foreign keys.
- Supports aggregation and analysis.
- Has a clearly defined grain.

### Dimension Table

A Dimension Table stores descriptive information used to analyze facts.

Common characteristics:
- Contains descriptive attributes.
- Provides context for business measurements.
- Uses primary keys.
- Supports filtering and grouping.

## 4. Types of Dimensional Models

### Star Schema

A Star Schema contains one central Fact Table connected directly to multiple Dimension Tables.

Advantages:
- Simple structure.
- Easy to understand.
- Supports analytical queries.
- Reduces complex joins.

### Snowflake Schema

A Snowflake Schema is an extension of the Star Schema in which Dimension Tables are normalized into related tables.

Advantages:
- Reduces data redundancy.
- Organizes hierarchical attributes.
- Improves dimension data consistency.

### Galaxy Schema

A Galaxy Schema, also called a Fact Constellation Schema, contains multiple Fact Tables that share common Dimension Tables.

Advantages:
- Supports multiple business processes.
- Allows shared dimensions.
- Supports enterprise-level analysis.

## 5. Important Modeling Components

### Grain

Grain defines exactly what one row in a Fact Table represents.

### Measures

Measures are numerical values used for calculations and analysis.

### Surrogate Key

A Surrogate Key is an artificial identifier generated for a dimension record.

### Natural Key

A Natural Key is an identifier originating from a business or source system.

### Conformed Dimension

A Conformed Dimension is a shared dimension that maintains consistent definitions and attributes across multiple Fact Tables.

### Hierarchies

Hierarchies organize dimension attributes into levels for analysis and drill-down operations.

## 6. Slowly Changing Dimensions (SCD)

SCD techniques manage changes in Dimension Table attributes over time.

### SCD Type 1

- Updates existing records.
- Does not maintain historical values.
- Replaces old attribute values with new values.

### SCD Type 2

- Preserves historical records.
- Inserts a new version when an attribute changes.
- Uses effective start dates and end dates.
- Uses a current-record flag.

### SCD Type 3

- Maintains limited historical information.
- Stores previous values in separate columns.
- Allows comparison of current and previous attributes.

## 7. Data Warehouse ERD

An Entity Relationship Diagram represents the structure of a Data Warehouse and shows relationships between tables.

Important elements:
- Entities or tables.
- Attributes or columns.
- Primary Keys.
- Foreign Keys.
- Relationships between tables.

ERDs help understand database structure and plan implementation.

## 8. Sample Data Warehouse Implementation

A sample Sales Data Warehouse was designed using PostgreSQL.

The implementation includes:

- Customer Dimension Table.
- Product Dimension Table.
- Date Dimension Table.
- Sales Fact Table.

Practical activities:
1. Created dimension tables.
2. Created a fact table.
3. Defined primary and foreign keys.
4. Inserted sample records.
5. Retrieved data using SQL JOIN operations.
6. Calculated total sales.
7. Analyzed sales by product category and customer city.

## 9. Tools and Technologies

- PostgreSQL
- SQL
- pgAdmin
- Visual Studio Code
- Markdown

## 10. Learning Outcomes

After completing this task, I gained knowledge of:

- Data Warehouse architecture.
- OLTP and OLAP concepts.
- Fact and Dimension Tables.
- Star, Snowflake, and Galaxy Schemas.
- Primary Keys and Foreign Keys.
- Surrogate and Natural Keys.
- Slowly Changing Dimensions Type 1, 2, and 3.
- Data Warehouse ERD design.
- SQL-based warehouse implementation and analysis.

## 11. Conclusion

This learning activity provided practical knowledge of Data Warehousing and Dimensional Modeling. I understood how Fact Tables and Dimension Tables organize analytical data, how different schema designs work, and how SCD techniques preserve historical information.

I also practiced creating a sample Data Warehouse using PostgreSQL, inserting data, establishing relationships, and performing analytical SQL queries.