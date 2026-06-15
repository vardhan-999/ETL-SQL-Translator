-- ETL SQL Translator Sample Dataset
-- Source Dialect: MySQL
-- Purpose: Test SQL migration from MySQL to PostgreSQL / SQLite


-- Employee Table

CREATE TABLE employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    joining_date DATETIME
);


INSERT INTO employee VALUES
(1, 'John Smith', 'john@test.com', 'IT', 50000.00, '2025-01-10 10:30:00'),
(2, 'Alice Brown', 'alice@test.com', 'HR', 45000.00, '2025-02-15 09:15:00');


-- Sales Table

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    product_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    sale_date DATE
);


INSERT INTO sales VALUES
(1, 1, 'Laptop', 5, 75000.00, '2025-03-01'),
(2, 2, 'Mobile', 10, 30000.00, '2025-03-05');


-- Customer Table

CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Join Query Migration Test

SELECT
    e.name,
    e.department,
    s.product_name,
    s.quantity,
    s.price
FROM employee e
JOIN sales s
ON e.id = s.employee_id
WHERE s.quantity > 5;


-- Functions for Dialect Translation Testing

SELECT
    name,
    DATE_FORMAT(joining_date, '%Y-%m-%d') AS joining_day
FROM employee;


-- Expected Migration Checks:
-- AUTO_INCREMENT -> PostgreSQL SERIAL
-- DATETIME -> PostgreSQL TIMESTAMP
-- DATE_FORMAT -> PostgreSQL TO_CHAR()
-- Backticks/functions should be converted
