
import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="bash_operator_dag",
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["day13", "bash"]
) as dag:

    first_task = BashOperator(
        task_id="display_message",
        bash_command="echo 'Welcome to Apache Airflow'"
    )

    second_task = BashOperator(
        task_id="display_date",
        bash_command="date"
    )

    third_task = BashOperator(
        task_id="display_directory",
        bash_command="pwd && ls -la"
    )

    first_task >> second_task >> third_task
