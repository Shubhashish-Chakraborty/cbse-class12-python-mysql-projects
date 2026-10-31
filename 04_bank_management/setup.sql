-- ============================================================
-- Project 4 : Bank Management System  -  Database Setup
--   mysql -u root -p < setup.sql
-- ============================================================

DROP DATABASE IF EXISTS bank_db;
CREATE DATABASE bank_db;
USE bank_db;

CREATE TABLE accounts (
    acc_no   INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(30) NOT NULL,
    acc_type VARCHAR(10) NOT NULL,      -- 'Savings' or 'Current'
    pin      INT NOT NULL,
    balance  INT DEFAULT 0
);

CREATE TABLE transactions (
    txn_id   INT AUTO_INCREMENT PRIMARY KEY,
    acc_no   INT NOT NULL,
    txn_type VARCHAR(15) NOT NULL,      -- Opening / Deposit / Withdraw / Transfer In / Transfer Out
    amount   INT NOT NULL,
    txn_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (acc_no) REFERENCES accounts(acc_no)
);

-- ---------------- sample data ----------------
INSERT INTO accounts VALUES
(1001, 'Rahul Gupta',   'Savings', 1234, 15000),
(1002, 'Anita Desai',   'Savings', 4321,  8500),
(1003, 'Vikas Traders', 'Current', 1111, 52000),
(1004, 'Meera Nair',    'Savings', 2222,  3000),
(1005, 'Zoya Khan',     'Current', 3333, 27500);
