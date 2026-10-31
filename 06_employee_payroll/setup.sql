-- ============================================================
-- Project 6 : Employee Payroll Management System
--   mysql -u root -p < setup.sql
-- ============================================================

DROP DATABASE IF EXISTS company_db;
CREATE DATABASE company_db;
USE company_db;

CREATE TABLE departments (
    dept_id   INT PRIMARY KEY,
    dept_name VARCHAR(20) NOT NULL,
    location  VARCHAR(20)
);

CREATE TABLE employees (
    emp_id       INT PRIMARY KEY,
    name         VARCHAR(30) NOT NULL,
    dept_id      INT NOT NULL,
    designation  VARCHAR(25),
    basic_salary INT NOT NULL,
    join_date    DATE,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- ---------------- sample data ----------------
INSERT INTO departments VALUES
(10, 'Administration', 'Bhopal'),
(20, 'Accounts',       'Indore'),
(30, 'IT',             'Pune'),
(40, 'Sales',          'Mumbai'),
(50, 'Research',       'Delhi');          -- no employees yet

INSERT INTO employees VALUES
(1001, 'Suresh Rao',      10, 'Manager',         60000, '2015-04-12'),
(1002, 'Kavita Joshi',    20, 'Accountant',      38000, '2018-07-01'),
(1003, 'Manoj Tiwari',    30, 'Developer',       52000, '2019-01-15'),
(1004, 'Pooja Nair',      30, 'Developer',       48000, '2020-06-20'),
(1005, 'Deepak Yadav',    40, 'Sales Executive', 28000, '2021-03-10'),
(1006, 'Farhan Qureshi',  40, 'Sales Executive', 30000, '2017-11-05'),
(1007, 'Ritu Malhotra',   10, 'Clerk',           22000, '2016-09-18'),
(1008, 'Anil Kumar',      20, 'Clerk',           21000, '2022-02-14'),
(1009, 'Sneha Kulkarni',  30, 'Team Lead',       70000, '2014-08-25'),
(1010, 'Vivek Chauhan',   40, 'Sales Manager',   55000, '2013-05-30');
