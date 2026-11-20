
import json
import logging
from pathlib import Path
from datetime import date, datetime

import psycopg2
from dotenv import load_dotenv
import os


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

STATE_DIR = BASE_DIR / "data" / "state"
STATE_FILE = STATE_DIR / "warehouse_watermarks.json"

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "incremental_warehouse_loader.log"

STATE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "synthetic_data_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

REQUIRED_WATERMARKS = [
    "customers",
    "products",
    "order_items",
    "transactions"
]


# ============================================================
# 2. WATERMARK MANAGEMENT
# ============================================================

def get_initial_watermarks(cursor):
    """Get the existing warehouse maximum IDs."""

    cursor.execute("""
        SELECT
            (SELECT COALESCE(MAX(customer_id), 0)
             FROM warehouse.dim_customer
             WHERE is_current = TRUE),

            (SELECT COALESCE(MAX(product_id), 0)
             FROM warehouse.dim_product
             WHERE is_current = TRUE),

            (SELECT COALESCE(MAX(order_item_id), 0)
             FROM warehouse.fact_sales),

            (SELECT COALESCE(MAX(transaction_id), 0)
             FROM warehouse.fact_transactions);
    """)

    values = cursor.fetchone()

    return {
        "customers": int(values[0]),
        "products": int(values[1]),
        "order_items": int(values[2]),
        "transactions": int(values[3])
    }


def load_watermarks(cursor):
    """Load warehouse checkpoints or initialize from the warehouse."""

    if not STATE_FILE.exists():
        logger.info("Warehouse checkpoint file not found.")
        logger.info("Initializing from existing warehouse records.")

        return get_initial_watermarks(cursor)

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        watermarks = json.load(file)

    if not isinstance(watermarks, dict):
        raise ValueError("Invalid warehouse watermark file.")

    for key in REQUIRED_WATERMARKS:
        if key not in watermarks:
            raise ValueError(f"Missing watermark: {key}")

        watermarks[key] = int(watermarks[key])

        if watermarks[key] < 0:
            raise ValueError(f"Invalid negative watermark: {key}")

    return watermarks


def save_watermarks(watermarks):
    """Save checkpoints using an atomic file replacement."""

    temporary_file = STATE_FILE.with_suffix(".tmp")

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(watermarks, file, indent=4)

    temporary_file.replace(STATE_FILE)


# ============================================================
# 3. LOAD NEW CUSTOMER DIMENSIONS
# ============================================================

def load_new_customers(cursor):

    cursor.execute("""
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
    """)

    logger.info("New customer dimensions inserted: %s", cursor.rowcount)


# ============================================================
# 4. LOAD NEW PRODUCT DIMENSIONS
# ============================================================

def load_new_products(cursor):

    cursor.execute("""
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
    """)

    logger.info("New product dimensions inserted: %s", cursor.rowcount)


# ============================================================
# 5. LOAD NEW DATE DIMENSIONS
# ============================================================

def load_new_dates(cursor):

    cursor.execute("""
        WITH source_dates AS (
            SELECT order_date::date AS calendar_date
            FROM public.orders
            WHERE order_date IS NOT NULL

            UNION

            SELECT transaction_date::date
            FROM public.transactions
            WHERE transaction_date IS NOT NULL

            UNION

            SELECT created_at::date
            FROM public.customers
            WHERE created_at IS NOT NULL
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
        FROM source_dates
        ON CONFLICT (date_key) DO NOTHING;
    """)

    logger.info("New date dimension records inserted: %s", cursor.rowcount)


# ============================================================
# 6. LOAD NEW PAYMENT METHODS
# ============================================================

def load_new_payment_methods(cursor):

    cursor.execute("""
        INSERT INTO warehouse.dim_payment_method (
            payment_method_name
        )
        SELECT DISTINCT TRIM(payment_method)
        FROM public.transactions
        WHERE payment_method IS NOT NULL
          AND TRIM(payment_method) <> ''
        ON CONFLICT (payment_method_name) DO NOTHING;
    """)

    logger.info("New payment methods inserted: %s", cursor.rowcount)


# ============================================================
# 7. LOAD NEW SALES FACT RECORDS
# ============================================================

def load_new_sales(cursor, last_id):

    cursor.execute("""
        INSERT INTO warehouse.fact_sales (
            order_item_id,
            order_id,
            customer_key,
            product_key,
            date_key,
            order_status,
            quantity,
            unit_price,
            line_total
        )
        SELECT
            oi.order_item_id,
            oi.order_id,
            dc.customer_key,
            dp.product_key,
            dd.date_key,
            o.status,
            oi.quantity,
            oi.unit_price,
            COALESCE(
                oi.line_total,
                oi.quantity * oi.unit_price
            )
        FROM public.order_items oi

        JOIN public.orders o
            ON oi.order_id = o.order_id

        JOIN warehouse.dim_customer dc
            ON o.customer_id = dc.customer_id
           AND dc.is_current = TRUE

        JOIN warehouse.dim_product dp
            ON oi.product_id = dp.product_id
           AND dp.is_current = TRUE

        JOIN warehouse.dim_date dd
            ON o.order_date = dd.full_date

        WHERE oi.order_item_id > %s

        ON CONFLICT (order_item_id) DO NOTHING;
    """, (last_id,))

    inserted = cursor.rowcount

    logger.info("New sales fact records inserted: %s", inserted)

    return inserted


# ============================================================
# 8. LOAD NEW TRANSACTION FACT RECORDS
# ============================================================

def load_new_transactions(cursor, last_id):

    cursor.execute("""
        INSERT INTO warehouse.fact_transactions (
            transaction_id,
            order_id,
            customer_key,
            date_key,
            payment_method_key,
            amount,
            payment_status
        )
        SELECT
            t.transaction_id,
            t.order_id,
            dc.customer_key,
            dd.date_key,
            pm.payment_method_key,
            t.amount,
            t.payment_status
        FROM public.transactions t

        JOIN public.orders o
            ON t.order_id = o.order_id

        JOIN warehouse.dim_customer dc
            ON o.customer_id = dc.customer_id
           AND dc.is_current = TRUE

        JOIN warehouse.dim_date dd
            ON t.transaction_date = dd.full_date

        JOIN warehouse.dim_payment_method pm
            ON TRIM(t.payment_method) = pm.payment_method_name

        WHERE t.transaction_id > %s

        ON CONFLICT (transaction_id) DO NOTHING;
    """, (last_id,))

    inserted = cursor.rowcount

    logger.info("New transaction fact records inserted: %s", inserted)

    return inserted


# ============================================================
# 9. VERIFY THAT ALL NEW FACTS WERE LOADED
# ============================================================

def verify_new_records(cursor, sales_watermark, transaction_watermark):

    cursor.execute("""
        SELECT COUNT(*)
        FROM public.order_items oi
        LEFT JOIN warehouse.fact_sales fs
            ON oi.order_item_id = fs.order_item_id
        WHERE oi.order_item_id > %s
          AND fs.order_item_id IS NULL;
    """, (sales_watermark,))

    missing_sales = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM public.transactions t
        LEFT JOIN warehouse.fact_transactions ft
            ON t.transaction_id = ft.transaction_id
        WHERE t.transaction_id > %s
          AND ft.transaction_id IS NULL;
    """, (transaction_watermark,))

    missing_transactions = cursor.fetchone()[0]

    if missing_sales > 0 or missing_transactions > 0:
        raise RuntimeError(
            "Incremental loading incomplete. "
            f"Missing sales: {missing_sales}, "
            f"missing transactions: {missing_transactions}"
        )

    logger.info("Incremental fact verification passed.")


# ============================================================
# 10. UPDATE WATERMARKS AFTER SUCCESSFUL LOAD
# ============================================================

def get_updated_watermarks(cursor, old_watermarks):

    updated = old_watermarks.copy()

    source_tables = {
        "customers": "customer_id",
        "products": "product_id",
        "order_items": "order_item_id",
        "transactions": "transaction_id"
    }

    for table, primary_key in source_tables.items():

        cursor.execute(
            f"SELECT COALESCE(MAX({primary_key}), 0) FROM public.{table};"
        )

        maximum_id = cursor.fetchone()[0]

        updated[table] = max(
            old_watermarks[table],
            int(maximum_id)
        )

    return updated


# ============================================================
# 11. MAIN INCREMENTAL PIPELINE
# ============================================================

def run_incremental_pipeline():

    logger.info("=" * 60)
    logger.info("INCREMENTAL WAREHOUSE LOADING STARTED")
    logger.info("=" * 60)

    connection = None
    updated_watermarks = None

    try:

        if not DB_CONFIG["password"]:
            raise ValueError(
                "DB_PASSWORD is missing. Check your local .env file."
            )

        connection = psycopg2.connect(**DB_CONFIG)

        logger.info(
            "Connected to database: %s",
            DB_CONFIG["database"]
        )

        # All warehouse changes happen in one database transaction.
        with connection:

            with connection.cursor() as cursor:

                watermarks = load_watermarks(cursor)

                logger.info("Current warehouse watermarks: %s", watermarks)

                # Save the previous fact checkpoints for verification.
                old_sales_id = watermarks["order_items"]
                old_transaction_id = watermarks["transactions"]

                # Load dimensions before loading facts.
                load_new_customers(cursor)
                load_new_products(cursor)
                load_new_dates(cursor)
                load_new_payment_methods(cursor)

                # Load only new fact records.
                load_new_sales(cursor, old_sales_id)
                load_new_transactions(cursor, old_transaction_id)

                # Confirm that every new fact has been loaded.
                verify_new_records(
                    cursor,
                    old_sales_id,
                    old_transaction_id
                )

                # Calculate new checkpoints inside the transaction.
                updated_watermarks = get_updated_watermarks(
                    cursor,
                    watermarks
                )

        # The database transaction has committed successfully.
        # Only now save the new checkpoint file.
        save_watermarks(updated_watermarks)

        logger.info("Updated warehouse watermarks: %s", updated_watermarks)

        logger.info("INCREMENTAL WAREHOUSE LOADING COMPLETED SUCCESSFULLY")

    except Exception:

        logger.exception("INCREMENTAL WAREHOUSE LOADING FAILED")

        raise

    finally:

        if connection is not None:
            connection.close()
            logger.info("Database connection closed.")

        logger.info("=" * 60)


if __name__ == "__main__":
    run_incremental_pipeline()
