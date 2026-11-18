
"""
DAY 23 - CENTRALIZED DATA INGESTION PIPELINE

Runs:
1. API collection
2. Web scraping
3. File processing
4. PostgreSQL database extraction

Features:
- Sequential execution
- Error handling
- Centralized logging
- Execution time tracking
- JSON execution summary
"""

import json
import logging
import subprocess
import sys
import time

from datetime import datetime
from pathlib import Path


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

LOG_DIR = BASE_DIR / "logs"
SUMMARY_DIR = BASE_DIR / "data" / "staging" / "pipeline"

LOG_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

LOG_FILE = LOG_DIR / "ingestion_pipeline.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ],
    force=True
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. COLLECTION SCRIPTS
# --------------------------------------------------

PIPELINE_TASKS = [
    {
        "name": "API Data Collection",
        "script": BASE_DIR / "src" / "ingestion" / "api" / "api_collector.py"
    },
    {
        "name": "Web Scraping",
        "script": BASE_DIR / "src" / "ingestion" / "scraping" / "product_scraper.py"
    },
    {
        "name": "File Processing",
        "script": BASE_DIR / "src" / "ingestion" / "files" / "file_collector.py"
    },
    {
        "name": "Database Extraction",
        "script": BASE_DIR / "src" / "ingestion" / "database" / "database_extractor.py"
    }
]


# --------------------------------------------------
# 4. EXECUTE ONE COLLECTION SCRIPT
# --------------------------------------------------

def execute_task(task):

    task_name = task["name"]
    script_path = task["script"]

    logger.info("=" * 60)
    logger.info("STARTING: %s", task_name)
    logger.info("SCRIPT: %s", script_path)

    start_time = time.time()
    start_timestamp = datetime.now().isoformat(timespec="seconds")

    result = {
        "task": task_name,
        "script": str(script_path.relative_to(BASE_DIR)),
        "status": "FAILED",
        "start_time": start_timestamp,
        "end_time": None,
        "duration_seconds": 0,
        "return_code": None,
        "error": None
    }

    try:

        if not script_path.exists():
            raise FileNotFoundError(
                f"Collection script not found: {script_path}"
            )

        process = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=900
        )

        result["return_code"] = process.returncode

        if process.stdout:
            logger.info(
                "%s OUTPUT:\n%s",
                task_name,
                process.stdout.strip()
            )

        if process.stderr:
            logger.warning(
                "%s MESSAGES:\n%s",
                task_name,
                process.stderr.strip()
            )

        if process.returncode == 0:
            result["status"] = "SUCCESS"
            logger.info("SUCCESS: %s", task_name)

        else:
            result["error"] = (
                f"Script exited with code {process.returncode}"
            )
            logger.error(
                "FAILED: %s | Exit code: %s",
                task_name,
                process.returncode
            )

    except subprocess.TimeoutExpired:
        result["error"] = "Script exceeded the 15-minute timeout."
        logger.error("TIMEOUT: %s", task_name)

    except Exception as error:
        result["error"] = str(error)
        logger.exception("ERROR while running %s", task_name)

    finally:

        end_time = time.time()

        result["end_time"] = datetime.now().isoformat(
            timespec="seconds"
        )

        result["duration_seconds"] = round(
            end_time - start_time, 2
        )

        logger.info(
            "FINISHED: %s | Status: %s | Duration: %s seconds",
            task_name,
            result["status"],
            result["duration_seconds"]
        )

    return result


# --------------------------------------------------
# 5. RUN COMPLETE INGESTION PIPELINE
# --------------------------------------------------

def run_pipeline():

    pipeline_start = datetime.now()

    logger.info("=" * 60)
    logger.info("DAY 23 DATA INGESTION PIPELINE STARTED")
    logger.info("START TIME: %s", pipeline_start.isoformat())
    logger.info("=" * 60)

    task_results = []

    for task in PIPELINE_TASKS:

        task_result = execute_task(task)
        task_results.append(task_result)

        if task_result["status"] == "FAILED":
            logger.warning(
                "Pipeline continuing despite failure in: %s",
                task_result["task"]
            )

    pipeline_end = datetime.now()

    successful_tasks = sum(
        1 for result in task_results
        if result["status"] == "SUCCESS"
    )

    failed_tasks = len(task_results) - successful_tasks

    total_duration = round(
        (pipeline_end - pipeline_start).total_seconds(), 2
    )

    # --------------------------------------------------
    # 6. CREATE EXECUTION SUMMARY
    # --------------------------------------------------

    summary = {
        "pipeline_name": "Day 23 Data Ingestion Pipeline",
        "start_time": pipeline_start.isoformat(),
        "end_time": pipeline_end.isoformat(),
        "total_duration_seconds": total_duration,
        "total_tasks": len(task_results),
        "successful_tasks": successful_tasks,
        "failed_tasks": failed_tasks,
        "overall_status": (
            "SUCCESS" if failed_tasks == 0 else "PARTIAL_SUCCESS"
        ),
        "tasks": task_results
    }

    timestamp = pipeline_end.strftime("%Y%m%d_%H%M%S")

    summary_file = SUMMARY_DIR / f"pipeline_summary_{timestamp}.json"

    with open(summary_file, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    # --------------------------------------------------
    # 7. FINAL REPORT
    # --------------------------------------------------

    logger.info("=" * 60)
    logger.info("DATA INGESTION PIPELINE FINISHED")
    logger.info("TOTAL TASKS: %s", len(task_results))
    logger.info("SUCCESSFUL TASKS: %s", successful_tasks)
    logger.info("FAILED TASKS: %s", failed_tasks)
    logger.info("TOTAL DURATION: %s seconds", total_duration)
    logger.info("OVERALL STATUS: %s", summary["overall_status"])
    logger.info("SUMMARY FILE: %s", summary_file)
    logger.info("LOG FILE: %s", LOG_FILE)
    logger.info("=" * 60)

    if failed_tasks > 0:
        logger.warning(
            "Some tasks failed. Review the pipeline log and JSON summary."
        )
        return 1

    return 0


# --------------------------------------------------
# 8. MAIN ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    exit_code = run_pipeline()
    sys.exit(exit_code)
