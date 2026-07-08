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

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
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

    #student table register
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    print("Database and tables created successfully.")