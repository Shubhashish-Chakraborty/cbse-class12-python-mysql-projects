# Project 1 : Hotel Management System

**Database:** `hotel_db`  |  **Difficulty:** ★★★ (Flagship project)  |  **Files:** `setup.sql`, `main.py`, `sample_output.txt`

## Problem Statement

**Hotel Sunrise** has 8 rooms of three types (Standard, Deluxe and Suite). At present the receptionist keeps all records in a register, which makes it difficult to find free rooms, calculate bills and know how much money the hotel has earned.

Write a menu-driven Python program, connected to a MySQL database, that helps the receptionist to:

1. register new customers,
2. see all rooms / only the available rooms,
3. **check-in** a customer into a free room (the room must become *Occupied*),
4. **check-out** a customer, calculate the number of nights, add 12% GST and print the **bill** (the room must become *Available* again),
5. see the guests who are currently staying in the hotel,
6. search a customer by name and see the booking history of a customer,
7. see a **room-type wise revenue report** and the total revenue.

## Concepts Used (Sumita Arora, Class XII)

- **Ch 13** – `SELECT`, `WHERE`, `LIKE`, `IS NULL`, `ORDER BY`, `DATEDIFF()`, aggregate functions `COUNT / SUM`
- **Ch 14** – `CREATE TABLE` with `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `DEFAULT`, `AUTO_INCREMENT`; `INSERT`, `UPDATE`
- **Ch 15** – `GROUP BY`, equi-join of tables using table aliases (`bookings b, customers c, rooms r`)
- **Ch 16** – `pymysql.connect()`, `cursor()`, `execute()`, `fetchone()`, `fetchall()`, parameterised queries (`%s`), `commit()`, `rollback()`, `lastrowid`

## Database Design

| Table | Columns | Purpose |
|---|---|---|
| `rooms` | **room_no** (PK), room_type, price_per_night, status | All rooms of the hotel. `status` is *Available* or *Occupied* |
| `customers` | **cust_id** (PK, auto), name, phone, city | Guest details |
| `bookings` | **booking_id** (PK, auto), cust_id (FK), room_no (FK), check_in, check_out, nights, bill | One row per stay. `check_out IS NULL` means the guest is still staying |

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
========== HOTEL BILL ==========
Guest         : Ananya Rao
Room No       : 201
Check-in      : 2026-10-30
Check-out     : 2026-11-02
Nights        : 3 x Rs. 2500
Room charges  : Rs. 7500.00
GST (12%)     : Rs. 900.00
TOTAL BILL    : Rs. 8400.00
================================
```

## Practice Tasks for Students

Try to extend the project yourself:

1. Add a menu option to **cancel a booking** that was made by mistake (the room should become Available again).
2. Display all *available* rooms of a particular type (for example only *Deluxe* rooms).
3. Give a **10% discount** on the room charges if the guest stayed for more than 5 nights.
4. Display the list of customers belonging to a particular city.
5. Display the room which has earned the **maximum revenue** (use `GROUP BY`, `ORDER BY` and `LIMIT`).

## Viva Questions

1. Why do we use `%s` placeholders in `cur.execute()` instead of joining the values into the query string?
2. Why is `con.commit()` needed after `INSERT` and `UPDATE`, but not after `SELECT`?
3. What does `check_out IS NULL` tell us? Why can't we write `check_out = NULL`?
4. What is a foreign key? Which foreign keys are present in the `bookings` table?
5. Difference between `fetchone()` and `fetchall()`.
