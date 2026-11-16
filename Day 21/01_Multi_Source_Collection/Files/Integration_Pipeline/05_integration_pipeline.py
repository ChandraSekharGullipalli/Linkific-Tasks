
"""
DAY 21 - DATA INTEGRATION PIPELINE

Sources:
1. PostgreSQL customer and product CSV exports
2. API product CSV export
3. File-based customer, product and employee CSV exports
4. SQLite employee CSV export
5. SFTP employee CSV export

Outputs:
Unified customer, product and employee datasets.
"""

import logging
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "output" / "Integration_Pipeline"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "integration_pipeline.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ==================================================
# 2. SOURCE FILE LOCATIONS
# ==================================================

SOURCES = {
    "postgresql_customers":
        BASE_DIR / "output/Databases/postgresql_customers.csv",

    "file_customers":
        BASE_DIR / "output/Files/collected_customers.csv",

    "api_products":
        BASE_DIR / "output/APIs/products.csv",

    "postgresql_products":
        BASE_DIR / "output/Databases/postgresql_products.csv",

    "file_products":
        BASE_DIR / "output/Files/collected_products.csv",

    "sqlite_employees":
        BASE_DIR / "output/Databases/sqlite_employees.csv",

    "file_employees":
        BASE_DIR / "output/Files/collected_employees.csv",

    "sftp_employees":
        BASE_DIR / "output/FTP_SFTP/employees_downloaded_paramiko.csv"
}


# ==================================================
# 3. SOURCE PRIORITY
# LOWER NUMBER = HIGHER PRIORITY
# ==================================================

SOURCE_PRIORITY = {
    "postgresql_customers": 1,
    "file_customers": 2,

    "postgresql_products": 1,
    "file_products": 2,
    "api_products": 3,

    "sqlite_employees": 1,
    "file_employees": 2,
    "sftp_employees": 3
}


# ==================================================
# 4. LOGGING AND SOURCE LOADING
# ==================================================

def load_and_map(source_name, mapping, standard_columns):

    file_path = SOURCES[source_name]

    if not file_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    raw_df = pd.read_csv(file_path)

    mapped_df = pd.DataFrame(index=raw_df.index)

    for target_column, source_column in mapping.items():

        if source_column in raw_df.columns:
            mapped_df[target_column] = raw_df[source_column]
        else:
            mapped_df[target_column] = pd.NA

    for column in standard_columns:

        if column not in mapped_df.columns:
            mapped_df[column] = pd.NA

    # Preserve the original source record ID.
    mapped_df["source_record_id"] = (
        mapped_df["source_record_id"].astype("string")
    )

    mapped_df["source_system"] = source_name

    mapped_df["ingested_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    # Standardize text values.
    for column in mapped_df.select_dtypes(
        include=["object", "string"]
    ).columns:

        mapped_df[column] = (
            mapped_df[column]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    logging.info(
        "Loaded %s: %s records",
        source_name,
        len(mapped_df)
    )

    print(
        f"Loaded {source_name}: {len(mapped_df)} records"
    )

    return mapped_df


# ==================================================
# 5. CREATE DEDUPLICATION KEYS
# ==================================================

def normalize_key(value):

    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def create_dedupe_key(row, entity):

    if entity == "customers":

        email = normalize_key(row["email"])

        if email:
            return "email:" + email

        return (
            "name_city:"
            + normalize_key(row["customer_name"])
            + "|"
            + normalize_key(row["city"])
        )

    elif entity == "products":

        return (
            normalize_key(row["product_name"])
            + "|"
            + normalize_key(row["category"])
        )

    elif entity == "employees":

        email = normalize_key(row["email"])

        if email:
            return "email:" + email

        return (
            "employee:"
            + normalize_key(row["employee_name"])
            + "|"
            + normalize_key(row["department"])
            + "|"
            + normalize_key(row["department_id"])
            + "|"
            + normalize_key(row["salary"])
        )


# ==================================================
# 6. STANDARDIZE AND INTEGRATE DATASETS
# ==================================================

def integrate_entity(dataframes, entity, output_columns):

    combined = pd.concat(
        dataframes,
        ignore_index=True
    )

    if combined.empty:
        raise ValueError(f"No records found for {entity}")

    # Create matching key.
    combined["_dedupe_key"] = combined.apply(
        lambda row: create_dedupe_key(row, entity),
        axis=1
    )

    # Sort by source priority.
    combined["_priority"] = combined["source_system"].map(
        SOURCE_PRIORITY
    )

    combined = combined.sort_values(
        by="_priority",
        ascending=True
    )

    input_count = len(combined)

    # Resolve duplicate records.
    # Higher-priority source is retained.
    integrated = combined.drop_duplicates(
        subset=["_dedupe_key"],
        keep="first"
    ).copy()

    duplicate_count = input_count - len(integrated)

    integrated = integrated.drop(
        columns=["_dedupe_key", "_priority"]
    )

    # Keep the standard output column order.
    integrated = integrated[output_columns]

    print(f"\n{entity.upper()} INTEGRATION")
    print("Input records:", input_count)
    print("Final records:", len(integrated))
    print("Duplicates removed:", duplicate_count)

    logging.info(
        "%s: input=%s, final=%s, duplicates=%s",
        entity,
        input_count,
        len(integrated),
        duplicate_count
    )

    return integrated, input_count, duplicate_count


# ==================================================
# 7. SAVE OUTPUTS
# ==================================================

def save_dataset(dataframe, entity):

    csv_path = OUTPUT_DIR / f"integrated_{entity}.csv"
    json_path = OUTPUT_DIR / f"integrated_{entity}.json"

    dataframe.to_csv(csv_path, index=False)

    dataframe.to_json(
        json_path,
        orient="records",
        indent=4
    )

    print("CSV saved:", csv_path.name)
    print("JSON saved:", json_path.name)

    logging.info(
        "Saved %s CSV and JSON outputs",
        entity
    )


# ==================================================
# 8. CREATE DATA LINEAGE REPORT
# ==================================================

def create_lineage_report(lineage_rows):

    lineage_df = pd.DataFrame(lineage_rows)

    lineage_path = OUTPUT_DIR / "data_lineage.csv"

    lineage_df.to_csv(
        lineage_path,
        index=False
    )

    print("\nDATA LINEAGE REPORT")
    print(lineage_df.to_string(index=False))

    logging.info("Data lineage report created.")

    return lineage_df


# ==================================================
# 9. MAIN INTEGRATION PIPELINE
# ==================================================

def main():

    print("=" * 60)
    print("DAY 21 - DATA INTEGRATION PIPELINE")
    print("=" * 60)

    logging.info("Integration pipeline started.")

    lineage_rows = []

    # ------------------------------------------------
    # CUSTOMER DATA
    # ------------------------------------------------

    customer_columns = [
        "source_record_id",
        "customer_name",
        "email",
        "phone",
        "city",
        "age",
        "created_at",
        "source_system",
        "ingested_at"
    ]

    pg_customers = load_and_map(
        "postgresql_customers",
        {
            "source_record_id": "customer_id",
            "customer_name": "customer_name",
            "email": "email",
            "phone": "phone",
            "city": "city",
            "age": "age",
            "created_at": "created_at"
        },
        customer_columns
    )

    file_customers = load_and_map(
        "file_customers",
        {
            "source_record_id": "customer_id",
            "customer_name": "name",
            "city": "city",
            "age": "age"
        },
        customer_columns
    )

    customers, count, duplicates = integrate_entity(
        [pg_customers, file_customers],
        "customers",
        customer_columns
    )

    save_dataset(customers, "customers")

    lineage_rows.append({
        "entity": "customers",
        "input_records": count,
        "output_records": len(customers),
        "duplicates_removed": duplicates,
        "sources": "PostgreSQL, Files"
    })

    # ------------------------------------------------
    # PRODUCT DATA
    # ------------------------------------------------

    product_columns = [
        "source_record_id",
        "product_name",
        "category",
        "price",
        "stock_quantity",
        "brand",
        "source_system",
        "ingested_at"
    ]

    api_products = load_and_map(
        "api_products",
        {
            "source_record_id": "id",
            "product_name": "title",
            "category": "category",
            "price": "price",
            "stock_quantity": "stock",
            "brand": "brand"
        },
        product_columns
    )

    pg_products = load_and_map(
        "postgresql_products",
        {
            "source_record_id": "product_id",
            "product_name": "product_name",
            "category": "category",
            "price": "price",
            "stock_quantity": "stock_quantity"
        },
        product_columns
    )

    file_products = load_and_map(
        "file_products",
        {
            "source_record_id": "product_id",
            "product_name": "product_name",
            "category": "category",
            "price": "price"
        },
        product_columns
    )

    products, count, duplicates = integrate_entity(
        [pg_products, file_products, api_products],
        "products",
        product_columns
    )

    products["price"] = pd.to_numeric(
        products["price"],
        errors="coerce"
    )

    products["stock_quantity"] = pd.to_numeric(
        products["stock_quantity"],
        errors="coerce"
    )

    save_dataset(products, "products")

    lineage_rows.append({
        "entity": "products",
        "input_records": count,
        "output_records": len(products),
        "duplicates_removed": duplicates,
        "sources": "PostgreSQL, Files, API"
    })

    # ------------------------------------------------
    # EMPLOYEE DATA
    # ------------------------------------------------

    employee_columns = [
        "source_record_id",
        "employee_name",
        "email",
        "department",
        "department_id",
        "salary",
        "source_system",
        "ingested_at"
    ]

    sqlite_employees = load_and_map(
        "sqlite_employees",
        {
            "source_record_id": "employee_id",
            "employee_name": "employee_name",
            "email": "email",
            "department_id": "department_id",
            "salary": "salary"
        },
        employee_columns
    )

    file_employees = load_and_map(
        "file_employees",
        {
            "source_record_id": "employee_id",
            "employee_name": "employee_name",
            "department": "department",
            "salary": "salary"
        },
        employee_columns
    )

    sftp_employees = load_and_map(
        "sftp_employees",
        {
            "source_record_id": "employee_id",
            "employee_name": "employee_name",
            "department": "department",
            "salary": "salary"
        },
        employee_columns
    )

    employees, count, duplicates = integrate_entity(
        [sqlite_employees, file_employees, sftp_employees],
        "employees",
        employee_columns
    )

    employees["salary"] = pd.to_numeric(
        employees["salary"],
        errors="coerce"
    )

    save_dataset(employees, "employees")

    lineage_rows.append({
        "entity": "employees",
        "input_records": count,
        "output_records": len(employees),
        "duplicates_removed": duplicates,
        "sources": "SQLite, Files, SFTP"
    })

    # ------------------------------------------------
    # DATA LINEAGE
    # ------------------------------------------------

    create_lineage_report(lineage_rows)

    # ------------------------------------------------
    # FINAL VALIDATION
    # ------------------------------------------------

    print("\nFINAL VALIDATION")

    datasets = {
        "Customers": customers,
        "Products": products,
        "Employees": employees
    }

    for name, dataframe in datasets.items():

        if dataframe.empty:
            raise ValueError(f"{name} dataset is empty.")

        print(
            f"{name}: {len(dataframe)} records - PASS"
        )

    print("\nAll integrated datasets created successfully!")

    print("Output folder:", OUTPUT_DIR)
    print("Log file:", LOG_FILE)

    logging.info("Integration pipeline completed successfully.")


# ==================================================
# 10. EXECUTE
# ==================================================

if __name__ == "__main__":

    try:
        main()

    except Exception as error:

        logging.exception(
            "Integration pipeline failed."
        )

        print("\nPIPELINE ERROR:", error)
