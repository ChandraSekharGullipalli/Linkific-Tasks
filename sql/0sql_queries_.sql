
-- 1. Customers
CREATE TABLE customers (
    customer_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    city VARCHAR(50)
);

-- 2. Products
CREATE TABLE products (
    product_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

-- 3. Orders
CREATE TABLE orders (
    order_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(30) DEFAULT 'Pending'
);

-- 4. Order Items
CREATE TABLE order_items (
    order_item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id),
    product_id INT NOT NULL REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0)
);

-- 5. Payments
CREATE TABLE payments (
    payment_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id),
    amount NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
    payment_method VARCHAR(30),
    payment_status VARCHAR(30) DEFAULT 'Pending'
);


INSERT INTO customers (customer_name, email, city) VALUES
('Ravi Kumar', 'ravi@example.com', 'Hyderabad'),
('Priya Sharma', 'priya@example.com', 'Bengaluru'),
('Arjun Reddy', 'arjun@example.com', 'Chennai');

INSERT INTO products (product_name, category, price, stock) VALUES
('Laptop', 'Electronics', 55000, 10),
('Headphones', 'Electronics', 2000, 25),
('Office Chair', 'Furniture', 7500, 8),
('Keyboard', 'Electronics', 1500, 30);

INSERT INTO orders (customer_id, order_date, status) VALUES
(1, '2026-10-20', 'Delivered'),
(2, '2026-10-22', 'Pending'),
(1, '2026-10-24', 'Shipped');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 55000),
(1, 2, 2, 2000),
(2, 3, 1, 7500),
(3, 4, 2, 1500);

INSERT INTO payments (order_id, amount, payment_method, payment_status) VALUES
(1, 59000, 'Card', 'Paid'),
(2, 7500, 'UPI', 'Pending'),
(3, 3000, 'UPI', 'Paid');


-- =====================================================
-- E-COMMERCE SQL PROJECT
-- PostgreSQL Practice: 60 Queries
-- Database: ecommerce_db
-- =====================================================

-- SECTION 1: BASIC SELECT QUERIES

-- 1. Display all customers
SELECT * FROM customers;

-- 2. Display all products
SELECT * FROM products;

-- 3. Display all orders
SELECT * FROM orders;

-- 4. Display all payments
SELECT * FROM payments;

-- 5. Display selected customer columns
SELECT customer_name, email FROM customers;

-- 6. Display unique product categories
SELECT DISTINCT category FROM products;

-- 7. Find products costing more than 5000
SELECT * FROM products WHERE price > 5000;

-- 8. Find products costing between 1000 and 10000
SELECT * FROM products
WHERE price BETWEEN 1000 AND 10000;

-- 9. Find customers from Hyderabad
SELECT * FROM customers WHERE city = 'Hyderabad';

-- 10. Find products in Electronics
SELECT * FROM products
WHERE category = 'Electronics';


-- SECTION 2: FILTERING AND SORTING

-- 11. Sort products by price from highest to lowest
SELECT * FROM products ORDER BY price DESC;

-- 12. Sort customers alphabetically
SELECT * FROM customers ORDER BY customer_name ASC;

-- 13. Find products with stock below 15
SELECT * FROM products WHERE stock < 15;

-- 14. Find customers whose names start with P
SELECT * FROM customers
WHERE customer_name LIKE 'P%';

-- 15. Find products whose names contain "o"
SELECT * FROM products
WHERE product_name ILIKE '%o%';

-- 16. Find orders with Pending status
SELECT * FROM orders WHERE status = 'Pending';

-- 17. Find orders placed after October 20, 2026
SELECT * FROM orders
WHERE order_date > DATE '2026-10-20';

-- 18. Display the three most expensive products
SELECT * FROM products
ORDER BY price DESC
LIMIT 3;

-- 19. Find products with stock between 10 and 30
SELECT * FROM products
WHERE stock BETWEEN 10 AND 30;

-- 20. Find customers from selected cities
SELECT * FROM customers
WHERE city IN ('Hyderabad', 'Bengaluru');


-- SECTION 3: AGGREGATE FUNCTIONS

-- 21. Count total customers
SELECT COUNT(*) AS total_customers FROM customers;

-- 22. Count total products
SELECT COUNT(*) AS total_products FROM products;

-- 23. Calculate average product price
SELECT ROUND(AVG(price), 2) AS average_price
FROM products;

-- 24. Find the highest product price
SELECT MAX(price) AS highest_price FROM products;

-- 25. Find the lowest product price
SELECT MIN(price) AS lowest_price FROM products;

-- 26. Calculate total product stock
SELECT SUM(stock) AS total_stock FROM products;

-- 27. Count products in each category
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category;

-- 28. Calculate average price by category
SELECT category, ROUND(AVG(price), 2) AS average_price
FROM products
GROUP BY category;

-- 29. Find categories containing more than two products
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 2;

-- 30. Calculate total quantity sold for each product
SELECT p.product_name, SUM(oi.quantity) AS quantity_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY quantity_sold DESC;


-- SECTION 4: JOINS

-- 31. Display customers and their orders
SELECT c.customer_name, o.order_id, o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- 32. Display order details with product names
SELECT oi.order_id, p.product_name,
       oi.quantity, oi.unit_price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id;

-- 33. Display customers with payment information
SELECT c.customer_name, o.order_id,
       p.amount, p.payment_method, p.payment_status
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN payments p ON o.order_id = p.order_id;

-- 34. Show all customers, including those without orders
SELECT c.customer_name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- 35. Find customers who have not placed orders
SELECT c.customer_id, c.customer_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- 36. Display complete order line details
SELECT o.order_id, c.customer_name,
       p.product_name, oi.quantity,
       oi.unit_price,
       oi.quantity * oi.unit_price AS line_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;

-- 37. Find products that have never been ordered
SELECT p.product_id, p.product_name
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;

-- 38. Display order and payment statuses
SELECT o.order_id, o.status AS order_status,
       p.payment_status
FROM orders o
LEFT JOIN payments p ON o.order_id = p.order_id;

-- 39. Find customers who purchased Electronics
SELECT DISTINCT c.customer_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE p.category = 'Electronics';

-- 40. Calculate revenue by product category
SELECT p.category,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status IN ('Delivered', 'Shipped')
GROUP BY p.category
ORDER BY revenue DESC;


-- SECTION 5: SUBQUERIES AND CTEs

-- 41. Find products priced above the average
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- 42. Find the most expensive product
SELECT product_name, price
FROM products
WHERE price = (SELECT MAX(price) FROM products);

-- 43. Find orders above the average order total
WITH order_totals AS (
    SELECT order_id,
           SUM(quantity * unit_price) AS total
    FROM order_items
    GROUP BY order_id
)
SELECT order_id, total
FROM order_totals
WHERE total > (SELECT AVG(total) FROM order_totals);

-- 44. Calculate total spending per customer
SELECT c.customer_name,
       COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS spending
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY spending DESC;

-- 45. Find customers with at least two orders
SELECT c.customer_name, COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(o.order_id) >= 2;

-- 46. Use a CTE to summarize product stock value
WITH stock_summary AS (
    SELECT product_name, price, stock,
           price * stock AS stock_value
    FROM products
)
SELECT *, SUM(stock_value) OVER () AS total_stock_value
FROM stock_summary;

-- 47. Find orders containing more than one unit in total
SELECT order_id, SUM(quantity) AS total_units
FROM order_items
GROUP BY order_id
HAVING SUM(quantity) > 1;

-- 48. Find products priced above their category average
SELECT product_name, category, price
FROM (
    SELECT product_name, category, price,
           AVG(price) OVER (PARTITION BY category) AS category_avg
    FROM products
) AS product_comparison
WHERE price > category_avg;

-- 49. Find customers who have made a paid payment
SELECT DISTINCT c.customer_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN payments p ON o.order_id = p.order_id
WHERE p.payment_status = 'Paid';

-- 50. Calculate payment totals by payment method
SELECT payment_method, SUM(amount) AS total_amount
FROM payments
GROUP BY payment_method;


-- SECTION 6: ADVANCED SQL AND BUSINESS ANALYSIS

-- 51. Rank products by price
SELECT product_name, price,
       RANK() OVER (ORDER BY price DESC) AS price_rank
FROM products;

-- 52. Number each customer's orders by date
SELECT customer_id, order_id, order_date,
       ROW_NUMBER() OVER (
           PARTITION BY customer_id
           ORDER BY order_date
       ) AS order_number
FROM orders;

-- 53. Calculate running order total by date
WITH daily_orders AS (
    SELECT order_date, SUM(oi.quantity * oi.unit_price) AS total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY order_date
)
SELECT order_date, total,
       SUM(total) OVER (ORDER BY order_date) AS running_total
FROM daily_orders;

-- 54. Compare each product price with the previous price
SELECT product_name, price,
       LAG(price) OVER (ORDER BY price) AS previous_price
FROM products;

-- 55. Calculate each product's percentage of catalog value
SELECT product_name, price,
       ROUND(
           100.0 * price / NULLIF(SUM(price) OVER (), 0), 2
       ) AS percentage_of_total_price
FROM products;

-- 56. Show order totals with customer and status
SELECT c.customer_name, o.order_id, o.status,
       SUM(oi.quantity * oi.unit_price) AS order_total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_name, o.order_id, o.status
ORDER BY order_total DESC;

-- 57. Find orders where payment amount differs from order total
WITH order_totals AS (
    SELECT order_id,
           SUM(quantity * unit_price) AS total
    FROM order_items
    GROUP BY order_id
),
payment_totals AS (
    SELECT order_id, SUM(amount) AS paid_amount
    FROM payments
    GROUP BY order_id
)
SELECT o.order_id, ot.total, pt.paid_amount
FROM orders o
JOIN order_totals ot ON o.order_id = ot.order_id
JOIN payment_totals pt ON o.order_id = pt.order_id
WHERE ot.total <> pt.paid_amount;

-- 58. Count orders by status
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- 59. Estimate the value of current inventory
SELECT SUM(price * stock) AS inventory_value
FROM products;

-- 60. Create a customer order summary
SELECT c.customer_id, c.customer_name,
       COUNT(DISTINCT o.order_id) AS total_orders,
       COALESCE(SUM(oi.quantity * oi.unit_price), 0)
           AS total_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_order_value DESC;

