
from pathlib import Path
import pandas as pd
import pytest

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "data" / "quality_reports"


def test_quality_report_directory_exists():
    """Check that the quality report directory exists."""
    assert REPORT_DIR.exists()


def test_quality_report_files_exist():
    """Check that quality report files have been generated."""

    files = list(REPORT_DIR.glob("*"))

    assert files, "No quality report files found"


def test_quality_report_csv_has_data():
    """Check that at least one CSV report contains data."""

    csv_files = list(REPORT_DIR.glob("*.csv"))

    assert csv_files, "No CSV quality report found"

    valid_reports = []

    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)

            if not df.empty:
                valid_reports.append(file_path.name)

        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            continue

    assert valid_reports, "No non-empty quality CSV report found"


def test_quality_framework_log_exists():
    """Check whether a quality framework log is available."""

    log_dir = BASE_DIR / "logs"

    assert log_dir.exists(), "Logs directory is missing"

    log_files = list(log_dir.glob("*"))

    assert log_files, "No log files found"
