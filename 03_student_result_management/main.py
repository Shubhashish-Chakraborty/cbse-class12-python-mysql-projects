"""
Project 3 : STUDENT RESULT MANAGEMENT SYSTEM
Class XII - Computer Science (Python-MySQL connectivity)

Run setup.sql first, then change the PASSWORD below and run:  python main.py
"""
import pymysql

con = pymysql.connect(host="localhost", user="root",
                      password="your_password", database="school_db")
cur = con.cursor()

PASS_MARKS = 33
# SQL expression that adds the marks of all 5 subjects
TOTAL = "(m.physics + m.chemistry + m.maths + m.english + m.cs)"
SUBJECTS = {"1": "physics", "2": "chemistry", "3": "maths", "4": "english", "5": "cs"}


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


def get_grade(percent):
    if percent >= 90:
        return "A+"
    elif percent >= 75:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 45:
        return "C"
    else:
        return "D"


def read_mark(subject):
    m = int(input("Marks in " + subject + " (0-100) : "))
    if m < 0 or m > 100:
        raise ValueError
    return m


def add_student():
    roll = int(input("Roll number : "))
    name = input("Name        : ")
    sec = input("Section     : ").upper()
    p = read_mark("Physics")
    c = read_mark("Chemistry")
    m = read_mark("Maths")
    e = read_mark("English")
    cs = read_mark("Computer Science")
    cur.execute("INSERT INTO students VALUES (%s, %s, %s)", (roll, name, sec))
    cur.execute("INSERT INTO marks VALUES (%s, %s, %s, %s, %s, %s)", (roll, p, c, m, e, cs))
    con.commit()
    print("Student record added successfully.")


def report_card():
    roll = int(input("Enter roll number : "))
    cur.execute("SELECT s.name, s.section, m.physics, m.chemistry, m.maths, m.english, m.cs "
                "FROM students s, marks m WHERE s.roll_no = m.roll_no AND s.roll_no = %s", (roll,))
    r = cur.fetchone()
    if r is None:
        print("No student with this roll number.")
        return

    name, sec, p, c, m, e, cs = r
    total = p + c + m + e + cs
    percent = total / 5
    passed = min(p, c, m, e, cs) >= PASS_MARKS

    print("\n============ REPORT CARD ============")
    print("Roll No :", roll, "   Section :", sec)
    print("Name    :", name)
    print("-------------------------------------")
    print("Physics          :", p)
    print("Chemistry        :", c)
    print("Maths            :", m)
    print("English          :", e)
    print("Computer Science :", cs)
    print("-------------------------------------")
    print("Total            :", total, "/ 500")
    print("Percentage       :", format(percent, ".2f"), "%")
    if passed:
        print("Result           : PASS    Grade :", get_grade(percent))
    else:
        print("Result           : FAIL (below " + str(PASS_MARKS) + " in a subject)")
    print("=====================================")


def result_sheet():
    cur.execute("SELECT s.roll_no, s.name, s.section, " + TOTAL + " AS total, "
                "ROUND(" + TOTAL + " / 5, 2) AS percent "
                "FROM students s, marks m WHERE s.roll_no = m.roll_no "
                "ORDER BY total DESC")
    rows = cur.fetchall()
    ranked = []
    for i in range(len(rows)):
        ranked.append((i + 1,) + rows[i])
    show(["Rank", "Roll", "Name", "Sec", "Total", "Percent"], ranked)


def update_marks():
    roll = int(input("Roll number : "))
    print("1.Physics  2.Chemistry  3.Maths  4.English  5.Computer Science")
    ch = input("Choose subject : ")
    if ch not in SUBJECTS:
        print("Invalid subject.")
        return
    new = read_mark("this subject")
    cur.execute("UPDATE marks SET " + SUBJECTS[ch] + " = %s WHERE roll_no = %s", (new, roll))
    con.commit()
    if cur.rowcount == 0:
        print("No student with this roll number (or marks unchanged).")
    else:
        print("Marks updated successfully.")


def topper():
    cur.execute("SELECT s.name, s.section, " + TOTAL + " AS total "
                "FROM students s, marks m WHERE s.roll_no = m.roll_no "
                "ORDER BY total DESC LIMIT 1")
    name, sec, total = cur.fetchone()
    print("School Topper :", name, "(Section " + sec + ") with", total, "/ 500 marks")


def section_report():
    low = float(input("Show only sections with average percentage >= (0 for all) : "))
    cur.execute("SELECT s.section, COUNT(*), ROUND(AVG(" + TOTAL + " / 5), 2), MAX" +
                TOTAL + " FROM students s, marks m WHERE s.roll_no = m.roll_no "
                "GROUP BY s.section HAVING AVG(" + TOTAL + " / 5) >= %s", (low,))
    show(["Section", "Students", "Avg Percent", "Highest Total"], cur.fetchall())


def failed_students():
    cur.execute("SELECT s.roll_no, s.name, m.physics, m.chemistry, m.maths, m.english, m.cs "
                "FROM students s, marks m WHERE s.roll_no = m.roll_no "
                "AND (m.physics < %s OR m.chemistry < %s OR m.maths < %s "
                "OR m.english < %s OR m.cs < %s)",
                (PASS_MARKS, PASS_MARKS, PASS_MARKS, PASS_MARKS, PASS_MARKS))
    show(["Roll", "Name", "Phy", "Chem", "Maths", "Eng", "CS"], cur.fetchall())


def subject_report():
    cur.execute("SELECT ROUND(AVG(physics),2), MAX(physics), MIN(physics), "
                "ROUND(AVG(chemistry),2), MAX(chemistry), MIN(chemistry), "
                "ROUND(AVG(maths),2), MAX(maths), MIN(maths), "
                "ROUND(AVG(english),2), MAX(english), MIN(english), "
                "ROUND(AVG(cs),2), MAX(cs), MIN(cs) FROM marks")
    r = cur.fetchone()
    names = ["Physics", "Chemistry", "Maths", "English", "Computer Science"]
    rows = []
    for i in range(5):
        rows.append((names[i], r[i * 3], r[i * 3 + 1], r[i * 3 + 2]))
    show(["Subject", "Average", "Highest", "Lowest"], rows)


def delete_student():
    roll = int(input("Roll number to delete : "))
    cur.execute("DELETE FROM marks WHERE roll_no = %s", (roll,))   # child table first
    cur.execute("DELETE FROM students WHERE roll_no = %s", (roll,))
    con.commit()
    if cur.rowcount == 0:
        print("No student with this roll number.")
    else:
        print("Student record deleted.")


MENU = """
======== STUDENT RESULT MANAGEMENT SYSTEM ========
  1. Add student with marks
  2. Show report card of a student
  3. Class result sheet (rank-wise)
  4. Update marks of a subject
  5. Find the topper
  6. Section-wise performance
  7. List of failed students
  8. Subject-wise average / highest / lowest
  9. Delete a student
  0. Exit
=================================================="""

while True:
    print(MENU)
    choice = input("Enter your choice : ")
    try:
        if choice == "1":
            add_student()
        elif choice == "2":
            report_card()
        elif choice == "3":
            result_sheet()
        elif choice == "4":
            update_marks()
        elif choice == "5":
            topper()
        elif choice == "6":
            section_report()
        elif choice == "7":
            failed_students()
        elif choice == "8":
            subject_report()
        elif choice == "9":
            delete_student()
        elif choice == "0":
            print("Thank you for using the Result Management System!")
            break
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Please enter valid numbers (marks must be between 0 and 100).")
        con.rollback()
    except pymysql.Error as e:
        print("Database error :", e)
        con.rollback()

con.close()
