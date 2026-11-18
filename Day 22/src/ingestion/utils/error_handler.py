
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path


# --------------------------------------------------
# 1. SET PROJECT DIRECTORIES
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

LOG_DIR = BASE_DIR / "logs"
ERROR_DIR = BASE_DIR / "data" / "staging" / "errors"

LOG_DIR.mkdir(parents=True, exist_ok=True)
ERROR_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. CONFIGURE CENTRALIZED ERROR LOGGING
# --------------------------------------------------

logger = logging.getLogger("central_error_handler")
logger.setLevel(logging.ERROR)

if not logger.handlers:
    handler = logging.FileHandler(
        LOG_DIR / "error_handling.log",
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)


# --------------------------------------------------
# 3. RECORD ERROR DETAILS
# --------------------------------------------------

def record_error(source, error, record_id=None):

    error_details = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "record_id": record_id,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "traceback": traceback.format_exc()
    }

    logger.error(
        "Source: %s | Record: %s | %s: %s",
        source,
        record_id,
        type(error).__name__,
        str(error)
    )

    return error_details


# --------------------------------------------------
# 4. SAVE ERRORS TO JSON REPORT
# --------------------------------------------------

def save_error_report(errors):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = ERROR_DIR / f"error_report_{timestamp}.json"

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_errors": len(errors),
        "errors": errors
    }

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Error report saved: {report_path}")

    return report_path


# --------------------------------------------------
# 5. PROCESS RECORDS SAFELY
# --------------------------------------------------

def safe_process(source, records, process_function):

    successful_records = []
    errors = []

    for index, record in enumerate(records, start=1):

        try:
            result = process_function(record)
            successful_records.append(result)

        except Exception as error:

            error_details = record_error(
                source=source,
                error=error,
                record_id=index
            )

            errors.append(error_details)

            print(
                f"Failed record {index} from {source}: {error}"
            )

    if errors:
        save_error_report(errors)

    return successful_records, errors


# --------------------------------------------------
# 6. TEST ERROR HANDLING
# --------------------------------------------------

if __name__ == "__main__":

    # Sample data with one intentionally invalid record
    sample_records = [10, 20, "invalid", 40, 50]

    def sample_processor(value):

        if not isinstance(value, (int, float)):
            raise TypeError(
                "Only numeric values are allowed"
            )

        return value * 2

    successful, failed = safe_process(
        source="error_handler_test",
        records=sample_records,
        process_function=sample_processor
    )

    print("\nError Handling Test Results")
    print("---------------------------")

    print("Successful records:", successful)
    print("Failed records:", len(failed))
