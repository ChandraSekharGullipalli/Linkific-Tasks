# Power BI – Time Intelligence DAX Library

## 1. Project Overview

This project demonstrates how to use DAX (Data Analysis Expressions) Time Intelligence functions in Power BI to analyze sales performance across different time periods.

Time Intelligence helps businesses compare sales data by day, month, quarter, and year. It provides insights into sales growth, previous-period performance, and cumulative revenue.

## 2. Project Objectives

- Understand DAX Time Intelligence functions.
- Calculate Year-to-Date (YTD) sales.
- Calculate Month-to-Date (MTD) sales.
- Calculate Quarter-to-Date (QTD) sales.
- Compare current-year and previous-year sales.
- Calculate Year-over-Year (YoY) growth.
- Calculate previous-month and previous-quarter sales.
- Create running totals.
- Build interactive Power BI dashboards.

## 3. Data Model

The project uses four tables:

| Table | Description |
|---|---|
| Customer | Contains customer information |
| Product | Contains product information |
| Sales | Contains sales transactions and sales amounts |
| Calendar | Contains dates, years, months, and quarters |

### Relationships

The data model follows a star schema.

- Customer[CustomerID] → Sales[CustomerID]
- Product[ProductID] → Sales[ProductID]
- Calendar[Date] → Sales[OrderDate]

The dimension tables have one-to-many relationships with the Sales fact table.

## 4. DAX Measures Library

### 4.1 Total Sales

```dax
Total Sales =
SUM(Sales[SalesAmount])
```

Calculates the total sales revenue.

### 4.2 Previous Year Sales

```dax
Sales Previous Year =
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR('Calendar'[Date])
)
```

Calculates sales for the equivalent period in the previous year.

### 4.3 Year-to-Date Sales (YTD)

```dax
YTD Sales =
TOTALYTD(
    [Total Sales],
    'Calendar'[Date]
)
```

Calculates sales from the beginning of the year to the selected date.

### 4.4 Month-to-Date Sales (MTD)

```dax
MTD Sales =
TOTALMTD(
    [Total Sales],
    'Calendar'[Date]
)
```

Calculates sales from the beginning of the month to the selected date.

### 4.5 Quarter-to-Date Sales (QTD)

```dax
QTD Sales =
TOTALQTD(
    [Total Sales],
    'Calendar'[Date]
)
```

Calculates sales from the beginning of the quarter.

### 4.6 Year-over-Year Growth

```dax
YoY Growth =
[Total Sales] - [Sales Previous Year]
```

Calculates the difference between current-period sales and previous-year sales.

### 4.7 Year-over-Year Growth Percentage

```dax
YoY Growth % =
DIVIDE(
    [YoY Growth],
    [Sales Previous Year],
    0
)
```

Calculates the percentage change in sales compared with the previous year.

Format this measure as Percentage.

### 4.8 Previous Month Sales

```dax
Previous Month Sales =
CALCULATE(
    [Total Sales],
    PREVIOUSMONTH('Calendar'[Date])
)
```

Calculates sales for the previous month.

### 4.9 Previous Quarter Sales

```dax
Previous Quarter Sales =
CALCULATE(
    [Total Sales],
    PREVIOUSQUARTER('Calendar'[Date])
)
```

Calculates sales for the previous quarter.

### 4.10 Running Total Sales

```dax
Running Total =
CALCULATE(
    [Total Sales],
    FILTER(
        ALLSELECTED('Calendar'[Date]),
        'Calendar'[Date] <= MAX('Calendar'[Date])
    )
)
```

Calculates cumulative sales over the selected date range.

## 5. Important DAX Functions

| Function | Purpose |
|---|---|
| SUM() | Calculates total sales |
| CALCULATE() | Changes filter context |
| SAMEPERIODLASTYEAR() | Returns the same period from last year |
| TOTALYTD() | Calculates year-to-date values |
| TOTALMTD() | Calculates month-to-date values |
| TOTALQTD() | Calculates quarter-to-date values |
| PREVIOUSMONTH() | Returns the previous month |
| PREVIOUSQUARTER() | Returns the previous quarter |
| DIVIDE() | Performs safe division |
| FILTER() | Applies filter conditions |
| ALLSELECTED() | Retains external selections while removing specified filters |

## 6. Dashboard Visualizations

The following Power BI visuals can be used:

1. Card Visual – Total Sales, YTD Sales, and MTD Sales.
2. Line Chart – Monthly sales trends.
3. Clustered Column Chart – Current-year versus previous-year sales.
4. Matrix Visual – Monthly sales comparison and YoY growth.
5. Slicer – Filter sales by year, month, customer, and product.

## 7. Calendar Table Requirements

A proper Calendar table is essential for Time Intelligence calculations.

The Calendar table should contain:

- Date
- Year
- Month
- Month Number
- Quarter

Requirements:

- Dates must be continuous.
- The Date column must contain unique dates.
- Mark the Calendar table as a date table.
- Create an active relationship between Calendar[Date] and Sales[OrderDate].

## 8. Common Issues and Troubleshooting

### Same values appearing in all periods

Possible causes:

- Incorrect or inactive relationships.
- Using Sales[OrderDate] instead of Calendar[Date] in date-based visuals.
- Incorrect date data types.
- Missing or incomplete Calendar dates.
- Missing previous-year sales data.

### Previous Year Sales showing blank

Possible causes:

- No sales data in the previous year.
- Calendar table does not cover the previous year.
- Incorrect relationship between the Calendar and Sales tables.

### YTD, MTD, and QTD showing unexpected values

Check the date filters, date relationship, Calendar table, and visual configuration.

## 9. Learning Outcomes

Through this project, I practised:

- Creating DAX measures.
- Understanding filter context.
- Working with Calendar tables.
- Implementing Time Intelligence calculations.
- Comparing sales across different periods.
- Building interactive Power BI reports.
- Troubleshooting data model relationships.

## 10. Conclusion

This project helped me understand how Power BI Time Intelligence functions are used to analyze business performance over time.

I learned how to calculate cumulative sales, compare current and previous periods, measure growth, and create time-based business reports using DAX.

**Tools Used:** Microsoft Power BI Desktop, DAX, Data Modeling, and Power BI Visualizations.