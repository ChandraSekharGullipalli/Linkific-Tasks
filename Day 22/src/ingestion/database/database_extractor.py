
import json
import logging
import os
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# --------------------------------------------------
# PATHS AND CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

OUTPUT_DIR = BASE_DIR / "data" / "raw" / "database"
STATE_FILE = BASE_DIR / "data" / "raw" / "database" / "watermarks.json"
LOG_FILE = BASE_DIR / "logs" / "database_extraction.log"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "synthetic_data_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}


# --------------------------------------------------
# ALLOWED TABLES AND PRIMARY KEYS
# --------------------------------------------------

TABLES = {
    "customers": "customer_id",
    "order_items": "order_item_id",
    "orders": "order_id",
    "products": "product_id",
    "transactions": "transaction_id"
}


# --------------------------------------------------
# JSON SERIALIZATION
# --------------------------------------------------

def json_serializer(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()

    if isinstance(value, Decimal):
        return float(value)

    raise TypeError(f"Unsupported JSON value: {type(value)}")

# --------------------------------------------------
# WATERMARK MANAGEMENT
# --------------------------------------------------

def load_watermarks():
    if not STATE_FILE.exists():
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        logger.exception("Could not read watermark file")
        raise


def save_watermarks(watermarks):
    temporary_file = STATE_FILE.with_suffix(".tmp")

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(watermarks, file, indent=4)

    temporary_file.replace(STATE_FILE)


# --------------------------------------------------
# DATABASE EXTRACTION
# --------------------------------------------------

def extract_table(cursor, table_name, primary_key, last_id):
    query = f"""
        SELECT *
        FROM public.{table_name}
        WHERE {primary_key} > %s
        ORDER BY {primary_key}
    """

    cursor.execute(query, (last_id,))
    records = cursor.fetchall()

    return records


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def run_extraction():

    logger.info("=" * 60)
    logger.info("DAY 23 DATABASE EXTRACTION STARTED")
    logger.info("=" * 60)

    connection = None

    try:
        if not DB_CONFIG["password"]:
            raise ValueError(
                "DB_PASSWORD is missing. Add your PostgreSQL password "
                "to the local .env file."
            )

        connection = psycopg2.connect(**DB_CONFIG)

        logger.info(
            "Connected to PostgreSQL database: %s",
            DB_CONFIG["database"]
        )

        watermarks = load_watermarks()
        updated_watermarks = watermarks.copy()

        total_records = 0
        successful_tables = 0
        failed_tables = 0

        with connection.cursor(cursor_factory=RealDictCursor) as cursor:

            for table_name, primary_key in TABLES.items():

                try:
                    last_id = int(watermarks.get(table_name, 0))

                    logger.info(
                        "Extracting %s records after ID %s",
                        table_name,
                        last_id
                    )

                    records = extract_table(
                        cursor,
                        table_name,
                        primary_key,
                        last_id
                    )

                    records = [dict(record) for record in records]

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

                    output_file = (
                        OUTPUT_DIR /
                        f"{table_name}_{timestamp}.json"
                    )

                    output_data = {
                        "source_database": DB_CONFIG["database"],
                        "source_table": table_name,
                        "primary_key": primary_key,
                        "extraction_type": (
                            "incremental" if last_id > 0 else "initial"
                        ),
                        "previous_watermark": last_id,
                        "record_count": len(records),
                        "extracted_at": datetime.now().isoformat(),
                        "records": records
                    }

                    with open(output_file, "w", encoding="utf-8") as file:
                        json.dump(
                            output_data,
                            file,
                            indent=4,
                            default=json_serializer
                        )

                    if records:
                        new_watermark = max(
                            int(record[primary_key])
                            for record in records
                        )
                    else:
                        new_watermark = last_id

                    updated_watermarks[table_name] = new_watermark

                    total_records += len(records)
                    successful_tables += 1

                    logger.info(
                        "SUCCESS: %s | Records: %s | New watermark: %s",
                        table_name,
                        len(records),
                        new_watermark
                    )

                    logger.info("Saved raw data: %s", output_file)

                except Exception:
                    failed_tables += 1
                    logger.exception(
                        "FAILED to extract table: %s",
                        table_name
                    )

        # Persist watermarks only for successfully extracted tables.
        for table_name in TABLES:
            if table_name in updated_watermarks:
                watermarks[table_name] = updated_watermarks[table_name]

        save_watermarks(watermarks)

        logger.info("-" * 60)
        logger.info("TOTAL RECORDS EXTRACTED: %s", total_records)
        logger.info("SUCCESSFUL TABLES: %s", successful_tables)
        logger.info("FAILED TABLES: %s", failed_tables)
        logger.info("WATERMARK FILE: %s", STATE_FILE)
        logger.info("DATABASE EXTRACTION COMPLETED")
        logger.info("=" * 60)

    except Exception:
        logger.exception("DATABASE EXTRACTION PIPELINE FAILED")
        raise

    finally:
        if connection is not None:
            connection.close()
            logger.info("PostgreSQL connection closed")


if __name__ == "__main__":
    run_extraction()
