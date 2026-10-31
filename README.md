# Class XII – Python & MySQL Connectivity Projects

Seven menu-driven **Python + MySQL** projects for the **CBSE Class XII Computer Science practical**, written to match the level of the *Sumita Arora* textbook (Chapters 12 – 16: Relational Databases, Simple Queries in SQL, Table Creation & DML, Grouping & Joins, Interface Python with MySQL).

Every project contains:

| File | What it is |
|---|---|
| `README.md` | Problem statement, concepts used (with chapter numbers), table design, practice tasks, viva questions |
| `setup.sql` | Creates the database, tables and sample data |
| `main.py` | The complete Python program |
| `sample_output.txt` | A real session recorded by running the program |

> All 7 programs were run against a real MySQL-compatible server and the outputs in `sample_output.txt` are genuine.

## The Projects

| # | Project | Database | Level | Special things it teaches |
|---|---|---|---|---|
| 1 | [**Hotel Management System**](01_hotel_management) | `hotel_db` | ★★★ | check-in / check-out, bill with GST, 3-table join, revenue `GROUP BY` |
| 2 | [Library Management System](02_library_management) | `library_db` | ★★ | issue / return, late-fine calculation with `DATEDIFF`, `IntegrityError` |
| 3 | [Student Result Management System](03_student_result_management) | `school_db` | ★★ | report card, ranks, `GROUP BY` + **`HAVING`**, SQL expressions & aliases |
| 4 | [Bank Management System](04_bank_management) | `bank_db` | ★★★ | PIN check, **`commit` / `rollback`** for money transfer, mini statement |
| 5 | [Stationery Shop Billing & Inventory](05_shop_billing_inventory) | `shop_db` | ★★★ | multi-item bill using `lastrowid`, stock update, sales reports |
| 6 | [Employee Payroll System](06_employee_payroll) | `company_db` | ★★ | salary slip, bulk `UPDATE`, `GROUP BY` + `HAVING`, `rowcount` |
| 7 | [Cinema Ticket Booking System](07_cinema_ticket_booking) | `cinema_db` | ★★ | seat availability, cancel & refund, housefull shows |

## Syllabus Coverage

| Topic (Sumita Arora) | Where it is used |
|---|---|
| Ch 13 – `SELECT`, `WHERE`, `LIKE`, `ORDER BY`, `IS NULL`, aliases, functions (`ROUND`, `DATEDIFF`, `CURDATE`), aggregates (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`) | All projects |
| Ch 14 – `CREATE TABLE`, constraints (PK, FK, NOT NULL, DEFAULT), `INSERT`, `UPDATE`, `DELETE` | All projects (`setup.sql` + `main.py`) |
| Ch 15 – `GROUP BY`, `HAVING`, equi-join, table aliases | All projects; `HAVING` in projects 3 and 6 |
| Ch 16 – `connect()`, `cursor()`, `execute()`, `fetchone()`, `fetchall()`, parameterised queries (`%s`), `commit()`, `rollback()`, `rowcount` | All projects |

## Setup (one time)

1. Install **MySQL Server** (and optionally MySQL Workbench) and **Python 3**.
2. Install the connector used in the textbook:
   ```
   pip install -r requirements.txt
   ```
3. Go inside a project folder and create its database:
   ```
   cd 01_hotel_management
   mysql -u root -p < setup.sql
   ```
   *(Alternatively open `setup.sql` in MySQL Workbench and press the lightning button.)*
4. Open `main.py` and replace `your_password` with your MySQL root password.
5. Run it:
   ```
   python main.py
   ```

`setup.sql` can be run again at any time – it drops and re-creates the database, so it also works as a **reset**.

## Common Errors

| Error | Reason / Fix |
|---|---|
| `ModuleNotFoundError: No module named 'pymysql'` | Run `pip install pymysql` |
| `RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password` | MySQL 8 login needs one extra package: `pip install cryptography` |
| `Access denied for user 'root'` | Wrong password in `main.py` |
| `Can't connect to MySQL server` | MySQL service is not running – start it |
| `Unknown database 'hotel_db'` | `setup.sql` was not run for that project |

## Notes for the Teacher

- The code uses **only what is in the textbook**: functions, `if / elif / else`, `while`, `try / except`, tuples and strings. No classes or extra libraries.
- Queries use **parameterised `%s` placeholders** (Section 16.3) and never join user input into SQL text.
- Each `README.md` has **5 practice tasks** (so different students can extend the same project differently) and **5 viva questions**.
- Students can be asked to **write the tables themselves** from the "Database Design" section instead of using `setup.sql`, which covers Chapter 14 as well.
- The programs were tested with **PyMySQL**, as used in the textbook. If your school uses `mysql.connector`, the calls used here are standard, so replacing `pymysql` with `mysql.connector` in the `import` line and in `pymysql.Error` / `pymysql.IntegrityError` should work, but please run it once before giving it to students.
