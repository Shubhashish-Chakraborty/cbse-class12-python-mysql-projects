"""
Project 4 : BANK MANAGEMENT SYSTEM
Class XII - Computer Science (Python-MySQL connectivity)

Run setup.sql first, then change the PASSWORD below and run:  python main.py
"""
import pymysql

con = pymysql.connect(host="localhost", user="root",
                      password="your_password", database="bank_db")
cur = con.cursor()

MIN_BALANCE = 500          # every account must always keep at least Rs. 500


def show(headers, rows):
    """Prints rows (list of tuples) as a neat table."""
    if not rows:
        print("No records found.")
        return
    widths = [len(h) for h in headers]
    for r in rows:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len(str(v)))
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(line)
    print("|" + "|".join(" " + h.ljust(widths[i]) + " " for i, h in enumerate(headers)) + "|")
    print(line)
    for r in rows:
        print("|" + "|".join(" " + ("-" if v is None else str(v)).ljust(widths[i]) + " "
                             for i, v in enumerate(r)) + "|")
    print(line)


def verify(acc_no, pin):
    """Returns (name, balance) if account number and PIN are correct, else None."""
    cur.execute("SELECT name, balance FROM accounts WHERE acc_no = %s AND pin = %s",
                (acc_no, pin))
    return cur.fetchone()


def record(acc_no, txn_type, amount):
    cur.execute("INSERT INTO transactions (acc_no, txn_type, amount) VALUES (%s, %s, %s)",
                (acc_no, txn_type, amount))


def open_account():
    name = input("Account holder name        : ")
    t = input("Account type (S-Savings / C-Current) : ").upper()
    if t not in ("S", "C"):
        print("Invalid account type.")
        return
    acc_type = "Savings" if t == "S" else "Current"
    pin = int(input("Set a 4-digit PIN          : "))
    amount = int(input("Opening deposit (min Rs.500) : "))
    if amount < MIN_BALANCE:
        print("Opening deposit must be at least Rs.", MIN_BALANCE)
        return
    cur.execute("INSERT INTO accounts (name, acc_type, pin, balance) VALUES (%s, %s, %s, %s)",
                (name, acc_type, pin, amount))
    acc_no = cur.lastrowid
    record(acc_no, "Opening", amount)
    con.commit()
    print("Account opened successfully! Your account number is", acc_no)


def deposit():
    acc = int(input("Account number : "))
    pin = int(input("PIN            : "))
    if verify(acc, pin) is None:
        print("Wrong account number or PIN.")
        return
    amt = int(input("Amount to deposit : "))
    if amt <= 0:
        print("Amount must be positive.")
        return
    cur.execute("UPDATE accounts SET balance = balance + %s WHERE acc_no = %s", (amt, acc))
    record(acc, "Deposit", amt)
    con.commit()
    print("Rs.", amt, "deposited successfully.")


def withdraw():
    acc = int(input("Account number : "))
    pin = int(input("PIN            : "))
    user = verify(acc, pin)
    if user is None:
        print("Wrong account number or PIN.")
        return
    amt = int(input("Amount to withdraw : "))
    if amt <= 0:
        print("Amount must be positive.")
    elif user[1] - amt < MIN_BALANCE:
        print("Insufficient balance! Minimum balance of Rs.", MIN_BALANCE, "must be maintained.")
    else:
        cur.execute("UPDATE accounts SET balance = balance - %s WHERE acc_no = %s", (amt, acc))
        record(acc, "Withdraw", amt)
        con.commit()
        print("Please collect your cash: Rs.", amt)


def transfer():
    src = int(input("Your account number : "))
    pin = int(input("PIN                 : "))
    user = verify(src, pin)
    if user is None:
        print("Wrong account number or PIN.")
        return
    dest = int(input("Receiver account no.  : "))
    cur.execute("SELECT name FROM accounts WHERE acc_no = %s", (dest,))
    receiver = cur.fetchone()
    if receiver is None or dest == src:
        print("Invalid receiver account.")
        return
    amt = int(input("Amount to transfer   : "))
    if amt <= 0 or user[1] - amt < MIN_BALANCE:
        print("Transfer failed: insufficient balance or invalid amount.")
        return

    try:
        # both updates must succeed together, otherwise none of them should happen
        cur.execute("UPDATE accounts SET balance = balance - %s WHERE acc_no = %s", (amt, src))
        cur.execute("UPDATE accounts SET balance = balance + %s WHERE acc_no = %s", (amt, dest))
        record(src, "Transfer Out", amt)
        record(dest, "Transfer In", amt)
        con.commit()
        print("Rs.", amt, "transferred to", receiver[0], "successfully.")
    except pymysql.Error:
        con.rollback()
        print("Transfer failed. No money has been deducted.")


def balance_enquiry():
    acc = int(input("Account number : "))
    pin = int(input("PIN            : "))
    user = verify(acc, pin)
    if user is None:
        print("Wrong account number or PIN.")
    else:
        print("Account holder :", user[0])
        print("Available balance : Rs.", user[1])


def mini_statement():
    acc = int(input("Account number : "))
    pin = int(input("PIN            : "))
    if verify(acc, pin) is None:
        print("Wrong account number or PIN.")
        return
    cur.execute("SELECT txn_id, txn_type, amount, txn_time FROM transactions "
                "WHERE acc_no = %s ORDER BY txn_id DESC LIMIT 5", (acc,))
    print("Last 5 transactions of account", acc)
    show(["Txn ID", "Type", "Amount", "Date & Time"], cur.fetchall())


def bank_summary():
    cur.execute("SELECT acc_type, COUNT(*), SUM(balance), MAX(balance) FROM accounts "
                "GROUP BY acc_type")
    show(["Account Type", "Accounts", "Total Balance", "Highest Balance"], cur.fetchall())
    cur.execute("SELECT SUM(balance) FROM accounts")
    print("Total money held by the bank : Rs.", cur.fetchone()[0])


def close_account():
    acc = int(input("Account number : "))
    pin = int(input("PIN            : "))
    user = verify(acc, pin)
    if user is None:
        print("Wrong account number or PIN.")
        return
    sure = input("Close account of " + user[0] + " with balance Rs." + str(user[1]) + "? (y/n) : ")
    if sure.lower() == "y":
        cur.execute("DELETE FROM transactions WHERE acc_no = %s", (acc,))
        cur.execute("DELETE FROM accounts WHERE acc_no = %s", (acc,))
        con.commit()
        print("Account closed. Please collect Rs.", user[1])
    else:
        print("Account closing cancelled.")


MENU = """
========== BANK MANAGEMENT SYSTEM ==========
 1. Open a new account
 2. Deposit money
 3. Withdraw money
 4. Transfer money
 5. Balance enquiry
 6. Mini statement (last 5 transactions)
 7. Bank summary (account-type wise)
 8. Close an account
 0. Exit
============================================"""

while True:
    print(MENU)
    choice = input("Enter your choice : ")
    try:
        if choice == "1":
            open_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            transfer()
        elif choice == "5":
            balance_enquiry()
        elif choice == "6":
            mini_statement()
        elif choice == "7":
            bank_summary()
        elif choice == "8":
            close_account()
        elif choice == "0":
            print("Thank you for banking with us!")
            break
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Please enter numbers only where a number is required.")
        con.rollback()
    except pymysql.Error as e:
        print("Database error :", e)
        con.rollback()

con.close()
