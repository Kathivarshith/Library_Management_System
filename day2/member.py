import sqlite3
from database import connect_db


def add_member(name, email, phone):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO members(name, email, phone)
            VALUES (?, ?, ?)
        """, (name, email, phone))

        conn.commit()
        print(" Member added successfully.")

    except sqlite3.IntegrityError:
        print(" Email already exists.")

    finally:
        conn.close()


def view_members():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    conn.close()

    if not members:
        print("\nNo members found.\n")
        return

    print("\n========== MEMBER LIST ==========")

    for member in members:
        print(f"""
Member ID : {member[0]}
Name      : {member[1]}
Email     : {member[2]}
Phone     : {member[3]}
-------------------------------
""")


def search_member(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM members
        WHERE name LIKE ? OR email LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    members = cursor.fetchall()

    conn.close()

    if not members:
        print("\nMember not found.\n")
        return

    print("\n========== SEARCH RESULT ==========")

    for member in members:
        print(f"""
Member ID : {member[0]}
Name      : {member[1]}
Email     : {member[2]}
Phone     : {member[3]}
-------------------------------
""")


def update_member(member_id, name, email, phone):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE members
        SET name = ?,
            email = ?,
            phone = ?
        WHERE id = ?
    """, (name, email, phone, member_id))

    conn.commit()

    if cursor.rowcount > 0:
        print(" Member updated successfully.")
    else:
        print(" Member ID not found.")

    conn.close()


def delete_member(member_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM members
        WHERE id = ?
    """, (member_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print(" Member deleted successfully.")
    else:
        print(" Member ID not found.")

    conn.close()