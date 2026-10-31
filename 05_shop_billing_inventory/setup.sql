-- ============================================================
-- Project 5 : Stationery Shop - Billing & Inventory System
--   mysql -u root -p < setup.sql
-- ============================================================

DROP DATABASE IF EXISTS shop_db;
CREATE DATABASE shop_db;
USE shop_db;

CREATE TABLE products (
    prod_id  INT PRIMARY KEY,
    name     VARCHAR(30) NOT NULL,
    category VARCHAR(20),
    price    INT NOT NULL,
    stock    INT NOT NULL
);

CREATE TABLE bills (
    bill_no   INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(30),
    bill_date DATE,
    total     INT DEFAULT 0
);

CREATE TABLE bill_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_no INT NOT NULL,
    prod_id INT NOT NULL,
    qty     INT NOT NULL,
    amount  INT NOT NULL,
    FOREIGN KEY (bill_no) REFERENCES bills(bill_no),
    FOREIGN KEY (prod_id) REFERENCES products(prod_id)
);

-- ---------------- sample data ----------------
INSERT INTO products VALUES
(1,  'Notebook (200 pages)',    'Stationery',  60,  45),
(2,  'Ball Pen (Blue)',         'Stationery',  10, 190),
(3,  'Pencil Box',              'Stationery', 120,  14),
(4,  'Geometry Box',            'Stationery', 150,  19),
(5,  'Scientific Calculator',   'Electronics',650,   7),
(6,  'Highlighter Set',         'Stationery',  90,  12),
(7,  'Graph Book',              'Stationery',  45,  36),
(8,  'Drawing File',            'Stationery',  70,   6),
(9,  'Eraser',                  'Stationery',   5, 100),
(10, 'Marker Pen',              'Stationery',  25,  30);

-- three old bills so that the sales reports have some data
INSERT INTO bills (cust_name, bill_date, total) VALUES
('Ravi Kumar', '2026-10-29',  400),
('Sneha Roy',  '2026-10-29',  270),
('Aman Soni',  '2026-10-30',  830);

INSERT INTO bill_items (bill_no, prod_id, qty, amount) VALUES
(1, 1, 5, 300), (1, 2, 10, 100),
(2, 4, 1, 150), (2, 3, 1, 120),
(3, 5, 1, 650), (3, 7, 4, 180);
