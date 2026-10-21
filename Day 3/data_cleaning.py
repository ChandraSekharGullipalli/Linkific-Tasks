
import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Input and output files
INPUT_FILE = DATA_DIR / "books_main.csv"
OUTPUT_FILE = DATA_DIR / "books_cleaned.csv"
REPORT_FILE = DATA_DIR / "cleaning_report.txt"


def clean_data():
    if not INPUT_FILE.exists():
        print(f"Input file not found: {INPUT_FILE}")
        print("Run scrape_datasets.py first.")
        return

    # Load the scraped dataset
    df = pd.read_csv(INPUT_FILE)

    original_rows = len(df)
    original_missing = int(df.isna().sum().sum())

    # Standardize column names
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_")
    )

    # Remove duplicate records
    df = df.drop_duplicates()

    # Clean text fields
    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].map(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

    # Standardize title capitalization
    if "title" in df.columns:
        df["title"] = df["title"].replace("", pd.NA)

    # Clean price and create a numeric price column
    if "price" in df.columns:
        df["price_numeric"] = pd.to_numeric(
            df["price"]
            .astype("string")
            .str.replace(r"[£$€]", "", regex=True)
            .str.strip(),
            errors="coerce",
        )

    # Normalize availability values
    if "availability" in df.columns:
        df["availability"] = (
            df["availability"]
            .astype("string")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    # Identify missing values instead of inventing replacements
    missing_by_column = df.isna().sum()

    # Save the cleaned dataset
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    # Create a cleaning report
    report = [
        "DATA CLEANING REPORT",
        "=" * 35,
        f"Input file: {INPUT_FILE.name}",
        f"Output file: {OUTPUT_FILE.name}",
        f"Rows before cleaning: {original_rows}",
        f"Rows after cleaning: {len(df)}",
        f"Duplicate rows removed: {original_rows - len(df)}",
        f"Missing values before cleaning: {original_missing}",
        "",
        "Missing values after cleaning:",
    ]

    for column, count in missing_by_column.items():
        report.append(f"{column}: {count}")

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print("\nData cleaning completed successfully!")
    print(f"Rows before cleaning: {original_rows}")
    print(f"Rows after cleaning: {len(df)}")
    print(f"Cleaned dataset: {OUTPUT_FILE}")
    print(f"Cleaning report: {REPORT_FILE}")


if __name__ == "__main__":
    clean_data()
