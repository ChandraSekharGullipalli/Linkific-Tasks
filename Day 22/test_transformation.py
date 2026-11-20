
from pathlib import Path

import pandas as pd
import pytest

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "transformed"

EXPECTED_FILES = {
    "customers_transformed.csv": 1000,
    "products_transformed.csv": 200,
    "sales_transformed.csv": 2516,
    "transactions_transformed.csv": 1000,
    "monthly_sales_summary.csv": 25,
    "customer_sales_summary.csv": 627,
}


@pytest.mark.parametrize(
    "filename, expected_rows",
    EXPECTED_FILES.items()
)
def test_transformed_file_exists(filename, expected_rows):
    """Check that every expected transformed CSV exists."""

    file_path = DATA_DIR / filename

    assert file_path.exists(), f"Missing transformed file: {filename}"


@pytest.mark.parametrize(
    "filename, expected_rows",
    EXPECTED_FILES.items()
)
def test_transformed_record_count(filename, expected_rows):
    """Check the number of records in each transformed CSV."""

    file_path = DATA_DIR / filename

    assert file_path.exists(), f"Missing transformed file: {filename}"

    df = pd.read_csv(file_path)

    assert len(df) == expected_rows, (
        f"{filename}: expected {expected_rows} rows, "
        f"found {len(df)}"
    )


@pytest.mark.parametrize(
    "filename",
    EXPECTED_FILES.keys()
)
def test_transformed_file_not_empty(filename):
    """Check that transformed files contain columns."""

    file_path = DATA_DIR / filename

    assert file_path.exists(), f"Missing transformed file: {filename}"

    df = pd.read_csv(file_path)

    assert len(df.columns) > 0, (
        f"{filename} contains no columns"
    )
