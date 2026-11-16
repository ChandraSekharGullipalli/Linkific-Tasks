
"""
Day 21 - Format Conversion Examples

Convert employee data between:
CSV, JSON, XML, Parquet and Avro.

Also read every converted format and verify record counts.
"""

import json
import logging
from pathlib import Path

import pandas as pd
from lxml import etree
from fastavro import writer, reader, parse_schema


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR / "FTP_SFTP" / "local_server" / "employees.csv"
)

OUTPUT_DIR = BASE_DIR / "output" / "Format_Conversion"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "employees.csv"
JSON_FILE = OUTPUT_DIR / "employees.json"
XML_FILE = OUTPUT_DIR / "employees.xml"
PARQUET_FILE = OUTPUT_DIR / "employees.parquet"
AVRO_FILE = OUTPUT_DIR / "employees.avro"

LOG_FILE = LOG_DIR / "format_conversion.log"


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# --------------------------------------------------
# 3. READ SOURCE CSV
# --------------------------------------------------

def read_source_data():

    print("\n1. Reading source CSV...")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Source file not found: {INPUT_FILE}"
        )

    dataframe = pd.read_csv(INPUT_FILE)

    required_columns = [
        "employee_id",
        "employee_name",
        "department",
        "salary"
    ]

    if not all(column in dataframe.columns for column in required_columns):
        raise ValueError("Source CSV is missing required columns.")

    print("Source data loaded successfully.")
    print("Total records:", len(dataframe))

    logging.info(
        "Source CSV loaded. Records: %s",
        len(dataframe)
    )

    return dataframe


# --------------------------------------------------
# 4. CSV CONVERSION
# --------------------------------------------------

def convert_to_csv(dataframe):

    dataframe.to_csv(CSV_FILE, index=False)

    print("CSV conversion completed.")
    logging.info("CSV conversion completed.")


# --------------------------------------------------
# 5. JSON CONVERSION
# --------------------------------------------------

def convert_to_json(dataframe):

    records = dataframe.to_dict(orient="records")

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)

    print("JSON conversion completed.")
    logging.info("JSON conversion completed.")


# --------------------------------------------------
# 6. XML CONVERSION
# --------------------------------------------------

def convert_to_xml(dataframe):

    root = etree.Element("employees")

    for record in dataframe.to_dict(orient="records"):

        employee = etree.SubElement(root, "employee")

        for column, value in record.items():

            field = etree.SubElement(employee, column)
            field.text = str(value)

    tree = etree.ElementTree(root)

    tree.write(
        str(XML_FILE),
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8"
    )

    print("XML conversion completed.")
    logging.info("XML conversion completed.")


# --------------------------------------------------
# 7. PARQUET CONVERSION
# --------------------------------------------------

def convert_to_parquet(dataframe):

    dataframe.to_parquet(
        PARQUET_FILE,
        index=False,
        engine="pyarrow"
    )

    print("Parquet conversion completed.")
    logging.info("Parquet conversion completed.")


# --------------------------------------------------
# 8. AVRO CONVERSION
# --------------------------------------------------

def convert_to_avro(dataframe):

    schema = {
        "type": "record",
        "name": "Employee",
        "namespace": "linkific.day21",
        "fields": [
            {"name": "employee_id", "type": "int"},
            {"name": "employee_name", "type": "string"},
            {"name": "department", "type": "string"},
            {"name": "salary", "type": "int"}
        ]
    }

    parsed_schema = parse_schema(schema)

    records = []

    for row in dataframe.itertuples(index=False):

        records.append({
            "employee_id": int(row.employee_id),
            "employee_name": str(row.employee_name),
            "department": str(row.department),
            "salary": int(row.salary)
        })

    with open(AVRO_FILE, "wb") as file:
        writer(file, parsed_schema, records)

    print("Avro conversion completed.")
    logging.info("Avro conversion completed.")


# --------------------------------------------------
# 9. READ AND VERIFY ALL FORMATS
# --------------------------------------------------

def verify_conversions(expected_count):

    print("\n2. Verifying converted files...")

    # Read CSV
    csv_data = pd.read_csv(CSV_FILE)

    # Read JSON
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    json_df = pd.DataFrame(json_data)

    # Read XML
    tree = etree.parse(str(XML_FILE))

    xml_records = []

    for employee in tree.getroot().findall("employee"):

        xml_records.append({
            "employee_id": int(employee.findtext("employee_id")),
            "employee_name": employee.findtext("employee_name"),
            "department": employee.findtext("department"),
            "salary": int(employee.findtext("salary"))
        })

    xml_df = pd.DataFrame(xml_records)

    # Read Parquet
    parquet_data = pd.read_parquet(PARQUET_FILE)

    # Read Avro
    with open(AVRO_FILE, "rb") as file:
        avro_records = list(reader(file))

    avro_df = pd.DataFrame(avro_records)

    results = {
        "CSV": len(csv_data),
        "JSON": len(json_df),
        "XML": len(xml_df),
        "Parquet": len(parquet_data),
        "Avro": len(avro_df)
    }

    print("\nFormat verification results:")

    all_passed = True

    for format_name, count in results.items():

        status = "PASS" if count == expected_count else "FAIL"

        print(
            f"{format_name:10} | "
            f"Records: {count} | "
            f"{status}"
        )

        logging.info(
            "%s verification: %s records - %s",
            format_name,
            count,
            status
        )

        if count != expected_count:
            all_passed = False

    if not all_passed:
        raise ValueError("One or more format conversions failed verification.")

    print("\nAll format conversions verified successfully!")

    logging.info("All format conversions verified successfully.")


# --------------------------------------------------
# 10. MAIN EXECUTION
# --------------------------------------------------

def main():

    try:

        print("=" * 55)
        print("DAY 21 - DATA FORMAT CONVERSION")
        print("=" * 55)

        dataframe = read_source_data()

        print("\n2. Converting employee data...")

        convert_to_csv(dataframe)
        convert_to_json(dataframe)
        convert_to_xml(dataframe)
        convert_to_parquet(dataframe)
        convert_to_avro(dataframe)

        verify_conversions(len(dataframe))

        print("\nOutput folder:", OUTPUT_DIR)
        print("Log file:", LOG_FILE)

        print("\nPROJECT COMPLETED SUCCESSFULLY!")

    except Exception as error:

        logging.exception("Format conversion failed.")

        print("\nERROR:", error)


if __name__ == "__main__":
    main()
