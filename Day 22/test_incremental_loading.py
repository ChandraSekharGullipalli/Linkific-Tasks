
import json
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "data" / "state" / "warehouse_watermarks.json"

EXPECTED_WATERMARKS = {
    "customers": 1000,
    "products": 200,
    "order_items": 2516,
    "transactions": 1000
}


@pytest.fixture
def watermarks():
    """Read the warehouse watermark file."""

    assert STATE_FILE.exists(), "Warehouse watermark file is missing"

    with STATE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_watermark_file_exists():
    """Verify that the watermark file exists."""

    assert STATE_FILE.exists()


def test_watermark_file_contains_valid_json():
    """Verify that the watermark file contains valid JSON."""

    with STATE_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, dict)


@pytest.mark.parametrize(
    "table, expected_value",
    EXPECTED_WATERMARKS.items()
)
def test_watermark_values(watermarks, table, expected_value):
    """Verify the expected incremental checkpoint values."""

    assert table in watermarks, f"Missing watermark: {table}"

    assert watermarks[table] == expected_value, (
        f"{table}: expected {expected_value}, "
        f"found {watermarks[table]}"
    )


def test_watermarks_are_non_negative(watermarks):
    """Ensure that watermark values are non-negative integers."""

    for table, value in watermarks.items():
        assert isinstance(value, int), f"{table} watermark is not an integer"
        assert value >= 0, f"{table} watermark cannot be negative"
