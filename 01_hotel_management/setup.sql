-- ============================================================
-- Project 1 : Hotel Management System  -  Database Setup
-- Run this file ONCE in MySQL before running main.py
--   mysql -u root -p < setup.sql
-- ============================================================

DROP DATABASE IF EXISTS hotel_db;
CREATE DATABASE hotel_db;
USE hotel_db;

CREATE TABLE rooms (
    room_no         INT PRIMARY KEY,
    room_type       VARCHAR(20) NOT NULL,
    price_per_night INT NOT NULL,
    status          VARCHAR(10) DEFAULT 'Available'
);

CREATE TABLE customers (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(30) NOT NULL,
    phone   VARCHAR(10),
    city    VARCHAR(20)
);

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id    INT NOT NULL,
    room_no    INT NOT NULL,
    check_in   DATE NOT NULL,
    check_out  DATE,
    nights     INT,
    bill       DECIMAL(10,2),
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id),
    FOREIGN KEY (room_no) REFERENCES rooms(room_no)
);

-- ---------------- sample data ----------------
INSERT INTO rooms VALUES
(101, 'Standard', 1500, 'Available'),
(102, 'Standard', 1500, 'Available'),
(103, 'Standard', 1500, 'Available'),
(201, 'Deluxe',   2500, 'Available'),
(202, 'Deluxe',   2500, 'Occupied'),
(203, 'Deluxe',   2500, 'Available'),
(301, 'Suite',    4500, 'Available'),
(302, 'Suite',    4500, 'Available');

INSERT INTO customers (name, phone, city) VALUES
('Aarav Sharma', '9876501234', 'Bhopal'),
('Neha Verma',   '9876505678', 'Indore'),
('Rohit Patel',  '9876509012', 'Nagpur'),
('Simran Kaur',  '9876503456', 'Delhi'),
('Imran Khan',   '9876507890', 'Jabalpur');

-- three completed stays and one guest who is still staying (room 202)
INSERT INTO bookings (cust_id, room_no, check_in, check_out, nights, bill) VALUES
(1, 101, '2026-10-01', '2026-10-03', 2,  3360.00),
(2, 201, '2026-10-05', '2026-10-08', 3,  8400.00),
(3, 301, '2026-10-10', '2026-10-12', 2, 10080.00);

INSERT INTO bookings (cust_id, room_no, check_in) VALUES
(4, 202, '2026-10-28');
