-- ============================================
-- DAY 11: SCD TYPE 2 IMPLEMENTATION
-- Customer Historical Data Management
-- ============================================

-- STEP 1: Create Customer Dimension Table

CREATE TABLE IF NOT EXISTS dim_customer_scd2 (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL
);

-- STEP 2: Ensure only one current record per customer

CREATE UNIQUE INDEX IF NOT EXISTS idx_one_current_customer
ON dim_customer_scd2(customer_id)
WHERE is_current = TRUE;


-- STEP 3: Remove previous demo data

DELETE FROM dim_customer_scd2
WHERE customer_id = 'C1001';


-- STEP 4: Insert Original Customer Record

INSERT INTO dim_customer_scd2 (
    customer_id,
    customer_name,
    city,
    effective_start_date,
    effective_end_date,
    is_current
)
VALUES (
    'C1001',
    'Rahul',
    'Hyderabad',
    CURRENT_DATE - 365,
    DATE '9999-12-31',
    TRUE
);


-- STEP 5: Display Original Customer Record

SELECT * 
FROM dim_customer_scd2
WHERE customer_id = 'C1001';


-- STEP 6: Expire the Old Customer Record

UPDATE dim_customer_scd2
SET
    effective_end_date = CURRENT_DATE - 1,
    is_current = FALSE
WHERE customer_id = 'C1001'
AND is_current = TRUE;


-- STEP 7: Insert Updated Customer Record

INSERT INTO dim_customer_scd2 (
    customer_id,
    customer_name,
    city,
    effective_start_date,
    effective_end_date,
    is_current
)
VALUES (
    'C1001',
    'Rahul',
    'Bengaluru',
    CURRENT_DATE,
    DATE '9999-12-31',
    TRUE
);


-- STEP 8: Display Complete Customer History

SELECT
    customer_key,
    customer_id,
    customer_name,
    city,
    effective_start_date,
    effective_end_date,
    is_current
FROM dim_customer_scd2
WHERE customer_id = 'C1001'
ORDER BY effective_start_date;


-- STEP 9: Display Only Current Customer Records

SELECT *
FROM dim_customer_scd2
WHERE is_current = TRUE;


-- STEP 10: Display Historical Customer Records

SELECT *
FROM dim_customer_scd2
WHERE is_current = FALSE;