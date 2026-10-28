
-- DAY 9: HOSPITAL MANAGEMENT DATASET + JOIN QUERIES
-- Database: PostgreSQL

-- STEP 1: CREATE TABLES

CREATE TABLE hospital_departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50)
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    doctor_name VARCHAR(50),
    department_id INT REFERENCES hospital_departments(department_id),
    consultation_fee NUMERIC(10,2)
);

CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(50),
    age INT,
    city VARCHAR(50)
);

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    appointment_date DATE,
    status VARCHAR(20)
);

CREATE TABLE medicines (
    medicine_id INT PRIMARY KEY,
    medicine_name VARCHAR(50),
    price NUMERIC(10,2),
    stock_quantity INT
);

CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY,
    appointment_id INT REFERENCES appointments(appointment_id),
    medicine_id INT REFERENCES medicines(medicine_id),
    quantity INT
);

CREATE TABLE hospital_bills (
    bill_id INT PRIMARY KEY,
    appointment_id INT REFERENCES appointments(appointment_id),
    bill_amount NUMERIC(10,2),
    payment_status VARCHAR(20)
);

-- STEP 2: INSERT SAMPLE DATA

INSERT INTO hospital_departments VALUES
(1, 'Cardiology'),
(2, 'Neurology'),
(3, 'Orthopedics'),
(4, 'Pediatrics'),
(5, 'Dermatology');

INSERT INTO doctors VALUES
(101, 'Dr. Ravi', 1, 800),
(102, 'Dr. Priya', 2, 1000),
(103, 'Dr. Arun', 3, 700),
(104, 'Dr. Sneha', 1, 900),
(105, 'Dr. Kiran', 4, 600);

INSERT INTO patients VALUES
(201, 'Rahul', 35, 'Hyderabad'),
(202, 'Anjali', 28, 'Bengaluru'),
(203, 'Suresh', 50, 'Chennai'),
(204, 'Divya', 12, 'Hyderabad'),
(205, 'Meena', 42, 'Pune'),
(206, 'Karthik', 31, 'Vijayawada');

INSERT INTO appointments VALUES
(301, 201, 101, '2026-10-20', 'Completed'),
(302, 202, 102, '2026-10-21', 'Completed'),
(303, 203, 103, '2026-10-22', 'Pending'),
(304, 201, 104, '2026-10-23', 'Completed'),
(305, 204, 105, '2026-10-24', 'Completed'),
(306, 205, 101, '2026-10-25', 'Cancelled');

INSERT INTO medicines VALUES
(401, 'Paracetamol', 50, 100),
(402, 'Vitamin D', 120, 60),
(403, 'Antibiotic A', 200, 40),
(404, 'Pain Relief Gel', 150, 25),
(405, 'Cough Syrup', 90, 0);

INSERT INTO prescriptions VALUES
(501, 301, 401, 2),
(502, 301, 402, 1),
(503, 302, 403, 1),
(504, 304, 404, 2),
(505, 305, 401, 3);

INSERT INTO hospital_bills VALUES
(601, 301, 950, 'Paid'),
(602, 302, 1200, 'Paid'),
(603, 303, 700, 'Pending'),
(604, 304, 1100, 'Paid'),
(605, 305, 750, 'Pending'),
(606, 306, 800, 'Unpaid');

-- STEP 3: VERIFY DATASETS

SELECT * FROM hospital_departments;
SELECT * FROM doctors;
SELECT * FROM patients;
SELECT * FROM appointments;
SELECT * FROM medicines;
SELECT * FROM prescriptions;
SELECT * FROM hospital_bills;

-- STEP 4: SQL JOIN QUERIES

-- QUERY 1: Patients and their appointments
SELECT p.patient_name, a.appointment_date, a.status
FROM patients p
INNER JOIN appointments a
ON p.patient_id = a.patient_id;

-- QUERY 2: Doctors and departments
SELECT d.doctor_name, hd.department_name, d.consultation_fee
FROM doctors d
JOIN hospital_departments hd
ON d.department_id = hd.department_id;

-- QUERY 3: All patients, including those without appointments
SELECT p.patient_name, a.appointment_id
FROM patients p
LEFT JOIN appointments a
ON p.patient_id = a.patient_id;

-- QUERY 4: Patients without appointments
SELECT p.patient_id, p.patient_name
FROM patients p
LEFT JOIN appointments a
ON p.patient_id = a.patient_id
WHERE a.appointment_id IS NULL;

-- QUERY 5: Doctors without appointments
SELECT d.doctor_name
FROM doctors d
LEFT JOIN appointments a
ON d.doctor_id = a.doctor_id
WHERE a.appointment_id IS NULL;

-- QUERY 6: Patients, doctors, and appointment details
SELECT p.patient_name, d.doctor_name,
       a.appointment_date, a.status
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id;

-- QUERY 7: Appointments and bill details
SELECT a.appointment_id, p.patient_name,
       b.bill_amount, b.payment_status
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
LEFT JOIN hospital_bills b
ON a.appointment_id = b.appointment_id;

-- QUERY 8: Total bills by payment status
SELECT payment_status,
       SUM(bill_amount) AS total_amount,
       COUNT(*) AS total_bills
FROM hospital_bills
GROUP BY payment_status;

-- QUERY 9: Total appointments per doctor
SELECT d.doctor_name,
       COUNT(a.appointment_id) AS total_appointments
FROM doctors d
LEFT JOIN appointments a
ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.doctor_name
ORDER BY total_appointments DESC;

-- QUERY 10: Most expensive prescribed medicine
SELECT m.medicine_name, m.price, pr.quantity
FROM prescriptions pr
JOIN medicines m ON pr.medicine_id = m.medicine_id
ORDER BY m.price DESC
LIMIT 1;

-- QUERY 11: Calculate prescription medicine costs
SELECT pr.prescription_id, m.medicine_name,
       pr.quantity, m.price,
       pr.quantity * m.price AS total_medicine_cost
FROM prescriptions pr
JOIN medicines m ON pr.medicine_id = m.medicine_id;

-- QUERY 12: Doctors with more than one appointment
SELECT d.doctor_name,
       COUNT(a.appointment_id) AS total_appointments
FROM doctors d
JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.doctor_name
HAVING COUNT(a.appointment_id) > 1;

-- QUERY 13: Medicines never prescribed
SELECT m.medicine_name
FROM medicines m
LEFT JOIN prescriptions pr
ON m.medicine_id = pr.medicine_id
WHERE pr.prescription_id IS NULL;

-- QUERY 14: Departments with average consultation fee above 750
SELECT hd.department_name,
       AVG(d.consultation_fee) AS average_fee
FROM hospital_departments hd
JOIN doctors d ON hd.department_id = d.department_id
GROUP BY hd.department_id, hd.department_name
HAVING AVG(d.consultation_fee) > 750;

-- QUERY 15: Complete hospital summary report
SELECT p.patient_name, d.doctor_name,
       hd.department_name, a.appointment_date,
       a.status,
       COALESCE(b.bill_amount, 0) AS bill_amount,
       COALESCE(b.payment_status, 'Not Generated') AS payment_status
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id
JOIN hospital_departments hd ON d.department_id = hd.department_id
LEFT JOIN hospital_bills b ON a.appointment_id = b.appointment_id
ORDER BY a.appointment_date;

