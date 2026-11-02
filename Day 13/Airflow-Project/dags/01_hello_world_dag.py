import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def hello_world():
    print("Hello! Welcome to Apache Airflow.")
    print("My first Airflow DAG is running successfully!")


with DAG(
    dag_id="hello_world_dag",
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["day13", "beginner"]
) as dag:

    hello_task = PythonOperator(
        task_id="hello_world_task",
        python_callable=hello_world
    )
    