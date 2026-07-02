from database import connect_db

def library_report():
    
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM members")
    members = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*) 
    FROM transactions
    where return_date IS NULL
    """)
    issued = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUm(quantity)
    FROM books
    """)

    available = cursor.fetchone()[0]

    if available is None:
        available = 0

    print("\n====== LIBRARY REPORT ======")
    print(f"Books Available: {available}")
    print(f"Total Books: {books}")
    print(f"Total Members: {members}")
    print(f"Books Issued: {issued}")

    conn.close()

from database import connect_db
from datetime import datetime

def overdue_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        m.name,
        b.title,
        t.issue_date,
        t.due_date
    FROM transactions t
    JOIN members m ON t.member_id = m.id
    JOIN books b ON t.book_id = b.id
    WHERE t.return_date IS NULL 
    """)

    records = cursor.fetchall()
    conn.close

    if not records:
        print("\nNo overdue books found.")
        return
    
    today = datetime.now().date()
    overdue_found = False

    print("\n====== OVERDUE BOOKS ======")

    for record in records:
        member_name = record[0]
        book_title = record[1]
        issue_date = datetime.strptime(record[2], "%Y-%m-%d").date()
        due_date = datetime.strptime(record[3], "%Y-%m-%d").date()

        due = datetime.strptime(due_date, "%Y-%m-%d").date()

        if today > due:
            overdue_found = True

            days_overdue = (today - due).days
            print(f"Member: {member_name}, Book: {book_title}, Issue Date: {issue_date}, Due Date: {due_date}, Days Overdue: {days_overdue}")

    if not overdue_found:
        print("\nNo overdue books found.")