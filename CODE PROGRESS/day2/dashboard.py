from database import connect_db

def dashboard():
    conn = connect_db()
    cursor = conn.cursor()

    # Total Books
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    # Available Books
    cursor.execute("SELECT COUNT(*) FROM books WHERE quantity > 0")
    available_books = cursor.fetchone()[0]

    if available_books == 0:
        available_books = "No books available"

    # Total Members
    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    # Issued Books
    cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE return_date IS NULL
    """)
    issued_books = cursor.fetchone()[0]

    conn.close()
    print("\n========== DASHBOARD ==========")
    print("\n" + "=" *40)
    print(" LIBRARY MANAGEMENT SYSTEM DASHBOARD")
    print("=" * 40)
    print(f" Total Books      : {total_books}")     
    print(f" Available Books  : {available_books}")     
    print(f" Total Members    : {total_members}")     
    print(f" Issued Books     : {issued_books}")     
    print("=" * 40)