# Day 9: SQL Patterns and JOIN Practice

## 1. Overview
Today, I practiced SQL queries using PostgreSQL and created a Hospital Management System database. I worked with multiple related tables and learned how to retrieve and analyze data using different SQL patterns.

## 2. Technologies Used
- PostgreSQL
- SQL
- VS Code / PostgreSQL Query Tool

## 3. Tables Created
- `hospital_departments` – Stores department details.
- `doctors` – Stores doctor information and salaries.
- `patients` – Stores patient details.
- `appointments` – Stores patient appointments.
- `medicines` – Stores medicine names and prices.
- `prescriptions` – Stores prescribed medicines and quantities.
- `hospital_bills` – Stores billing and payment details.

## 4. SQL Patterns Practiced

### INNER JOIN
Returns matching records from both tables.
```sql
SELECT p.patient_name, a.status
FROM patients p
INNER JOIN appointments a
ON p.patient_id = a.patient_id;
```

### LEFT JOIN
Returns all records from the left table and matching records from the right table.
```sql
SELECT p.patient_name, a.appointment_id
FROM patients p
LEFT JOIN appointments a
ON p.patient_id = a.patient_id;
```

### RIGHT JOIN
Returns all records from the right table and matching records from the left table.
```sql
SELECT d.department_name, doc.doctor_name
FROM doctors doc
RIGHT JOIN hospital_departments d
ON doc.department_id = d.department_id;
```

### FULL OUTER JOIN
Returns matching and non-matching records from both tables.
```sql
SELECT p.patient_name, a.appointment_id
FROM patients p
FULL OUTER JOIN appointments a
ON p.patient_id = a.patient_id;
```

### GROUP BY and Aggregate Functions
Used to calculate totals and counts.
```sql
SELECT payment_status,
       COUNT(*) AS total_bills,
       SUM(bill_amount) AS total_amount
FROM hospital_bills
GROUP BY payment_status;
```

### Subquery
Used to find the most expensive medicine.
```sql
SELECT medicine_name, price
FROM medicines
WHERE price = (SELECT MAX(price) FROM medicines);
```

### Filtering and Sorting
Used `WHERE` and `ORDER BY` to filter and sort records.
```sql
SELECT doctor_name, salary
FROM doctors
WHERE salary > 80000
ORDER BY salary DESC;
```

### Finding Missing Matches
Used `LEFT JOIN` and `IS NULL` to find patients without appointments.
```sql
SELECT p.patient_name
FROM patients p
LEFT JOIN appointments a
ON p.patient_id = a.patient_id
WHERE a.appointment_id IS NULL;
```

## 5. Key Learnings
- Created relational tables with primary and foreign keys.
- Practiced INNER, LEFT, RIGHT, and FULL OUTER JOINs.
- Combined multiple tables in a single query.
- Used `COUNT()`, `SUM()`, and `MAX()` aggregate functions.
- Applied filtering, sorting, grouping, and subqueries.
- Analyzed appointments, doctor details, medicine costs, and hospital bills.

## 6. Project Structure
```text
Day 9/
├── day9_hospital_management.sql
└── README.md
```

## 7. Conclusion
This practice improved my understanding of SQL JOINs, relationships between tables, and data analysis using PostgreSQL. These SQL patterns are useful for working with relational databases and solving real-world data problems.
