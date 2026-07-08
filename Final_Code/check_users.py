from database import connect_db

conn = connect_db()
cursor = conn.cursor()

cursor.execute("""
SELECT id, name, username, role
FROM users
""")

for row in cursor.fetchall():
    print(row)

conn.close()