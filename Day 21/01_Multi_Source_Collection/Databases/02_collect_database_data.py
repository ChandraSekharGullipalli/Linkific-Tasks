
"""
Day 21 - Multi-Source Data Collection
Task: Collect data from PostgreSQL and SQLite.

Features:
1. Connect to PostgreSQL.
2. Discover available PostgreSQL tables.
3. Extract records from every table.
4. Create and populate a sample SQLite database.
5. Extract SQLite tables.
6. Save all extracted data as CSV and JSON.
7. Log operations and handle errors.
"""

import os
import json
import logging
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    inspect,
    text
)
from sqlalchemy.engine import URL


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output" / "Databases"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "database_collection.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. SAVE DATABASE TABLES
# --------------------------------------------------

def save_table(dataframe, database_name, table_name):
    """Save extracted table data into CSV and JSON."""

    if dataframe.empty:
        logger.warning(f"{table_name}: Table contains no records.")

    safe_name = f"{database_name}_{table_name}"

    csv_path = OUTPUT_DIR / f"{safe_name}.csv"
    json_path = OUTPUT_DIR / f"{safe_name}.json"

    try:
        dataframe.to_csv(csv_path, index=False)

        records = dataframe.to_json(
            orient="records",
            date_format="iso"
        )

        with open(json_path, "w", encoding="utf-8") as file:
            file.write(
                json.dumps(
                    json.loads(records),
                    indent=4,
                    ensure_ascii=False
                )
            )

        logger.info(
            f"Saved {safe_name}: {len(dataframe)} records"
        )

    except (OSError, ValueError, TypeError) as error:
        logger.exception(f"Failed to save {safe_name}: {error}")


# --------------------------------------------------
# 4. GENERIC DATABASE EXTRACTION
# --------------------------------------------------

def extract_database_tables(engine, database_name):
    """Discover and extract every table in a database."""

    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        logger.info(
            f"{database_name}: Found {len(tables)} tables"
        )

        if not tables:
            logger.warning(f"No tables found in {database_name}")
            return

        for table_name in tables:

            try:
                query = text(
                    f'SELECT * FROM "{table_name}"'
                )

                with engine.connect() as connection:
                    dataframe = pd.read_sql(
                        query,
                        connection
                    )

                logger.info(
                    f"Extracted {table_name}: "
                    f"{len(dataframe)} records"
                )

                save_table(
                    dataframe,
                    database_name,
                    table_name
                )

            except Exception:
                logger.exception(
                    f"Error extracting table: {table_name}"
                )

    except Exception:
        logger.exception(
            f"Database inspection failed: {database_name}"
        )


# --------------------------------------------------
# 5. POSTGRESQL CONNECTION
# --------------------------------------------------

def collect_postgresql():

    logger.info("=" * 50)
    logger.info("POSTGRESQL DATA COLLECTION STARTED")
    logger.info("=" * 50)

    required = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
    ]

    missing = [
        key for key in required
        if not os.getenv(key)
        or os.getenv(key) == "YOUR_POSTGRES_PASSWORD"
    ]

    if missing:
        logger.error(
            f"Missing PostgreSQL configuration: {missing}"
        )
        return

    try:
        database_url = URL.create(
            drivername="postgresql+psycopg2",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            database=os.getenv("DB_NAME")
        )

        engine = create_engine(
            database_url,
            pool_pre_ping=True
        )

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("PostgreSQL connection successful.")

        extract_database_tables(
            engine,
            "postgresql"
        )

        engine.dispose()

    except Exception:
        logger.exception("PostgreSQL connection failed.")


# --------------------------------------------------
# 6. CREATE SAMPLE SQLITE DATABASE
# --------------------------------------------------

def create_sqlite_database():

    sqlite_path = (
        BASE_DIR / "Databases" / "source_data.db"
    )

    engine = create_engine(
        f"sqlite:///{sqlite_path.as_posix()}"
    )

    try:
        with engine.begin() as connection:

            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS departments (
                    department_id INTEGER PRIMARY KEY,
                    department_name TEXT NOT NULL
                )
            """))

            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id INTEGER PRIMARY KEY,
                    employee_name TEXT NOT NULL,
                    email TEXT,
                    department_id INTEGER,
                    salary REAL,
                    FOREIGN KEY (department_id)
                    REFERENCES departments(department_id)
                )
            """))

            connection.execute(text("""
                INSERT OR IGNORE INTO departments
                VALUES
                (1, 'Data Engineering'),
                (2, 'Analytics'),
                (3, 'Human Resources')
            """))

            connection.execute(text("""
                INSERT OR IGNORE INTO employees
                VALUES
                (1, 'Rahul Sharma', 'rahul@example.com', 1, 55000),
                (2, 'Priya Reddy', 'priya@example.com', 2, 48000),
                (3, 'Arjun Kumar', 'arjun@example.com', 1, 60000),
                (4, 'Sneha Rao', 'sneha@example.com', 3, 45000),
                (5, 'Kiran Das', 'kiran@example.com', 2, 52000)
            """))

        logger.info(
            f"SQLite database ready: {sqlite_path}"
        )

        return engine

    except Exception:
        engine.dispose()
        logger.exception("SQLite database creation failed.")
        raise


# --------------------------------------------------
# 7. SQLITE DATA COLLECTION
# --------------------------------------------------

def collect_sqlite():

    logger.info("=" * 50)
    logger.info("SQLITE DATA COLLECTION STARTED")
    logger.info("=" * 50)

    engine = None

    try:
        engine = create_sqlite_database()

        extract_database_tables(
            engine,
            "sqlite"
        )

    except Exception:
        logger.exception("SQLite collection failed.")

    finally:
        if engine is not None:
            engine.dispose()


# --------------------------------------------------
# 8. MAIN FUNCTION
# --------------------------------------------------

def main():

    logger.info("DATABASE COLLECTION PIPELINE STARTED")

    collect_postgresql()

    collect_sqlite()

    logger.info("DATABASE COLLECTION PIPELINE COMPLETED")


if __name__ == "__main__":
    main()
