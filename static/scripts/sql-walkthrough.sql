-- Create database
--CREATE DATABASE test_db

-- Switch context to specific database:
USE test_db

CREATE TABLE test_table
( id INT NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  first_name VARCHAR(50),
  age INT
);

INSERT INTO dbo.test_table (id, last_name, first_name, age)  
VALUES ('1', 'Phu', 'Winnie', NULL),  
       ('2', 'Pan', 'Peter', '17')