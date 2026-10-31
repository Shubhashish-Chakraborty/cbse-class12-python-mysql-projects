# Project 4 : Bank Management System

**Database:** `bank_db`  |  **Difficulty:** ★★★  |  **Files:** `setup.sql`, `main.py`, `sample_output.txt`

## Problem Statement

A small co-operative bank wants a simple computer program for its counter staff. Every customer has an account number and a secret 4-digit PIN. Every account (Savings or Current) must always keep a **minimum balance of Rs. 500**.

Write a menu-driven Python-MySQL program that can:

1. open a new account (opening deposit at least Rs. 500),
2. **deposit** and **withdraw** money after verifying the PIN (a withdrawal must not take the balance below Rs. 500),
3. **transfer** money from one account to another – the money must be deducted from one account and added to the other **together**; if anything fails, nothing should change,
4. show the balance of an account,
5. print a **mini statement** (last 5 transactions),
6. show a **bank summary** – number of accounts, total balance and highest balance for each account type,
7. close an account.

## Concepts Used (Sumita Arora, Class XII)

- **Ch 13** – `SELECT`, `ORDER BY ... DESC`, `LIMIT`, aggregate functions `COUNT / SUM / MAX`
- **Ch 14** – `CREATE TABLE`, `INSERT`, `UPDATE` (with expressions like `balance = balance + 500`), `DELETE`, foreign key
- **Ch 15** – `GROUP BY`
- **Ch 16** – parameterised queries, **transactions: `commit()` and `rollback()`**, `lastrowid`, `try / except` with `pymysql.Error`

## Database Design

| Table | Columns | Purpose |
|---|---|---|
| `accounts` | **acc_no** (PK, auto), name, acc_type, pin, balance | One row per bank account |
| `transactions` | **txn_id** (PK, auto), acc_no (FK), txn_type, amount, txn_time | Every deposit, withdrawal, transfer. `txn_time` is filled automatically |

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
Last 5 transactions of account 1006
+--------+-------------+--------+---------------------+
| Txn ID | Type        | Amount | Date & Time         |
+--------+-------------+--------+---------------------+
| 5      | Transfer In | 5000   | 2026-10-31 07:43:36 |
| 3      | Withdraw    | 1200   | 2026-10-31 07:43:36 |
| 2      | Deposit     | 1500   | 2026-10-31 07:43:36 |
| 1      | Opening     | 2000   | 2026-10-31 07:43:36 |
+--------+-------------+--------+---------------------+
```

## Practice Tasks for Students

Try to extend the project yourself:

1. Add an option to **change the PIN** (the old PIN must be verified first).
2. Display all accounts having a balance **greater than a given amount**.
3. Add **4% yearly interest** to every Savings account using one `UPDATE` query and record it as a transaction.
4. Set a **daily withdrawal limit of Rs. 10,000** (use `SUM` on the `transactions` table for today).
5. Show the total deposits and total withdrawals of an account (`GROUP BY txn_type`).

## Viva Questions

1. Why are both `UPDATE` statements of a transfer committed with a single `con.commit()`?
2. What does `con.rollback()` do and when is it useful?
3. Why do we verify the PIN with a `SELECT ... WHERE acc_no = %s AND pin = %s` query?
4. Why is `ORDER BY txn_id DESC LIMIT 5` used in the mini statement?
5. Why must the transactions of an account be deleted before the account is deleted?
