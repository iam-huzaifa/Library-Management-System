
import streamlit as st
import pandas as pd
import os

# ===============================
# 🔧 File Setup
# ===============================
file = "library_books.csv"
if not os.path.exists(file):
    df = pd.DataFrame(columns=["Book ID", "Title", "Author", "Genre", "Available"])
    df.to_csv(file, index=False)

# ===============================
# 🎨 Streamlit UI Configuration
# ===============================
st.set_page_config(page_title="📚 Library Management System", page_icon="📖", layout="centered")

st.markdown(
    """
    <style>
        .main {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
        }
        h1 {
            color: #2e7d32;
            text-align: center;
        }
        h2, h3 {
            color: #424242;
        }
        .stButton>button {
            color: white !important;
            background-color: #2e7d32 !important;
            border-radius: 8px;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #1b5e20 !important;
            transform: scale(1.02);
        }
        .stRadio > div {
            flex-direction: row;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📖 Library Management System")
st.markdown("<h3 style='text-align:center;color:gray;'>Manage your library with ease</h3>", unsafe_allow_html=True)

# ===============================
# 📂 Helper Functions
# ===============================
def load_data():
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=["Book ID", "Title", "Author", "Genre", "Available"])

def save_data(df):
    df.to_csv(file, index=False)

# ===============================
# 📋 Sidebar Navigation
# ===============================
menu = ["Add Book", "View All Books", "Search Book", "Update Book", "Delete Book"]
choice = st.sidebar.radio("📂 Menu", menu)

# ===============================
# ➕ Add Book
# ===============================
if choice == "Add Book":
    st.subheader("➕ Add New Book")

    col1, col2 = st.columns(2)
    with col1:
        book_id = st.text_input("Book ID")
        author = st.text_input("Author Name")
    with col2:
        title = st.text_input("Book Title")
        genre = st.text_input("Genre")

    add_button = st.button("Add Book")

    if add_button:
        try:
            df = load_data()

            if book_id in df["Book ID"].astype(str).values:
                st.warning("⚠️ Book ID already exists.")
            elif not book_id or not title or not author or not genre:
                st.error("❌ Please fill in all fields.")
            else:
                new_book = pd.DataFrame([{
                    "Book ID": book_id,
                    "Title": title,
                    "Author": author,
                    "Genre": genre,
                    "Available": "Yes"
                }])
                df = pd.concat([df, new_book], ignore_index=True)
                save_data(df)
                st.success(f"✅ Book '{title}' added successfully!")
        except Exception as e:
            st.error(f"Error adding book: {e}")

# ===============================
# 📖 View All Books
# ===============================
elif choice == "View All Books":
    st.subheader("📚 View All Books")
    try:
        df = load_data()
        if df.empty:
            st.info("No books found in the library.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")

# ===============================
# 🔍 Search Book
# ===============================
elif choice == "Search Book":
    st.subheader("🔍 Search Book")
    df = load_data()

    if df.empty:
        st.info("Library is empty.")
    else:
        search_option = st.radio("Search by:", ["Title", "Author"])
        search_term = st.text_input(f"Enter {search_option} to search")
        search_button = st.button("Search")

        if search_button:
            try:
                if search_option == "Title":
                    results = df[df["Title"].str.lower().str.contains(search_term.lower(), na=False)]
                else:
                    results = df[df["Author"].str.lower().str.contains(search_term.lower(), na=False)]

                if results.empty:
                    st.warning("No matching books found.")
                else:
                    st.dataframe(results, use_container_width=True)
            except Exception as e:
                st.error(f"Error searching book: {e}")

# ===============================
# ✏️ Update Book
# ===============================
elif choice == "Update Book":
    st.subheader("✏️ Update Book Information")
    df = load_data()

    if df.empty:
        st.info("No books available to update.")
    else:
        if "book_to_update" not in st.session_state:
            st.session_state.book_to_update = None

        book_id = st.text_input("Enter Book ID to update")
        find_button = st.button("Find Book")

        if find_button:
            if book_id not in df["Book ID"].astype(str).values:
                st.warning("Book not found.")
                st.session_state.book_to_update = None
            else:
                st.session_state.book_to_update = book_id

        if st.session_state.book_to_update:
            index = df[df["Book ID"].astype(str) == st.session_state.book_to_update].index[0]
            st.write("### Current Book Details:")
            st.dataframe(df.loc[[index]])

            new_title = st.text_input("New Title", df.at[index, "Title"])
            new_author = st.text_input("New Author", df.at[index, "Author"])
            new_genre = st.text_input("New Genre", df.at[index, "Genre"])
            new_available = st.selectbox(
                "Availability", ["Yes", "No"],
                index=0 if df.at[index, "Available"] == "Yes" else 1
            )

            if st.button("Update Book"):
                try:
                    df.at[index, "Title"] = new_title
                    df.at[index, "Author"] = new_author
                    df.at[index, "Genre"] = new_genre
                    df.at[index, "Available"] = new_available
                    save_data(df)
                    st.success("✅ Book updated successfully!")
                    st.session_state.book_to_update = None
                except Exception as e:
                    st.error(f"Error updating book: {e}")

# ===============================
# 🗑️ Delete Book
# ===============================
elif choice == "Delete Book":
    st.subheader("🗑️ Delete Book Record")
    df = load_data()

    if df.empty:
        st.info("No books available to delete.")
    else:
        book_id = st.text_input("Enter Book ID to delete")
        delete_button = st.button("Delete Book")

        if delete_button:
            try:
                if book_id not in df["Book ID"].astype(str).values:
                    st.warning("Book not found.")
                else:
                    df = df[df["Book ID"].astype(str) != book_id]
                    save_data(df)
                    st.success("✅ Book deleted successfully.")
            except Exception as e:
                st.error(f"Error deleting book: {e}")
