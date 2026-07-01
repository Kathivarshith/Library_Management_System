
from database import create_tables
from transaction import issue_book, return_book, view_transactions
from dashboard import dashboard

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
        print("15. Exit")

        choice = input("\n Enter your choice (1-14)")

        if choice == "1":
            dashboard()
        elif choice == "2":
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            category = input("Enter Category: ")
            isbn = input("Enter ISBN: ")
            quantity = int(input("Enter Qunatity: "))

            add_book(title,author,category,isbn,quantity)

        elif choice == "3":
            view_books()

        elif choice == "4":
            keyword = input("Enter Book Title or ISBN: ")
            search_book(keyword)

        elif choice == "5":
            book_id = int(input("Enter Book ID to Update:  "))
            title = input("Enter New Title: ")
            author = input("Enter New Author: ")
            category = input("Enter New Category: ")
            isbn = input("Enter New ISBN: ")
            quantity = int(input(" Enter Quantity: "))

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
            member_id = int(input("Enter Member ID: "))
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
            print("\n Thank You for using Library Management System.")
            break

        else:
            print("\n Invalid Choice. Try Again.")


def main():
    create_tables()
    menu()

if __name__ == "__main__":
    main() 






