
"""
Day 23 - File Processing and Batch Ingestion

Supported formats:
1. CSV
2. Excel
3. JSON

Features:
- Batch file processing
- File format detection
- Record validation
- Null handling
- Standardized column names
- Staging JSON output
- Error handling
- Logging
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

SAMPLE_DIR = PROJECT_ROOT / "data" / "sample"
STAGING_DIR = PROJECT_ROOT / "data" / "staging" / "files"
LOG_DIR = PROJECT_ROOT / "logs"

STAGING_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "file_processing.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. STANDARDIZE DATA
# --------------------------------------------------

def standardize_dataframe(df):

    # Normalize column names
    df.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in df.columns
    ]

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate records
    before = len(df)
    df = df.drop_duplicates()
    duplicates = before - len(df)

    logger.info(
        "Removed %s duplicate records",
        duplicates
    )

    # Convert missing values to JSON-safe nulls
    df = df.astype(object).where(
        pd.notna(df),
        None
    )

    return df


# --------------------------------------------------
# 4. READ CSV FILE
# --------------------------------------------------

def read_csv_file(file_path):

    logger.info("Reading CSV: %s", file_path.name)

    return pd.read_csv(
        file_path,
        encoding="utf-8-sig"
    )


# --------------------------------------------------
# 5. READ EXCEL FILE
# --------------------------------------------------

def read_excel_file(file_path):

    logger.info("Reading Excel: %s", file_path.name)

    return pd.read_excel(
        file_path,
        engine="openpyxl"
    )


# --------------------------------------------------
# 6. READ JSON FILE
# --------------------------------------------------

def read_json_file(file_path):

    logger.info("Reading JSON: %s", file_path.name)

    with file_path.open(
        "r",
        encoding="utf-8-sig"
    ) as file:

        data = json.load(file)

    # Handle JSON object containing a records list
    if isinstance(data, dict):

        if "orders" in data and isinstance(
            data["orders"], list
        ):
            return pd.DataFrame(data["orders"])

        if "records" in data and isinstance(
            data["records"], list
        ):
            return pd.DataFrame(data["records"])

        return pd.DataFrame([data])

    if isinstance(data, list):
        return pd.DataFrame(data)

    raise ValueError("Unsupported JSON structure")


# --------------------------------------------------
# 7. PROCESS ONE FILE
# --------------------------------------------------

def process_file(file_path):

    extension = file_path.suffix.lower()

    try:

        if extension == ".csv":
            df = read_csv_file(file_path)

        elif extension in [".xlsx", ".xls"]:
            df = read_excel_file(file_path)

        elif extension == ".json":
            df = read_json_file(file_path)

        else:
            logger.warning(
                "Unsupported file skipped: %s",
                file_path.name
            )
            return None

        original_count = len(df)

        df = standardize_dataframe(df)

        records = df.to_dict(orient="records")

        output = {
            "source_file": file_path.name,
            "file_type": extension,
            "processed_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "original_records": original_count,
            "processed_records": len(records),
            "records": records
        }

        output_file = (
    STAGING_DIR /
    f"{file_path.stem}_{extension.lstrip('.')}_staged.json"
)

        with output_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                output,
                file,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        logger.info(
            "Processed %s: %s records",
            file_path.name,
            len(records)
        )

        logger.info(
            "Staging output: %s",
            output_file
        )

        return {
            "file": file_path.name,
            "status": "SUCCESS",
            "records": len(records)
        }

    except Exception as error:

        logger.exception(
            "Failed to process %s: %s",
            file_path.name,
            error
        )

        return {
            "file": file_path.name,
            "status": "FAILED",
            "error": str(error)
        }


# --------------------------------------------------
# 8. BATCH PROCESSING
# --------------------------------------------------

def main():

    logger.info("=" * 60)
    logger.info("DAY 23 FILE PROCESSING STARTED")
    logger.info("=" * 60)

    files = sorted(
        file_path
        for file_path in SAMPLE_DIR.iterdir()
        if file_path.is_file()
    )

    if not files:
        logger.warning("No sample files found")
        return

    results = []

    for file_path in files:

        logger.info(
            "Processing file: %s",
            file_path.name
        )

        result = process_file(file_path)

        if result is not None:
            results.append(result)

    successful = sum(
        result["status"] == "SUCCESS"
        for result in results
    )

    failed = sum(
        result["status"] == "FAILED"
        for result in results
    )

    logger.info("-" * 60)
    logger.info("TOTAL FILES: %s", len(results))
    logger.info("SUCCESSFUL: %s", successful)
    logger.info("FAILED: %s", failed)
    logger.info("=" * 60)
    logger.info("FILE PROCESSING COMPLETED")


if __name__ == "__main__":
    main()
