-- ============================================================
-- Project 3 : Student Result Management System  -  Database Setup
--   mysql -u root -p < setup.sql
-- ============================================================

DROP DATABASE IF EXISTS school_db;
CREATE DATABASE school_db;
USE school_db;

CREATE TABLE students (
    roll_no INT PRIMARY KEY,
    name    VARCHAR(30) NOT NULL,
    section CHAR(1) NOT NULL
);

CREATE TABLE marks (
    roll_no   INT PRIMARY KEY,
    physics   INT,
    chemistry INT,
    maths     INT,
    english   INT,
    cs        INT,
    FOREIGN KEY (roll_no) REFERENCES students(roll_no)
);

-- ---------------- sample data ----------------
INSERT INTO students VALUES
(1,  'Aditya Singh',   'A'),
(2,  'Bhavna Gupta',   'A'),
(3,  'Chirag Jain',    'A'),
(4,  'Divya Thakur',   'A'),
(5,  'Eshaan Malik',   'A'),
(6,  'Fatima Sheikh',  'B'),
(7,  'Gaurav Pandey',  'B'),
(8,  'Harleen Kaur',   'B'),
(9,  'Ishaan Dubey',   'B'),
(10, 'Jhanvi Soni',    'B');

INSERT INTO marks VALUES
(1,  78, 82, 91, 74, 96),
(2,  88, 90, 95, 85, 98),
(3,  56, 61, 48, 70, 72),
(4,  67, 72, 80, 78, 84),
(5,  30, 45, 52, 60, 66),
(6,  92, 89, 97, 88, 99),
(7,  40, 38, 35, 55, 62),
(8,  75, 70, 68, 82, 90),
(9,  28, 50, 44, 61, 58),
(10, 83, 79, 86, 91, 94);
