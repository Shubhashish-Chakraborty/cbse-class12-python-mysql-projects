# Project 7 : Cinema Ticket Booking System

**Database:** `cinema_db`  |  **Difficulty:** ★★  |  **Files:** `setup.sql`, `main.py`, `sample_output.txt`

## Problem Statement

A multiplex wants an online-style program for booking movie tickets. It runs several **shows** (movie + date + time) and every show has a limited number of seats.

Write a menu-driven Python-MySQL program that can:

1. display all movies and **search movies by language**,
2. display the **show timings** with the number of seats left,
3. **book tickets** for a show – at most 6 tickets at a time, not more than the seats left, no booking for a *HOUSEFULL* show – and print an **e-ticket**,
4. **cancel a booking** (the seats must become available again and the refund is 80% of the amount),
5. show the bookings of a customer,
6. show a **movie-wise revenue report** and the total box-office collection,
7. list the **housefull shows**,
8. let the admin **add a new show**.

## Concepts Used (Sumita Arora, Class XII)

- **Ch 13** – `SELECT`, `WHERE`, `LIKE`, `ORDER BY`, aggregate functions `COUNT / SUM`
- **Ch 14** – `CREATE TABLE` with a chain of foreign keys (`bookings → shows → movies`), `INSERT`, `UPDATE`, `DELETE`
- **Ch 15** – `GROUP BY`, equi-join of two and of three tables
- **Ch 16** – parameterised queries, tuple unpacking of `fetchone()`, `lastrowid`, `commit()` / `rollback()`

## Database Design

| Table | Columns | Purpose |
|---|---|---|
| `movies` | **movie_id** (PK), title, language, duration, ticket_price | Movies being screened |
| `shows` | **show_id** (PK), movie_id (FK), show_date, show_time, seats_left | One row for every screening |
| `bookings` | **booking_id** (PK, auto), show_id (FK), cust_name, seats, amount | Tickets booked by customers |

## How to Run

1. Install **MySQL Server** and **Python 3**, then install the connector: `pip install pymysql`
2. Create the database and sample data (run from this folder):
   ```
   mysql -u root -p < setup.sql
   ```
   *(or open `setup.sql` in MySQL Workbench and execute it)*
3. Open `main.py` and change `password="your_password"` to your MySQL root password.
4. Run the program:
   ```
   python main.py
   ```

## Sample Output

A short extract is shown below. The **complete session** (every menu option, including wrong inputs) is in [`sample_output.txt`](sample_output.txt).

```text
************ E-TICKET ************
Booking ID : 4
Name       : Kabir Anand
Movie      : The Last Train
Date/Time  : 2026-11-01 09:00 PM
Tickets    : 5 x Rs. 200
AMOUNT PAID: Rs. 1000
**********************************

```

## Practice Tasks for Students

Try to extend the project yourself:

1. Display all the shows of one particular movie.
2. Display the shows which have **fewer than 10 seats left** ("almost full").
3. Give a **10% discount** when 4 or more tickets are booked together.
4. Display the **movie with the highest revenue** (`ORDER BY SUM(amount) DESC LIMIT 1`).
5. Add an option for the admin to **change the ticket price** of a movie.

## Viva Questions

1. Why do we update `seats_left` both when booking and when cancelling?
2. Which tables are joined in the revenue report and what is the joining condition between them?
3. Why is `cust_name LIKE %s` used with `'%' + name + '%'` in *My bookings*?
4. Difference between `DELETE` and `DROP TABLE`.
5. What does `fetchone()` return when no row matches? How does the program use this?
