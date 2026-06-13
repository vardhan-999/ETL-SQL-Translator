CREATE TABLE employee(
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department_id INT,
    created DATETIME,
    salary DECIMAL(10, 2)
);

INSERT INTO employee (first_name, last_name, department_id, created, salary)
VALUES ('John', 'Doe', 1, NOW(), 50000.00);
