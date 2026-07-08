from database import connect_db
from datetime import datetime, timedelta


def issue_book(member_id, book_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Check Member
    cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    member = cursor.fetchone()

    if not member:
        print(" Member not found.")
        conn.close()
        return

    # Check Book
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()

    if not book:
        print(" Book not found.")
        conn.close()
        return

    # Check Quantity
    if book[5] <= 0:
        print("Book is out of stock.")
        conn.close()
        return

    issue_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO transactions
        (member_id, book_id, issue_date, due_date, return_date)
        VALUES (?, ?, ?, ?, ?)
    """, (member_id, book_id, issue_date, due_date, None))

    # Reduce Quantity
    cursor.execute("""
        UPDATE books
        SET quantity = quantity - 1
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

    print("Book issued successfully.")

def return_book(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Check transaction
    cursor.execute("""
        SELECT book_id, due_date, return_date
        FROM transactions
        WHERE id = ?
    """, (transaction_id,))

    transaction = cursor.fetchone()

    if not transaction:
        print(" Transaction not found.")
        conn.close()
        return

    book_id, due_date, returned = transaction

    if returned is not None:
        print("This book has already been returned.")
        conn.close()
        return

    today = datetime.now()

    return_date = today.strftime("%Y-%m-%d")

    # Update transaction
    cursor.execute("""
        UPDATE transactions
        SET return_date = ?
        WHERE id = ?
    """, (return_date, transaction_id))

    # Increase quantity
    cursor.execute("""
        UPDATE books
        SET quantity = quantity + 1
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

    # Fine Calculation
    due = datetime.strptime(due_date, "%Y-%m-%d")

    if today > due:
        late_days = (today - due).days
        fine = late_days * 10

        print(f"\nBook returned successfully.")
        print(f"Late by {late_days} days.")
        print(f"Fine: ₹{fine}")

    else:
        print("\nBook returned successfully.")
        print("No Fine.")

def view_transactions():
    
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.id,
            m.name,
            b.title,
            t.issue_date,
            t.due_date,
            t.return_date
        FROM transactions t
        JOIN members m
            ON t.member_id = m.id
        JOIN books b
            ON t.book_id = b.id
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("\nNo Transactions Found.")
        return

    print("\n========== TRANSACTIONS ==========")

    for row in rows:
        print(f"""
Transaction ID : {row[0]}
Member         : {row[1]}
Book           : {row[2]}
Issue Date     : {row[3]}
Due Date       : {row[4]}
Return Date    : {row[5]}
---------------------------------------
""")
        
def recent_transactions():
    
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        m.name,
        b.title,
        t.issue_date,
        t.return_date
    FROM transactions t
    JOIN members m
    ON t.member_id=m.id
    JOIN books b
    ON t.book_id=b.id
    ORDER BY t.id DESC
    LIMIT 5
    """)

    rows=cursor.fetchall()

    conn.close()

    return rows


# streamlit functions
from database import connect_db
from datetime import datetime, timedelta


def get_all_transactions():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.id,
            m.name,
            b.title,
            t.issue_date,
            t.due_date,
            t.return_date
        FROM transactions t
        JOIN members m ON t.member_id = m.id
        JOIN books b ON t.book_id = b.id
        ORDER BY t.id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_student_books(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            books.title,
            transactions.issue_date,
            transactions.due_date,
            transactions.return_date
        FROM transactions
        JOIN books
            ON transactions.book_id = books.id
        WHERE transactions.member_id = ?
        ORDER BY transactions.id DESC
    """, (user_id,))

    books = cursor.fetchall()

    conn.close()

    return books