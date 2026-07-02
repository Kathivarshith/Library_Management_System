ADMIN_USERNAME = "admin"
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