"""
Project 6 : EMPLOYEE PAYROLL MANAGEMENT SYSTEM
Class XII - Computer Science (Python-MySQL connectivity)

Run setup.sql first, then change the PASSWORD below and run:  python main.py
"""
import pymysql

con = pymysql.connect(host="localhost", user="root",
                      password="your_password", database="company_db")
cur = con.cursor()

DA_PERCENT = 20       # Dearness Allowance  = 20% of basic
HRA_PERCENT = 15      # House Rent Allowance = 15% of basic
PF_PERCENT = 12       # Provident Fund deduction = 12% of basic


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


def add_employee():
    eid = int(input("Employee ID          : "))
    name = input("Name                 : ")
    cur.execute("SELECT dept_id, dept_name FROM departments")
    show(["Dept ID", "Department"], cur.fetchall())
    dept = int(input("Department ID       : "))
    desig = input("Designation          : ")
    basic = int(input("Basic salary (Rs.)   : "))
    jd = input("Joining date (YYYY-MM-DD): ")
    cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)",
                (eid, name, dept, desig, basic, jd))
    con.commit()
    print("Employee added successfully.")


def view_employees():
    cur.execute("SELECT e.emp_id, e.name, d.dept_name, e.designation, e.basic_salary "
                "FROM employees e, departments d WHERE e.dept_id = d.dept_id "
                "ORDER BY e.emp_id")
    show(["Emp ID", "Name", "Department", "Designation", "Basic (Rs.)"], cur.fetchall())


def search_employee():
    word = input("Search by name or designation : ")
    cur.execute("SELECT e.emp_id, e.name, d.dept_name, e.designation, e.basic_salary "
                "FROM employees e, departments d WHERE e.dept_id = d.dept_id "
                "AND (e.name LIKE %s OR e.designation LIKE %s)",
                ("%" + word + "%", "%" + word + "%"))
    show(["Emp ID", "Name", "Department", "Designation", "Basic (Rs.)"], cur.fetchall())


def payslip():
    eid = int(input("Employee ID : "))
    cur.execute("SELECT e.name, d.dept_name, e.designation, e.basic_salary "
                "FROM employees e, departments d "
                "WHERE e.dept_id = d.dept_id AND e.emp_id = %s", (eid,))
    r = cur.fetchone()
    if r is None:
        print("No employee with this ID.")
        return

    name, dept, desig, basic = r
    da = basic * DA_PERCENT / 100
    hra = basic * HRA_PERCENT / 100
    gross = basic + da + hra
    pf = basic * PF_PERCENT / 100
    net = gross - pf

    print("\n=========== SALARY SLIP ===========")
    print("Emp ID      :", eid)
    print("Name        :", name)
    print("Department  :", dept, "-", desig)
    print("-----------------------------------")
    print("Basic Salary".ljust(18) + ":", format(basic, ".2f").rjust(10))
    print(("DA  (" + str(DA_PERCENT) + "%)").ljust(18) + ":", format(da, ".2f").rjust(10))
    print(("HRA (" + str(HRA_PERCENT) + "%)").ljust(18) + ":", format(hra, ".2f").rjust(10))
    print("Gross Salary".ljust(18) + ":", format(gross, ".2f").rjust(10))
    print(("PF  (" + str(PF_PERCENT) + "%) [-]").ljust(18) + ":", format(pf, ".2f").rjust(10))
    print("-----------------------------------")
    print("NET SALARY".ljust(18) + ":", format(net, ".2f").rjust(10))
    print("===================================")


def increment_one():
    eid = int(input("Employee ID : "))
    pct = float(input("Increment percentage : "))
    cur.execute("UPDATE employees SET basic_salary = ROUND(basic_salary + basic_salary * %s / 100) "
                "WHERE emp_id = %s", (pct, eid))
    con.commit()
    if cur.rowcount == 0:
        print("No employee with this ID.")
    else:
        cur.execute("SELECT name, basic_salary FROM employees WHERE emp_id = %s", (eid,))
        r = cur.fetchone()
        print("Increment given. New basic salary of", r[0], "= Rs.", r[1])


def increment_department():
    dept = int(input("Department ID : "))
    pct = float(input("Increment percentage : "))
    cur.execute("UPDATE employees SET basic_salary = ROUND(basic_salary + basic_salary * %s / 100) "
                "WHERE dept_id = %s", (pct, dept))
    con.commit()
    print(cur.rowcount, "employee(s) received the increment.")


def department_summary():
    n = int(input("Show departments having at least how many employees? (0 for all) : "))
    cur.execute("SELECT d.dept_name, d.location, COUNT(*), SUM(e.basic_salary), "
                "ROUND(AVG(e.basic_salary)), MAX(e.basic_salary) "
                "FROM employees e, departments d WHERE e.dept_id = d.dept_id "
                "GROUP BY d.dept_name, d.location HAVING COUNT(*) >= %s "
                "ORDER BY d.dept_name", (n,))
    show(["Department", "Location", "Employees", "Total Basic", "Avg Basic", "Highest Basic"],
         cur.fetchall())


def highest_lowest():
    cur.execute("SELECT name, designation, basic_salary FROM employees "
                "ORDER BY basic_salary DESC LIMIT 1")
    r = cur.fetchone()
    print("Highest paid :", r[0], "(" + r[1] + ") - Rs.", r[2])
    cur.execute("SELECT name, designation, basic_salary FROM employees "
                "ORDER BY basic_salary LIMIT 1")
    r = cur.fetchone()
    print("Lowest paid  :", r[0], "(" + r[1] + ") - Rs.", r[2])


def total_payroll():
    cur.execute("SELECT SUM(basic_salary) FROM employees")
    basic = cur.fetchone()[0]
    net = basic * (100 + DA_PERCENT + HRA_PERCENT - PF_PERCENT) / 100
    print("Total basic salary of all employees  : Rs.", format(basic, ".2f"))
    print("Total net salary to be paid this month: Rs.", format(net, ".2f"))


def remove_employee():
    eid = int(input("Employee ID to remove : "))
    cur.execute("DELETE FROM employees WHERE emp_id = %s", (eid,))
    con.commit()
    if cur.rowcount == 0:
        print("No employee with this ID.")
    else:
        print("Employee record removed.")


MENU = """
======= EMPLOYEE PAYROLL MANAGEMENT SYSTEM =======
  1. Add new employee
  2. View all employees
  3. Search employee (name / designation)
  4. Generate salary slip
  5. Give increment to one employee
  6. Give increment to a whole department
  7. Department-wise summary
  8. Highest and lowest paid employee
  9. Total monthly payroll
 10. Remove an employee
  0. Exit
=================================================="""

while True:
    print(MENU)
    choice = input("Enter your choice : ")
    try:
        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employees()
        elif choice == "3":
            search_employee()
        elif choice == "4":
            payslip()
        elif choice == "5":
            increment_one()
        elif choice == "6":
            increment_department()
        elif choice == "7":
            department_summary()
        elif choice == "8":
            highest_lowest()
        elif choice == "9":
            total_payroll()
        elif choice == "10":
            remove_employee()
        elif choice == "0":
            print("Thank you for using the Payroll System!")
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
