
import csv
import os
import random
from datetime import datetime, timedelta

import psycopg2

# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "synthetic_hr_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432"),
}

CSV_FILE = os.path.join("data", "employees.csv")

random.seed(42)


def main():
    if not DB_CONFIG["password"]:
        raise ValueError("DB_PASSWORD is not set in this PowerShell session.")

    # Read employee data
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        employees = list(csv.DictReader(file))

    if not employees:
        raise ValueError("employees.csv contains no employee records.")

    connection = psycopg2.connect(**DB_CONFIG)

    try:
        with connection.cursor() as cursor:

            # Clear this HR database before reloading
            cursor.execute("""
                TRUNCATE TABLE
                    attendance,
                    performance_reviews,
                    salaries,
                    employees,
                    departments
                RESTART IDENTITY CASCADE;
            """)

            # --------------------------------------------------
            # 2. Insert departments
            # --------------------------------------------------

            department_names = sorted({
                employee["department"] for employee in employees
            })

            cursor.executemany(
                "INSERT INTO departments (department_name) VALUES (%s)",
                [(name,) for name in department_names]
            )

            cursor.execute("""
                SELECT department_id, department_name
                FROM departments
            """)

            department_map = {
                name: department_id
                for department_id, name in cursor.fetchall()
            }

            # --------------------------------------------------
            # 3. Insert employees and salaries
            # --------------------------------------------------

            employee_rows = []
            salary_rows = []

            for employee in employees:
                employee_id = int(employee["employee_id"])
                join_date = datetime.strptime(
                    employee["join_date"], "%Y-%m-%d"
                ).date()

                employee_rows.append((
                    employee_id,
                    employee["employee_name"],
                    employee["email"],
                    department_map[employee["department"]],
                    employee["job_role"],
                    employee["city"],
                    join_date,
                    employee["employment_status"]
                ))

                salary_rows.append((
                    employee_id,
                    float(employee["salary"]),
                    join_date
                ))

            cursor.executemany("""
                INSERT INTO employees (
                    employee_id, employee_name, email,
                    department_id, job_role, city,
                    join_date, employment_status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, employee_rows)

            cursor.executemany("""
                INSERT INTO salaries (
                    employee_id, salary, effective_date
                )
                VALUES (%s, %s, %s)
            """, salary_rows)

            # --------------------------------------------------
            # 4. Generate attendance records
            # --------------------------------------------------

            attendance_rows = []

            for employee in employees:
                employee_id = int(employee["employee_id"])
                current_date = datetime.strptime(
                    employee["join_date"], "%Y-%m-%d"
                ).date()

                working_days = 0

                while working_days < 20:
                    if current_date.weekday() < 5:
                        status = random.choices(
                            ["Present", "Absent", "Leave"],
                            weights=[90, 5, 5]
                        )[0]

                        hours = 8.0 if status == "Present" else 0.0

                        attendance_rows.append((
                            employee_id,
                            current_date,
                            status,
                            hours
                        ))

                        working_days += 1

                    current_date += timedelta(days=1)

            cursor.executemany("""
                INSERT INTO attendance (
                    employee_id, attendance_date,
                    attendance_status, hours_worked
                )
                VALUES (%s, %s, %s, %s)
            """, attendance_rows)

            # --------------------------------------------------
            # 5. Generate performance reviews
            # --------------------------------------------------

            review_rows = []

            comments = [
                "Excellent performance and teamwork.",
                "Consistently meets assigned targets.",
                "Shows good technical and communication skills.",
                "Needs improvement in time management.",
                "Demonstrates strong problem-solving skills."
            ]

            for employee in employees:
                employee_id = int(employee["employee_id"])
                join_date = datetime.strptime(
                    employee["join_date"], "%Y-%m-%d"
                ).date()

                review_rows.append((
                    employee_id,
                    join_date + timedelta(days=365),
                    round(random.uniform(3.0, 5.0), 1),
                    random.choice(comments)
                ))

            cursor.executemany("""
                INSERT INTO performance_reviews (
                    employee_id, review_date, rating, comments
                )
                VALUES (%s, %s, %s, %s)
            """, review_rows)

        connection.commit()

        print("\nHR DATABASE LOADED SUCCESSFULLY")
        print("--------------------------------")
        print(f"Departments: {len(department_names)}")
        print(f"Employees: {len(employee_rows)}")
        print(f"Salaries: {len(salary_rows)}")
        print(f"Attendance records: {len(attendance_rows)}")
        print(f"Performance reviews: {len(review_rows)}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
