# PostgreSQL E-Commerce Database – SQL Reference

## 1. Project Overview

This project focuses on practicing SQL queries using PostgreSQL. I created an e-commerce database to understand how to store, retrieve, filter, analyze, and manage data using SQL.

The database contains customer details, product information, orders, order items, and payment records.

## 2. Technologies Used

- **Database:** PostgreSQL
- **SQL Tool:** pgAdmin 4
- **Language:** SQL

## 3. Database Structure

Database name: `ecommerce_db`

| Table Name | Description |
|---|---|
| `customers` | Stores customer details |
| `products` | Stores product names, prices, categories, and stock |
| `orders` | Stores customer order details |
| `order_items` | Stores products and quantities in each order |
| `payments` | Stores payment amounts and statuses |

## 4. SQL Concepts Practiced

### Basic Queries

Retrieve all customer records:

```sql
SELECT * FROM customers;
```

Retrieve selected columns:

```sql
SELECT product_name, price
FROM products;
```

### Filtering and Sorting

Find products costing more than 5,000:

```sql
SELECT product_name, price
FROM products
WHERE price > 5000
ORDER BY price DESC;
```

Find customers from a specific city:

```sql
SELECT *
FROM customers
WHERE city = 'Hyderabad';
```

### Aggregate Functions

Count the total number of customers:

```sql
SELECT COUNT(*) AS total_customers
FROM customers;
```

Find the average product price:

```sql
SELECT AVG(price) AS average_price
FROM products;
```

Find the highest product price:

```sql
SELECT MAX(price) AS highest_price
FROM products;
```

### GROUP BY and HAVING

Count products in each category:

```sql
SELECT category, COUNT(*) AS total_products
FROM products
GROUP BY category;
```

Find categories with more than one product:

```sql
SELECT category, COUNT(*) AS total_products
FROM products
GROUP BY category
HAVING COUNT(*) > 1;
```

### Joins

Display orders along with customer names:

```sql
SELECT
    o.order_id,
    c.customer_name,
    o.order_date,
    o.status
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id;
```

Display order items with product names:

```sql
SELECT
    oi.order_id,
    p.product_name,
    oi.quantity,
    oi.unit_price
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id;
```

### Subqueries

Find products priced above the average product price:

```sql
SELECT product_name, price
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
);
```

### Common Table Expressions (CTEs)

Calculate the total value of each order's items:

```sql
WITH order_totals AS (
    SELECT
        order_id,
        SUM(quantity * unit_price) AS total_amount
    FROM order_items
    GROUP BY order_id
)
SELECT *
FROM order_totals
ORDER BY total_amount DESC;
```

### Window Functions

Rank products by price:

```sql
SELECT
    product_name,
    price,
    RANK() OVER (ORDER BY price DESC) AS price_rank
FROM products;
```

Number each customer's orders from newest to oldest:

```sql
SELECT
    customer_id,
    order_id,
    order_date,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY order_date DESC
    ) AS order_number
FROM orders;
```

## 5. Data Modification

Insert a new customer:

```sql
INSERT INTO customers (customer_name, email, city)
VALUES ('Sample Customer', 'sample.customer@example.com', 'Hyderabad');
```

Update a customer's city:

```sql
UPDATE customers
SET city = 'Bengaluru'
WHERE customer_id = 1;
```

Delete a test customer only when it is safe to do so:

```sql
DELETE FROM customers
WHERE email = 'sample.customer@example.com';
```

## 6. How to Execute Queries

1. Open pgAdmin 4.
2. Expand **Servers → PostgreSQL → Databases**.
3. Select `ecommerce_db`.
4. Right-click the database and choose **Query Tool**.
5. Write or paste a SQL query.
6. Select the query and click **Execute** or press **F5**.
7. Check the output in the **Data Output** panel.
8. Save your SQL file as `practice_queries.sql`.

## 7. Learning Outcomes

- Understood relational database tables and relationships.
- Practiced retrieving and filtering data using `SELECT`, `WHERE`, and `ORDER BY`.
- Used aggregate functions such as `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX`.
- Practiced `GROUP BY` and `HAVING`.
- Retrieved related information using joins.
- Learned subqueries, CTEs, and window functions.
- Practiced basic data modification using `INSERT`, `UPDATE`, and `DELETE`.

## 8. Project Conclusion

This project helped me improve my practical SQL skills using PostgreSQL. I practiced querying related tables, analyzing e-commerce data, and writing queries that can be useful in data analysis and data engineering tasks.
