
-- DAY 9: SQL JOINS AND QUERY PRACTICE
-- Database: PostgreSQL
-- Project: Hospital Management System

-- STEP 1: DROP OLD TABLES
DROP TABLE IF EXISTS hospital_bills CASCADE;
DROP TABLE IF EXISTS prescriptions CASCADE;
DROP TABLE IF EXISTS appointments CASCADE;
DROP TABLE IF EXISTS medicines CASCADE;
DROP TABLE IF EXISTS patients CASCADE;
DROP TABLE IF EXISTS doctors CASCADE;
DROP TABLE IF EXISTS hospital_departments CASCADE;

-- STEP 2: CREATE TABLES

CREATE TABLE hospital_departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    doctor_name VARCHAR(100),
    department_id INT REFERENCES hospital_departments(department_id),
    salary NUMERIC(10,2)
);

CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(100),
    age INT,
    city VARCHAR(50)
);

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    appointment_date DATE,
    status VARCHAR(30)
);

CREATE TABLE medicines (
    medicine_id INT PRIMARY KEY,
    medicine_name VARCHAR(100),
    price NUMERIC(8,2)
);

CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY,
    appointment_id INT REFERENCES appointments(appointment_id),
    medicine_id INT REFERENCES medicines(medicine_id),
    quantity INT
);

CREATE TABLE hospital_bills (
    bill_id INT PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    bill_amount NUMERIC(10,2),
    payment_status VARCHAR(30)
);

-- STEP 3: INSERT DEPARTMENTS

INSERT INTO hospital_departments VALUES
(1, 'Cardiology'),
(2, 'Neurology'),
(3, 'Orthopedics'),
(4, 'General Medicine');

-- STEP 4: INSERT DOCTORS

INSERT INTO doctors VALUES
(101, 'Dr. Ravi', 1, 90000),
(102, 'Dr. Priya', 2, 85000),
(103, 'Dr. Arjun', 3, 80000),
(104, 'Dr. Sneha', 4, 75000),
(105, 'Dr. Kiran', 1, 95000);

-- STEP 5: INSERT PATIENTS

INSERT INTO patients VALUES
(201, 'Amit', 35, 'Hyderabad'),
(202, 'Neha', 28, 'Bengaluru'),
(203, 'Rahul', 45, 'Chennai'),
(204, 'Divya', 32, 'Pune'),
(205, 'Suresh', 60, 'Hyderabad'),
(206, 'Meena', 25, 'Mumbai');

-- STEP 6: INSERT APPOINTMENTS

INSERT INTO appointments VALUES
(301, 201, 101, '2026-10-01', 'Completed'),
(302, 202, 102, '2026-10-02', 'Completed'),
(303, 203, 103, '2026-10-03', 'Pending'),
(304, 204, 104, '2026-10-04', 'Completed'),
(305, 205, 105, '2026-10-05', 'Cancelled');

-- STEP 7: INSERT MEDICINES

INSERT INTO medicines VALUES
(401, 'Paracetamol', 50),
(402, 'Vitamin C', 120),
(403, 'Ibuprofen', 80),
(404, 'Antibiotic', 200);

-- STEP 8: INSERT PRESCRIPTIONS

INSERT INTO prescriptions VALUES
(501, 301, 401, 2),
(502, 301, 402, 1),
(503, 302, 403, 3),
(504, 303, 404, 2),
(505, 304, 401, 1);

-- STEP 9: INSERT BILLS

INSERT INTO hospital_bills VALUES
(601, 201, 1500, 'Paid'),
(602, 202, 2500, 'Pending'),
(603, 203, 1800, 'Paid'),
(604, 204, 1200, 'Pending'),
(605, 205, 3000, 'Paid');

-- =====================================================
-- DAY 9: JOIN QUERIES
-- =====================================================

-- 1. INNER JOIN: Patients with appointments

SELECT p.patient_name, a.appointment_date, a.status
FROM patients p
INNER JOIN appointments a
ON p.patient_id = a.patient_id;

-- 2. LEFT JOIN: All patients and their appointments

SELECT p.patient_name, a.appointment_id, a.status
FROM patients p
LEFT JOIN appointments a
ON p.patient_id = a.patient_id;

-- 3. RIGHT JOIN: All departments and their doctors

SELECT d.department_name, doc.doctor_name
FROM doctors doc
RIGHT JOIN hospital_departments d
ON doc.department_id = d.department_id;

-- 4. FULL OUTER JOIN: All patients and appointments

SELECT p.patient_name, a.appointment_id, a.status
FROM patients p
FULL OUTER JOIN appointments a
ON p.patient_id = a.patient_id;

-- 5. Multiple JOINs: Patient, appointment and doctor

SELECT
    p.patient_name,
    doc.doctor_name,
    a.appointment_date
FROM patients p
JOIN appointments a
ON p.patient_id = a.patient_id
JOIN doctors doc
ON a.doctor_id = doc.doctor_id;

-- 6. JOIN with department names

SELECT
    doc.doctor_name,
    dep.department_name,
    doc.salary
FROM doctors doc
JOIN hospital_departments dep
ON doc.department_id = dep.department_id;

-- 7. JOIN prescriptions and medicines

SELECT
    pr.prescription_id,
    med.medicine_name,
    pr.quantity,
    med.price
FROM prescriptions pr
JOIN medicines med
ON pr.medicine_id = med.medicine_id;

-- 8. Calculate prescription cost

SELECT
    pr.prescription_id,
    med.medicine_name,
    pr.quantity,
    med.price,
    pr.quantity * med.price AS total_cost
FROM prescriptions pr
JOIN medicines med
ON pr.medicine_id = med.medicine_id;

-- 9. Patients with hospital bills

SELECT
    p.patient_name,
    b.bill_amount,
    b.payment_status
FROM patients p
JOIN hospital_bills b
ON p.patient_id = b.patient_id;

-- 10. Patients without appointments

SELECT p.patient_id, p.patient_name
FROM patients p
LEFT JOIN appointments a
ON p.patient_id = a.patient_id
WHERE a.appointment_id IS NULL;

-- 11. Doctors earning more than 80000

SELECT doctor_name, salary
FROM doctors
WHERE salary > 80000
ORDER BY salary DESC;

-- 12. Count appointments per doctor

SELECT
    doc.doctor_name,
    COUNT(a.appointment_id) AS total_appointments
FROM doctors doc
LEFT JOIN appointments a
ON doc.doctor_id = a.doctor_id
GROUP BY doc.doctor_id, doc.doctor_name
ORDER BY total_appointments DESC;

-- 13. Total bills per payment status

SELECT
    payment_status,
    COUNT(*) AS total_bills,
    SUM(bill_amount) AS total_amount
FROM hospital_bills
GROUP BY payment_status;

-- 14. Appointments completed by each doctor

SELECT
    doc.doctor_name,
    COUNT(a.appointment_id) AS completed_appointments
FROM doctors doc
LEFT JOIN appointments a
ON doc.doctor_id = a.doctor_id
AND a.status = 'Completed'
GROUP BY doc.doctor_id, doc.doctor_name;

-- 15. Patients with bills above 1500

SELECT
    p.patient_name,
    b.bill_amount
FROM patients p
JOIN hospital_bills b
ON p.patient_id = b.patient_id
WHERE b.bill_amount > 1500
ORDER BY b.bill_amount DESC;

-- 16. Appointments with department names

SELECT
    p.patient_name,
    doc.doctor_name,
    dep.department_name,
    a.appointment_date,
    a.status
FROM appointments a
JOIN patients p
ON a.patient_id = p.patient_id
JOIN doctors doc
ON a.doctor_id = doc.doctor_id
JOIN hospital_departments dep
ON doc.department_id = dep.department_id;

-- 17. Find the most expensive medicine

SELECT medicine_name, price
FROM medicines
WHERE price = (SELECT MAX(price) FROM medicines);

-- 18. Patients from Hyderabad

SELECT patient_name, age, city
FROM patients
WHERE city = 'Hyderabad';

-- 19. Total number of patients

SELECT COUNT(*) AS total_patients
FROM patients;

-- 20. Total hospital revenue from paid bills

SELECT SUM(bill_amount) AS paid_revenue
FROM hospital_bills
WHERE payment_status = 'Paid';

-- 21. Find patients with pending bills

SELECT
    p.patient_name,
    b.bill_amount,
    b.payment_status
FROM patients p
JOIN hospital_bills b
ON p.patient_id = b.patient_id
WHERE b.payment_status = 'Pending';

-- 22. Verify records in all main tables

SELECT 'Departments' AS table_name, COUNT(*) AS total_records
FROM hospital_departments
UNION ALL
SELECT 'Doctors', COUNT(*) FROM doctors
UNION ALL
SELECT 'Patients', COUNT(*) FROM patients
UNION ALL
SELECT 'Appointments', COUNT(*) FROM appointments
UNION ALL
SELECT 'Medicines', COUNT(*) FROM medicines
UNION ALL
SELECT 'Prescriptions', COUNT(*) FROM prescriptions
UNION ALL
SELECT 'Hospital Bills', COUNT(*) FROM hospital_bills;

-- END OF DAY 9 SQL PRACTICE
