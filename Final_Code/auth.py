"""ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login():
    print("\n ============ADMIN LOGIN============")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if username ==  ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login Successful!")
        return True
    else:
        print("Invalid username or password.")
        return False
    
"""
# Streamlit login function
import sqlite3
import hashlib
from database import connect_db



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(name, email, phone, username, password, role="student"):

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users
            (name,email,phone,username,password,role)
            VALUES (?,?,?,?,?,?)
            """,(
            name,
            email,
            phone,
            username,
            hash_password(password),
            role
        ))  

        conn.commit()

        return True,"Registration Successful."

    except sqlite3.IntegrityError:

        return False,"Username or Email already exists."

    finally:

        conn.close()


def login_user(username,password):

    conn=connect_db()
    cursor=conn.cursor()

    cursor.execute("""
        SELECT id,name,role
        FROM users
        WHERE username=?
        AND password=?
    """,(
        username,
        hash_password(password)
    ))

    user=cursor.fetchone()

    conn.close()

    return user


def get_user_profile(user_id):
    
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            email,
            phone,
            username,
            role
        FROM users
        WHERE id=?
    """,(user_id,))

    user = cursor.fetchone()

    conn.close()

    return user


def create_default_admin():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    )

    admin = cursor.fetchone()

    if admin is None:
        cursor.execute("""
            INSERT INTO users
            (name, email, phone, username, password, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Admin",
            "admin@gmail.com",
            "9999999999",
            "admin",
            hash_password("admin123"),
            "admin"
        ))

        conn.commit()

    conn.close()
