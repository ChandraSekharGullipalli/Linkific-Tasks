
"""
DAY 23 - RAW DATA STAGING

Copies collected raw JSON files into a structured staging layer.
Preserves existing files and avoids unnecessary recopying.
"""

import json
import logging
import shutil

from datetime import datetime
from pathlib import Path


# --------------------------------------------------
# 1. PROJECT DIRECTORIES
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DIR = BASE_DIR / "data" / "raw"
STAGING_DIR = BASE_DIR / "data" / "staging"

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "raw_staging.log"


# --------------------------------------------------
# 2. LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. SOURCE MAPPING
# --------------------------------------------------

SOURCE_FOLDERS = {
    "api": RAW_DIR / "api",
    "scraped": RAW_DIR / "scraped",
    "database": RAW_DIR / "database"
}

STAGING_RAW_DIR = STAGING_DIR / "raw"

MANIFEST_FILE = STAGING_RAW_DIR / "staging_manifest.json"


# --------------------------------------------------
# 4. COPY RAW DATA
# --------------------------------------------------

def stage_source(source_name, source_folder):

    destination_folder = STAGING_RAW_DIR / source_name

    destination_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    copied_files = 0
    unchanged_files = 0
    failed_files = 0
    file_details = []

    if not source_folder.exists():

        logger.warning(
            "Source folder not found: %s",
            source_folder
        )

        return {
            "source": source_name,
            "status": "SOURCE_NOT_FOUND",
            "copied": 0,
            "unchanged": 0,
            "failed": 0,
            "files": []
        }

    json_files = sorted(source_folder.glob("*.json"))

    for source_file in json_files:

        # Watermarks are extraction state, not raw business data.
        if source_file.name == "watermarks.json":
            continue

        destination_file = destination_folder / source_file.name

        try:

            needs_copy = (
                not destination_file.exists()
                or source_file.stat().st_size != destination_file.stat().st_size
                or source_file.stat().st_mtime_ns != destination_file.stat().st_mtime_ns
            )

            if needs_copy:

                shutil.copy2(
                    source_file,
                    destination_file
                )

                copied_files += 1

                logger.info(
                    "COPIED: %s -> %s",
                    source_file.name,
                    destination_file
                )

            else:

                unchanged_files += 1

                logger.info(
                    "UNCHANGED: %s",
                    source_file.name
                )

            file_details.append({
                "file_name": source_file.name,
                "size_bytes": destination_file.stat().st_size,
                "status": "COPIED" if needs_copy else "UNCHANGED"
            })

        except Exception as error:

            failed_files += 1

            logger.exception(
                "FAILED TO STAGE %s: %s",
                source_file.name,
                error
            )

    return {
        "source": source_name,
        "status": "SUCCESS" if failed_files == 0 else "PARTIAL_FAILURE",
        "source_file_count": len(json_files),
        "copied": copied_files,
        "unchanged": unchanged_files,
        "failed": failed_files,
        "files": file_details
    }


# --------------------------------------------------
# 5. RUN STAGING PROCESS
# --------------------------------------------------

def run_staging():

    start_time = datetime.now()

    logger.info("=" * 60)
    logger.info("RAW DATA STAGING STARTED")
    logger.info("=" * 60)

    source_results = []

    for source_name, source_folder in SOURCE_FOLDERS.items():

        logger.info("PROCESSING SOURCE: %s", source_name)

        result = stage_source(
            source_name,
            source_folder
        )

        source_results.append(result)

    # --------------------------------------------------
    # 6. CREATE STAGING MANIFEST
    # --------------------------------------------------

    total_copied = sum(
        item["copied"] for item in source_results
    )

    total_unchanged = sum(
        item["unchanged"] for item in source_results
    )

    total_failed = sum(
        item["failed"] for item in source_results
    )

    end_time = datetime.now()

    manifest = {
        "pipeline": "Day 23 Raw Data Staging",
        "started_at": start_time.isoformat(),
        "completed_at": end_time.isoformat(),
        "duration_seconds": round(
            (end_time - start_time).total_seconds(), 2
        ),
        "total_sources": len(source_results),
        "total_copied": total_copied,
        "total_unchanged": total_unchanged,
        "total_failed": total_failed,
        "overall_status": (
            "SUCCESS" if total_failed == 0 else "PARTIAL_FAILURE"
        ),
        "sources": source_results
    }

    STAGING_RAW_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        MANIFEST_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            manifest,
            file,
            indent=4
        )

    logger.info("=" * 60)
    logger.info("RAW DATA STAGING COMPLETED")
    logger.info("FILES COPIED: %s", total_copied)
    logger.info("FILES UNCHANGED: %s", total_unchanged)
    logger.info("FILES FAILED: %s", total_failed)
    logger.info("MANIFEST: %s", MANIFEST_FILE)
    logger.info("LOG: %s", LOG_FILE)
    logger.info("=" * 60)

    return 1 if total_failed > 0 else 0


# --------------------------------------------------
# 7. MAIN
# --------------------------------------------------

if __name__ == "__main__":

    exit_code = run_staging()

    raise SystemExit(exit_code)
