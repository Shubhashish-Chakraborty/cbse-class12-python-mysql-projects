-- ============================================================
-- Project 2 : Library Management System  -  Database Setup
--   mysql -u root -p < setup.sql
-- ============================================================

DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db;
USE library_db;

CREATE TABLE books (
    book_id  INT PRIMARY KEY,
    title    VARCHAR(50) NOT NULL,
    author   VARCHAR(30),
    category VARCHAR(20),
    copies   INT DEFAULT 1
);

CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(30) NOT NULL,
    class     VARCHAR(5)
);

CREATE TABLE issues (
    issue_id    INT AUTO_INCREMENT PRIMARY KEY,
    book_id     INT NOT NULL,
    member_id   INT NOT NULL,
    issue_date  DATE NOT NULL,
    return_date DATE,
    fine        INT DEFAULT 0,
    FOREIGN KEY (book_id)   REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- ---------------- sample data ----------------
INSERT INTO books VALUES
(101, 'Wings of Fire',               'A.P.J. Abdul Kalam',  'Biography', 3),
(102, 'Computer Science with Python','Sumita Arora',        'Textbook',  5),
(103, 'Malgudi Days',                'R.K. Narayan',        'Fiction',   2),
(104, 'The Discovery of India',      'Jawaharlal Nehru',    'History',   2),
(105, 'Godan',                       'Munshi Premchand',    'Fiction',   2),
(106, 'A Brief History of Time',     'Stephen Hawking',     'Science',   0),
(107, 'Gitanjali',                   'Rabindranath Tagore', 'Poetry',    2),
(108, 'Concepts of Physics',         'H.C. Verma',          'Textbook',  4);

INSERT INTO members (name, class) VALUES
('Ankit Jain',  '12A'),
('Priya Singh', '12B'),
('Karan Mehta', '11A'),
('Sara Ali',    '12A');

-- one old returned issue, and book 106 (last copy) is currently issued to Karan
INSERT INTO issues (book_id, member_id, issue_date, return_date, fine) VALUES
(103, 2, '2026-09-10', '2026-09-20', 0);
INSERT INTO issues (book_id, member_id, issue_date) VALUES
(106, 3, '2026-10-05');
