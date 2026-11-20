
"""
DAY 22 - DATA QUALITY FRAMEWORK

Validates transformed datasets for:
1. Completeness
2. Uniqueness
3. Validity
4. Range checks
5. Referential integrity
6. Data consistency

Outputs:
- data_quality_report.csv
- data_quality_summary.txt
- Invalid records in quarantine folder
"""

import logging
from pathlib import Path

import pandas as pd


# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = PROJECT_ROOT / "data" / "transformed"
REPORT_DIR = PROJECT_ROOT / "data" / "quality_reports"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "quarantine"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ==================================================
# 2. LOGGING CONFIGURATION
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "data_quality.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


# ==================================================
# 3. LOAD TRANSFORMED DATASETS
# ==================================================

def load_datasets():

    logger.info("Loading transformed datasets.")

    filenames = {
        "customers": "customers_transformed.csv",
        "products": "products_transformed.csv",
        "sales": "sales_transformed.csv",
        "transactions": "transactions_transformed.csv",
        "monthly_summary": "monthly_sales_summary.csv",
        "customer_summary": "customer_sales_summary.csv"
    }

    datasets = {}

    for name, filename in filenames.items():

        file_path = INPUT_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required dataset not found: {file_path}"
            )

        datasets[name] = pd.read_csv(file_path)

        logger.info(
            "Loaded %s: %s records",
            filename,
            len(datasets[name])
        )

    return datasets


# ==================================================
# 4. QUALITY CHECK HELPER
# ==================================================

quality_results = []
invalid_records = {}


def record_result(
    dataset,
    rule,
    total_records,
    failed_records,
    description
):

    passed_records = total_records - failed_records

    status = "PASS" if failed_records == 0 else "FAIL"

    quality_results.append({
        "dataset": dataset,
        "quality_rule": rule,
        "total_records": total_records,
        "passed_records": passed_records,
        "failed_records": failed_records,
        "status": status,
        "description": description
    })

    logger.info(
        "%s | %s | Passed: %s | Failed: %s",
        dataset,
        rule,
        passed_records,
        failed_records
    )


def save_invalid_records(dataset, rule, dataframe, mask):

    invalid = dataframe.loc[mask].copy()

    if invalid.empty:
        return

    invalid["failed_quality_rule"] = rule

    invalid_records.setdefault(dataset, []).append(invalid)


def check_missing_values(dataset_name, dataframe, columns):

    for column in columns:

        if column not in dataframe.columns:
            logger.warning(
                "%s: Column %s not found.",
                dataset_name,
                column
            )
            continue

        mask = (
            dataframe[column].isna()
            | dataframe[column].astype("string").str.strip().eq("").fillna(False)
        )

        failed = int(mask.sum())

        record_result(
            dataset_name,
            f"Completeness - {column}",
            len(dataframe),
            failed,
            f"Check for missing values in {column}"
        )

        save_invalid_records(
            dataset_name,
            f"missing_{column}",
            dataframe,
            mask
        )


def check_positive_values(
    dataset_name,
    dataframe,
    column,
    allow_zero=False
):

    if column not in dataframe.columns:
        return

    values = pd.to_numeric(
        dataframe[column],
        errors="coerce"
    )

    if allow_zero:
        mask = values.isna() | (values < 0)
    else:
        mask = values.isna() | (values <= 0)

    failed = int(mask.sum())

    record_result(
        dataset_name,
        f"Range - {column}",
        len(dataframe),
        failed,
        f"Check valid numeric range for {column}"
    )

    save_invalid_records(
        dataset_name,
        f"invalid_{column}",
        dataframe,
        mask
    )


def check_unique(dataset_name, dataframe, column):

    if column not in dataframe.columns:
        return

    mask = (
        dataframe[column].isna()
        | dataframe[column].duplicated(keep=False)
    )

    failed = int(mask.sum())

    record_result(
        dataset_name,
        f"Uniqueness - {column}",
        len(dataframe),
        failed,
        f"Check missing or duplicate values in {column}"
    )

    save_invalid_records(
        dataset_name,
        f"duplicate_{column}",
        dataframe,
        mask
    )


# ==================================================
# 5. CUSTOMER QUALITY CHECKS
# ==================================================

def validate_customers(customers):

    logger.info("Validating customers.")

    check_missing_values(
        "customers",
        customers,
        ["customer_id", "customer_name", "email"]
    )

    check_unique(
        "customers",
        customers,
        "customer_id"
    )

    if "email" in customers.columns:

        email = customers["email"].astype("string").str.strip()

        mask = ~email.str.match(
            r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
            na=False
        )

        record_result(
            "customers",
            "Validity - email format",
            len(customers),
            int(mask.sum()),
            "Check email address format"
        )

        save_invalid_records(
            "customers",
            "invalid_email",
            customers,
            mask
        )


# ==================================================
# 6. PRODUCT QUALITY CHECKS
# ==================================================

def validate_products(products):

    logger.info("Validating products.")

    check_missing_values(
        "products",
        products,
        ["product_id", "product_name", "category"]
    )

    check_unique(
        "products",
        products,
        "product_id"
    )

    check_positive_values(
        "products",
        products,
        "price"
    )

    check_positive_values(
        "products",
        products,
        "stock_quantity",
        allow_zero=True
    )


# ==================================================
# 7. SALES QUALITY CHECKS
# ==================================================

def validate_sales(sales, customers, products):

    logger.info("Validating sales.")

    check_missing_values(
        "sales",
        sales,
        [
            "order_item_id",
            "order_id",
            "customer_id",
            "product_id",
            "order_date"
        ]
    )

    check_unique(
        "sales",
        sales,
        "order_item_id"
    )

    check_positive_values(
        "sales",
        sales,
        "quantity"
    )

    check_positive_values(
        "sales",
        sales,
        "unit_price"
    )

    check_positive_values(
        "sales",
        sales,
        "line_total"
    )

    # Validate order dates.

    if "order_date" in sales.columns:

        dates = pd.to_datetime(
            sales["order_date"],
            errors="coerce"
        )

        mask = dates.isna()

        record_result(
            "sales",
            "Validity - order_date",
            len(sales),
            int(mask.sum()),
            "Check valid order dates"
        )

        save_invalid_records(
            "sales",
            "invalid_order_date",
            sales,
            mask
        )

    # Check customer references.

    if "customer_id" in sales.columns:

        mask = (
            sales["customer_id"].isna()
            | ~sales["customer_id"].isin(customers["customer_id"])
        )

        record_result(
            "sales",
            "Referential integrity - customer_id",
            len(sales),
            int(mask.sum()),
            "Every sales customer must exist in customers"
        )

        save_invalid_records(
            "sales",
            "invalid_customer_reference",
            sales,
            mask
        )

    # Check product references.

    if "product_id" in sales.columns:

        mask = (
            sales["product_id"].isna()
            | ~sales["product_id"].isin(products["product_id"])
        )

        record_result(
            "sales",
            "Referential integrity - product_id",
            len(sales),
            int(mask.sum()),
            "Every sales product must exist in products"
        )

        save_invalid_records(
            "sales",
            "invalid_product_reference",
            sales,
            mask
        )

    # Verify sales calculation.

    if all(
        column in sales.columns
        for column in ["quantity", "unit_price", "line_total"]
    ):

        expected_total = (
            pd.to_numeric(sales["quantity"], errors="coerce")
            * pd.to_numeric(sales["unit_price"], errors="coerce")
        )

        actual_total = pd.to_numeric(
            sales["line_total"],
            errors="coerce"
        )

        mask = (
            expected_total.isna()
            | actual_total.isna()
            | ~(
                (expected_total - actual_total).abs()
                <= 0.01
            )
        )

        record_result(
            "sales",
            "Consistency - line_total",
            len(sales),
            int(mask.sum()),
            "Check line_total = quantity multiplied by unit_price"
        )

        save_invalid_records(
            "sales",
            "incorrect_line_total",
            sales,
            mask
        )


# ==================================================
# 8. TRANSACTION QUALITY CHECKS
# ==================================================

def validate_transactions(transactions, sales):

    logger.info("Validating transactions.")

    check_missing_values(
        "transactions",
        transactions,
        [
            "transaction_id",
            "order_id",
            "transaction_date",
            "amount",
            "payment_method",
            "payment_status"
        ]
    )

    check_unique(
        "transactions",
        transactions,
        "transaction_id"
    )

    check_positive_values(
        "transactions",
        transactions,
        "amount"
    )

    if "transaction_date" in transactions.columns:

        dates = pd.to_datetime(
            transactions["transaction_date"],
            errors="coerce"
        )

        mask = dates.isna()

        record_result(
            "transactions",
            "Validity - transaction_date",
            len(transactions),
            int(mask.sum()),
            "Check valid transaction dates"
        )

        save_invalid_records(
            "transactions",
            "invalid_transaction_date",
            transactions,
            mask
        )

    if "order_id" in transactions.columns:

        valid_order_ids = sales["order_id"].dropna().unique()

        mask = (
            transactions["order_id"].isna()
            | ~transactions["order_id"].isin(valid_order_ids)
        )

        record_result(
            "transactions",
            "Referential integrity - order_id",
            len(transactions),
            int(mask.sum()),
            "Every transaction must reference an existing sales order"
        )

        save_invalid_records(
            "transactions",
            "invalid_transaction_order",
            transactions,
            mask
        )


# ==================================================
# 9. SUMMARY QUALITY CHECKS
# ==================================================

def validate_summaries(monthly_summary, customer_summary):

    logger.info("Validating summary datasets.")

    check_missing_values(
        "monthly_summary",
        monthly_summary,
        ["order_month", "total_revenue"]
    )

    check_missing_values(
        "customer_summary",
        customer_summary,
        ["customer_id", "total_revenue"]
    )

    check_unique(
        "customer_summary",
        customer_summary,
        "customer_id"
    )

    for name, dataframe in [
        ("monthly_summary", monthly_summary),
        ("customer_summary", customer_summary)
    ]:

        if "total_revenue" in dataframe.columns:

            values = pd.to_numeric(
                dataframe["total_revenue"],
                errors="coerce"
            )

            mask = values.isna() | (values < 0)

            record_result(
                name,
                "Range - total_revenue",
                len(dataframe),
                int(mask.sum()),
                "Revenue must be a valid non-negative number"
            )

            save_invalid_records(
                name,
                "invalid_total_revenue",
                dataframe,
                mask
            )


# ==================================================
# 10. SAVE QUARANTINED RECORDS
# ==================================================

def save_quarantine_records():

    logger.info("Saving invalid records.")

    for dataset_name, frames in invalid_records.items():

        combined = pd.concat(
            frames,
            ignore_index=True
        )

        output_path = (
            QUARANTINE_DIR
            / f"{dataset_name}_invalid_records.csv"
        )

        combined.to_csv(
            output_path,
            index=False
        )

        logger.info(
            "Quarantined %s records for %s",
            len(combined),
            dataset_name
        )


# ==================================================
# 11. GENERATE QUALITY REPORTS
# ==================================================

def generate_reports():

    report = pd.DataFrame(quality_results)

    report_path = REPORT_DIR / "data_quality_report.csv"

    report.to_csv(
        report_path,
        index=False
    )

    total_checks = len(report)

    passed_checks = int(
        (report["status"] == "PASS").sum()
    )

    failed_checks = int(
        (report["status"] == "FAIL").sum()
    )

    total_failed_records = int(
        report["failed_records"].sum()
    )

    pass_percentage = (
        passed_checks / total_checks * 100
        if total_checks else 0
    )

    summary = f"""
DAY 22 - DATA QUALITY SUMMARY
================================

Total quality checks : {total_checks}
Passed checks        : {passed_checks}
Failed checks        : {failed_checks}
Pass percentage      : {pass_percentage:.2f}%

Total failed record-check occurrences: {total_failed_records}

Report file:
{report_path}

Quarantine folder:
{QUARANTINE_DIR}

Note:
A record can fail more than one quality check.
Therefore, failed record-check occurrences are not necessarily
the number of unique invalid records.
"""

    summary_path = REPORT_DIR / "data_quality_summary.txt"

    summary_path.write_text(
        summary,
        encoding="utf-8"
    )

    logger.info("Data quality report generated.")
    logger.info("Total checks: %s", total_checks)
    logger.info("Passed checks: %s", passed_checks)
    logger.info("Failed checks: %s", failed_checks)
    logger.info("Pass percentage: %.2f%%", pass_percentage)


# ==================================================
# 12. MAIN DATA QUALITY PIPELINE
# ==================================================

def main():

    try:

        logger.info("=" * 55)
        logger.info("DATA QUALITY FRAMEWORK STARTED")
        logger.info("=" * 55)

        datasets = load_datasets()

        validate_customers(
            datasets["customers"]
        )

        validate_products(
            datasets["products"]
        )

        validate_sales(
            datasets["sales"],
            datasets["customers"],
            datasets["products"]
        )

        validate_transactions(
            datasets["transactions"],
            datasets["sales"]
        )

        validate_summaries(
            datasets["monthly_summary"],
            datasets["customer_summary"]
        )

        save_quarantine_records()

        generate_reports()

        logger.info("=" * 55)
        logger.info("DATA QUALITY FRAMEWORK COMPLETED")
        logger.info("=" * 55)

    except Exception:

        logger.exception(
            "Data quality framework failed."
        )

        raise


if __name__ == "__main__":
    main()
