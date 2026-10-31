"""
Project 7 : CINEMA TICKET BOOKING SYSTEM
Class XII - Computer Science (Python-MySQL connectivity)

Run setup.sql first, then change the PASSWORD below and run:  python main.py
"""
import pymysql

con = pymysql.connect(host="localhost", user="root",
                      password="your_password", database="cinema_db")
cur = con.cursor()

MAX_SEATS = 6         # maximum tickets in a single booking


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


def now_showing():
    cur.execute("SELECT * FROM movies ORDER BY movie_id")
    show(["ID", "Movie", "Language", "Duration (min)", "Ticket (Rs.)"], cur.fetchall())


def search_by_language():
    lang = input("Enter language : ")
    cur.execute("SELECT movie_id, title, duration, ticket_price FROM movies WHERE language = %s",
                (lang,))
    show(["ID", "Movie", "Duration (min)", "Ticket (Rs.)"], cur.fetchall())


def show_timings():
    cur.execute("SELECT s.show_id, m.title, s.show_date, s.show_time, s.seats_left "
                "FROM shows s, movies m WHERE s.movie_id = m.movie_id "
                "ORDER BY s.show_date, s.show_id")
    show(["Show ID", "Movie", "Date", "Time", "Seats Left"], cur.fetchall())


def book_tickets():
    sid = int(input("Show ID                 : "))
    cur.execute("SELECT m.title, m.ticket_price, s.seats_left, s.show_date, s.show_time "
                "FROM shows s, movies m WHERE s.movie_id = m.movie_id AND s.show_id = %s",
                (sid,))
    sh = cur.fetchone()
    if sh is None:
        print("No such show.")
        return
    title, price, left, sdate, stime = sh
    if left == 0:
        print("Sorry, this show is HOUSEFULL.")
        return

    name = input("Customer name           : ")
    seats = int(input("Number of tickets (max " + str(MAX_SEATS) + ") : "))
    if seats <= 0 or seats > MAX_SEATS:
        print("You can book between 1 and", MAX_SEATS, "tickets at a time.")
        return
    if seats > left:
        print("Only", left, "seats are left for this show.")
        return

    amount = seats * price
    cur.execute("INSERT INTO bookings (show_id, cust_name, seats, amount) VALUES (%s, %s, %s, %s)",
                (sid, name, seats, amount))
    booking_id = cur.lastrowid
    cur.execute("UPDATE shows SET seats_left = seats_left - %s WHERE show_id = %s", (seats, sid))
    con.commit()

    print("\n************ E-TICKET ************")
    print("Booking ID :", booking_id)
    print("Name       :", name)
    print("Movie      :", title)
    print("Date/Time  :", sdate, stime)
    print("Tickets    :", seats, "x Rs.", price)
    print("AMOUNT PAID: Rs.", amount)
    print("**********************************")


def cancel_booking():
    bid = int(input("Booking ID to cancel : "))
    cur.execute("SELECT show_id, seats, amount FROM bookings WHERE booking_id = %s", (bid,))
    b = cur.fetchone()
    if b is None:
        print("No booking with this ID.")
        return
    cur.execute("UPDATE shows SET seats_left = seats_left + %s WHERE show_id = %s", (b[1], b[0]))
    cur.execute("DELETE FROM bookings WHERE booking_id = %s", (bid,))
    con.commit()
    refund = b[2] * 80 / 100              # 20% cancellation charges
    print("Booking cancelled. Refund amount : Rs.", format(refund, ".2f"), "(20% deducted)")


def my_bookings():
    name = input("Enter your name : ")
    cur.execute("SELECT b.booking_id, m.title, s.show_date, s.show_time, b.seats, b.amount "
                "FROM bookings b, shows s, movies m "
                "WHERE b.show_id = s.show_id AND s.movie_id = m.movie_id "
                "AND b.cust_name LIKE %s", ("%" + name + "%",))
    show(["Booking", "Movie", "Date", "Time", "Seats", "Amount"], cur.fetchall())


def revenue_report():
    cur.execute("SELECT m.title, COUNT(*), SUM(b.seats), SUM(b.amount) "
                "FROM bookings b, shows s, movies m "
                "WHERE b.show_id = s.show_id AND s.movie_id = m.movie_id "
                "GROUP BY m.title ORDER BY SUM(b.amount) DESC")
    show(["Movie", "Bookings", "Tickets Sold", "Revenue (Rs.)"], cur.fetchall())
    cur.execute("SELECT SUM(amount) FROM bookings")
    print("Total box-office collection : Rs.", cur.fetchone()[0])


def housefull_shows():
    cur.execute("SELECT s.show_id, m.title, s.show_date, s.show_time "
                "FROM shows s, movies m WHERE s.movie_id = m.movie_id AND s.seats_left = 0")
    print("Housefull shows:")
    show(["Show ID", "Movie", "Date", "Time"], cur.fetchall())


def add_show():
    sid = int(input("New Show ID         : "))
    mid = int(input("Movie ID            : "))
    d = input("Date (YYYY-MM-DD)    : ")
    t = input("Time (e.g. 03:00 PM) : ")
    seats = int(input("Total seats         : "))
    cur.execute("INSERT INTO shows VALUES (%s, %s, %s, %s, %s)", (sid, mid, d, t, seats))
    con.commit()
    print("New show added.")


MENU = """
======== CINEMA TICKET BOOKING SYSTEM ========
 1. Now showing (list of movies)
 2. Search movies by language
 3. Show timings
 4. Book tickets
 5. Cancel a booking
 6. View my bookings
 7. Revenue report (movie-wise)
 8. Housefull shows
 9. Add a new show (admin)
 0. Exit
=============================================="""

while True:
    print(MENU)
    choice = input("Enter your choice : ")
    try:
        if choice == "1":
            now_showing()
        elif choice == "2":
            search_by_language()
        elif choice == "3":
            show_timings()
        elif choice == "4":
            book_tickets()
        elif choice == "5":
            cancel_booking()
        elif choice == "6":
            my_bookings()
        elif choice == "7":
            revenue_report()
        elif choice == "8":
            housefull_shows()
        elif choice == "9":
            add_show()
        elif choice == "0":
            print("Thank you! Enjoy the movie!")
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
