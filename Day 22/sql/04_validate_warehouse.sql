
-- DAY 22: DATA WAREHOUSE VALIDATION
-- Source: public schema
-- Target: warehouse schema

-- ==========================================
-- 1. SOURCE VS WAREHOUSE RECORD COUNTS
-- ==========================================

SELECT 'Customers' AS data_table,
       (SELECT COUNT(*) FROM public.customers) AS source_count,
       (SELECT COUNT(*) FROM warehouse.dim_customer
        WHERE is_current = TRUE) AS warehouse_count

UNION ALL

SELECT 'Products',
       (SELECT COUNT(*) FROM public.products),
       (SELECT COUNT(*) FROM warehouse.dim_product
        WHERE is_current = TRUE)

UNION ALL

SELECT 'Sales',
       (SELECT COUNT(*) FROM public.order_items),
       (SELECT COUNT(*) FROM warehouse.fact_sales)

UNION ALL

SELECT 'Transactions',
       (SELECT COUNT(*) FROM public.transactions),
       (SELECT COUNT(*) FROM warehouse.fact_transactions);


-- ==========================================
-- 2. DUPLICATE RECORD VALIDATION
-- ==========================================

SELECT 'Duplicate customers' AS validation,
       COUNT(*) AS duplicate_count
FROM (
    SELECT customer_id
    FROM warehouse.dim_customer
    WHERE is_current = TRUE
    GROUP BY customer_id
    HAVING COUNT(*) > 1
) duplicates

UNION ALL

SELECT 'Duplicate products',
       COUNT(*)
FROM (
    SELECT product_id
    FROM warehouse.dim_product
    WHERE is_current = TRUE
    GROUP BY product_id
    HAVING COUNT(*) > 1
) duplicates

UNION ALL

SELECT 'Duplicate sales',
       COUNT(*)
FROM (
    SELECT order_item_id
    FROM warehouse.fact_sales
    GROUP BY order_item_id
    HAVING COUNT(*) > 1
) duplicates

UNION ALL

SELECT 'Duplicate transactions',
       COUNT(*)
FROM (
    SELECT transaction_id
    FROM warehouse.fact_transactions
    GROUP BY transaction_id
    HAVING COUNT(*) > 1
) duplicates;


-- ==========================================
-- 3. SALES REFERENTIAL INTEGRITY
-- ==========================================

SELECT
    COUNT(*) AS total_sales,
    COUNT(dc.customer_key) AS matched_customers,
    COUNT(dp.product_key) AS matched_products,
    COUNT(dd.date_key) AS matched_dates
FROM warehouse.fact_sales fs
LEFT JOIN warehouse.dim_customer dc
    ON fs.customer_key = dc.customer_key
LEFT JOIN warehouse.dim_product dp
    ON fs.product_key = dp.product_key
LEFT JOIN warehouse.dim_date dd
    ON fs.date_key = dd.date_key;


-- ==========================================
-- 4. TRANSACTION REFERENTIAL INTEGRITY
-- ==========================================

SELECT
    COUNT(*) AS total_transactions,
    COUNT(dc.customer_key) AS matched_customers,
    COUNT(dd.date_key) AS matched_dates,
    COUNT(pm.payment_method_key) AS matched_payment_methods
FROM warehouse.fact_transactions ft
LEFT JOIN warehouse.dim_customer dc
    ON ft.customer_key = dc.customer_key
LEFT JOIN warehouse.dim_date dd
    ON ft.date_key = dd.date_key
LEFT JOIN warehouse.dim_payment_method pm
    ON ft.payment_method_key = pm.payment_method_key;


-- ==========================================
-- 5. NULL VALUE VALIDATION
-- ==========================================

SELECT
    COUNT(*) FILTER (WHERE customer_key IS NULL)
        AS missing_customer_keys,
    COUNT(*) FILTER (WHERE product_key IS NULL)
        AS missing_product_keys,
    COUNT(*) FILTER (WHERE date_key IS NULL)
        AS missing_date_keys,
    COUNT(*) FILTER (WHERE quantity IS NULL)
        AS missing_quantities,
    COUNT(*) FILTER (WHERE line_total IS NULL)
        AS missing_sales_amounts
FROM warehouse.fact_sales;


SELECT
    COUNT(*) FILTER (WHERE customer_key IS NULL)
        AS missing_customer_keys,
    COUNT(*) FILTER (WHERE date_key IS NULL)
        AS missing_date_keys,
    COUNT(*) FILTER (WHERE payment_method_key IS NULL)
        AS missing_payment_keys,
    COUNT(*) FILTER (WHERE amount IS NULL)
        AS missing_transaction_amounts
FROM warehouse.fact_transactions;


-- ==========================================
-- 6. INVALID VALUE VALIDATION
-- ==========================================

SELECT COUNT(*) AS invalid_sales_records
FROM warehouse.fact_sales
WHERE quantity <= 0
   OR unit_price < 0
   OR line_total < 0;

SELECT COUNT(*) AS invalid_transaction_records
FROM warehouse.fact_transactions
WHERE amount < 0;


-- ==========================================
-- 7. SALES TOTAL VALIDATION
-- ==========================================

SELECT
    (SELECT ROUND(COALESCE(SUM(line_total), 0), 2)
     FROM public.order_items) AS source_sales_total,

    (SELECT ROUND(COALESCE(SUM(line_total), 0), 2)
     FROM warehouse.fact_sales) AS warehouse_sales_total;


-- ==========================================
-- 8. TRANSACTION TOTAL VALIDATION
-- ==========================================

SELECT
    (SELECT ROUND(COALESCE(SUM(amount), 0), 2)
     FROM public.transactions) AS source_transaction_total,

    (SELECT ROUND(COALESCE(SUM(amount), 0), 2)
     FROM warehouse.fact_transactions) AS warehouse_transaction_total;

