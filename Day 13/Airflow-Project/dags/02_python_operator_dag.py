
import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def extract_data():
    print("Step 1: Extracting data...")
    print("Data extracted successfully.")


def transform_data():
    print("Step 2: Transforming data...")
    print("Data transformed successfully.")


def load_data():
    print("Step 3: Loading data...")
    print("Data loaded successfully.")


with DAG(
    dag_id="python_operator_dag",
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["day13", "python"]
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

    extract >> transform >> load
