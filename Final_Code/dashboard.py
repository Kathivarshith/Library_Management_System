from database import connect_db


def get_dashboard_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Total Book Titles
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    # Available Books
    cursor.execute("SELECT IFNULL(SUM(quantity), 0) FROM books")
    available_books = cursor.fetchone()[0]

    # Total Members
    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    # Issued Books
    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE return_date IS NULL
    """)
    issued_books = cursor.fetchone()[0]

    # Overdue Books
    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE return_date IS NULL
        AND due_date < DATE('now')
    """)
    overdue_books = cursor.fetchone()[0]

    conn.close()

    return {
        "total_books": total_books,
        "available_books": available_books,
        "total_members": total_members,
        "issued_books": issued_books,
        "overdue_books": overdue_books
    }