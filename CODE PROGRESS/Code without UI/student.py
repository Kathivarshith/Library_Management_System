import sqlite3
from database import connect_db

def student_register(name, email, phone, username, password):

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO students 
        (name, email, phone, username, password)
        VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, username, password))
        
        conn.commit()
        
        print("Student registered successfully.")
    
    except sqlite3.IntegrityError:
        print("Error: Username or email already exists.")
    
    finally:
        conn.close()

def student_login(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM students WHERE username = ? AND password = ?
    """, (username, password))

    student = cursor.fetchone()
    conn.close()

    if student:
        return student
    else:
        print("Invalid username or password.")
        return None
    
