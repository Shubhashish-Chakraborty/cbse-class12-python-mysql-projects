-- ============================================================
-- Project 7 : Cinema Ticket Booking System
--   mysql -u root -p < setup.sql
-- ============================================================

DROP DATABASE IF EXISTS cinema_db;
CREATE DATABASE cinema_db;
USE cinema_db;

CREATE TABLE movies (
    movie_id     INT PRIMARY KEY,
    title        VARCHAR(40) NOT NULL,
    language     VARCHAR(15),
    duration     INT,                 -- in minutes
    ticket_price INT NOT NULL
);

CREATE TABLE shows (
    show_id    INT PRIMARY KEY,
    movie_id   INT NOT NULL,
    show_date  DATE NOT NULL,
    show_time  VARCHAR(8) NOT NULL,
    seats_left INT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    show_id    INT NOT NULL,
    cust_name  VARCHAR(30) NOT NULL,
    seats      INT NOT NULL,
    amount     INT NOT NULL,
    FOREIGN KEY (show_id) REFERENCES shows(show_id)
);

-- ---------------- sample data ----------------
INSERT INTO movies VALUES
(1, 'Galaxy Rangers',        'English', 142, 250),
(2, 'Monsoon Melody',        'Hindi',   128, 180),
(3, 'The Last Train',        'Hindi',   135, 200),
(4, 'Laughter Club',         'Hindi',   118, 150),
(5, 'Cosmic Kids',           'English',  98, 120);

INSERT INTO shows VALUES
(101, 1, '2026-11-01', '10:00 AM', 48),
(102, 1, '2026-11-01', '06:00 PM', 40),
(103, 2, '2026-11-01', '01:00 PM', 56),
(104, 3, '2026-11-01', '09:00 PM',  5),
(105, 4, '2026-11-02', '04:00 PM', 45),
(106, 5, '2026-11-02', '11:00 AM',  0),     -- housefull
(107, 2, '2026-11-02', '07:00 PM', 55);

INSERT INTO bookings (show_id, cust_name, seats, amount) VALUES
(101, 'Mehul Shah',  2,  500),
(103, 'Isha Kapoor', 4,  720),
(104, 'Rohan Das',   3,  600);
