SELECT
    'fact_sales' AS fact_table,
    COUNT(*) AS total_records
FROM warehouse.fact_sales

UNION ALL

SELECT
    'fact_transactions',
    COUNT(*)
FROM warehouse.fact_transactions;