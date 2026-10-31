# Project 5 : Stationery Shop – Billing & Inventory System

**Database:** `shop_db`  |  **Difficulty:** ★★★  |  **Files:** `setup.sql`, `main.py`, `sample_output.txt`

## Problem Statement

A stationery shop near the school wants to stop using handwritten bills. The shopkeeper needs a program that keeps the **stock** of products and prepares **bills** for customers.

Write a menu-driven Python-MySQL program that can:

1. add a new product, view all products, change the price and **restock** a product,
2. show a **low-stock alert** (stock below 10),
3. create a **new bill** – the shopkeeper keeps entering product ID and quantity until he enters 0; the stock must reduce automatically and a bill with a grand total must be printed (a product cannot be sold if the stock is not enough; an empty bill must be cancelled),
4. reprint an old bill by its number,
5. show a **daily sales report**,
6. show the **top 3 best-selling products**,
7. delete a product (a product that was sold earlier cannot be deleted).

## Concepts Used (Sumita Arora, Class XII)

- **Ch 13** – `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `CURDATE()`, aggregate functions
- **Ch 14** – `CREATE TABLE` with three related tables, `INSERT`, `UPDATE` (`stock = stock - 3`), `DELETE`
- **Ch 15** – `GROUP BY` with `SUM` and `COUNT`, equi-join of `bill_items` and `products`
- **Ch 16** – `lastrowid` (to link bill items with the new bill), loops with multiple `execute()` calls, `commit()` / `rollback()`, handling `IntegrityError`

## Database Design

| Table | Columns | Purpose |
|---|---|---|
| `products` | **prod_id** (PK), name, category, price, stock | Items sold in the shop |
| `bills` | **bill_no** (PK, auto), cust_name, bill_date, total | Header of each bill |
| `bill_items` | **item_id** (PK, auto), bill_no (FK), prod_id (FK), qty, amount | The items on each bill |

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

> **Note:** Bills use `CURDATE()`, so a new bill carries **today's date** on your computer (the sample output shows the date on which it was recorded).

## Sample Output

A short extract is shown below. The **complete session** (every menu option, including wrong inputs) is in [`sample_output.txt`](sample_output.txt).

```text
============== STATIONERY SHOP ==============
Bill No : 4           Date : 2026-10-31
Customer: Meenal Arora
---------------------------------------------
Item                      Rate  Qty  Amount
---------------------------------------------
Notebook (200 pages)        60    3     180
Ball Pen (Blue)             10   10     100
Drawing File                70    2     140
---------------------------------------------
GRAND TOTAL                            Rs.420
=============================================
```

## Practice Tasks for Students

Try to extend the project yourself:

1. Give a **10% discount** if the bill total is Rs. 500 or more and show it on the bill.
2. Add an option to **search a product by name** (use `LIKE`).
3. Show the **total value of stock** of each category (`SUM(price * stock)` with `GROUP BY category`).
4. Show all the bills of a particular customer.
5. Display the **most expensive** and the **cheapest** product.

## Viva Questions

1. Why is the row in `bills` inserted first and the rows of `bill_items` afterwards? What gives us the new bill number?
2. Why do we call `con.rollback()` when the bill total is 0?
3. What would happen if the program crashed after reducing the stock but before the `commit()`?
4. Why can't product 1 be deleted, but a newly added product can?
5. Difference between `COUNT(*)` and `SUM(total)` in the daily sales report.
