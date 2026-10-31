# Project 6 : Employee Payroll Management System

**Database:** `company_db`  |  **Difficulty:** ★★  |  **Files:** `setup.sql`, `main.py`, `sample_output.txt`

## Problem Statement

A company wants to automate the salary calculation of its employees. Every employee belongs to a department. The salary is calculated as follows:

- DA (Dearness Allowance) = 20% of basic salary
- HRA (House Rent Allowance) = 15% of basic salary
- Gross salary = Basic + DA + HRA
- PF (Provident Fund) = 12% of basic salary (deducted)
- **Net salary = Gross salary − PF**

Write a menu-driven Python-MySQL program that can:

1. add, view, search (by name or designation) and remove employees,
2. generate the **salary slip** of an employee,
3. give an **increment (%)** to one employee, or to a **whole department** with one query,
4. show a **department-wise summary** (employees, total, average and highest basic salary) – with an option to show only departments having at least *N* employees,
5. show the highest and lowest paid employee,
6. show the total salary the company has to pay this month.

## Concepts Used (Sumita Arora, Class XII)

- **Ch 13** – `SELECT`, `LIKE`, `ORDER BY`, `LIMIT`, `ROUND()`, aggregate functions `COUNT / SUM / AVG / MAX`, arithmetic in SQL
- **Ch 14** – `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `INSERT`, `UPDATE` (bulk update with `WHERE`), `DELETE`
- **Ch 15** – `GROUP BY` **with `HAVING`**, equi-join of `employees` and `departments`
- **Ch 16** – parameterised queries, `rowcount` (to show how many rows an `UPDATE` changed), formatting numbers in Python

## Database Design

| Table | Columns | Purpose |
|---|---|---|
| `departments` | **dept_id** (PK), dept_name, location | Departments of the company |
| `employees` | **emp_id** (PK), name, dept_id (FK), designation, basic_salary, join_date | Employee records |

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
=========== SALARY SLIP ===========
Emp ID      : 1009
Name        : Sneha Kulkarni
Department  : IT - Team Lead
-----------------------------------
Basic Salary      :   70000.00
DA  (20%)         :   14000.00
HRA (15%)         :   10500.00
Gross Salary      :   94500.00
PF  (12%) [-]     :    8400.00
-----------------------------------
NET SALARY        :   86100.00
===================================
```

## Practice Tasks for Students

Try to extend the project yourself:

1. Display the employees who **joined before 2018** (compare the `join_date` with a date).
2. Display all employees of a department whose **name** is typed by the user (join with `WHERE dept_name = %s`).
3. Show the **experience (in years)** of every employee using `YEAR(CURDATE()) - YEAR(join_date)`.
4. Show the **department that pays the highest total basic salary**.
5. Add an option to **transfer an employee** to another department (`UPDATE dept_id`).

## Viva Questions

1. In the original sample data the *Research* department has no employees, so it does not appear in the department summary. Why? (Think about the equi-join.)
2. Why is `HAVING` used in the summary and not `WHERE`?
3. What is the use of `cur.rowcount` after the department-wise increment?
4. The salary slip is calculated in Python while the summary is calculated in SQL. Which one do you prefer and why?
5. What are the allowed values of `dept_id` in `employees`? Which constraint decides this?
