
from datetime import datetime, timedelta, timezone
from pathlib import Path
import logging

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

logger = logging.getLogger("day22_failure_monitor")

# Docker-mounted Day 22 project directory
PROJECT_DIR = Path("/opt/day22")

# Python interpreter inside the Docker Airflow container
PYTHON = "/usr/local/bin/python"

# PostgreSQL runs on the Windows host
TASK_ENV = {
    "DB_HOST": "host.docker.internal",
    "PYTHONUNBUFFERED": "1",
}

def on_task_failure(context):
    task = context.get("task_instance")
    exception = context.get("exception")

    if task:
        logger.error(
            "TASK FAILED | DAG: %s | TASK: %s | RUN: %s | ERROR: %s",
            task.dag_id,
            task.task_id,
            task.run_id,
            exception,
        )

def on_task_retry(context):
    task = context.get("task_instance")

    if task:
        logger.warning(
            "TASK RETRY | DAG: %s | TASK: %s | TRY: %s",
            task.dag_id,
            task.task_id,
            task.try_number,
        )

DEFAULT_ARGS = {
    "owner": "linkific",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": on_task_failure,
    "on_retry_callback": on_task_retry,
}

with DAG(
    dag_id="day22_etl_pipeline",
    description="Day 22 ETL pipeline with monitoring and failure handling",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 11, 21, tzinfo=timezone.utc),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(hours=3),
    tags=["linkific", "day22", "etl", "data-engineering"],
) as dag:

    ingestion = BashOperator(
        task_id="data_ingestion",
        bash_command=(
            f'"{PYTHON}" '
            f'"{PROJECT_DIR}/src/ingestion/ingestion_pipeline.py"'
        ),
        cwd=str(PROJECT_DIR),
        env=TASK_ENV,
        append_env=True,
        execution_timeout=timedelta(minutes=60),
    )

    transformation = BashOperator(
        task_id="data_transformation",
        bash_command=(
            f'"{PYTHON}" '
            f'"{PROJECT_DIR}/src/transformation/transform_data.py"'
        ),
        cwd=str(PROJECT_DIR),
        env=TASK_ENV,
        append_env=True,
        execution_timeout=timedelta(minutes=60),
    )

    warehouse_loading = BashOperator(
        task_id="incremental_warehouse_loading",
        bash_command=(
            f'"{PYTHON}" '
            f'"{PROJECT_DIR}/src/loading/incremental_warehouse_loader.py"'
        ),
        cwd=str(PROJECT_DIR),
        env=TASK_ENV,
        append_env=True,
        execution_timeout=timedelta(minutes=60),
    )

    data_quality = BashOperator(
        task_id="data_quality_checks",
        bash_command=(
            f'"{PYTHON}" '
            f'"{PROJECT_DIR}/src/data_quality/data_quality_framework.py"'
        ),
        cwd=str(PROJECT_DIR),
        env=TASK_ENV,
        append_env=True,
        execution_timeout=timedelta(minutes=60),
    )

    quality_gate = BashOperator(
        task_id="data_quality_gate",
        bash_command=f"""
"{PYTHON}" - <<'CHECK'
import csv
from pathlib import Path

report = Path("data/quality_reports/data_quality_report.csv")

if not report.is_file():
    raise FileNotFoundError(f"Quality report not found: {{report}}")

with report.open("r", newline="", encoding="utf-8-sig") as file:
    rows = list(csv.DictReader(file))

if not rows:
    raise ValueError("Quality report is empty.")

if "status" not in rows[0]:
    raise ValueError("The quality report does not contain a status column.")

failed = [
    row for row in rows
    if row.get("status", "").strip().upper() == "FAIL"
]

passed = sum(
    row.get("status", "").strip().upper() == "PASS"
    for row in rows
)

print(f"Total checks: {{len(rows)}}")
print(f"Passed checks: {{passed}}")
print(f"Failed checks: {{len(failed)}}")

if failed:
    for row in failed:
        print("FAILED CHECK:", row)
    raise RuntimeError("DATA QUALITY GATE FAILED")

print("DATA QUALITY GATE PASSED")
CHECK
""",
        cwd=str(PROJECT_DIR),
        env=TASK_ENV,
        append_env=True,
    )

    ingestion >> transformation >> warehouse_loading >> data_quality >> quality_gate
