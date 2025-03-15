import streamlit as st
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Library App With Ashir 📚",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state variables
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, 'r') as file:
                data = file.read()
                if data:
                    st.session_state.library = json.loads(data)
        except Exception as e:
            st.error(f"Error loading library: {e}")

# Save library to file
def save_library():
    try:
        with open(LIBRARY_FILE, 'w') as file:
            json.dump(st.session_state.library, file, indent=4)
    except Exception as e:
        st.error(f"Error saving library: {e}")

# Add a book to library
def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': str(publication_year),
        'genre': genre,
        'read_status': read_status.lower() == "yes",  # Convert to boolean
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True

# Remove books
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True

# Search books
def search_books(search_term, search_by):
    search_term = search_term.lower()
    st.session_state.search_results = [
        book for book in st.session_state.library
        if (search_by == "Title" and search_term in book['title'].lower()) or
           (search_by == "Author" and search_term in book['author'].lower()) or
           (search_by == "Genre" and search_term in book['genre'].lower())
    ]

# Calculate library stats
def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book.get('read_status', False))
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0
    genres, authors, decades = {}, {}, {}

    for book in st.session_state.library:
        genre = book.get('genre', "Unknown")
        author = book.get('author', "Unknown")
        publication_year = str(book.get('publication_year', "0000"))

        genres[genre] = genres.get(genre, 0) + 1
        authors[author] = authors.get(author, 0) + 1
        decade = publication_year[:3] + "0s"
        decades[decade] = decades.get(decade, 0) + 1
    
    return {
        'total_books': total_books,
        'read_books': read_books,
        'percent_read': percent_read,
        'genres': dict(sorted(genres.items(), key=lambda item: item[1], reverse=True)),
        'authors': dict(sorted(authors.items(), key=lambda item: item[1], reverse=True)),
        'decades': dict(sorted(decades.items(), key=lambda item: item[1], reverse=True))
    }

# Load library when app starts
load_library()

# Streamlit UI Components
st.title("📚 Personal Library App with Ashir's")

if st.button("Load Library"):
    load_library()
    st.success("Library Loaded Successfully!")

st.sidebar.header("Add a Book")
title = st.sidebar.text_input("Title")
author = st.sidebar.text_input("Author")
publication_year = st.sidebar.text_input("Publication Year")
genre = st.sidebar.text_input("Genre")
read_status = st.sidebar.selectbox("Read Status", ["Yes", "No"])

if st.sidebar.button("Add Book"):
    if title and author and publication_year.isdigit() and genre:
        add_book(title, author, publication_year, genre, read_status)
        st.sidebar.success("Book Added Successfully!")
    else:
        st.sidebar.error("Please fill all fields correctly!")

st.sidebar.header("Search Books")
search_term = st.sidebar.text_input("Search Term")
search_by = st.sidebar.selectbox("Search By", ["Title", "Author", "Genre"])

if st.sidebar.button("Search"):
    search_books(search_term, search_by)

# Display search results or entire library
if st.session_state.search_results:
    st.subheader("Search Results")
    st.table(st.session_state.search_results)
else:
    st.subheader("Library Collection")
    st.table(st.session_state.library)

# Display library statistics
st.subheader("Library Statistics")
st.json(get_library_stats())