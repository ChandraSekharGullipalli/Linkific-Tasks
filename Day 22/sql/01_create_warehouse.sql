
-- ============================================================
-- DAY 23: E-COMMERCE DATA WAREHOUSE
-- Existing Database: synthetic_data_db
-- Warehouse Schema: warehouse
-- Architecture: Star Schema
-- ============================================================

BEGIN;

-- 1. CREATE WAREHOUSE SCHEMA
CREATE SCHEMA IF NOT EXISTS warehouse;

-- ============================================================
-- 2. DIMENSION TABLES
-- ============================================================

-- CUSTOMER DIMENSION
-- Supports Slowly Changing Dimension Type 2

CREATE TABLE IF NOT EXISTS warehouse.dim_customer (
    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    customer_name VARCHAR(150),
    email VARCHAR(150),
    phone VARCHAR(50),
    city VARCHAR(100),

    effective_start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    effective_end_date DATE NOT NULL DEFAULT DATE '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_customer_dates
    CHECK (effective_end_date >= effective_start_date)
);

-- PRODUCT DIMENSION
-- Supports Slowly Changing Dimension Type 2

CREATE TABLE IF NOT EXISTS warehouse.dim_product (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INTEGER NOT NULL,
    product_name VARCHAR(150),
    category VARCHAR(100),
    price NUMERIC(12,2),
    effective_start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    effective_end_date DATE NOT NULL DEFAULT DATE '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_product_dates
    CHECK (effective_end_date >= effective_start_date),

    CONSTRAINT chk_product_price
    CHECK (price IS NULL OR price >= 0)
);

-- DATE DIMENSION
-- Date records will be generated in the next task.

CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,

    day_number INTEGER NOT NULL,
    month_number INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter_number INTEGER NOT NULL,
    year_number INTEGER NOT NULL,

    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    week_number INTEGER NOT NULL,

    is_weekend BOOLEAN NOT NULL DEFAULT FALSE,
    is_holiday BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT chk_date_month
    CHECK (month_number BETWEEN 1 AND 12),

    CONSTRAINT chk_date_quarter
    CHECK (quarter_number BETWEEN 1 AND 4)
);

-- PAYMENT METHOD DIMENSION

CREATE TABLE IF NOT EXISTS warehouse.dim_payment_method (
    payment_method_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    payment_method_name VARCHAR(100) NOT NULL UNIQUE
);

-- ============================================================
-- 3. FACT TABLES
-- ============================================================

-- SALES FACT TABLE
-- Grain: One record per order item

CREATE TABLE IF NOT EXISTS warehouse.fact_sales (
    sales_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    order_item_id INTEGER NOT NULL UNIQUE,
    order_id INTEGER NOT NULL,

    customer_key BIGINT NOT NULL,
    product_key BIGINT NOT NULL,
    date_key INTEGER NOT NULL,

    order_status VARCHAR(50),

    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    line_total NUMERIC(14,2) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sales_customer
    FOREIGN KEY (customer_key)
    REFERENCES warehouse.dim_customer(customer_key),

    CONSTRAINT fk_sales_product
    FOREIGN KEY (product_key)
    REFERENCES warehouse.dim_product(product_key),

    CONSTRAINT fk_sales_date
    FOREIGN KEY (date_key)
    REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT chk_sales_quantity
    CHECK (quantity > 0),

    CONSTRAINT chk_sales_unit_price
    CHECK (unit_price >= 0),

    CONSTRAINT chk_sales_line_total
    CHECK (line_total >= 0)
);

-- TRANSACTIONS FACT TABLE
-- Grain: One record per payment transaction

CREATE TABLE IF NOT EXISTS warehouse.fact_transactions (
    transaction_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    transaction_id INTEGER NOT NULL UNIQUE,
    order_id INTEGER NOT NULL,

    customer_key BIGINT NOT NULL,
    date_key INTEGER NOT NULL,
    payment_method_key BIGINT NOT NULL,

    amount NUMERIC(14,2) NOT NULL,
    payment_status VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transaction_customer
    FOREIGN KEY (customer_key)
    REFERENCES warehouse.dim_customer(customer_key),

    CONSTRAINT fk_transaction_date
    FOREIGN KEY (date_key)
    REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_transaction_payment_method
    FOREIGN KEY (payment_method_key)
    REFERENCES warehouse.dim_payment_method(payment_method_key),

    CONSTRAINT chk_transaction_amount
    CHECK (amount >= 0)
);

-- ============================================================
-- 4. UNIQUE INDEXES FOR SCD TYPE 2
-- ============================================================

CREATE UNIQUE INDEX IF NOT EXISTS
idx_dim_customer_current
ON warehouse.dim_customer(customer_id)
WHERE is_current = TRUE;

CREATE UNIQUE INDEX IF NOT EXISTS
idx_dim_product_current
ON warehouse.dim_product(product_id)
WHERE is_current = TRUE;

-- ============================================================
-- 5. FACT TABLE INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_fact_sales_customer
ON warehouse.fact_sales(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product
ON warehouse.fact_sales(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date
ON warehouse.fact_sales(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_order
ON warehouse.fact_sales(order_id);

CREATE INDEX IF NOT EXISTS idx_fact_transactions_customer
ON warehouse.fact_transactions(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_transactions_date
ON warehouse.fact_transactions(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_transactions_payment
ON warehouse.fact_transactions(payment_method_key);

CREATE INDEX IF NOT EXISTS idx_fact_transactions_order
ON warehouse.fact_transactions(order_id);

COMMIT;

-- ============================================================
-- 6. COMPLETION MESSAGE
-- ============================================================

SELECT
    'Data Warehouse Created Successfully' AS status,
    'synthetic_data_db' AS database_name,
    'warehouse' AS schema_name;
