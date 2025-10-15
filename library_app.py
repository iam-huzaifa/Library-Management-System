import streamlit as st
import pandas as pd
import os

# File to store book data
file = "library_books.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(file):
    df = pd.DataFrame(columns=["Book ID", "Title", "Author", "Genre", "Available"])
    df.to_csv(file, index=False)

st.set_page_config(page_title="📚 Library Management System", layout="centered")
st.title("📚 Library Management System")

# Load Data
def load_data():
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=["Book ID", "Title", "Author", "Genre", "Available"])

# Save Data
def save_data(df):
    df.to_csv(file, index=False)


# Sidebar Menu
menu = ["Add Book", "View All Books", "Search Book", "Update Book", "Delete Book"]
choice = st.sidebar.radio("Select an Option", menu)

# ===========================
# 1️⃣ Add Book
# ===========================
if choice == "Add Book":
    st.subheader("➕ Add New Book")

    book_id = st.text_input("Enter Book ID")
    title = st.text_input("Enter Book Title")
    author = st.text_input("Enter Author Name")
    genre = st.text_input("Enter Genre")
    add_button = st.button("Add Book")

    if add_button:
        try:
            df = load_data()

            # Check for duplicate ID
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


# ===========================
# 2️⃣ View All Books
# ===========================
elif choice == "View All Books":
    st.subheader("📖 View All Books")
    try:
        df = load_data()
        if df.empty:
            st.info("No books found in the library.")
        else:
            st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading data: {e}")


# ===========================
# 3️⃣ Search Book
# ===========================
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
                    st.dataframe(results)
            except Exception as e:
                st.error(f"Error searching book: {e}")


# ===========================
# 4️⃣ Update Book
# ===========================
elif choice == "Update Book":
    st.subheader("✏️ Update Book Information")
    df = load_data()

    if df.empty:
        st.info("No books available to update.")
    else:
        book_id = st.text_input("Enter Book ID to update")
        update_button = st.button("Find Book")

        if update_button:
            if book_id not in df["Book ID"].astype(str).values:
                st.warning("Book not found.")
            else:
                index = df[df["Book ID"].astype(str) == book_id].index[0]
                st.write("### Current Book Details:")
                st.dataframe(df.loc[[index]])

                new_title = st.text_input("New Title", df.at[index, "Title"])
                new_author = st.text_input("New Author", df.at[index, "Author"])
                new_genre = st.text_input("New Genre", df.at[index, "Genre"])
                new_available = st.selectbox("Availability", ["Yes", "No"], index=0 if df.at[index, "Available"] == "Yes" else 1)

                if st.button("Update Book"):
                    try:
                        df.at[index, "Title"] = new_title
                        df.at[index, "Author"] = new_author
                        df.at[index, "Genre"] = new_genre
                        df.at[index, "Available"] = new_available
                        save_data(df)
                        st.success("✅ Book updated successfully!")
                    except Exception as e:
                        st.error(f"Error updating book: {e}")


# ===========================
# 5️⃣ Delete Book
# ===========================
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
