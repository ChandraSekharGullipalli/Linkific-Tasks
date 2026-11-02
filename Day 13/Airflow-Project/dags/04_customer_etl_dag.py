
import csv
import os
import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

INPUT_FILE = "/opt/airflow/dags/data/customers.csv"
OUTPUT_FILE = "/opt/airflow/dags/data/cleaned_customers.csv"


def extract_data(ti):
    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    print("Extracted records:", len(records))
    ti.xcom_push(key="raw_data", value=records)


def transform_data(ti):
    records = ti.xcom_pull(task_ids="extract_task", key="raw_data")

    cleaned_records = []

    for row in records:
        if row["customer_id"].strip() and row["email"].strip():
            cleaned_records.append({
                "customer_id": row["customer_id"].strip(),
                "name": row["name"].strip().title(),
                "email": row["email"].strip().lower(),
                "city": row["city"].strip().title()
            })

    print("Cleaned records:", len(cleaned_records))
    ti.xcom_push(key="cleaned_data", value=cleaned_records)


def load_data(ti):
    records = ti.xcom_pull(task_ids="transform_task", key="cleaned_data")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["customer_id", "name", "email", "city"]
        )
        writer.writeheader()
        writer.writerows(records)

    print("Loaded records:", len(records))


def validate_data():
    with open(OUTPUT_FILE, "r", newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    assert len(records) > 0, "No records found!"

    for row in records:
        assert row["customer_id"], "Missing customer ID"
        assert row["email"], "Missing email"

    print("Data quality validation passed!")
    print("Total valid records:", len(records))


with DAG(
    dag_id="customer_etl_pipeline",
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["day13", "etl", "data-engineering"],
) as dag:

    extract = PythonOperator(
        task_id="extract_task",
        python_callable=extract_data
    )

    transform = PythonOperator(
        task_id="transform_task",
        python_callable=transform_data
    )

    load = PythonOperator(
        task_id="load_task",
        python_callable=load_data
    )

    quality = PythonOperator(
        task_id="data_quality_task",
        python_callable=validate_data
    )

    extract >> transform >> load >> quality
