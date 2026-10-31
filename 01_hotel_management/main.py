"""
Project 1 : HOTEL MANAGEMENT SYSTEM
Class XII - Computer Science (Python-MySQL connectivity)

Run setup.sql first, then change the PASSWORD below and run:  python main.py
"""
import pymysql

# ------------------------------------------------------------
#  Step 1 : connect to MySQL  (change user / password if needed)
# ------------------------------------------------------------
con = pymysql.connect(host="localhost", user="root",
                      password="your_password", database="hotel_db")
cur = con.cursor()

GST_PERCENT = 12


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


# ------------------------------------------------------------
#  Step 2 : one function for every feature of the project
# ------------------------------------------------------------
def add_customer():
    name = input("Customer name   : ")
    phone = input("Phone number    : ")
    city = input("City            : ")
    cur.execute("INSERT INTO customers (name, phone, city) VALUES (%s, %s, %s)",
                (name, phone, city))
    con.commit()
    print("Customer added successfully. Customer ID =", cur.lastrowid)


def view_rooms(only_available):
    if only_available:
        cur.execute("SELECT room_no, room_type, price_per_night FROM rooms "
                    "WHERE status = 'Available' ORDER BY room_no")
        show(["Room No", "Type", "Price/Night"], cur.fetchall())
    else:
        cur.execute("SELECT room_no, room_type, price_per_night, status "
                    "FROM rooms ORDER BY room_no")
        show(["Room No", "Type", "Price/Night", "Status"], cur.fetchall())


def check_in():
    cid = int(input("Customer ID            : "))
    cur.execute("SELECT name FROM customers WHERE cust_id = %s", (cid,))
    cust = cur.fetchone()
    if cust is None:
        print("No customer with this ID. Add the customer first.")
        return

    rno = int(input("Room number            : "))
    cur.execute("SELECT status FROM rooms WHERE room_no = %s", (rno,))
    room = cur.fetchone()
    if room is None:
        print("No such room.")
        return
    if room[0] != "Available":
        print("Sorry, room", rno, "is already occupied.")
        return

    cin = input("Check-in date (YYYY-MM-DD): ")
    cur.execute("INSERT INTO bookings (cust_id, room_no, check_in) VALUES (%s, %s, %s)",
                (cid, rno, cin))
    cur.execute("UPDATE rooms SET status = 'Occupied' WHERE room_no = %s", (rno,))
    con.commit()
    print("Check-in done. Room", rno, "allotted to", cust[0])


def check_out():
    rno = int(input("Room number to check-out: "))
    cur.execute("SELECT b.booking_id, c.name, b.check_in, r.price_per_night "
                "FROM bookings b, customers c, rooms r "
                "WHERE b.cust_id = c.cust_id AND b.room_no = r.room_no "
                "AND b.room_no = %s AND b.check_out IS NULL", (rno,))
    rec = cur.fetchone()
    if rec is None:
        print("This room has no active booking.")
        return

    bid, name, cin, price = rec
    cout = input("Check-out date (YYYY-MM-DD): ")
    cur.execute("SELECT DATEDIFF(%s, %s)", (cout, cin))
    nights = cur.fetchone()[0]
    if nights is None or nights < 0:
        print("Invalid check-out date.")
        return
    if nights == 0:                      # same-day stay is charged for 1 night
        nights = 1

    amount = nights * price
    gst = amount * GST_PERCENT / 100
    total = amount + gst

    cur.execute("UPDATE bookings SET check_out = %s, nights = %s, bill = %s "
                "WHERE booking_id = %s", (cout, nights, total, bid))
    cur.execute("UPDATE rooms SET status = 'Available' WHERE room_no = %s", (rno,))
    con.commit()

    print("\n========== HOTEL BILL ==========")
    print("Guest         :", name)
    print("Room No       :", rno)
    print("Check-in      :", cin)
    print("Check-out     :", cout)
    print("Nights        :", nights, "x Rs.", price)
    print("Room charges  : Rs.", format(amount, ".2f"))
    print("GST (" + str(GST_PERCENT) + "%)     : Rs.", format(gst, ".2f"))
    print("TOTAL BILL    : Rs.", format(total, ".2f"))
    print("================================")


def current_guests():
    cur.execute("SELECT r.room_no, c.name, c.phone, r.room_type, b.check_in "
                "FROM bookings b, customers c, rooms r "
                "WHERE b.cust_id = c.cust_id AND b.room_no = r.room_no "
                "AND b.check_out IS NULL ORDER BY r.room_no")
    show(["Room No", "Guest", "Phone", "Type", "Check-in"], cur.fetchall())


def search_customer():
    name = input("Enter name (or part of name): ")
    cur.execute("SELECT cust_id, name, phone, city FROM customers WHERE name LIKE %s",
                ("%" + name + "%",))
    show(["Cust ID", "Name", "Phone", "City"], cur.fetchall())


def customer_history():
    cid = int(input("Customer ID: "))
    cur.execute("SELECT b.booking_id, b.room_no, r.room_type, b.check_in, b.check_out, b.bill "
                "FROM bookings b, rooms r "
                "WHERE b.room_no = r.room_no AND b.cust_id = %s", (cid,))
    show(["Booking", "Room", "Type", "Check-in", "Check-out", "Bill (Rs.)"], cur.fetchall())


def revenue_report():
    cur.execute("SELECT r.room_type, COUNT(*), SUM(b.nights), SUM(b.bill) "
                "FROM bookings b, rooms r "
                "WHERE b.room_no = r.room_no AND b.check_out IS NOT NULL "
                "GROUP BY r.room_type")
    show(["Room Type", "Stays", "Total Nights", "Revenue (Rs.)"], cur.fetchall())

    cur.execute("SELECT SUM(bill) FROM bookings WHERE check_out IS NOT NULL")
    print("Total revenue so far : Rs.", cur.fetchone()[0])


# ------------------------------------------------------------
#  Step 3 : menu-driven main program
# ------------------------------------------------------------
MENU = """
=========== HOTEL MANAGEMENT SYSTEM ===========
 1. Add new customer
 2. View all rooms
 3. View available rooms
 4. Check-in  (allot a room)
 5. Check-out (generate bill)
 6. View current guests
 7. Search customer by name
 8. Booking history of a customer
 9. Revenue report (room-type wise)
 0. Exit
==============================================="""

while True:
    print(MENU)
    choice = input("Enter your choice : ")
    try:
        if choice == "1":
            add_customer()
        elif choice == "2":
            view_rooms(False)
        elif choice == "3":
            view_rooms(True)
        elif choice == "4":
            check_in()
        elif choice == "5":
            check_out()
        elif choice == "6":
            current_guests()
        elif choice == "7":
            search_customer()
        elif choice == "8":
            customer_history()
        elif choice == "9":
            revenue_report()
        elif choice == "0":
            print("Thank you for using the Hotel Management System!")
            break
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Please enter a number where a number is required.")
        con.rollback()
    except pymysql.Error as e:
        print("Database error :", e)
        con.rollback()

con.close()
