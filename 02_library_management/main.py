"""
Project 2 : LIBRARY MANAGEMENT SYSTEM
Class XII - Computer Science (Python-MySQL connectivity)

Run setup.sql first, then change the PASSWORD below and run:  python main.py
"""
import pymysql

con = pymysql.connect(host="localhost", user="root",
                      password="your_password", database="library_db")
cur = con.cursor()

FREE_DAYS = 14        # a book can be kept for 14 days without fine
FINE_PER_DAY = 2      # Rs. 2 per day after that


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


def add_book():
    bid = int(input("Book ID            : "))
    title = input("Title              : ")
    author = input("Author             : ")
    category = input("Category           : ")
    copies = int(input("Number of copies   : "))
    cur.execute("INSERT INTO books VALUES (%s, %s, %s, %s, %s)",
                (bid, title, author, category, copies))
    con.commit()
    print("Book added successfully.")


def add_member():
    name = input("Member name : ")
    cls = input("Class       : ")
    cur.execute("INSERT INTO members (name, class) VALUES (%s, %s)", (name, cls))
    con.commit()
    print("Member added. Member ID =", cur.lastrowid)


def view_books():
    cur.execute("SELECT * FROM books ORDER BY book_id")
    show(["Book ID", "Title", "Author", "Category", "Copies"], cur.fetchall())


def search_book():
    word = input("Enter title or author to search: ")
    cur.execute("SELECT book_id, title, author, copies FROM books "
                "WHERE title LIKE %s OR author LIKE %s", ("%" + word + "%", "%" + word + "%"))
    show(["Book ID", "Title", "Author", "Copies"], cur.fetchall())


def issue_book():
    bid = int(input("Book ID                : "))
    mid = int(input("Member ID              : "))

    cur.execute("SELECT title, copies FROM books WHERE book_id = %s", (bid,))
    book = cur.fetchone()
    if book is None:
        print("No such book.")
        return
    cur.execute("SELECT name FROM members WHERE member_id = %s", (mid,))
    member = cur.fetchone()
    if member is None:
        print("No such member.")
        return
    if book[1] == 0:
        print("Sorry, all copies of '" + book[0] + "' are issued right now.")
        return

    d = input("Issue date (YYYY-MM-DD) : ")
    cur.execute("INSERT INTO issues (book_id, member_id, issue_date) VALUES (%s, %s, %s)",
                (bid, mid, d))
    cur.execute("UPDATE books SET copies = copies - 1 WHERE book_id = %s", (bid,))
    con.commit()
    print("'" + book[0] + "' issued to " + member[0])


def return_book():
    bid = int(input("Book ID               : "))
    mid = int(input("Member ID             : "))
    cur.execute("SELECT issue_id, issue_date FROM issues "
                "WHERE book_id = %s AND member_id = %s AND return_date IS NULL", (bid, mid))
    rec = cur.fetchone()
    if rec is None:
        print("No pending issue found for this book and member.")
        return

    issue_id, issue_date = rec
    d = input("Return date (YYYY-MM-DD): ")
    cur.execute("SELECT DATEDIFF(%s, %s)", (d, issue_date))
    days = cur.fetchone()[0]
    if days is None or days < 0:
        print("Invalid return date.")
        return

    fine = 0
    if days > FREE_DAYS:
        fine = (days - FREE_DAYS) * FINE_PER_DAY

    cur.execute("UPDATE issues SET return_date = %s, fine = %s WHERE issue_id = %s",
                (d, fine, issue_id))
    cur.execute("UPDATE books SET copies = copies + 1 WHERE book_id = %s", (bid,))
    con.commit()
    print("Book returned after", days, "days.")
    if fine > 0:
        print("Late fine to be paid : Rs.", fine)
    else:
        print("No fine.")


def issued_books():
    cur.execute("SELECT i.issue_id, b.title, m.name, m.class, i.issue_date "
                "FROM issues i, books b, members m "
                "WHERE i.book_id = b.book_id AND i.member_id = m.member_id "
                "AND i.return_date IS NULL ORDER BY i.issue_date")
    show(["Issue No", "Book", "Member", "Class", "Issued On"], cur.fetchall())


def category_report():
    cur.execute("SELECT category, COUNT(*), SUM(copies) FROM books "
                "GROUP BY category ORDER BY category")
    show(["Category", "No. of Titles", "Copies Available"], cur.fetchall())


def delete_book():
    bid = int(input("Book ID to delete: "))
    try:
        cur.execute("DELETE FROM books WHERE book_id = %s", (bid,))
        con.commit()
        if cur.rowcount == 0:
            print("No such book.")
        else:
            print("Book deleted.")
    except pymysql.IntegrityError:
        con.rollback()
        print("Cannot delete: this book has issue records.")


MENU = """
========== LIBRARY MANAGEMENT SYSTEM ==========
 1. Add new book
 2. Add new member
 3. View all books
 4. Search a book (title / author)
 5. Issue a book
 6. Return a book (with fine calculation)
 7. View currently issued books
 8. Category-wise report
 9. Delete a book
 0. Exit
==============================================="""

while True:
    print(MENU)
    choice = input("Enter your choice : ")
    try:
        if choice == "1":
            add_book()
        elif choice == "2":
            add_member()
        elif choice == "3":
            view_books()
        elif choice == "4":
            search_book()
        elif choice == "5":
            issue_book()
        elif choice == "6":
            return_book()
        elif choice == "7":
            issued_books()
        elif choice == "8":
            category_report()
        elif choice == "9":
            delete_book()
        elif choice == "0":
            print("Thank you for using the Library Management System!")
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
