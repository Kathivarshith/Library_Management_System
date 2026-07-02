import sqlite3

DATABASE_NAME = "library.db"


def connect_db():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            isbn TEXT UNIQUE,
            quantity INTEGER NOT NULL
        )
    """)

    # Members Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT
        )
    """)

    # Transactions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            book_id INTEGER,
            issue_date TEXT,
            due_date TEXT,
            return_date TEXT,
            FOREIGN KEY(member_id) REFERENCES members(id),
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database and tables created successfully.")