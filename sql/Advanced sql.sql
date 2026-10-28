
-- DAY 9: 35+ ADVANCED SQL QUERIES
-- PostgreSQL Practice

-- 3. Display all employees
SELECT * FROM employees;

-- 4. Employees earning above 60000
SELECT * FROM employees WHERE salary > 60000;

-- 5. Second-highest distinct salary
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- 6. Third-highest distinct salary
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
OFFSET 2 LIMIT 1;

-- 7. Employees earning above average salary
SELECT employee_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 8. Salary between 40000 and 70000
SELECT employee_name, salary
FROM employees
WHERE salary BETWEEN 40000 AND 70000;

-- 9. INNER JOIN employees and departments
SELECT e.employee_name, d.department_name
FROM employees e
INNER JOIN departments d
ON e.department_id = d.department_id;

-- 10. LEFT JOIN including employees without departments
SELECT e.employee_name, d.department_name
FROM employees e
LEFT JOIN departments d
ON e.department_id = d.department_id;

-- 11. Departments with no employees
SELECT d.department_name
FROM departments d
LEFT JOIN employees e
ON d.department_id = e.department_id
WHERE e.employee_id IS NULL;

-- 12. Employees in IT
SELECT e.employee_name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE d.department_name = 'IT';

-- 13. Employees earning above their department average
SELECT e.employee_name, e.salary, e.department_id
FROM employees e
WHERE e.department_id IS NOT NULL
AND e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id
);

-- 14. Employee count by department
SELECT d.department_name, COUNT(e.employee_id) AS total_employees
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name;

-- 15. Average salary by department
SELECT department_id, AVG(salary) AS average_salary
FROM employees
WHERE department_id IS NOT NULL
GROUP BY department_id;

-- 16. Departments with average salary above 60000
SELECT department_id, AVG(salary) AS average_salary
FROM employees
WHERE department_id IS NOT NULL
GROUP BY department_id
HAVING AVG(salary) > 60000;

-- 17. Highest salary in each department
SELECT department_id, MAX(salary) AS highest_salary
FROM employees
WHERE department_id IS NOT NULL
GROUP BY department_id;

-- 18. Employee count by city
SELECT city, COUNT(*) AS employee_count
FROM employees
GROUP BY city
ORDER BY employee_count DESC;

-- 19. Rank employees by salary
SELECT employee_name, salary,
RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees;

-- 20. Assign row numbers by salary
SELECT employee_name, salary,
ROW_NUMBER() OVER (ORDER BY salary DESC, employee_id) AS row_num
FROM employees;

-- 21. Rank employees within each department
SELECT employee_name, department_id, salary,
DENSE_RANK() OVER (
    PARTITION BY department_id ORDER BY salary DESC
) AS department_rank
FROM employees;

-- 22. Highest-paid employee(s) in each department
WITH ranked AS (
    SELECT employee_name, department_id, salary,
    DENSE_RANK() OVER (
        PARTITION BY department_id ORDER BY salary DESC
    ) AS salary_rank
    FROM employees
    WHERE department_id IS NOT NULL
)
SELECT employee_name, department_id, salary
FROM ranked
WHERE salary_rank = 1;

-- 23. Running total of salaries
SELECT employee_name, salary,
SUM(salary) OVER (
    ORDER BY employee_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_total
FROM employees;

-- 24. Previous employee salary using LAG
SELECT employee_name, salary,
LAG(salary) OVER (ORDER BY employee_id) AS previous_salary
FROM employees;

-- 25. Next employee salary using LEAD
SELECT employee_name, salary,
LEAD(salary) OVER (ORDER BY employee_id) AS next_salary
FROM employees;

-- 26. Difference from department average
SELECT employee_name, department_id, salary,
salary - AVG(salary) OVER (
    PARTITION BY department_id
) AS difference_from_average
FROM employees;

-- 27. Employees earning more than Ravi
SELECT employee_name, salary
FROM employees
WHERE salary > (
    SELECT salary FROM employees WHERE employee_name = 'Ravi'
);

-- 28. Employees in departments with at least two employees
SELECT employee_name, department_id
FROM employees
WHERE department_id IN (
    SELECT department_id
    FROM employees
    WHERE department_id IS NOT NULL
    GROUP BY department_id
    HAVING COUNT(*) >= 2
);

-- 29. EXISTS: employees with a valid department
SELECT e.employee_name
FROM employees e
WHERE EXISTS (
    SELECT 1 FROM departments d
    WHERE d.department_id = e.department_id
);

-- 30. CTE: employees above overall average salary
WITH salary_summary AS (
    SELECT AVG(salary) AS avg_salary FROM employees
)
SELECT e.employee_name, e.salary
FROM employees e
CROSS JOIN salary_summary s
WHERE e.salary > s.avg_salary;

-- 31. Multiple CTEs: department salary analysis
WITH department_stats AS (
    SELECT department_id,
           COUNT(*) AS total_employees,
           AVG(salary) AS avg_salary
    FROM employees
    WHERE department_id IS NOT NULL
    GROUP BY department_id
),
high_salary_departments AS (
    SELECT *
    FROM department_stats
    WHERE avg_salary > 60000
)
SELECT d.department_name, h.total_employees, h.avg_salary
FROM high_salary_departments h
JOIN departments d ON h.department_id = d.department_id;

-- 32. Employees hired after January 1, 2024
SELECT employee_name, hire_date
FROM employees
WHERE hire_date > DATE '2024-01-01'
ORDER BY hire_date;

-- 33. Employee tenure in completed years
SELECT employee_name, hire_date,
EXTRACT(YEAR FROM AGE(CURRENT_DATE, hire_date)) AS completed_years
FROM employees;

-- 34. Categorize salaries using CASE
SELECT employee_name, salary,
CASE
    WHEN salary >= 70000 THEN 'High'
    WHEN salary >= 50000 THEN 'Medium'
    ELSE 'Low'
END AS salary_category
FROM employees;

-- 35. Employees hired per year
SELECT EXTRACT(YEAR FROM hire_date) AS hire_year,
COUNT(*) AS employees_hired
FROM employees
GROUP BY EXTRACT(YEAR FROM hire_date)
ORDER BY hire_year;

-- 36. Find duplicate salaries
SELECT salary, COUNT(*) AS employee_count
FROM employees
GROUP BY salary
HAVING COUNT(*) > 1;

-- 37. Find employees with the same salary
SELECT e1.employee_name AS employee_1,
       e2.employee_name AS employee_2,
       e1.salary
FROM employees e1
JOIN employees e2
ON e1.salary = e2.salary
AND e1.employee_id < e2.employee_id;

-- 38. Self join: employees and their managers
SELECT e.employee_name AS employee,
       m.employee_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;

-- 39. Find the minimum salary in each department
SELECT department_id, MIN(salary) AS minimum_salary
FROM employees
WHERE department_id IS NOT NULL
GROUP BY department_id;

-- 40. Find the top three distinct salary levels
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 3;
