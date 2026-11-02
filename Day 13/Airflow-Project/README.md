# Day 13 – Apache Airflow: ETL Pipeline and Scheduled Workflows

## 1. Project Overview

This project demonstrates how to use **Apache Airflow** to create, manage, execute, and schedule automated data workflows.

The project uses Docker to run Apache Airflow and Python-based DAGs (Directed Acyclic Graphs) to perform different workflow tasks.

The main ETL pipeline extracts customer data from a CSV file, transforms and cleans the records, loads the cleaned data into an output CSV file, and validates the results.

## 2. Learning Objectives

- Understand Apache Airflow architecture and DAGs.
- Create and execute Python-based workflows.
- Use PythonOperator to execute Python functions.
- Use BashOperator to execute shell commands.
- Build an ETL pipeline using Extract, Transform, and Load tasks.
- Manage task dependencies.
- Schedule workflows using cron expressions.
- Monitor workflow execution through the Airflow web interface.
- Validate output data and troubleshoot workflow errors.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL programming |
| Apache Airflow 3.3.2 | Workflow orchestration |
| Docker Desktop | Running Airflow containers |
| Docker Compose | Managing multiple services |
| PostgreSQL | Airflow metadata database |
| CSV | Input and output data storage |
| VS Code | Writing and editing code |
| PowerShell | Running commands |

## 4. Project Structure

```text
Airflow-Project/
│
├── dags/
│   ├── 01_hello_world_dag.py
│   ├── 02_python_operator_dag.py
│   ├── 03_bash_operator_dag.py
│   ├── 04_customer_etl_dag.py
│   │
│   └── data/
│       ├── customers.csv
│       └── cleaned_customers.csv
│
├── config/
├── logs/
├── plugins/
│
├── docker-compose.yaml
├── docker-compose.backup.yaml
├── .env
└── README.md
```

**Note:** Do not upload `.env`, passwords, generated secrets, or unnecessary log files to GitHub. The backup Compose file is optional and does not need to be submitted.

## 5. Apache Airflow Setup

### Step 1: Install prerequisites

Install the following:

1. Python
2. Docker Desktop
3. Visual Studio Code

Docker Desktop should be configured to use the WSL 2 backend.

### Step 2: Open the project folder

Open PowerShell and execute:

```powershell
cd "C:\Linkific Tasks\Linkific-Tasks\Day 13\Airflow-Project"
```

### Step 3: Validate Docker Compose configuration

```powershell
docker compose config --quiet
```

If there are no configuration errors, continue.

### Step 4: Start Airflow

```powershell
docker compose up -d
```

### Step 5: Check running containers

```powershell
docker compose ps
```

Wait until the required Airflow services are running and the database is healthy.

### Step 6: Open Airflow

Open your browser:

http://localhost:8081

Log in using the credentials configured in your Docker Compose environment.

## 6. Understanding Airflow DAGs

A DAG stands for **Directed Acyclic Graph**.

It defines:
- What tasks should execute.
- The order in which tasks execute.
- Dependencies between tasks.
- When the workflow should run.

This project contains four DAG files.

| DAG file | Description |
|---|---|
| `01_hello_world_dag.py` | Basic Airflow workflow |
| `02_python_operator_dag.py` | Executes Python functions |
| `03_bash_operator_dag.py` | Executes Bash commands |
| `04_customer_etl_dag.py` | Complete customer ETL pipeline |

## 7. Customer ETL Pipeline

The main project is `04_customer_etl_dag.py`.

It contains four tasks.

### Task 1: Extract

- Reads customer records from `customers.csv`.
- Uses Python CSV functionality.
- Loads the records into memory.
- Passes the extracted data to the next task using XCom.

### Task 2: Transform

- Removes records with missing customer IDs or email addresses.
- Removes unnecessary whitespace.
- Converts names and cities into title case.
- Converts email addresses into lowercase.
- Passes cleaned records to the load task.

### Task 3: Load

- Creates the output directory if required.
- Writes the cleaned records into `cleaned_customers.csv`.
- Uses Python's `csv.DictWriter`.

### Task 4: Data Quality Validation

- Checks whether output records exist.
- Checks customer IDs and email addresses.
- Validates that email addresses contain `@`.
- Reports whether data quality validation passed.

### ETL Workflow

```text
customers.csv
      |
      v
EXTRACT TASK
      |
      v
TRANSFORM TASK
      |
      v
LOAD TASK
      |
      v
DATA QUALITY TASK
      |
      v
cleaned_customers.csv
```

## 8. Sample Input Data

File: `dags/data/customers.csv`

```csv
customer_id,name,email,city
101,Ravi,ravi@gmail.com,Hyderabad
102,Kiran,,Bengaluru
103,Arjun,arjun@gmail.com,Vijayawada
104,Priya,priya@gmail.com,Chennai
105,Sneha,,Pune
```

The input file contains five customer records, including two records with missing email addresses.

## 9. Expected Output

File: `dags/data/cleaned_customers.csv`

```csv
customer_id,name,email,city
101,Ravi,ravi@gmail.com,Hyderabad
103,Arjun,arjun@gmail.com,Vijayawada
104,Priya,priya@gmail.com,Chennai
```

**Expected result:**

- Total input records: 5
- Records removed: 2
- Cleaned records: 3
- Data quality validation: Passed

## 10. Running the DAG

1. Open the Airflow dashboard.
2. Locate `customer_etl_pipeline`.
3. Enable/unpause the DAG.
4. Click the Trigger button to start a manual run.
5. Open the Grid view.
6. Monitor the four tasks.
7. Check that all tasks finish successfully.

A successful execution should show all four tasks as successful.

### Verify the output in PowerShell

From the project folder, execute:

```powershell
Get-Content ".\dags\data\cleaned_customers.csv"
```

## 11. Scheduling DAGs by Time

Airflow supports automatic workflow scheduling through cron expressions.

Examples:

| Cron expression | Schedule |
|---|---|
| `0 9 * * *` | Every day at 9:00 AM |
| `0 6 * * *` | Every day at 6:00 AM |
| `0 18 * * *` | Every day at 6:00 PM |
| `0 * * * *` | Every hour |
| `*/30 * * * *` | Every 30 minutes |
| `0 8 * * 1` | Every Monday at 8:00 AM |
| `0 10 * * 0` | Every Sunday at 10:00 AM |

### Example: Schedule the Customer ETL DAG daily at 9 AM IST

Inside the DAG definition, use:

```python
with DAG(
    dag_id="customer_etl_pipeline",
    description="Customer CSV ETL Pipeline",
    start_date=pendulum.datetime(
        2026, 11, 1, tz="Asia/Kolkata"
    ),
    schedule="0 9 * * *",
    catchup=False,
    tags=["day13", "etl", "data-engineering"],
) as dag:
```

**Important:**

- `schedule=None` means manual execution only.
- `schedule="0 9 * * *"` configures a daily 9 AM schedule.
- `Asia/Kolkata` sets the DAG's timezone to Indian Standard Time.
- `catchup=False` prevents Airflow from automatically creating all missed historical runs.
- The DAG must be unpaused and the Airflow scheduler must be running.
- Scheduled runs may start shortly after the scheduled interval ends, depending on the timetable and scheduler.

After changing the schedule, save the DAG file and verify the schedule in the Airflow dashboard.

## 12. Useful Docker Commands

Run these commands from the project folder.

| Command | Purpose |
|---|---|
| `docker compose up -d` | Start Airflow services |
| `docker compose ps` | Check service status |
| `docker compose logs airflow-scheduler` | View scheduler logs |
| `docker compose logs airflow-apiserver` | View API server logs |
| `docker compose down` | Stop and remove containers |
| `docker compose restart` | Restart services |
| `docker compose config --quiet` | Validate Compose configuration |

To check whether the customer DAG is detected:

```powershell
docker compose exec airflow-apiserver airflow dags list
```

## 13. Troubleshooting

**Problem 1: Airflow dashboard is not opening**

- Check whether Docker Desktop is running.
- Execute `docker compose ps`.
- Check the Airflow API server logs.
- Confirm that port 8081 is available.

**Problem 2: DAG is not visible**

- Confirm that the Python file is inside the `dags` folder.
- Check for Python syntax errors.
- Check the DAG processor logs.
- Wait for Airflow to discover the DAG.

**Problem 3: DAG execution failed**

- Open the failed task in the Airflow Grid view.
- Check the task logs.
- Verify input file paths and Python imports.
- Check whether the input CSV file exists.

**Problem 4: Output file is not generated**

- Verify that the extract and transform tasks completed successfully.
- Check the load task logs.
- Confirm that the output directory is writable.

## 14. Key Learnings

Through this project, I learned:

1. How Apache Airflow manages data workflows.
2. How to create DAGs and define task dependencies.
3. How to execute Python and Bash tasks.
4. How to develop an end-to-end CSV-based ETL pipeline.
5. How to transfer data between tasks using XCom.
6. How to clean and validate customer records.
7. How to schedule automated workflows using cron expressions.
8. How to monitor and troubleshoot Airflow tasks using Docker and the web interface.

## 15. Conclusion

This project demonstrates a basic automated ETL workflow using Apache Airflow.

The pipeline extracts customer data from a CSV file, transforms and cleans the records, loads the processed data into a new CSV file, and performs data quality validation.

It also introduces workflow orchestration, task dependencies, Docker-based deployment, and time-based scheduling.

**Project Status:** Day 13 – Apache Airflow ETL Pipeline and Scheduled Workflows.

