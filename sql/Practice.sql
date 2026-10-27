
-- E-COMMERCE PRACTICE DATA
-- Run only when you want to reset the sample data.

TRUNCATE TABLE payments, order_items, orders,
    products, customers RESTART IDENTITY CASCADE;

-- 1. CUSTOMERS: 10 records
INSERT INTO customers (customer_name, email, city) VALUES
('Ravi Kumar', 'ravi@example.com', 'Hyderabad'),
('Priya Sharma', 'priya@example.com', 'Bengaluru'),
('Arjun Reddy', 'arjun@example.com', 'Chennai'),
('Sneha Patel', 'sneha@example.com', 'Mumbai'),
('Kiran Rao', 'kiran@example.com', 'Hyderabad'),
('Ananya Das', 'ananya@example.com', 'Kolkata'),
('Vikram Singh', 'vikram@example.com', 'Delhi'),
('Meera Nair', 'meera@example.com', 'Kochi'),
('Rahul Verma', 'rahul@example.com', 'Pune'),
('Divya Iyer', 'divya@example.com', 'Chennai');

-- 2. PRODUCTS: 12 records
INSERT INTO products
(product_name, category, price, stock) VALUES
('Laptop', 'Electronics', 55000, 10),
('Headphones', 'Electronics', 2000, 25),
('Office Chair', 'Furniture', 7500, 8),
('Keyboard', 'Electronics', 1500, 30),
('Mouse', 'Electronics', 800, 50),
('Desk', 'Furniture', 12000, 5),
('Smartphone', 'Electronics', 30000, 15),
('Notebook', 'Stationery', 100, 200),
('Pen Pack', 'Stationery', 250, 100),
('Monitor', 'Electronics', 18000, 12),
('Bookshelf', 'Furniture', 6500, 7),
('Webcam', 'Electronics', 3500, 20);

-- 3. ORDERS: 15 records
INSERT INTO orders (customer_id, order_date, status) VALUES
(1, '2026-10-01', 'Delivered'),
(2, '2026-10-02', 'Delivered'),
(3, '2026-10-03', 'Shipped'),
(1, '2026-10-05', 'Delivered'),
(4, '2026-10-06', 'Pending'),
(5, '2026-10-07', 'Delivered'),
(6, '2026-10-08', 'Cancelled'),
(7, '2026-10-10', 'Shipped'),
(2, '2026-10-12', 'Delivered'),
(8, '2026-10-13', 'Pending'),
(9, '2026-10-15', 'Delivered'),
(3, '2026-10-17', 'Shipped'),
(10, '2026-10-19', 'Delivered'),
(4, '2026-10-21', 'Pending'),
(5, '2026-10-24', 'Delivered');

-- 4. ORDER ITEMS: 22 records
INSERT INTO order_items
(order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 55000),
(1, 2, 2, 2000),
(2, 3, 1, 7500),
(2, 4, 2, 1500),
(3, 7, 1, 30000),
(3, 5, 1, 800),
(4, 10, 1, 18000),
(4, 12, 2, 3500),
(5, 6, 1, 12000),
(6, 8, 10, 100),
(6, 9, 2, 250),
(7, 2, 1, 2000),
(8, 11, 1, 6500),
(8, 4, 1, 1500),
(9, 7, 1, 30000),
(9, 2, 1, 2000),
(10, 3, 2, 7500),
(11, 1, 1, 55000),
(12, 10, 2, 18000),
(13, 5, 3, 800),
(14, 12, 1, 3500),
(15, 6, 1, 12000);

-- 5. PAYMENTS: 15 records
INSERT INTO payments
(order_id, amount, payment_method, payment_status) VALUES
(1, 59000, 'Card', 'Paid'),
(2, 10500, 'UPI', 'Paid'),
(3, 30800, 'Card', 'Paid'),
(4, 25000, 'UPI', 'Paid'),
(5, 12000, 'Card', 'Pending'),
(6, 1500, 'UPI', 'Paid'),
(7, 2000, 'Card', 'Refunded'),
(8, 8000, 'UPI', 'Paid'),
(9, 32000, 'Card', 'Paid'),
(10, 15000, 'UPI', 'Pending'),
(11, 55000, 'Net Banking', 'Paid'),
(12, 36000, 'Card', 'Paid'),
(13, 2400, 'UPI', 'Paid'),
(14, 3500, 'Card', 'Pending'),
(15, 12000, 'UPI', 'Paid');

-- Check how many records each table contains
SELECT 'customers' AS table_name, COUNT(*) AS total
FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'payments', COUNT(*) FROM payments;
