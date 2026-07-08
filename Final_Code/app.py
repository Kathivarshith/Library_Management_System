import streamlit as st
import pandas as pd
import plotly.express as px
from book import get_available_books
from auth import login_user, register_user
from auth import get_user_profile
from transaction import get_student_books
from book import (
    add_book,
    get_books,
    get_available_books,
    search_books,
    update_book_streamlit,
    delete_book_streamlit
)
from member import (
    add_member,
    get_members,
    search_members,
    update_member_streamlit,
    delete_member_streamlit
)
from dashboard import get_dashboard_data
from transaction import (
    issue_book,
    return_book,
    get_all_transactions,
    recent_transactions
)

from reports import (
    get_library_summary,
    get_overdue_books,
    get_transaction_report
)
from database import create_tables
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_tables()

from auth import create_default_admin

create_tables()
create_default_admin()
# -----------------------------
# Session State
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None

# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.main{
    background-color:#F7F9FC;
}

h1{
    color:#1565C0;
}

section[data-testid="stSidebar"]{
    background:#0F172A;
}

section[data-testid="stSidebar"] *{
    color:white;
}

.stButton>button{
    width:100%;
    border-radius:10px;
}

</style>
""",unsafe_allow_html=True)


# -----------------------------
# Login / Register
# -----------------------------

if not st.session_state.logged_in:

    st.title("📚 Library Management System")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    # ---------------- Login ----------------

    with tab1:

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", use_container_width=True):

            user = login_user(username, password)

            if user:
    
                st.session_state.logged_in = True

                # Save logged-in user's ID
                st.session_state.user_id = user[0]

                # Save user's name
                st.session_state.user = user[1]

                # Save user's role (admin/student)
                st.session_state.role = user[2]

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Username or Password")

    # ---------------- Register ----------------

    with tab2:

        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register", use_container_width=True):

            success, message = register_user(
                name,
                email,
                phone,
                username,
                password,
                "student"
            )

            if success:
                st.success(message)
            else:
                st.error(message)

    st.stop()




# -----------------------------
# Sidebar
# -----------------------------

#st.sidebar.title("📚 Library")
#st.sidebar.markdown("---")
st.sidebar.markdown("---")

st.sidebar.write(f"👋 Welcome, **{st.session_state.user}**")



# Initialize page
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

st.sidebar.title("📚 Library Management System")
st.sidebar.markdown("---")

# -----------------------------
# Admin Menu
# -----------------------------
if st.session_state.role == "admin":

    if st.sidebar.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

    if st.sidebar.button("📚 Books", use_container_width=True):
        st.session_state.page = "Books"

    if st.sidebar.button("👤 Members", use_container_width=True):
        st.session_state.page = "Members"

    if st.sidebar.button("🔄 Transactions", use_container_width=True):
        st.session_state.page = "Transactions"

    if st.sidebar.button("📊 Reports", use_container_width=True):
        st.session_state.page = "Reports"

    if st.sidebar.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = "Settings"

# -----------------------------
# Student Menu
# -----------------------------
else:

    if st.sidebar.button("📚 Books", use_container_width=True):
        st.session_state.page = "Books"

    if st.sidebar.button("📖 My Books", use_container_width=True):
        st.session_state.page = "My Books"

    if st.sidebar.button("👤 Profile", use_container_width=True):
        st.session_state.page = "Profile"

page = st.session_state.page

if st.sidebar.button("🚪 Logout", use_container_width=True):
    
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user = None
    st.session_state.role = None

    st.rerun()



# -----------------------------
# Dashboard
# -----------------------------

if page == "Dashboard":

    st.markdown("""
    <div style="
    background: linear-gradient(90deg,#1565C0,#42A5F5);
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
    ">
        <h1>📚 Library Management Dashboard</h1>
        <p>Monitor Books • Members • Transactions • Reports</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    data = get_dashboard_data()

    # ---------------- Metrics ----------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        with st.container(border=True):
            st.metric("📚 Books", data["total_books"])

    with col2:
        with st.container(border=True):
            st.metric("📦 Available", data["available_books"])

    with col3:
        with st.container(border=True):
            st.metric("👤 Members", data["total_members"])

    with col4:
        with st.container(border=True):
            st.metric("📖 Issued", data["issued_books"])

    with col5:
        with st.container(border=True):
            st.metric("⚠️ Overdue", data["overdue_books"])

    st.divider()

    # ---------------- Charts ----------------

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.pie(
            names=["Available", "Issued"],
            values=[
                data["available_books"],
                data["issued_books"]
            ],
            title="Book Availability"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with col2:

        fig2 = px.bar(
            x=[
                "Books",
                "Members",
                "Issued",
                "Overdue"
            ],
            y=[
                data["total_books"],
                data["total_members"],
                data["issued_books"],
                data["overdue_books"]
            ],
            title="Library Overview"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ---------------- Recent Transactions ----------------

    st.subheader("📋 Recent Transactions")

    rows = recent_transactions()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Member",
                "Book",
                "Issue Date",
                "Return Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No Transactions Found.")

# -----------------------------
# -----------------------------
# Books
# -----------------------------

elif page == "Books":

    # ==================================================
    # ADMIN VIEW
    # ==================================================

    if st.session_state.role == "admin":

        st.title("📚 Book Management")

        # ---------------- Add Book ----------------

        with st.form("book_form"):

            title = st.text_input("Title")
            author = st.text_input("Author")
            category = st.text_input("Category")
            isbn = st.text_input("ISBN")

            quantity = st.number_input(
                "Quantity",
                min_value=0,
                step=1
            )

            submitted = st.form_submit_button("➕ Add Book")

            if submitted:

                success, message = add_book(
                    title,
                    author,
                    category,
                    isbn,
                    quantity
                )

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        st.divider()

        # ---------------- View & Search ----------------

        st.subheader("📚 Available Books")

        keyword = st.text_input(
            "🔍 Search Books",
            key="admin_search"
        )

        if keyword:
            books = search_books(keyword)
        else:
            books = get_books()

        if books:

            df = pd.DataFrame(
                books,
                columns=[
                    "ID",
                    "Title",
                    "Author",
                    "Category",
                    "ISBN",
                    "Quantity"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No Books Found.")

        st.divider()

        # ---------------- Update ----------------

        st.subheader("✏️ Update Book")

        books = get_books()

        if books:

            book_options = {
                f"{book[1]} (ISBN: {book[4]})": book
                for book in books
            }

            selected = st.selectbox(
                "Select Book",
                list(book_options.keys())
            )

            selected_book = book_options[selected]

            title = st.text_input(
                "Title",
                value=selected_book[1],
                key="u_title"
            )

            author = st.text_input(
                "Author",
                value=selected_book[2],
                key="u_author"
            )

            category = st.text_input(
                "Category",
                value=selected_book[3],
                key="u_category"
            )

            isbn = st.text_input(
                "ISBN",
                value=selected_book[4],
                key="u_isbn"
            )

            quantity = st.number_input(
                "Quantity",
                min_value=0,
                value=selected_book[5],
                key="u_quantity"
            )

            if st.button("💾 Update Book"):

                success, message = update_book_streamlit(
                    selected_book[0],
                    title,
                    author,
                    category,
                    isbn,
                    quantity
                )

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        st.divider()

        # ---------------- Delete ----------------

        st.subheader("🗑️ Delete Book")

        if books:

            delete_option = st.selectbox(
                "Select Book",
                list(book_options.keys()),
                key="delete_book"
            )

            if st.button("Delete Book"):

                success, message = delete_book_streamlit(
                    book_options[delete_option][0]
                )

                if success:
                    st.success(message)
                    st.rerun()

    # ==================================================
    # STUDENT VIEW
    # ==================================================

    else:

        st.title("📚 Library Books")

        keyword = st.text_input(
            "🔍 Search Books",
            key="student_search"
        )

        if keyword:
            books = search_books(keyword)
        else:
            books = get_available_books()

        if books:

            df = pd.DataFrame(
                books,
                columns=[
                    "Book ID",
                    "Title",
                    "Author",
                    "Category",
                    "ISBN",
                    "Available"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("📖 Borrow Book")

            options = {
                f"{book[1]} ({book[2]})": book
                for book in books
            }

            selected = st.selectbox(
                "Select Book",
                list(options.keys())
            )

            if st.button("Borrow Book"):

                book_id = options[selected][0]

                issue_book(
                    st.session_state.user_id,
                    book_id
                )

                st.success("Book Issued Successfully")

                st.rerun()

        else:

            st.info("No Books Available.")


elif page == "My Books":
    
    st.title("📖 My Issued Books")

    books = get_student_books(st.session_state.user_id)

    if books:

        df = pd.DataFrame(
            books,
            columns=[
                "Book",
                "Issue Date",
                "Due Date",
                "Return Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No books issued.")

# -----------------------------
# Members
# -----------------------------

elif page == "Members":

    st.title("👤 Member Management")

    # ---------------- Add Member ----------------

    with st.form("member_form"):

        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")

        submitted = st.form_submit_button("➕ Add Member")

        if submitted:

            success, message = add_member(
                name,
                email,
                phone
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    st.divider()

    # ---------------- Search Member ----------------

    st.subheader("👥 Registered Members")

    keyword = st.text_input(
        "🔍 Search by Name, Email or Phone"
    )

    if keyword:
        members = search_members(keyword)
    else:
        members = get_members()

    if members:

        df = pd.DataFrame(
            members,
            columns=[
                "ID",
                "Name",
                "Email",
                "Phone"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No Members Found.")

    st.divider()

    # ---------------- Update Member ----------------

    st.subheader("✏️ Update Member")

    members = get_members()

    if members:

        member_options = {
            f"{m[1]} ({m[2]})": m
            for m in members
        }

        selected = st.selectbox(
            "Select Member",
            list(member_options.keys())
        )

        member = member_options[selected]

        name = st.text_input(
            "Name",
            value=member[1],
            key="update_name"
        )

        email = st.text_input(
            "Email",
            value=member[2],
            key="update_email"
        )

        phone = st.text_input(
            "Phone",
            value=member[3],
            key="update_phone"
        )

        if st.button("💾 Update Member"):

            success, message = update_member_streamlit(
                member[0],
                name,
                email,
                phone
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    st.divider()

    # ---------------- Delete Member ----------------

    st.subheader("🗑️ Delete Member")

    if members:

        delete_option = st.selectbox(
            "Select Member to Delete",
            list(member_options.keys()),
            key="delete_member"
        )

        if st.button("Delete Member"):

            member_id = member_options[delete_option][0]

            success, message = delete_member_streamlit(
                member_id
            )

            if success:
                st.success(message)
                st.rerun()

#------------------------------
#Transactions
#------------------------------
# -----------------------------
# Transactions
# -----------------------------

elif page == "Transactions":

    st.title("🔄 Transaction Management")
# Issue Book
    st.subheader("📖 Issue Book")

    member_id = st.number_input(
        "Member ID",
        min_value=1,
        step=1
    )

    book_id = st.number_input(
        "Book ID",
        min_value=1,
        step=1
    )

    if st.button("Issue Book"):

        issue_book(member_id, book_id)

        st.success("Book Issued Successfully")

        st.rerun()

        st.divider()

    # Return Book

    st.subheader("📚 Return Book")

    transaction_id = st.number_input(
        "Transaction ID",
        min_value=1,
        step=1
    )

    if st.button("Return Book"):

        return_book(transaction_id)

        st.success("Book Returned Successfully")

        st.rerun()

# Transaction History
        st.divider()

    st.subheader("📋 Transaction History")

    rows = get_all_transactions()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Transaction ID",
                "Member",
                "Book",
                "Issue Date",
                "Due Date",
                "Return Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Transactions Found.")

# -----------------------------
# Reports
# -----------------------------

elif page == "Reports":
    
    st.title("📊 Library Reports")

    # ---------------- Summary ----------------

    summary = get_library_summary()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Books", summary["Total Books"])
    col2.metric("Available", summary["Available Books"])
    col3.metric("Members", summary["Total Members"])
    col4.metric("Issued", summary["Issued Books"])

    st.divider()

    # ---------------- Overdue ----------------

    st.subheader("⚠️ Overdue Books")

    overdue = get_overdue_books()

    if overdue:

        df = pd.DataFrame(
            overdue,
            columns=[
                "Member",
                "Book",
                "Issue Date",
                "Due Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("No Overdue Books 🎉")

    st.divider()

    # ---------------- Transactions ----------------

    st.subheader("📋 Transaction Report")

    transactions = get_transaction_report()

    if transactions:

        df = pd.DataFrame(
            transactions,
            columns=[
                "ID",
                "Member",
                "Book",
                "Issue Date",
                "Due Date",
                "Return Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download CSV",
            csv,
            "transaction_report.csv",
            "text/csv"
        )

    else:

        st.info("No Transactions Found.")
#--------------------------------
#my profile
#---------------------------------
elif page == "Profile":
    
    st.title("👤 My Profile")

    user = get_user_profile(
        st.session_state.user_id
    )

    if user:

        col1, col2 = st.columns(2)

        with col1:
            st.text_input(
                "Name",
                user[0],
                disabled=True
            )

            st.text_input(
                "Email",
                user[1],
                disabled=True
            )

        with col2:
            st.text_input(
                "Phone",
                user[2],
                disabled=True
            )

            st.text_input(
                "Username",
                user[3],
                disabled=True
            )

        st.text_input(
            "Role",
            user[4].title(),
            disabled=True
        )


# -----------------------------
# Settings
# -----------------------------

elif page == "Settings":
    
    st.title("⚙ Settings")

    st.subheader("Application Information")

    st.info("""
Library Management System

Version : 1.0

Developer : Kathi Varshith

Database : SQLite

Framework : Streamlit
""")

    st.divider()

    st.subheader("Database")

    st.success("Database Connected")

    st.divider()

    st.subheader("About")

    st.write("""
This project is developed using:

• Python

• SQLite

• Streamlit

• Pandas

• Plotly
""")
    




# Footer 
st.markdown("---")

st.markdown("""
<div style="text-align:center;font-size:15px;padding:10px;">
© 2026 <b>Library Management System</b> | Developed by <b>Kathi Varshith</b> | 🐍 <b>Open to Python Developer Opportunities - Hire Me</b> | 🌐 <a href="https://varshithkathi.netlify.app/" target="_blank">Portfolio</a> | 💼 <a href="https://www.linkedin.com/in/kathi-varshith/" target="_blank">LinkedIn</a> | 💻 <a href="https://github.com/Kathivarshith" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)
