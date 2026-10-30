
-- DAY 11: SAMPLE DATA WAREHOUSE WITH DATA

-- STEP 1: Create Customer Dimension

CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(20),
    customer_name VARCHAR(100),
    city VARCHAR(50)
);

-- STEP 2: Create Product Dimension

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(10,2)
);

-- STEP 3: Create Date Dimension

CREATE TABLE dim_date (
    date_key SERIAL PRIMARY KEY,
    full_date DATE,
    month VARCHAR(20),
    year INT
);

-- STEP 4: Create Sales Fact Table

CREATE TABLE fact_sales (
    sales_key SERIAL PRIMARY KEY,
    customer_key INT REFERENCES dim_customer(customer_key),
    product_key INT REFERENCES dim_product(product_key),
    date_key INT REFERENCES dim_date(date_key),
    quantity INT,
    sales_amount NUMERIC(10,2)
);

-- STEP 5: Insert Customer Data

INSERT INTO dim_customer
(customer_id, customer_name, city)
VALUES
('C101', 'Rahul', 'Hyderabad'),
('C102', 'Priya', 'Bengaluru'),
('C103', 'Arun', 'Chennai'),
('C104', 'Sneha', 'Pune'),
('C105', 'Kiran', 'Mumbai');

-- STEP 6: Insert Product Data

INSERT INTO dim_product
(product_name, category, price)
VALUES
('Laptop', 'Electronics', 55000),
('Mobile', 'Electronics', 25000),
('Keyboard', 'Accessories', 1500),
('Mouse', 'Accessories', 800),
('Monitor', 'Electronics', 12000);

-- STEP 7: Insert Date Data

INSERT INTO dim_date
(full_date, month, year)
VALUES
('2026-10-01', 'October', 2026),
('2026-10-02', 'October', 2026),
('2026-10-03', 'October', 2026),
('2026-10-04', 'October', 2026),
('2026-10-05', 'October', 2026);

-- STEP 8: Insert Sales Fact Data

INSERT INTO fact_sales
(customer_key, product_key, date_key, quantity, sales_amount)
VALUES
(1, 1, 1, 1, 55000),
(2, 2, 2, 2, 50000),
(3, 3, 3, 3, 4500),
(4, 4, 4, 2, 1600),
(5, 5, 5, 1, 12000);

-- STEP 9: Display Customer Data

SELECT * FROM dim_customer;

-- STEP 10: Display Product Data

SELECT * FROM dim_product;

-- STEP 11: Display Date Data

SELECT * FROM dim_date;

-- STEP 12: Display Sales Data

SELECT * FROM fact_sales;

-- STEP 13: Join All Warehouse Tables

SELECT
    fs.sales_key,
    dc.customer_name,
    dc.city,
    dp.product_name,
    dp.category,
    dd.full_date,
    fs.quantity,
    fs.sales_amount
FROM fact_sales fs
JOIN dim_customer dc
    ON fs.customer_key = dc.customer_key
JOIN dim_product dp
    ON fs.product_key = dp.product_key
JOIN dim_date dd
    ON fs.date_key = dd.date_key
ORDER BY fs.sales_key;

-- STEP 14: Calculate Total Sales

SELECT SUM(sales_amount) AS total_sales
FROM fact_sales;

-- STEP 15: Sales by Product Category

SELECT
    dp.category,
    SUM(fs.sales_amount) AS category_sales
FROM fact_sales fs
JOIN dim_product dp
    ON fs.product_key = dp.product_key
GROUP BY dp.category
ORDER BY category_sales DESC;

-- STEP 16: Sales by Customer City

SELECT
    dc.city,
    SUM(fs.sales_amount) AS total_sales
FROM fact_sales fs
JOIN dim_customer dc
    ON fs.customer_key = dc.customer_key
GROUP BY dc.city
ORDER BY total_sales DESC;