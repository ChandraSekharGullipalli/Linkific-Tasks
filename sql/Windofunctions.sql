
--SQL WINDOW FUNCTION DEMONSTRATIONS
-- Database: PostgreSQL

-- STEP 1: CREATE DATASET

CREATE TABLE staff (
    staff_id INT PRIMARY KEY,
    staff_name VARCHAR(50),
    department VARCHAR(50),
    salary NUMERIC(10,2),
    hire_date DATE,
    city VARCHAR(50)
);

-- STEP 2: INSERT SAMPLE DATA

INSERT INTO staff VALUES
(1, 'Ravi', 'IT', 60000, '2023-01-10', 'Hyderabad'),
(2, 'Priya', 'IT', 75000, '2022-06-15', 'Bengaluru'),
(3, 'Kiran', 'IT', 75000, '2023-07-12', 'Bengaluru'),
(4, 'Arun', 'HR', 45000, '2024-02-01', 'Hyderabad'),
(5, 'Divya', 'HR', 50000, '2022-11-05', 'Chennai'),
(6, 'Sneha', 'Finance', 80000, '2021-09-20', 'Pune'),
(7, 'Anu', 'Finance', 65000, '2024-05-22', 'Pune'),
(8, 'Manoj', 'Sales', 55000, '2023-03-18', 'Hyderabad'),
(9, 'Suresh', 'Sales', 40000, '2025-01-08', 'Chennai'),
(10, 'Meena', 'IT', 60000, '2024-04-10', 'Hyderabad');

-- STEP 3: VERIFY DATA

SELECT * FROM staff ORDER BY staff_id;

-- =====================================================
-- WINDOW FUNCTION DEMONSTRATIONS


-- 1. ROW_NUMBER: Unique row number by salary
SELECT staff_name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
FROM staff;

-- 2. RANK: Rank salaries, leaving gaps after ties
SELECT staff_name, salary,
       RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM staff;

-- 3. DENSE_RANK: Rank salaries without gaps
SELECT staff_name, salary,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM staff;

-- 4. Rank staff within each department
SELECT staff_name, department, salary,
       RANK() OVER (
           PARTITION BY department
           ORDER BY salary DESC
       ) AS department_rank
FROM staff;

-- 5. Highest-paid staff in each department
WITH ranked_staff AS (
    SELECT *,
           DENSE_RANK() OVER (
               PARTITION BY department
               ORDER BY salary DESC
           ) AS salary_rank
    FROM staff
)
SELECT staff_name, department, salary
FROM ranked_staff
WHERE salary_rank = 1;

-- 6. LAG: Previous row's salary
SELECT staff_name, salary,
       LAG(salary) OVER (ORDER BY staff_id) AS previous_salary
FROM staff;

-- 7. LEAD: Next row's salary
SELECT staff_name, salary,
       LEAD(salary) OVER (ORDER BY staff_id) AS next_salary
FROM staff;

-- 8. Salary difference from previous staff member
SELECT staff_name, salary,
       salary - LAG(salary) OVER (
           ORDER BY staff_id
       ) AS salary_difference
FROM staff;

-- 9. Running total of salaries
SELECT staff_name, salary,
       SUM(salary) OVER (
           ORDER BY staff_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM staff;

-- 10. Average salary across all staff
SELECT staff_name, salary,
       AVG(salary) OVER () AS overall_average
FROM staff;

-- 11. Average salary within each department
SELECT staff_name, department, salary,
       AVG(salary) OVER (
           PARTITION BY department
       ) AS department_average
FROM staff;

-- 12. Salary compared with department average
SELECT staff_name, department, salary,
       salary - AVG(salary) OVER (
           PARTITION BY department
       ) AS difference_from_average
FROM staff;

-- 13. Total salary expenditure per department
SELECT staff_name, department, salary,
       SUM(salary) OVER (
           PARTITION BY department
       ) AS department_total_salary
FROM staff;

-- 14. Employee count per department
SELECT staff_name, department,
       COUNT(*) OVER (
           PARTITION BY department
       ) AS department_employee_count
FROM staff;

-- 15. Highest salary across the whole company
SELECT staff_name, salary,
       MAX(salary) OVER () AS company_max_salary
FROM staff;

-- 16. Lowest salary within each department
SELECT staff_name, department, salary,
       MIN(salary) OVER (
           PARTITION BY department
       ) AS department_min_salary
FROM staff;

-- 17. Salary percentile using NTILE
SELECT staff_name, salary,
       NTILE(4) OVER (
           ORDER BY salary DESC
       ) AS salary_quartile
FROM staff;

-- 18. First and last salary in each department
SELECT staff_name, department, salary,
       FIRST_VALUE(salary) OVER (
           PARTITION BY department
           ORDER BY salary DESC
       ) AS highest_salary,
       LAST_VALUE(salary) OVER (
           PARTITION BY department
           ORDER BY salary DESC
           ROWS BETWEEN UNBOUNDED PRECEDING
                    AND UNBOUNDED FOLLOWING
       ) AS lowest_salary
FROM staff;

-- 19. Top two staff members by salary in each department
WITH ranked_staff AS (
    SELECT staff_name, department, salary,
           ROW_NUMBER() OVER (
               PARTITION BY department
               ORDER BY salary DESC, staff_id
           ) AS row_num
    FROM staff
)
SELECT staff_name, department, salary
FROM ranked_staff
WHERE row_num <= 2
ORDER BY department, row_num;

-- 20. Compare each salary with the next salary
SELECT staff_name, salary,
       LEAD(salary) OVER (
           ORDER BY salary DESC, staff_id
       ) AS next_salary,
       salary - LEAD(salary) OVER (
           ORDER BY salary DESC, staff_id
       ) AS difference_from_next
FROM staff
ORDER BY salary DESC, staff_id;

-- END OF WINDOW FUNCTION PRACTICE
