
"""
Day 21 - Multi-Source Data Collection
Task: Collect data from CSV, JSON and Excel files.

Features:
1. Read CSV files using Pandas.
2. Read JSON files using Python JSON.
3. Read Excel files using OpenPyXL through Pandas.
4. Convert extracted data into standard CSV and JSON.
5. Handle errors.
6. Maintain execution logs.
"""

import json
import logging
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "Files" / "input"
OUTPUT_DIR = BASE_DIR / "output" / "Files"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "file_collection.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. SAVE COLLECTED DATA
# --------------------------------------------------

def save_data(dataframe, filename):
    """Save collected data as CSV and JSON."""

    try:
        csv_path = OUTPUT_DIR / f"{filename}.csv"
        json_path = OUTPUT_DIR / f"{filename}.json"

        dataframe.to_csv(
            csv_path,
            index=False
        )

        records = json.loads(
            dataframe.to_json(
                orient="records",
                date_format="iso"
            )
        )

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                records,
                file,
                indent=4,
                ensure_ascii=False
            )

        logger.info(f"CSV saved: {csv_path}")
        logger.info(f"JSON saved: {json_path}")
        logger.info(f"Records collected: {len(dataframe)}")

    except (OSError, ValueError, TypeError) as error:
        logger.exception(
            f"Error saving {filename}: {error}"
        )


# --------------------------------------------------
# 4. COLLECT CSV DATA
# --------------------------------------------------

def collect_csv():

    logger.info("Starting CSV collection")

    file_path = INPUT_DIR / "customers.csv"

    try:
        dataframe = pd.read_csv(file_path)

        logger.info(
            f"CSV collection successful: {len(dataframe)} records"
        )

        save_data(
            dataframe,
            "collected_customers"
        )

    except FileNotFoundError:
        logger.error(f"CSV file not found: {file_path}")

    except Exception:
        logger.exception("CSV collection failed")


# --------------------------------------------------
# 5. COLLECT JSON DATA
# --------------------------------------------------

def collect_json():

    logger.info("Starting JSON collection")

    file_path = INPUT_DIR / "products.json"

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            records = json.load(file)

        dataframe = pd.json_normalize(records)

        logger.info(
            f"JSON collection successful: {len(dataframe)} records"
        )

        save_data(
            dataframe,
            "collected_products"
        )

    except FileNotFoundError:
        logger.error(f"JSON file not found: {file_path}")

    except json.JSONDecodeError:
        logger.exception("Invalid JSON format")

    except Exception:
        logger.exception("JSON collection failed")


# --------------------------------------------------
# 6. COLLECT EXCEL DATA
# --------------------------------------------------

def collect_excel():

    logger.info("Starting Excel collection")

    file_path = INPUT_DIR / "employees.xlsx"

    try:
        dataframe = pd.read_excel(
            file_path,
            engine="openpyxl"
        )

        logger.info(
            f"Excel collection successful: {len(dataframe)} records"
        )

        save_data(
            dataframe,
            "collected_employees"
        )

    except FileNotFoundError:
        logger.error(f"Excel file not found: {file_path}")

    except Exception:
        logger.exception("Excel collection failed")


# --------------------------------------------------
# 7. MAIN FUNCTION
# --------------------------------------------------

def main():

    logger.info("=" * 55)
    logger.info("FILE DATA COLLECTION STARTED")
    logger.info("=" * 55)

    collect_csv()

    collect_json()

    collect_excel()

    logger.info("=" * 55)
    logger.info("FILE DATA COLLECTION COMPLETED")
    logger.info("=" * 55)


if __name__ == "__main__":
    main()
