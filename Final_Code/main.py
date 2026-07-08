
from database import create_tables
from transaction import issue_book, return_book, view_transactions
from dashboard import dashboard
from auth import login
from student import student_login, student_register
from reports import library_report, overdue_books


from book import (
    add_book, 
    view_books, 
    search_book, 
    update_book, 
    delete_book
)

from member import (
    add_member,
    view_members,
    search_member,
    update_member,
    delete_member
)

def home_menu():
    while True:
        print("\n" + "=" * 45)
        print("LIBRARY MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. ADMIN LOGIN")
        print("2. STUDENT LOGIN")
        print("3. STUDENT REGISTER")
        print("4. EXIT")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            if login():
                menu()
        elif choice == "2":
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            student = student_login(username, password)
            if student:
                student_menu(student)
                
                # You can add more functionality for logged-in students here
        elif choice == "3":
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            phone = input("Enter Phone: ")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            student_register(name, email, phone, username, password)
        
        elif choice == "4":
            print("\nThank you for using the Library Management System.")
            break
        else:
            print("\nInvalid Choice. Try Again.")


def student_menu(student):
    while True:
        print("\n" + "=" * 45)
        print(f"WELCOME {student[1]} TO LIBRARY MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. VIEW BOOKS")
        print("2. SEARCH BOOK")
        print("3. VIEW TRANSACTIONS")
        print("4. LOGOUT")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            view_books()
        elif choice == "2":
            keyword = input("Enter Book Title or ISBN: ")
            search_book(keyword)
        elif choice == "3":
            view_transactions()
        elif choice == "4":
            print(f"\nGoodbye, {student[1]}!")
            break
        else:
            print("\nInvalid Choice. Try Again.")


def menu():
    while True:
        print("\n" + "=" *45)
        print("LIBRARY MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. DASHBOARD")
        print("---------------------")
        print("2.ADD BOOK")
        print("3.VIEW BOOK")
        print("4.SEARCH BOOK")
        print("5.UPDATE BOOK")
        print("6.DELETE BOOK")
        print("---------------------")
        print("7. ADD Member")
        print("8. View Member")
        print("9. Search Member")
        print("10. Update Member")
        print("11.Delete Member")
        print("----------------------")
        print("12. Issue Book")
        print("13. VIEW Transactions")
        print("14. Return Book")
        print("----------------------")
        print("15. Library Report")
        print("16. Overdue Books Report")

        print("17. Exit")

        choice = input("\n Enter your choice (1-17): ")

        if choice == "1":
            dashboard()
        elif choice == "2":
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            category = input("Enter Category: ")
            isbn = input("Enter ISBN: ")
            while True:
                try:
                    quantity = int(input("Enter Quantity: "))
                    
                    if quantity < 0:
                        print("Quantity cannot be negative. Please enter a valid integer.")
                        continue
                    
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for quantity.")

            

            add_book(title,author,category,isbn,quantity)

        elif choice == "3":
            view_books()

        elif choice == "4":
            keyword = input("Enter Book Title or ISBN: ")
            search_book(keyword)

        elif choice == "5":
            while True:
                try:
                    book_id = int(input("Enter Book ID to Update: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for Book ID.")

            title = input("Enter New Title: ").strip()
            if not title:
                print("Title cannot be empty. Please enter a valid title.")
                return
            
            author = input("Enter New Author: ").strip()
            if not author:
                print("Author cannot be empty. Please enter a valid author.")
                return


            category = input("Enter New Category: ").strip()
            if not category:
                print("Category cannot be empty. Please enter a valid category.")
                return

            isbn = input("Enter New ISBN: ").strip()

            if len(isbn) < 5:
                print("ISBN must be at least 5 characters long. Please enter a valid ISBN.")
                return
            
            while True:
                try:
                    quantity = int(input(" Enter Quantity: "))
                    if quantity < 0:
                        print("Quantity cannot be negative. Please enter a valid integer.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for quantity.")

            #from book import update_book
            update_book(book_id, title, author, category, isbn, quantity)


        elif choice == "6":
            book_id = int(input("Enter Book ID to Delete: "))

            confirm = input("Are you sure? (y/n): ")

            if confirm.lower() == "y":
                delete_book(book_id)
            else:
                print("Delete Cancelled.")

        elif choice == "7":
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            phone = input("Enter Phone: ")
            add_member(name, email, phone)

        elif choice == "8":
            view_members()

        elif choice == "9":
            keyword = input("Enter Name or Email: ")
            search_member(keyword)

        elif choice == "10":
            while True:
                try:
                    member_id = int(input("Enter Member ID: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for Member ID.")

            name = input("Enter New Name: ")
            email = input("Enter New Email: ")
            phone = input("Enter New Phone: ")
            

            update_member(member_id, name, email, phone)

        elif choice == "11":
            member_id = int(input("Enter Member ID: "))
            confirm = input("Delete this member? (y/n): ")
            if confirm.lower() == "y":
                delete_member(member_id)
            else:
                print("Delete cancelled.")

        elif choice == "12":
            member_id = int(input("Enter Member ID: "))
            book_id = int(input("Enter Book ID: "))

            issue_book(member_id, book_id)

        elif choice == "14":
            transaction_id = int(input("Enter Transaction ID: "))
            return_book(transaction_id)

        elif choice == "13":
            view_transactions()

        elif choice == "15":
            library_report()
        
        elif choice == "16":
            overdue_books()

        elif choice == "17":
            print("\n Thank You for using Library Management System.")
            break

        else:
            print("\n Invalid Choice. Try Again.")


def main():
    create_tables()
    home_menu()

if __name__ == "__main__":
    main() 






