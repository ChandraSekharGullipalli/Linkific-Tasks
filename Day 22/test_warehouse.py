
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@pytest.fixture(scope="module")
def warehouse_engine():
    """Connect to the PostgreSQL warehouse database."""

    required = [
        "DB_HOST", "DB_PORT", "DB_NAME",
        "DB_USER", "DB_PASSWORD"
    ]

    assert all(os.getenv(key) for key in required), (
        "Missing database configuration in .env"
    )

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    engine = create_engine(url)

    try:
        yield engine
    finally:
        engine.dispose()


def test_warehouse_tables_exist(warehouse_engine):
    """Check that the four required warehouse tables exist."""

    tables = [
        "dim_customer",
        "dim_product",
        "fact_sales",
        "fact_transactions"
    ]

    query = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'warehouse'
    """)

    with warehouse_engine.connect() as connection:
        existing = set(connection.execute(query).scalars().all())

    for table in tables:
        assert table in existing, f"Missing warehouse table: {table}"


@pytest.mark.parametrize(
    "table, expected_count, condition",
    [
        ("dim_customer", 1000, "WHERE is_current = TRUE"),
        ("dim_product", 200, "WHERE is_current = TRUE"),
        ("fact_sales", 2516, ""),
        ("fact_transactions", 1000, "")
    ]
)
def test_warehouse_record_counts(
    warehouse_engine, table, expected_count, condition
):
    """Verify the expected warehouse record counts."""

    query = text(
        f"SELECT COUNT(*) FROM warehouse.{table} {condition}"
    )

    with warehouse_engine.connect() as connection:
        actual_count = connection.execute(query).scalar()

    assert actual_count == expected_count, (
        f"{table}: expected {expected_count}, found {actual_count}"
    )


def test_sales_referential_integrity(warehouse_engine):
    """Check customer and product references in sales facts."""

    query = text("""
        SELECT COUNT(*)
        FROM warehouse.fact_sales f
        LEFT JOIN warehouse.dim_customer c
            ON f.customer_key = c.customer_key
        LEFT JOIN warehouse.dim_product p
            ON f.product_key = p.product_key
        WHERE c.customer_key IS NULL
           OR p.product_key IS NULL
    """)

    with warehouse_engine.connect() as connection:
        invalid_count = connection.execute(query).scalar()

    assert invalid_count == 0


def test_transaction_referential_integrity(warehouse_engine):
    """Check customer and payment references in transaction facts."""

    query = text("""
        SELECT COUNT(*)
        FROM warehouse.fact_transactions f
        LEFT JOIN warehouse.dim_customer c
            ON f.customer_key = c.customer_key
        LEFT JOIN warehouse.dim_payment_method p
            ON f.payment_method_key = p.payment_method_key
        WHERE c.customer_key IS NULL
           OR p.payment_method_key IS NULL
    """)

    with warehouse_engine.connect() as connection:
        invalid_count = connection.execute(query).scalar()

    assert invalid_count == 0
