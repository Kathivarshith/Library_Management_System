from auth import register_user

success, message = register_user(
    name="Admin",
    email="admin@gmail.com",
    phone="9999999999",
    username="admin",
    password="admin123",
    role="admin"
)

print(message)