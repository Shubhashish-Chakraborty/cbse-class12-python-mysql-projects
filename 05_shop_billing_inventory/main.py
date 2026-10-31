"""
Project 5 : STATIONERY SHOP - BILLING & INVENTORY SYSTEM
Class XII - Computer Science (Python-MySQL connectivity)

Run setup.sql first, then change the PASSWORD below and run:  python main.py
"""
import pymysql

con = pymysql.connect(host="localhost", user="root",
                      password="your_password", database="shop_db")
cur = con.cursor()

LOW_STOCK_LIMIT = 10      # products with stock below this are "low stock"


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


def add_product():
    pid = int(input("Product ID   : "))
    name = input("Product name : ")
    cat = input("Category     : ")
    price = int(input("Price (Rs.)  : "))
    stock = int(input("Stock        : "))
    cur.execute("INSERT INTO products VALUES (%s, %s, %s, %s, %s)", (pid, name, cat, price, stock))
    con.commit()
    print("Product added successfully.")


def view_products():
    cur.execute("SELECT * FROM products ORDER BY prod_id")
    show(["ID", "Product", "Category", "Price", "Stock"], cur.fetchall())


def restock():
    pid = int(input("Product ID : "))
    qty = int(input("Quantity received : "))
    cur.execute("UPDATE products SET stock = stock + %s WHERE prod_id = %s", (qty, pid))
    con.commit()
    if cur.rowcount == 0:
        print("No such product.")
    else:
        print("Stock updated.")


def change_price():
    pid = int(input("Product ID : "))
    price = int(input("New price (Rs.) : "))
    cur.execute("UPDATE products SET price = %s WHERE prod_id = %s", (price, pid))
    con.commit()
    if cur.rowcount == 0:
        print("No such product (or price is same as before).")
    else:
        print("Price updated.")


def low_stock():
    cur.execute("SELECT prod_id, name, stock FROM products WHERE stock < %s ORDER BY stock",
                (LOW_STOCK_LIMIT,))
    print("Products with stock below", LOW_STOCK_LIMIT, ": (order these soon!)")
    show(["ID", "Product", "Stock"], cur.fetchall())


def print_bill(bill_no):
    cur.execute("SELECT cust_name, bill_date, total FROM bills WHERE bill_no = %s", (bill_no,))
    head = cur.fetchone()
    if head is None:
        print("No such bill.")
        return
    cur.execute("SELECT p.name, p.price, bi.qty, bi.amount "
                "FROM bill_items bi, products p "
                "WHERE bi.prod_id = p.prod_id AND bi.bill_no = %s", (bill_no,))
    items = cur.fetchall()

    print("\n============== STATIONERY SHOP ==============")
    print("Bill No :", bill_no, "          Date :", head[1])
    print("Customer:", head[0])
    print("---------------------------------------------")
    print("Item".ljust(24), "Rate".rjust(5), "Qty".rjust(4), "Amount".rjust(7))
    print("---------------------------------------------")
    for it in items:
        print(it[0].ljust(24), str(it[1]).rjust(5), str(it[2]).rjust(4), str(it[3]).rjust(7))
    print("---------------------------------------------")
    print("GRAND TOTAL".ljust(35), ("Rs." + str(head[2])).rjust(9))
    print("=============================================")


def create_bill():
    cust = input("Customer name : ")
    cur.execute("INSERT INTO bills (cust_name, bill_date) VALUES (%s, CURDATE())", (cust,))
    bill_no = cur.lastrowid
    total = 0
    while True:
        pid = int(input("Product ID (0 to finish) : "))
        if pid == 0:
            break
        cur.execute("SELECT name, price, stock FROM products WHERE prod_id = %s", (pid,))
        p = cur.fetchone()
        if p is None:
            print("  Invalid product ID.")
            continue
        qty = int(input("  Quantity of " + p[0] + " : "))
        if qty <= 0 or qty > p[2]:
            print("  Not possible. Only", p[2], "in stock.")
            continue
        amount = qty * p[1]
        cur.execute("INSERT INTO bill_items (bill_no, prod_id, qty, amount) "
                    "VALUES (%s, %s, %s, %s)", (bill_no, pid, qty, amount))
        cur.execute("UPDATE products SET stock = stock - %s WHERE prod_id = %s", (qty, pid))
        total = total + amount
        print("  Added. Running total = Rs.", total)

    if total == 0:
        con.rollback()                      # nothing was bought, so cancel the bill
        print("Empty bill cancelled.")
        return
    cur.execute("UPDATE bills SET total = %s WHERE bill_no = %s", (total, bill_no))
    con.commit()
    print_bill(bill_no)


def view_bill():
    bno = int(input("Enter bill number : "))
    print_bill(bno)


def daily_sales():
    cur.execute("SELECT bill_date, COUNT(*), SUM(total) FROM bills "
                "GROUP BY bill_date ORDER BY bill_date")
    show(["Date", "Bills", "Sales (Rs.)"], cur.fetchall())


def top_selling():
    cur.execute("SELECT p.name, SUM(bi.qty), SUM(bi.amount) "
                "FROM bill_items bi, products p WHERE bi.prod_id = p.prod_id "
                "GROUP BY p.name ORDER BY SUM(bi.qty) DESC LIMIT 3")
    print("Top 3 best-selling products (by quantity):")
    show(["Product", "Units Sold", "Revenue (Rs.)"], cur.fetchall())


def delete_product():
    pid = int(input("Product ID to delete : "))
    try:
        cur.execute("DELETE FROM products WHERE prod_id = %s", (pid,))
        con.commit()
        if cur.rowcount == 0:
            print("No such product.")
        else:
            print("Product deleted.")
    except pymysql.IntegrityError:
        con.rollback()
        print("Cannot delete: this product appears in old bills.")


MENU = """
======= STATIONERY SHOP - BILLING & INVENTORY =======
  1. Add new product
  2. View all products
  3. Restock a product
  4. Change price of a product
  5. Low-stock alert
  6. Create new bill
  7. Reprint an old bill
  8. Daily sales report
  9. Top 3 best-selling products
 10. Delete a product
  0. Exit
====================================================="""

while True:
    print(MENU)
    choice = input("Enter your choice : ")
    try:
        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            restock()
        elif choice == "4":
            change_price()
        elif choice == "5":
            low_stock()
        elif choice == "6":
            create_bill()
        elif choice == "7":
            view_bill()
        elif choice == "8":
            daily_sales()
        elif choice == "9":
            top_selling()
        elif choice == "10":
            delete_product()
        elif choice == "0":
            print("Thank you! Visit again.")
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
