# Project 3 : Student Result Management System

**Database:** `school_db`  |  **Difficulty:** ★★  |  **Files:** `setup.sql`, `main.py`, `sample_output.txt`

## Problem Statement

The class teacher of Class XII wants to prepare the result of her students. Each student has marks in five subjects – Physics, Chemistry, Maths, English and Computer Science (each out of 100). A student passes only if he/she scores at least **33 in every subject**.

Write a menu-driven Python-MySQL program that can:

1. add a student along with the marks,
2. print a **report card** (total, percentage, result and grade: A+ ≥ 90, A ≥ 75, B ≥ 60, C ≥ 45, otherwise D),
3. display a **rank-wise result sheet** of the whole class,
4. update the marks of a student in any one subject,
5. find the **topper**,
6. display a **section-wise performance** report (number of students, average percentage, highest total) – with an option to show only sections above a given average,
7. list the students who have **failed**,
8. show the **average, highest and lowest** marks of every subject,
9. delete a student's record.

## Concepts Used (Sumita Arora, Class XII)

- **Ch 13** – scalar expressions (`physics + chemistry + ...`), column aliases (`AS total`), `ROUND()`, `ORDER BY ... DESC`, `LIMIT`, `AVG / MAX / MIN`, `OR` conditions
- **Ch 14** – `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `INSERT`, `UPDATE`, `DELETE` (child table first)
- **Ch 15** – `GROUP BY` **with `HAVING`**, equi-join of `students` and `marks`
- **Ch 16** – connecting with `pymysql`, parameterised queries, validating input before storing it

## Database Design

| Table | Columns | Purpose |
|---|---|---|
| `students` | **roll_no** (PK), name, section | Personal details of a student |
| `marks` | **roll_no** (PK, FK), physics, chemistry, maths, english, cs | Marks of the same student (one row per student) |

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
============ REPORT CARD ============
Roll No : 11    Section : A
Name    : Kunal Verma
-------------------------------------
Physics          : 85
Chemistry        : 80
Maths            : 90
English          : 72
Computer Science : 95
-------------------------------------
Total            : 422 / 500
Percentage       : 84.40 %
Result           : PASS    Grade : A
=====================================

======== STUDENT RESULT MANAGEMENT SYSTEM ========
```

## Practice Tasks for Students

Try to extend the project yourself:

1. Display the students who scored **more than 90 in Computer Science**.
2. Display the **topper of every section** (not only of the whole school).
3. Count how many students got each grade (A+, A, B, C, D) – think about how to use `GROUP BY` or Python.
4. Add an option to **search a student by name** (use `LIKE`).
5. Show the students who are in **compartment** – failed in exactly one subject.

## Viva Questions

1. Why are the personal details and the marks stored in two different tables?
2. Why do we delete from `marks` first and then from `students`?
3. Difference between `WHERE` and `HAVING`.
4. In `update_marks()` the column name is added to the query with `+`, but the marks value uses `%s`. Why can't a column name be passed through `%s`?
5. What does `ROUND(AVG(...), 2)` do?
