-- ETL SQL Translator Error Testing Dataset
-- Source Dialect: MySQL
-- Purpose: Test AI error detection and manual fix suggestions


-- ERROR 1: Missing closing bracket

CREATE TABLE employee_error (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    salary DECIMAL(10,2)
;


-- ERROR 2: Wrong data type

CREATE TABLE product_error (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    price MONEY,
    created_date DATETIME
);


-- ERROR 3: Invalid column name in INSERT

INSERT INTO employee_error
(employee_id, employee_name, email)
VALUES
(1,'John','john@test.com');


-- ERROR 4: Wrong SQL function for migration testing

SELECT
    employee_name,
    DATE_FORMAT(created_date,'%Y-%m-%d') AS joining_day
FROM employee_error;


-- ERROR 5: Join with missing table column

SELECT
    e.name,
    p.product_name
FROM employee_error e
JOIN product_error p
ON e.id = p.employee_id;


-- ERROR 6: Unsupported MySQL specific syntax

CREATE TABLE orders_error (
    order_id INT AUTO_INCREMENT,
    order_status ENUM('NEW','DONE'),
    created_at DATETIME DEFAULT NOW(),
    PRIMARY KEY(order_id)
);


-- Expected AI Agent Detection:

Issues:
1. Missing SQL syntax closing bracket
2. Invalid/unsupported data type conversion
3. Column mismatch during insert
4. DATE_FORMAT requires conversion in PostgreSQL
5. Missing employee_id relationship
6. ENUM and AUTO_INCREMENT need dialect conversion


Expected Output:

{
"status":"FAILED_WITH_SUGGESTIONS",
"issues_detected":[],
"manual_fix_required":"",
"confidence_score":"90%"
}
