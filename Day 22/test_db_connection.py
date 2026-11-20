
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Load environment variables from the project .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@pytest.fixture(scope="module")
def db_engine():
    """Create a PostgreSQL database connection for testing."""

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    # Check database configuration
    assert all([host, port, database, username, password]), (
        "Missing database configuration in .env"
    )

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=username,
        password=password,
        host=host,
        port=int(port),
        database=database
    )

    engine = create_engine(connection_url)

    try:
        yield engine
    finally:
        engine.dispose()


def test_database_connection(db_engine):
    """Verify that PostgreSQL is accessible."""

    with db_engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        ).scalar()

    assert result == 1


def test_database_name(db_engine):
    """Verify the connected database name."""

    expected_database = os.getenv("DB_NAME")

    with db_engine.connect() as connection:
        actual_database = connection.execute(
            text("SELECT current_database()")
        ).scalar()

    assert actual_database == expected_database
