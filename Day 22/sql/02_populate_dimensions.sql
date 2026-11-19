
-- DAY 22: POPULATE DATA WAREHOUSE DIMENSIONS

BEGIN;

-- 1. Populate DATE dimension
WITH date_range AS (
    SELECT
        LEAST(
            COALESCE((SELECT MIN(order_date) FROM public.orders), CURRENT_DATE),
            COALESCE((SELECT MIN(transaction_date) FROM public.transactions), CURRENT_DATE),
            COALESCE((SELECT MIN(created_at) FROM public.customers), CURRENT_DATE)
        ) AS start_date,
        GREATEST(
            COALESCE((SELECT MAX(order_date) FROM public.orders), CURRENT_DATE),
            COALESCE((SELECT MAX(transaction_date) FROM public.transactions), CURRENT_DATE),
            COALESCE((SELECT MAX(created_at) FROM public.customers), CURRENT_DATE)
        ) AS end_date
),
calendar AS (
    SELECT generate_series(
        start_date::timestamp,
        end_date::timestamp,
        INTERVAL '1 day'
    )::date AS calendar_date
    FROM date_range
)
INSERT INTO warehouse.dim_date (
    date_key,
    full_date,
    day_number,
    month_number,
    month_name,
    quarter_number,
    year_number,
    day_of_week,
    day_name,
    week_number,
    is_weekend,
    is_holiday
)
SELECT
    TO_CHAR(calendar_date, 'YYYYMMDD')::INTEGER,
    calendar_date,
    EXTRACT(DAY FROM calendar_date)::INTEGER,
    EXTRACT(MONTH FROM calendar_date)::INTEGER,
    TO_CHAR(calendar_date, 'FMMonth'),
    EXTRACT(QUARTER FROM calendar_date)::INTEGER,
    EXTRACT(YEAR FROM calendar_date)::INTEGER,
    EXTRACT(DOW FROM calendar_date)::INTEGER,
    TO_CHAR(calendar_date, 'FMDay'),
    EXTRACT(WEEK FROM calendar_date)::INTEGER,
    EXTRACT(DOW FROM calendar_date) IN (0, 6),
    FALSE
FROM calendar
ON CONFLICT (date_key) DO NOTHING;


-- 2. Populate CUSTOMER dimension
-- Initial load for SCD Type 2

INSERT INTO warehouse.dim_customer (
    customer_id,
    customer_name,
    email,
    phone,
    city,
    effective_start_date,
    effective_end_date,
    is_current
)
SELECT
    c.customer_id,
    c.customer_name,
    c.email,
    c.phone,
    c.city,
    COALESCE(c.created_at, CURRENT_DATE),
    DATE '9999-12-31',
    TRUE
FROM public.customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM warehouse.dim_customer d
    WHERE d.customer_id = c.customer_id
      AND d.is_current = TRUE
);


-- 3. Populate PRODUCT dimension
-- Initial load for SCD Type 2

INSERT INTO warehouse.dim_product (
    product_id,
    product_name,
    category,
    price,
    effective_start_date,
    effective_end_date,
    is_current
)
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    CURRENT_DATE,
    DATE '9999-12-31',
    TRUE
FROM public.products p
WHERE NOT EXISTS (
    SELECT 1
    FROM warehouse.dim_product d
    WHERE d.product_id = p.product_id
      AND d.is_current = TRUE
);


-- 4. Populate PAYMENT METHOD dimension

INSERT INTO warehouse.dim_payment_method (
    payment_method_name
)
SELECT DISTINCT
    TRIM(payment_method)
FROM public.transactions
WHERE payment_method IS NOT NULL
  AND TRIM(payment_method) <> ''
ON CONFLICT (payment_method_name) DO NOTHING;


COMMIT;
