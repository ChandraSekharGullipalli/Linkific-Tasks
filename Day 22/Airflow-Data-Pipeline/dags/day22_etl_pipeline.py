from datetime import datetime, timedelta, timezone
from pathlib import Path
import logging
import csv

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


# ============================================================
# DAY 22 - AIRFLOW ETL PIPELINE WITH FAILURE HANDLING
# ============================================================

logger = logging.getLogger("day22_failure_monitor")

PROJECT_DIR = Path(
    "/mnt/c/Linkific Tasks/Linkific-Tasks/Day 22"
)

PYTHON = "/home/chandra_sekhar/airflow-day22/.venv/bin/python"

# PostgreSQL connection settings for WSL
TASK_ENV = {
    "DB_HOST": "192.168.48.1",
    "PYTHONUNBUFFERED": "1",
}


# ============================================================
# FAILURE CALLBACK
# ============================================================

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


# ============================================================
# RETRY CALLBACK
# ============================================================

def on_task_retry(context):
    task = context.get("task_instance")

    if task:
        logger.warning(
            "TASK RETRY | DAG: %s | TASK: %s | TRY: %s",
            task.dag_id,
            task.task_id,
            task.try_number,
        )


# ============================================================
# DEFAULT TASK CONFIGURATION
# ============================================================

DEFAULT_ARGS = {
    "owner": "linkific",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": on_task_failure,
    "on_retry_callback": on_task_retry,
}


# ============================================================
# DAG DEFINITION
# ============================================================

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

    # --------------------------------------------------------
    # TASK 1: DATA INGESTION
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # TASK 2: DATA TRANSFORMATION
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # TASK 3: INCREMENTAL WAREHOUSE LOADING
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # TASK 4: DATA QUALITY CHECKS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # TASK 5: DATA QUALITY GATE
    # --------------------------------------------------------

    quality_gate = BashOperator(
        task_id="data_quality_gate",
        bash_command=f"""
"{PYTHON}" - <<'CHECK'
import csv
from pathlib import Path

report = Path("data/quality_reports/data_quality_report.csv")

if not report.is_file():
    raise FileNotFoundError(
        f"Quality report not found: {{report}}"
    )

with report.open(
    "r",
    newline="",
    encoding="utf-8-sig"
) as file:
    rows = list(csv.DictReader(file))

if not rows:
    raise ValueError("Quality report is empty.")

if "status" not in rows[0]:
    raise ValueError(
        "The quality report does not contain a status column."
    )

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

    # --------------------------------------------------------
    # PIPELINE EXECUTION ORDER
    # --------------------------------------------------------

    (
        ingestion
        >> transformation
        >> warehouse_loading
        >> data_quality
        >> quality_gate
    )
