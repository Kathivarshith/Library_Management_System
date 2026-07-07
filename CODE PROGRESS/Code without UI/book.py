from database import connect_db
import sqlite3


def add_book(title, author, category, isbn, quantity):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO books(title, author, category, isbn, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, category, isbn, quantity))

        conn.commit()
        print("Book added successfully.")
    
    except sqlite3.IntegrityError:
        print("Book with this ISBN already exists.")
    
    finally:
        conn.close()


    
    
    # ISBN =  International standard book number

def view_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print(books)

    conn.close()

    if not books:
        print("\nNo books found.\n")
        return
        
    print("\n============ BOOK LIST ==============")

    for book in books:
        print(f"""
Book ID  : {book[0]}
Title    : {book[1]}
Author   : {book[2]}
Category : {book[3]}
ISBN     : {book[4]}
Quantity : {book[5]}
---------------------""")
        
def search_book(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM books
        WHERE title LIKE ? OR isbn LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    books = cursor.fetchall()

    conn.close()

    
    if not books:
        print("\nNo books found.\n")
        return
        
    print("\n============ SEARCH RESULTS ==============")

    for book in books:
        print(f"""
Book ID  : {book[0]}
Title    : {book[1]}
Author   : {book[2]}
Category : {book[3]}
ISBN     : {book[4]}
Quantity : {book[5]}
---------------------""")
        
def update_book(book_id, title, author, category, isbn, quantity):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books
        SET title = ?,
            author = ?,
            category = ?,
            isbn = ?,
            quantity = ?
        WHERE id = ?
    """, (title, author, category, isbn, quantity, book_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("\n Book updated successfully.")
    else:
        print("\n Book ID not found.")

    conn.close()

def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM books
        WHERE id = ?
    """, (book_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("\n Book deleted Successfully.")
    else:
        print("\n Book ID not found.")

    conn.close()


