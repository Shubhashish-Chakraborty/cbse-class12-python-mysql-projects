# Project 2 : Library Management System

**Database:** `library_db`  |  **Difficulty:** ★★  |  **Files:** `setup.sql`, `main.py`, `sample_output.txt`

## Problem Statement

The school library issues books to students. The librarian wants a program to manage the books, the members and the issue/return of books.

Write a menu-driven Python-MySQL program that can:

1. add new books and new members,
2. display all books and **search** a book by a part of its title or author,
3. **issue** a book to a member (number of copies must reduce by one; a book with 0 copies cannot be issued),
4. **return** a book and calculate the **late fine** – a book may be kept for 14 days, after that the fine is Rs. 2 per day (number of copies must increase by one),
5. list all books that are currently issued (with member name and class),
6. show a **category-wise report** (number of titles and copies in each category),
7. delete a book (a book that has issue records cannot be deleted).

## Concepts Used (Sumita Arora, Class XII)

- **Ch 13** – `SELECT`, `LIKE` with `OR`, `ORDER BY`, `DATEDIFF()`, `IS NULL`
- **Ch 14** – `CREATE TABLE` with constraints, `INSERT`, `UPDATE`, `DELETE`, foreign keys
- **Ch 15** – `GROUP BY` with `COUNT / SUM`, equi-join of three tables
- **Ch 16** – connecting with `pymysql`, parameterised queries, `rowcount`, `commit()` / `rollback()`, handling `IntegrityError`

## Database Design

| Table | Columns | Purpose |
|---|---|---|
| `books` | **book_id** (PK), title, author, category, copies | Books and number of copies *available on the shelf* |
| `members` | **member_id** (PK, auto), name, class | Library members |
| `issues` | **issue_id** (PK, auto), book_id (FK), member_id (FK), issue_date, return_date, fine | One row per issue. `return_date IS NULL` means not yet returned |

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
Book ID               : 110
Member ID             : 5
Return date (YYYY-MM-DD): 2026-11-10
Book returned after 21 days.
Late fine to be paid : Rs. 14
```

## Practice Tasks for Students

Try to extend the project yourself:

1. Display all books of a particular **category**.
2. Display all the books currently issued to a particular member (use a join).
3. A member should not be allowed to hold **more than 3 books** at a time (use `COUNT(*)` on pending issues).
4. Show the **most frequently issued** book (use `GROUP BY` on `issues`, `ORDER BY COUNT(*) DESC`, `LIMIT 1`).
5. Add an option to **change the number of copies** of a book (for example when new copies are bought).

## Viva Questions

1. Why do we reduce `copies` when a book is issued, and increase it again on return?
2. How does the program know that a book has not been returned yet?
3. Why does deleting book 103 give an error even though it exists? Which constraint is responsible?
4. What does `cur.rowcount` give after `DELETE`?
5. Which SQL function is used to find the number of days between two dates?
